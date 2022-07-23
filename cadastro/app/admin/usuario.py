from django.contrib import admin, messages
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm
from app.models.usuario import Usuario
from django.urls import path
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.utils.html import escape
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.options import IS_POPUP_VAR
from django.urls import reverse
from django.template.response import TemplateResponse
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'endereco']
    search_fields = ['nome', 'email', 
                     'cep', 'pis']
    autocomplete_fields = ['endereco']
    change_password_form = AdminPasswordChangeForm
    form = UserChangeForm
    change_user_password_template = None

    def endereco(self, obj):
        return obj.endereco

    def get_fields(self, request, obj=None):
        fields = ['nome', 'email', 'password', 'cpf', 'pis', 'endereco', 'groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser']
        for field in super().get_fields(request, obj=obj):
            if not field in fields:
                fields.append(field)
        return fields

    def get_urls(self):
        return [
            path(
                "<id>/password/",
                self.admin_site.admin_view(self.user_change_password),
                name="auth_user_password_change",
            ),
        ] + super().get_urls()

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=""):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(
                _("%(name)s object with primary key %(key)r does not exist.")
                % {
                    "name": self.model._meta.verbose_name,
                    "key": escape(id),
                }
            )
        if request.method == "POST":
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = gettext("Password changed successfully.")
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        "%s:%s_%s_change"
                        % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {"fields": list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            "title": _("Change password: %s") % escape(user.get_username()),
            "adminForm": adminForm,
            "form_url": form_url,
            "form": form,
            "is_popup": (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
            "is_popup_var": IS_POPUP_VAR,
            "add": True,
            "change": False,
            "has_delete_permission": False,
            "has_change_permission": True,
            "has_absolute_url": False,
            "opts": self.model._meta,
            "original": user,
            "save_as": False,
            "show_save": True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template
            or "admin/auth/user/change_password.html",
            context,
        )

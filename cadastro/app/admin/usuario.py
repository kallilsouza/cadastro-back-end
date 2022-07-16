from django.contrib import admin
from app.models.usuario import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'endereco']
    search_fields = ['auth_user__first_name', 
                     'auth_user__last_name', 
                     'auth_user__email', 
                     'cep', 'pis']
    autocomplete_fields = ['auth_user', 'endereco']

    def endereco(self, obj):
        return obj.endereco
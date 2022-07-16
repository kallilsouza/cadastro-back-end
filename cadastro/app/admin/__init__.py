from django.contrib import admin
from app.models import *
from .endereco import EnderecoAdmin
from .usuario import UsuarioAdmin

admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Usuario, UsuarioAdmin)

admin.site.site_header = 'Cadastro'
admin.site.site_title = 'Cadastro'
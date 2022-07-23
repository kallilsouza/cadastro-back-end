from django.contrib import admin
from app.models.endereco import Endereco

class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['endereco', 'usuario']
    search_fields = ['cep', 'rua', 'numero', 'municipio', 'estado', 'pais']

    def endereco(self, obj):
        return f"{obj.rua[:10]}{'...' if len(obj.rua) > 10 else ''}, {obj.numero} - {obj.cep}"

    def usuario(self, obj):
        if obj.usuario:
            return obj.usuario.nome
        return None
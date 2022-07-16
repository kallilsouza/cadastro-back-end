from django.db import transaction
from rest_framework import serializers
from app.models import Usuario, Endereco

class EnderecoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endereco
        fields = ('id', 'pais', 'estado', 'municipio', 'cep', 'rua', 'numero', 'complemento')
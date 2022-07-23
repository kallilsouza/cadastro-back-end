from django.db import transaction
from rest_framework import serializers
from app.models import Usuario, Endereco
from .endereco import EnderecoSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from collections import OrderedDict
from rest_framework.exceptions import ValidationError

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    endereco = EnderecoSerializer()
    pis = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)

    class Meta:
        model = Usuario
        fields = ('id', 'nome', 'email', 'cpf', 'pis', 'password', 'endereco', 'password')

    def is_valid(self, raise_exception=False):
        errors = OrderedDict()
        if 'pis' in self.initial_data:
            if Usuario.objects.filter(pis=self.initial_data['pis']).exists():
                errors['pis'] = 'PIS already exists'
        if 'cpf' in self.initial_data:
            if Usuario.objects.filter(cpf=self.initial_data['cpf']).exists():
                errors['cpf'] = 'CPF already exists'
        if errors:
            raise ValidationError(errors)
        return super().is_valid(raise_exception=raise_exception)

    @transaction.atomic
    def create(self, validated_data):        
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        endereco.save()
        validated_data['endereco'] = endereco
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

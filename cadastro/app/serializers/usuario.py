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
            users = Usuario.objects.filter(pis=self.initial_data['pis'])
            if users.exists():
                if users.first().id != self.instance.id:
                    errors['pis'] = 'PIS já cadastrado'
        if 'cpf' in self.initial_data:
            users = Usuario.objects.filter(cpf=self.initial_data['cpf'])
            if users.exists():
                if users.first().id != self.instance.id:
                    errors['cpf'] = 'CPF já cadastrado'
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
        if 'endereco' in validated_data:
            endereco_data = validated_data.pop('endereco')
            if instance.endereco:
                instance.endereco.pais = endereco_data.get('pais', instance.endereco.pais)
                instance.endereco.estado = endereco_data.get('pais', instance.endereco.estado)
                instance.endereco.municipio = endereco_data.get('pais', instance.endereco.municipio)
                instance.endereco.cep = endereco_data.get('pais', instance.endereco.cep)
                instance.endereco.rua = endereco_data.get('pais', instance.endereco.rua)
                instance.endereco.numero = endereco_data.get('pais', instance.endereco.numero)
                instance.endereco.complemento = endereco_data.get('pais', instance.endereco.complemento)
                instance.endereco.save()
        return super().update(instance, validated_data)

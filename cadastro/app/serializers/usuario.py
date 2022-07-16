from django.db import transaction
from rest_framework import serializers
from app.models import Usuario, Endereco
from .endereco import EnderecoSerializer
from django.contrib.auth.models import User

class UsuarioSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='auth_user.first_name')
    email = serializers.EmailField(source='auth_user.email')
    cpf = serializers.CharField()
    pis = serializers.CharField()
    endereco = EnderecoSerializer()
    senha = serializers.CharField(source='auth_user.password')

    class Meta:
        model = Usuario
        fields = ('id', 'nome', 'email', 'cpf', 'pis', 'senha', 'endereco')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('senha')
        return data

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('auth_user')
        user_data['username'] = user_data['email']
        if User.objects.filter(username=user_data['username']).count() > 0:
            raise serializers.ValidationError({'user':'Usuário com este username já existe'})
        user = User(username=user_data['username'], 
                                   email=user_data['email'], 
                                   first_name=user_data['first_name'])
        user.set_password(user_data['password'])
        user.save()
        validated_data['auth_user'] = user
        endereco_data = validated_data.pop('endereco')
        endereco = Endereco.objects.create(**endereco_data)
        endereco.save()
        validated_data['endereco'] = endereco
        return super().create(validated_data)

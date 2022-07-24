from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'login'
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.nome
        token['id'] = user.id
        return token
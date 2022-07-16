from rest_framework import viewsets
from app.models.usuario import Usuario
from app.serializers.usuario import UsuarioSerializer
from rest_framework.decorators import authentication_classes

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    http_method_names = ['get', 'post'] # TODO: Permitir que usuário visualize apenas os próprios dados
    
    @authentication_classes([])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_permissions(self):        
        if self.request.method == 'POST':
            permissions = []
        else:
            permissions = super().get_permissions()
        return permissions
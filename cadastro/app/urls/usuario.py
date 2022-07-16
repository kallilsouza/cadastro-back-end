from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import UsuarioViewSet

usuario_router = DefaultRouter()
usuario_router.register('usuarios', UsuarioViewSet, basename='usuarios')
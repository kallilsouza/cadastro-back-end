from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .usuario import usuario_router
from app.views.login import MyTokenObtainPairView

urlpatterns = [
    path("", include(usuario_router.urls)),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh')
]
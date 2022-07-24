from rest_framework_simplejwt.views import TokenObtainPairView
from app.serializers.login import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
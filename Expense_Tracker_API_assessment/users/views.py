from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth.models import User

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=201)
        return Response(serializer.errors, status=400)
    
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = User.objects.get(username=username)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User logged in successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=200)
        return Response(serializer.errors, status=400)
    


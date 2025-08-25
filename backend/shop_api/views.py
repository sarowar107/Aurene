# shop_api/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from .models import Product
from .serializers import ProductSerializer
import traceback
from django.contrib.auth.models import User

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('?')
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all().order_by('?')
    serializer_class = ProductSerializer

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_409_CONFLICT)
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = True
        user.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_201_CREATED)



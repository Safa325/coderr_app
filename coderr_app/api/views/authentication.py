from django.contrib.auth.models import User
from coderr_app.api.serializers.autentication import  RegistrationSerializer, CustomAuthTokenSerializer
from rest_framework.generics import ListAPIView
from coderr_app.models import Profile, Offers,  OfferDetail, Order, Review
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Avg, Count
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 6  # Standardanzahl von Objekten pro Seite
    page_size_query_param = 'page_size' 

class RegistrationView(APIView):
    permission_classes = [AllowAny] 
   
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            response_data = serializer.save()  
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomLoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
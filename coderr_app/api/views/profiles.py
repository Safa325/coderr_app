from django.contrib.auth.models import User
from coderr_app.api.serializers.profiles import ProfileSerializer, BuisnessSerializer, CustomerSerializer
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
    page_size = 6  
    page_size_query_param = 'page_size' 

class ListProfileView(APIView):
    permission_classes = [AllowAny]
   
    def get(self, request):
        
        profiles = Profile.objects.all()

        serializer = ProfileSerializer(profiles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
       
        if request.user != profile.user:
            return Response(
                {"detail": "Forbidden: You do not have permission to view this profile."},
                status=status.HTTP_403_FORBIDDEN
            )
    
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessProfileListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BuisnessSerializer

    def get_queryset(self):
        return Profile.objects.filter(type='business')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"message": "No business profiles found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerProfileListView(ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Profile.objects.filter(type='customer')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({"message": "No customer profiles found."}, status=status.HTTP_404_NOT_FOUND)
       
        serializer = self.get_serializer(queryset, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from django.contrib.auth.models import User
from coderr.api.serializers.profiles import ProfileSerializer, BuisnessSerializer, CustomerSerializer
from rest_framework.generics import ListAPIView
from coderr.models import Profile, Offers,  OfferDetail, Order, Review
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

class BaseInfoView(APIView):
    """
    API-Endpunkt, der allgemeine Basisinformationen zur Plattform zurückgibt.
    """
    permission_classes = [AllowAny] 
    
    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        average_rating = round(average_rating, 1) 

        business_profile_count = Profile.objects.filter(type='business').count()

        offer_count = Offers.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }

        return Response(data, status=status.HTTP_200_OK)
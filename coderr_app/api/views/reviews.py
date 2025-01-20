from django.contrib.auth.models import User
from coderr_app.api.serializers.reviews import ReviewSerializer
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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from coderr_app.api.filters import ReviewFilter
from coderr_app.api.permissions import IsCustomerUser

class CustomPagination(PageNumberPagination):
    page_size = 6  
    page_size_query_param = 'page_size' 

class ReviewListView(ListAPIView):
    permission_classes = [IsCustomerUser]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ReviewFilter 
    ordering_fields = ['updated_at', 'rating']
    ordering = ['updated_at']
  
    def get_queryset(self):
        return Review.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    def post(self, request, *args, **kwargs):
        """
        Erstellt ein neues Review.
        """
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            review = serializer.save()
            response_serializer = ReviewSerializer(review, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class ReviewDetailView(APIView):
    permission_classes = [IsCustomerUser]
    def get(self, request, *args, **kwargs):
        """
        Holt die Details eines Reviews.
        """
        pk = self.kwargs.get('pk')
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        review = get_object_or_404(Review,pk=pk)
        serializer = ReviewSerializer(review, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Löscht eine Bestellung.
        """
        pk = self.kwargs.get('pk')
        review = get_object_or_404(Review, pk=pk)

        review.delete()
        return Response({"detail": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

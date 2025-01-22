from django.contrib.auth.models import User
from coderr.api.serializers.offers import  OffersSerializer, OfferDetailsSerializer, DetailOfferSerializer, SimplifiedOffersSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from coderr.models import Profile, Offers,  OfferDetail
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
from coderr.api.filters import OffersFilter
from django.db.models import Min,Max
from coderr.api.permissions import IsBusinessUser


class CustomPagination(PageNumberPagination):
    page_size = 6  
    page_size_query_param = 'page_size'  
    max_page_size = 100  

class OffersListView(ListAPIView):
    permission_classes = [IsBusinessUser]
    serializer_class = OffersSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    pagination_class = CustomPagination  
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price', 'max_delivery_time']
    ordering = ['updated_at']
    filterset_class = OffersFilter 

    def get_queryset(self):
        """
        Gibt das angepasste Queryset mit Annotationen und Benutzerfilterung zurück.
        """
        base_queryset = self.get_annotated_queryset()
        return self.filter_queryset_by_user(base_queryset)

    def get_annotated_queryset(self):
        """
        Fügt Annotationen für `min_price` und `max_delivery_time` zum Queryset hinzu.
        """
        return Offers.objects.annotate(
            min_price=Min('details__price'),  # Minimaler Preis aus OfferDetails
            max_delivery_time=Min('details__delivery_time_in_days')  # Maximale Lieferzeit
        )

    def filter_queryset_by_user(self, queryset):
        """
        Filtert das Queryset basierend auf der Benutzerrolle.
        """
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = user.profile
                if profile.type == 'business':
                    return queryset.filter(user=user)
                elif profile.type == 'customer':
                    return queryset
            except Profile.DoesNotExist:
                pass
        return queryset

    def post(self, request, *args, **kwargs):
        """
        Erstellt ein neues Angebot.
        """   
        serializer = OffersSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            offer = serializer.save(user=request.user)
            response_serializer = SimplifiedOffersSerializer(offer)  
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetailOfferView(RetrieveAPIView):
    permission_classes = [IsBusinessUser]
    queryset = Offers.objects.all()
    serializer_class = DetailOfferSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        offer = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        offer = get_object_or_404(Offers, pk=pk)
        
        serializer = OffersSerializer(offer, data=request.data, partial=True, context={'request': request})
        if offer.user != request.user:
            return Response(
                {"detail": "You do not have permission to patch this offer."},
                status=status.HTTP_403_FORBIDDEN
                )
            
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        offer = get_object_or_404(Offers, pk=pk)

        if offer.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this offer."},
                status=status.HTTP_403_FORBIDDEN
                )
    
        offer.delete()
        return Response({"detail": "Offer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class OfferDetailListView(ListAPIView):
    permission_classes = [IsBusinessUser]
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailsSerializer     

class DetailOfferDetailView(RetrieveAPIView):
    permission_classes = [IsBusinessUser]
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailsSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        offerDetail = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(offerDetail)
        return Response(serializer.data, status=status.HTTP_200_OK)



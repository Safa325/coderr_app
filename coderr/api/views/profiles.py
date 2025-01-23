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
    """
    Benutzerdefinierte Paginierungsklasse, um die Anzahl der Profile pro Seite zu steuern.
    """

    page_size = 6  
    page_size_query_param = 'page_size' 

class ListProfileView(APIView):
    """
    API-View, um eine Liste aller Profile zurückzugeben.
    """
    permission_classes = [AllowAny]
   
    def get(self, request):
        """
        Gibt eine Liste aller vorhandenen Profile zurück.
        """
        
        profiles = Profile.objects.all()

        serializer = ProfileSerializer(profiles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileDetailView(APIView):
    """
    API-View, um ein einzelnes Profil anzuzeigen oder teilweise zu aktualisieren.
    """
    permission_classes = [AllowAny]
    
    def get(self, request, pk, *args, **kwargs):
        """
        Gibt die Details eines spezifischen Profils zurück.
        """
        profile = get_object_or_404(Profile, pk=pk)
        
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        """
        Aktualisiert ein Profil teilweise, wenn der Benutzer berechtigt ist.
        """
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
    """
    API-View für die Liste aller Geschäftsnutzerprofile.
    """
    permission_classes = [AllowAny]
    serializer_class = BuisnessSerializer

    def get_queryset(self):
        """
        Filtert die Profile nach Geschäftsnutzern.
        """
        return Profile.objects.filter(type='business')

    def list(self, request, *args, **kwargs):
        """
        Gibt die Liste der Geschäftsnutzerprofile oder eine Nachricht zurück, falls keine gefunden wurden.
        """
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"message": "No business profiles found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerProfileListView(ListAPIView):
    """
    API-View für die Liste aller Kundenprofile.
    """
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """
        Filtert die Profile nach Kunden.
        """
        return Profile.objects.filter(type='customer')
   
    def list(self, request, *args, **kwargs):
        """
        Gibt die Liste der Kundenprofile oder eine Nachricht zurück, falls keine gefunden wurden.
        """
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({"message": "No customer profiles found."}, status=status.HTTP_404_NOT_FOUND)
       
        serializer = self.get_serializer(queryset, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
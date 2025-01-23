from django.contrib.auth.models import User
from coderr.api.serializers.autentication import  RegistrationSerializer, CustomAuthTokenSerializer
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
    Benutzerdefinierte Paginierungsklasse, die die Anzahl der Objekte pro Seite steuert.
    """
    page_size = 6  
    page_size_query_param = 'page_size' 

class RegistrationView(APIView):
    """
    API-View für die Benutzerregistrierung. Verwendet den RegistrationSerializer, um neue Benutzer zu erstellen.
    """
    permission_classes = [AllowAny] 
   
    def post(self, request, *args, **kwargs):
        """
        Erstellt einen neuen Benutzer basierend auf den übermittelten Daten und gibt bei Erfolg die Benutzerinformationen zurück.
        """
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            response_data = serializer.save()  
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomLoginView(APIView):
    """
    API-View für die Benutzeranmeldung. Authentifiziert Benutzer und gibt ein Authentifizierungs-Token zurück.
    """

    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        """
        Authentifiziert den Benutzer basierend auf den übermittelten Anmeldeinformationen.
        Gibt bei Erfolg ein Token und Benutzerinformationen zurück.
        """
        serializer = CustomAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
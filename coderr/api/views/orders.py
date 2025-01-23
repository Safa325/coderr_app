from django.contrib.auth.models import User
from coderr.api.serializers.orders import OrderSerializer
from rest_framework.generics import ListAPIView
from coderr.models import Profile, Offers,  OfferDetail, Order, Review
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Avg, Count
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from coderr.api.permissions import OrderPermissions

class CustomPagination(PageNumberPagination):
    """
    Benutzerdefinierte Paginierungsklasse, um die Anzahl der Bestellungen pro Seite zu steuern.
    """
    page_size = 6  
    page_size_query_param = 'page_size' 

class OrderListView(APIView):
    """
    API-View für die Liste der Bestellungen eines Benutzers.
    Zeigt Bestellungen an, bei denen der Benutzer entweder Kunde oder Geschäftspartner ist.
    """
    permission_classes = [OrderPermissions]
    def get(self, request, *args, **kwargs):
        """
        Gibt eine Liste der Bestellungen für den authentifizierten Benutzer zurück.
        """
        user = request.user
        orders = Order.objects.filter(Q(customer_user=user) | Q(business_user=user))
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Erstellt eine neue Bestellung basierend auf den OfferDetail-Daten und dem authentifizierten Benutzer.
        """
        serializer = OrderSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            offer_detail = serializer.validated_data['offer_detail']

            customer_user = request.user  
            business_user = offer_detail.offer.user 
            order = serializer.save(customer_user=customer_user, business_user=business_user)

            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    """
    API-View für die Detailansicht einer spezifischen Bestellung.
    Bietet Funktionen zum Anzeigen, Aktualisieren oder Löschen einer Bestellung.
    """
    permission_classes = [OrderPermissions]
    def get(self, request, *args, **kwargs):
        """
        Ruft die Details einer spezifischen Bestellung basierend auf der ID ab.
        """
        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        Aktualisiert eine Bestellung teilweise mit den übermittelten Daten.
        """
        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk)
        
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Löscht eine Bestellung basierend auf der ID.
        """
        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk)

        order.delete()
        return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class OrderCountView(APIView):
    """
    API-Endpunkt zum Abrufen der Gesamtanzahl von Bestellungen für einen Geschäftsnutzer.
    """
    def get(self, request, pk, *args, **kwargs):
        """
        Gibt die Anzahl der Bestellungen eines Geschäftsnutzers zurück.
        """
        try:
            business_user = Profile.objects.get(pk=pk,type='business')
        except Profile.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        order_count = Order.objects.filter(business_user=business_user.pk).count()
        
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)
   
class OrderCountCompletedView(APIView):
    """
    API-Endpunkt zum Abrufen der Anzahl der abgeschlossenen Bestellungen für einen Geschäftsnutzer.
    """
    def get(self, request, pk, *args, **kwargs):
        """
        Gibt die Anzahl der abgeschlossenen Bestellungen eines Geschäftsnutzers zurück.
        """
        try:
            business_user = Profile.objects.get(pk=pk,type='business')
        except Profile.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        order_count = Order.objects.filter(business_user=business_user.pk,status='completed').count()
        
        return Response({"completed_order_count": order_count}, status=status.HTTP_200_OK)
 
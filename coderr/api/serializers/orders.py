from rest_framework import serializers
from coderr.models import Profile, OfferDetail, Offers, Order, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class OrderSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.DecimalField(source='offer_detail.price', max_digits=10, decimal_places=2, read_only=True)
    features = serializers.ListField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(),
        source='offer_detail',
        write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'offer_detail_id',  # Eingabe bei POST
            'title',  # Ausgabe
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Erstellt eine neue Bestellung (Order) basierend auf den validierten Daten.
        """
        order = Order.objects.create(**validated_data)
        return order
   
    def update(self,instance,validated_data):
        """
        Aktualisiert den Status einer Bestellung und speichert die Änderungen.
        """
        instance.status = validated_data.get('status',instance.status)
        instance.save()
        return instance
        
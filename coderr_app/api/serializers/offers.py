from rest_framework import serializers
from coderr_app.models import Profile, OfferDetail, Offers, Order, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db import transaction
import json


class OfferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        ]


      
class OfferDetailsUrlSerializer(serializers.ModelSerializer):
    """
    Serializer für die URL und ID der OfferDetail-Objekte.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, instance):
        return instance.get_absolute_url()
 
class OffersSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()  
    min_delivery_time = serializers.SerializerMethodField()  
    user_details = serializers.SerializerMethodField()  
 
    class Meta:
        model = Offers
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]
        read_only_fields = ['user','created_at','updated_at']
      
    def get_details(self, obj):
        details = obj.details.all()
        details_url = []
        for detail in details:
            detail_url = {
                'id': detail.id,
                'url': f'/offerdetails/{detail.id}/'  
            }
            details_url.append(detail_url)
        return details_url
            
    def get_min_price(self, obj):
        """
        Gibt den niedrigsten Preis in den OfferDetails zurück.
        """
        details = obj.details.all()
        if details:
            return min(detail.price for detail in details)  
        return None
    
    def get_min_delivery_time(self, obj):
        """
        Gibt die kürzeste Lieferzeit in den OfferDetails zurück.
        """
        details = obj.details.all()
        if details:
            return min(detail.delivery_time_in_days for detail in details)  
        return None
   
    def get_user_details(self, obj):
        """
        Gibt die Benutzerdetails des Angebots zurück.
        """
        user = obj.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        } 
      
    def create(self, validated_data):
        """
        Erstellt ein Angebot und verarbeitet die OfferDetails aus der POST-Anfrage.
        """
        image = validated_data.get('image')
        if not image:
            print("Bild wurde nicht übergeben!")
        else:
            print(f"Bild gefunden: {image.name}")
        details_data = self.context['request'].data.get('details', [])

        with transaction.atomic():
            offer = Offers.objects.create(**validated_data)
            OfferDetail.objects.bulk_create([
                OfferDetail(offer=offer, **detail) for detail in details_data
            ])
        return offer
   
    def update(self, instance, validated_data):
        details_data = self.context['request'].data.get('details', [])
        existing_details = list(instance.details.all())  

        for detail, detail_data in zip(existing_details, details_data):
            detail.title = detail_data.get('title', detail.title)
            detail.revisions = detail_data.get('revisions', detail.revisions)
            detail.delivery_time_in_days = detail_data.get('delivery_time_in_days', detail.delivery_time_in_days)
            detail.price = detail_data.get('price', detail.price)
            detail.features = detail_data.get('features', detail.features)
            detail.offer_type = detail_data.get('offer_type', detail.offer_type)
            detail.save()
          
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance
    
   
        
           

class DetailOfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True) 
     
    class Meta:
        model = Offers
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
        ]     

class SimplifiedOffersSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True)

    class Meta:
        model = Offers
        fields = ['id', 'title', 'image', 'description', 'details']




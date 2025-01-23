from rest_framework import serializers
from coderr.models import Profile, OfferDetail, Offers, Order, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer für Bewertungen, einschließlich Felder für den Benutzer, die Bewertung und die Beschreibung.
    """
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',  # Wird automatisch gesetzt
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']  

    def create(self, validated_data):
        """
        Erstellt eine neue Bewertung und setzt den aktuellen Benutzer als Rezensenten.
        """
        request = self.context.get('request')  
        if request and hasattr(request, 'user'):
            validated_data['reviewer'] = request.user
        return super().create(validated_data)
   
    def update(self,instance,validated_data):
        """
        Aktualisiert die Bewertung (Rating und Beschreibung) und speichert die Änderungen.
        """
        instance.rating = validated_data.get('rating',instance.rating)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance
        

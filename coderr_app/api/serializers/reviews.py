from rest_framework import serializers
from coderr_app.models import Profile, OfferDetail, Offers, Order, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class ReviewSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')  
        if request and hasattr(request, 'user'):
            validated_data['reviewer'] = request.user
        return super().create(validated_data)
   
    def update(self,instance,validated_data):
        
        instance.rating = validated_data.get('rating',instance.rating)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance
        

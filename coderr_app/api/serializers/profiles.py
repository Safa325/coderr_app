from rest_framework import serializers
from coderr_app.models import Profile, OfferDetail, Offers, Order, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk', 'username','first_name','last_name'
        ]
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        
        return instance
   
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.pk', read_only=True)
    username = serializers.CharField(source='user.username', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    type = serializers.CharField()

    class Meta:
        model = Profile
        fields = [
            'user',           
            'username',       
            'first_name',     
            'last_name',      
            'email',          
            'file',           
            'location',       
            'tel',            
            'description',    
            'working_hours',  
            'type',           
            'created_at'      
        ]
        read_only_fields = ['created_at']
      
    def create(self, validated_data):
        
        user_data = validated_data.pop('user') 
        
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', '')
            }
        )
        
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
  
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        user = instance.user
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        instance.file = validated_data.get('file', instance.file)
        instance.location = validated_data.get('location', instance.location)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.description = validated_data.get('description', instance.description)
        instance.working_hours = validated_data.get('working_hours', instance.working_hours)
        instance.type = validated_data.get('type', instance.type)
        instance.save()

        return instance

class BuisnessSerializer(serializers.ModelSerializer):
    user = UserTypeSerializer()
    
    class Meta:
        model = Profile
        fields = [
            'user',                     
            'file',           
            'location',       
            'tel',            
            'description',    
            'working_hours',  
            'type'     
        ]
       
class CustomerSerializer(serializers.ModelSerializer):
    user = UserTypeSerializer()
    uploaded_at = serializers.DateTimeField(source='created_at')  

    class Meta:
        model = Profile
        fields = [
            'user',       
            'file',       
            'uploaded_at',
            'type'        
        ]








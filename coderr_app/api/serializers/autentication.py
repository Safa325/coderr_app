from rest_framework import serializers
from coderr_app.models import Profile, OfferDetail, Offers, Order, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(choices=Profile.TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 
                  'email', 
                  'password', 
                  'repeated_password', 
                  'type']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'repeated_password': {'write_only': True}
        }   

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        return data

    def create(self, validated_data):
        """
        Benutzer und Profil erstellen.
        """
        password = validated_data.pop('password')
        validated_data.pop('repeated_password')

        profile_type = validated_data.pop('type')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
        )
        
        profile = Profile.objects.create(
            user=user,
            type=profile_type  
            )
        
        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key,
        }

        return response_data

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "A user with this username don't exists."})

        token, created = Token.objects.get_or_create(user=user)
       
        response_data = {
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }

        return response_data
    
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',primary_key=True )
    file = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    working_hours = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} ({self.type})"


class OfferDetail(models.Model):
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
   
    offer = models.ForeignKey( 
        'Offers',
        on_delete=models.CASCADE,
        related_name='details'
    )
    title = models.CharField(max_length=50)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)  
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.title} ({self.offer_type})"

class Offers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='offers_pictures/', blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title}" 
    
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='customer_orders',
        null=True, 
        blank=True, 
        help_text="The customer who placed the order."
    )
    business_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='business_orders',
        null=True, 
        blank=True, 
        help_text="The business owner who created the offer."
    )
    offer_detail = models.ForeignKey(
        'OfferDetail', 
        on_delete=models.CASCADE, 
        related_name='orders',
        help_text="The offer detail selected for the order."
    )
    status = models.CharField(
        max_length=15, 
        choices=ORDER_STATUS_CHOICES, 
        default='in_progress'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.pk} - {self.offer_detail.title} by {self.customer_user.username}"
   
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        help_text="The business user being reviewed."
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='written_reviews',
        help_text="The user who wrote the review."
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, 
        help_text="Rating from 1 (Poor) to 5 (Excellent)."
    )
    description = models.TextField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Optional description or comment for the review."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the review was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the review was last updated."
    )

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.business_user.username} (Rating: {self.rating})"
  
from django.contrib import admin
from .models import Profile, Offers, OfferDetail, Order, Review

admin.site.register(Profile)
admin.site.register(Offers)
admin.site.register(OfferDetail)
admin.site.register(Order)
admin.site.register(Review)
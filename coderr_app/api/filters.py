import django_filters
from django.db.models import Min, Max
from coderr_app.models import Offers, Review, OfferDetail, Profile

class ReviewFilter(django_filters.FilterSet):
    business_user_id = django_filters.NumberFilter(field_name="business_user_id", label="Business User ID")
    reviewer_id = django_filters.NumberFilter(field_name="reviewer_id", label="Reviewer ID")

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']
    
    def filter_customer(self,queryset,value):
        return queryset.filter(reviewer_id=value)
    
    def filter_business(self,queryset,value):
        return queryset.filter(business_user_id=value)
       
class OffersFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(method='filter_min_price', label="Min Price")
    max_delivery_time = django_filters.NumberFilter(method='filter_max_delivery_time', label="Max Delivery Time")

    class Meta:
        model = Offers
        fields = ['min_price', 'max_delivery_time']  # Diese Felder verweisen auf die benutzerdefinierten Filtermethoden

    def filter_min_price(self, queryset, name, value):
        """
        Filter für Angebote mit einem minimalen Preis.
        """
        return queryset.filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Filter für Angebote mit einer maximalen Lieferzeit.
        """
        return queryset.filter(max_delivery_time__lte=value)

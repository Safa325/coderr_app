from django.urls import path
from coderr_app.api.views.offers import OffersListView, DetailOfferView, OfferDetailListView, DetailOfferDetailView
from coderr_app.api.views.orders import OrderListView ,OrderCountView, OrderCountCompletedView, OrderDetailView
from coderr_app.api.views.profiles import ProfileDetailView, ListProfileView, CustomerProfileListView, BusinessProfileListView
from coderr_app.api.views.authentication import RegistrationView, CustomLoginView
from coderr_app.api.views.reviews import ReviewListView, ReviewDetailView
from coderr_app.api.views.base_info import BaseInfoView

urlpatterns = [
    path('profile/', ListProfileView.as_view(), name='profile-list'),
    path('offers/', OffersListView.as_view(), name='offers-list'),
    path('offers/<int:pk>/', DetailOfferView.as_view(), name='detail-offer'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', OrderCountCompletedView.as_view(), name='completed-order-count'),
    path('offerdetails/', OfferDetailListView.as_view(), name='offerdetails'),
    path('offerdetails/<int:pk>/', DetailOfferDetailView.as_view(), name='offerdetails-detail'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessProfileListView.as_view(), name='profile-business'),
    path('profiles/customer/', CustomerProfileListView.as_view(), name='profile-customer'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
]

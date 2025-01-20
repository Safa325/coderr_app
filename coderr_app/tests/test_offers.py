from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from coderr_app.models import Offers, OfferDetail, Profile

class OffersAPITestCase(APITestCase):

    def setUp(self):
        # Set up users and profiles
        self.business_user = User.objects.create_user(
            username="business_user", password="password123"
        )
        self.customer_user = User.objects.create_user(
            username="customer_user", password="password123"
        )
        
        Profile.objects.create(user=self.business_user, type='business')
        Profile.objects.create(user=self.customer_user, type='customer')

        # Set up an offer and offer details
        self.offer = Offers.objects.create(
            user=self.business_user,
            title="Test Offer",
            description="Test Description"
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Test Detail",
            revisions=3,
            delivery_time_in_days=5,
            price=100,
            features="Feature1, Feature2",
            offer_type="basic"
        )

        self.client = APIClient()

    def test_list_offers(self):
        """Test that offers can be listed for authenticated users."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get('/api/offers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_create_offer(self):
        """Test that a business user can create an offer."""
        self.client.force_authenticate(user=self.business_user)
        payload = {
            "title": "New Offer",
            "description": "New Description",
            "details": [
                {
                    "title": "Detail 1",
                    "revisions": 2,
                    "delivery_time_in_days": 3,
                    "price": 150,
                    "features": "Feature A",
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post('/api/offers/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Offer")

    def test_update_offer(self):
        """Test that a business user can update their own offer."""
        self.client.force_authenticate(user=self.business_user)
        payload = {
            "title": "Updated Offer Title"
        }
        response = self.client.patch(f'/api/offers/{self.offer.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Offer Title")

    def test_delete_offer(self):
        """Test that a business user can delete their own offer."""
        self.client.force_authenticate(user=self.business_user)
        response = self.client.delete(f'/api/offers/{self.offer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offers.objects.filter(id=self.offer.id).exists())

    def test_permissions(self):
        """Test that permissions work correctly for different user roles."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post('/api/offers/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_detail(self):
        """Test retrieving the details of a specific offer."""
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(f'/api/offers/{self.offer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.offer.id)

    def test_list_offer_details(self):
        """Test listing offer details."""
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get('/api/offerdetails/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_offer_detail_endpoint(self):
        """Test retrieving a specific offer detail."""
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(f'/api/offerdetails/{self.offer_detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.offer_detail.id)





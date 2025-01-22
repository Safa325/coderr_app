from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from coderr.models import Profile, Offers, OfferDetail, Order


class OrderAPITestCase(APITestCase):

    def setUp(self):

        self.business_user = User.objects.create_user(
            username="business_user", password="password123"
        )
        self.customer_user = User.objects.create_user(
            username="customer_user", password="password123"
        )
        self.admin_user = User.objects.create_user(
            username="admin_user", password="admin123"
        )
        self.admin_user.is_staff = True  
        self.admin_user.is_superuser = True  
        self.admin_user.save() 

        Profile.objects.create(user=self.business_user, type='business')
        Profile.objects.create(user=self.customer_user, type='customer')

        self.offer = Offers.objects.create(
            user=self.business_user,
            title="Sample Offer",
            description="This is a sample offer."
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Sample Detail",
            revisions=2,
            delivery_time_in_days=3,
            price=150.00,
            features=["Feature A", "Feature B"],
            offer_type="premium"
        )

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer_detail=self.offer_detail,
            status="in_progress"
        )

        self.client = APIClient()

    def test_get_orders(self):
        """Testet das Abrufen von Bestellungen für authentifizierte Benutzer."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.order.id)

    def test_post_order(self):
        """Testet das Erstellen einer neuen Bestellung."""
        self.client.force_authenticate(user=self.customer_user)
        payload = {
            "offer_detail_id": self.offer_detail.id
        }
        response = self.client.post('/api/orders/', payload, format='json')
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 2)  
        self.assertEqual(response.data['customer_user'], self.customer_user.id)
        self.assertEqual(response.data['business_user'], self.business_user.id)


    def test_get_order_detail(self):
        """Testet das Abrufen der Details einer Bestellung."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)
        self.assertEqual(response.data['status'], "in_progress")

    def test_patch_order(self):
        """Testet die teilweise Aktualisierung des Status einer Bestellung."""
        self.client.force_authenticate(user=self.business_user)
        payload = {
            "status": "completed"
        }
        response = self.client.patch(f'/api/orders/{self.order.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "completed")

    def test_delete_order(self):
        """Testet das Löschen einer Bestellung durch den Admin."""
        self.client.force_authenticate(user=self.admin_user)  

        response = self.client.delete(f'/api/orders/{self.order.id}/')
        print(response.status_code)  # Debugging: Zeige den Statuscode
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())


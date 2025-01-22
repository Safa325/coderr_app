from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from coderr.models import Profile


class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user", password="password123", first_name="Business", last_name="User"
        )
        self.customer_user = User.objects.create_user(
            username="customer_user", password="password123", first_name="Customer", last_name="User"
        )
        self.other_user = User.objects.create_user(
            username="other_user", password="password123", first_name="Other", last_name="User"
        )

        self.business_profile = Profile.objects.create(
            user=self.business_user,
            file="business_file.png",
            location="Business City",
            tel="123456789",
            description="Business Description",
            working_hours="9-5",
            type="business",
        )

        self.customer_profile = Profile.objects.create(
            user=self.customer_user,
            file="customer_file.png",
            location="Customer City",
            tel="987654321",
            description="Customer Description",
            working_hours="10-6",
            type="customer",
        )

        self.client = APIClient()

    def test_list_profiles(self):
        """Testet das Abrufen aller Profile."""
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

    def test_get_profile_detail(self):
        """Testet das Abrufen der Details eines Profils."""
        response = self.client.get(f'/api/profile/{self.business_user.id}/')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.business_user.username)
        self.assertEqual(response.data['type'], "business")

    def test_patch_profile(self):
        """Testet das Aktualisieren eines Profils durch den Eigentümer."""
        self.client.force_authenticate(user=self.business_user)
        payload = {"description": "Updated Business Description"}
        response = self.client.patch(f'/api/profile/{self.business_user.id}/', payload, format='json')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Updated Business Description")

    def test_patch_profile_forbidden(self):
        """Testet, dass andere Benutzer ein Profil nicht bearbeiten können."""
        self.client.force_authenticate(user=self.other_user)
        payload = {"description": "Hacking Attempt"}
        response = self.client.patch(f'/api/profile/{self.business_user.id}/', payload, format='json')  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_business_profiles(self):
        """Testet das Abrufen aller Business-Profile."""
        response = self.client.get('/api/profiles/business/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], "business_user")
        self.assertEqual(response.data[0]['type'], "business")

    def test_list_customer_profiles(self):
        """Testet das Abrufen aller Customer-Profile."""
        response = self.client.get('/api/profiles/customer/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], "customer_user")
        self.assertEqual(response.data[0]['type'], "customer")

    def test_no_business_profiles_found(self):
        """Testet, dass eine Nachricht zurückgegeben wird, wenn keine Business-Profile gefunden werden."""
        Profile.objects.filter(type='business').delete()  
        response = self.client.get('/api/profiles/business/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "No business profiles found.")

    def test_no_customer_profiles_found(self):
        """Testet, dass eine Nachricht zurückgegeben wird, wenn keine Customer-Profile gefunden werden."""
        Profile.objects.filter(type='customer').delete()  
        response = self.client.get('/api/profiles/customer/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "No customer profiles found.")

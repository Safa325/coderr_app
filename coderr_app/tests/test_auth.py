from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from coderr_app.models import Profile
from rest_framework.authtoken.models import Token
from django.urls import reverse

class LoginAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        self.login_url = '/api/login/'  

    def test_login_success(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertIn('token', response.data)  

    def test_login_failure(self):
        data = {'username': 'wronguser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

    def test_login_missing_data(self):
        data = {'username': 'testuser'}  
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RegistrationAPITestCase(APITestCase):
    def setUp(self):
        self.registration_url = reverse('registration') 
        self.valid_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "repeated_password": "password123",
            "type": "business"
        }

    def test_registration_success(self):
        response = self.client.post(self.registration_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('token', response.data)

        user_exists = User.objects.filter(username="newuser").exists()
        self.assertTrue(user_exists)

        profile_exists = Profile.objects.filter(user__username="newuser").exists()
        self.assertTrue(profile_exists)

    def test_registration_missing_fields(self):
        data = {
            "username": "testuser"
        }
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)
        self.assertIn('repeated_password', response.data)
        self.assertIn('type', response.data)

    def test_registration_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "repeated_password": "wrongpassword",
            "type": "customer"
        }
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_duplicate_username(self):
        User.objects.create_user(
            username="newuser",
            email="newuser@example.com",
            password="password123"
        )
        response = self.client.post(self.registration_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_registration_duplicate_email(self):
        User.objects.create_user(
            username="anotheruser",
            email="newuser@example.com",
            password="password123"
        )
        response = self.client.post(self.registration_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_registration_invalid_email(self):
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_registration_missing_type(self):
        data = self.valid_data.copy()
        del data['type']
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)

    def test_token_creation_on_registration(self):
        response = self.client.post(self.registration_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="newuser")
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)
        
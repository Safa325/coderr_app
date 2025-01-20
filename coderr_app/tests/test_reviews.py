from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from coderr_app.models import Profile, Review, Offers


class ReviewAPITestCase(APITestCase):

    def setUp(self):
        # Benutzer und Profile erstellen
        self.business_user = User.objects.create_user(
            username="business_user", password="password123", first_name="Business", last_name="User"
        )
        self.customer_user = User.objects.create_user(
            username="customer_user", password="password123", first_name="Customer", last_name="User"
        )

        Profile.objects.create(user=self.business_user, type="business")
        Profile.objects.create(user=self.customer_user, type="customer")

        # Angebot erstellen
        self.offer = Offers.objects.create(
            user=self.business_user,
            title="Sample Offer",
            description="This is a sample offer."
        )

        # Reviews erstellen
        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Great service!"
        )

        # API-Client einrichten
        self.client = APIClient()

    def test_get_reviews(self):
        """Testet das Abrufen aller Reviews."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_post_review(self):
        """Testet das Erstellen eines neuen Reviews."""
        self.client.force_authenticate(user=self.customer_user)
        payload = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Excellent service!"
        }
        response = self.client.post('/api/reviews/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['description'], "Excellent service!")
        self.assertEqual(response.data['business_user'], self.business_user.id)

    def test_get_review_detail(self):
        """Testet das Abrufen eines spezifischen Reviews."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.review.id)
        self.assertEqual(response.data['description'], "Great service!")

    def test_patch_review(self):
        """Testet das Aktualisieren eines Reviews."""
        self.client.force_authenticate(user=self.customer_user)
        payload = {"rating": 5, "description": "Updated review description"}
        response = self.client.patch(f'/api/reviews/{self.review.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['description'], "Updated review description")

    def test_delete_review(self):
        """Testet das Löschen eines Reviews."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(f'/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_filter_reviews_by_rating(self):
        """Testet das Filtern von Reviews nach Bewertung."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get('/api/reviews/?rating=4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rating'], 4)

    def test_pagination_in_reviews(self):
        """Testet die Paginierung in Reviews."""
        for i in range(10):
            Review.objects.create(
                business_user=self.business_user,
                reviewer=self.customer_user,
                rating=3,
                description=f"Review {i+1}"
            )
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get('/api/reviews/?page_size=6')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)  

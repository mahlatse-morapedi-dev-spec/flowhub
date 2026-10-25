from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

# Create your tests here.

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="TestPassword123!"
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.profile_url = "/api/profile/"

    def test_authenticated_user_can_view(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "testuser@example.com")

    def test_unauthenticated_user_cannot_view(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegistrationTests(APITestCase):
    def setUp(self):
        self.register_url = "/api/users/"


    def test_user_can_register(self):

        payload = {
            "username": "newuser",
            "email": "mahlatse.test@example.com",
            "password": "test123"
        }

        response = self.client.post(
            self.register_url,
            payload,
            format="json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registration_fails_without_required_fields(self):
        payload = {
            "email": "testingerror@example.com"
        }

        response = self.client.post(
            self.register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

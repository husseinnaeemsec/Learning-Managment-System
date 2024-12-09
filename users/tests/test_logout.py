from users.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

class LogoutAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email="testeamil@example.com",username='testuser', password='password123',first_name='testuser',last_name='testuser')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.logout_url = reverse("logout") # Adjust URL to match your API endpoint

    def test_logout_success(self):
        """Test that a logged-in user can log out successfully by passing the token in the request data."""
        # Send the token in the request body
        response = self.client.post(self.logout_url, data={'token': self.token.key})
        
        # Check that the response indicates success
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logged out successfully')

        # Verify that the token is deleted
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_logout_without_authentication(self):
        """Test that logout fails if no token is provided."""
        self.client.credentials()  # Remove authentication
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_logout_with_invalid_token(self):
        """Test that logout fails if an invalid token is used."""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.client.credentials()  # Clean up authentication headers

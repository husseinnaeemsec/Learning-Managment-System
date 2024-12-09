from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User  

class AuthenticationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  # Replace with your registration endpoint
        self.login_url = reverse('login')  # Replace with your login endpoint
        self.protected_url = reverse('admin-only')  # Replace with your protected route endpoint
        
        # Create a test user
        self.test_user = {
            "username": "testuser",
            "email": "testuser@husseinnaeem.com",
            "password": "TestPassword"
        }
        self.user = User.objects.create_user(
            username=self.test_user['username'],
            email=self.test_user['email'],
            password=self.test_user['password']
        )
        
    def test_user_registration(self):
        """Test user registration with valid data"""
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "email": "newuser@husseinnaeem.com",
            "password": "TestPassword"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        
    def test_user_login_success(self):
        """Test login with valid credentials"""
        response = self.client.post(self.login_url, {
            "email": self.test_user['email'],
            "password": self.test_user['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
    def test_user_login_failure_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(self.login_url, {
            "email": self.test_user['email'],
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        
    def test_access_protected_route_with_valid_token(self):
        """Test access to a protected route with a valid token"""
        login_response = self.client.post(self.login_url, {
            "email": self.test_user['email'],
            "password": self.test_user['password']
        })
        token = login_response.data['token']
        
        # Access protected route
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_access_protected_route_with_invalid_token(self):
        """Test access to a protected route with an invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        
    def test_access_protected_route_without_token(self):
        """Test access to a protected route without a token"""
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

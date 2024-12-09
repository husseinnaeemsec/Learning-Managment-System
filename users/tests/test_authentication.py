from django.test import TestCase
from users.models import User
from django.urls import reverse


class AuthenticationTests(TestCase):

    def setUp(self):
        # Create Superuser to test only-superusers views
        self.superUser = User.objects.create(
            username='superuser',
            email='superuser@husseinnaeem.com',
            role='admin'
            )
        self.superUser.set_password('password123')
        self.superUser.save()
        
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@husseinnaeem.com"
        )
        self.user.set_password("password123")
        self.user.save()


    def test_user_exist(self):
        """ Test if superUser and user were created """

        # Superuser
        self.assertTrue(User.objects.filter(username=self.superUser.username).exists())
        # Test user         
        self.assertTrue(User.objects.filter(username=self.user.username).exists())


    def test_user_login(self):
        
        """Test that a user can log in with valid credentials."""

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)  

    def test_login_with_empty_credentials(self):
        """Test that login fails with invalid credentials."""

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400) 


    def test_login_with_invalid_credentials(self):
        """Test that login fails with invalid credentials."""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        
        self.assertEqual(response.status_code, 400)


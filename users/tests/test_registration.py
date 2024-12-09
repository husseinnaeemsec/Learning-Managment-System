from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from termcolor import colored



class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse("register")  # Update with your actual endpoint name.
        print(colored("\nTest User Registration. in users/tests/test_registration.py  ...", "cyan", attrs=["bold"]))  # This will print a colored header.

    def test_non_authoraized_admin_registration(self):
        """Test that a user can register successfully with valid data."""
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "first_name":"Test",
            "last_name":"User"
        }
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("User created successfully", response.data.get("message"))


    def test_unique_email(self):
        """Test that a user cannot register with a duplicate email address."""
        
        # Register the first user with a unique email
        data1 = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "securepassword123",
            "first_name":"Test",
            "last_name":"User"
        }
        response1 = self.client.post(self.registration_url, data1)
        # Assert user1 creation
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertIn("User created successfully", response1.data.get("message"))
        
        # Try to register the second user with the same email
        
        data2 = {
            "username": "user2",
            "email": "user1@example.com",  # This email should be unique
            "password": "securepassword123",
            "first_name":"Test",
            "last_name":"User"
        }

        response2 = self.client.post(self.registration_url, data2)
        
        # Assert user2 creation failure
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        if response2.data.get("email"):
            try:
                email_error_object = response2.data.get("email")
                self.assertIn("unique",email_error_object[0].code)
            except Exception as ErrorException:
                
                print(f"An error occurred: {ErrorException}")

    def test_unique_username(self):
            """Test that a user cannot register with a duplicate email address."""
            
            # Register the first user with a unique email
            data1 = {
                "username": "user1",
                "email": "user1@example.com",
                "password": "securepassword123",
                "first_name":"Test",
                "last_name":"User"
            }
            response1 = self.client.post(self.registration_url, data1)
            # Assert user1 creation
            self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
            self.assertIn("User created successfully", response1.data.get("message"))
            
            # Try to register the second user with the same email
            
            data2 = {
                "username": "user1",
                "email": "user2@example.com",  # This email should be unique
                "password": "securepassword123",
                "first_name":"Test",
                "last_name":"User"
            }

            response2 = self.client.post(self.registration_url, data2)
            
            # Assert user2 creation failure
            self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
            if response2.data.get("username"):
                try:
                    username_error_object = response2.data.get("username")
                    self.assertIn("unique",username_error_object[0].code)
                except Exception as ErrorException:
                    
                    print(f"An error occurred: {ErrorException}")


    def test_field_max_length(self):
        data = {
            "first_name":"TestName"*100,
            "last_name":"User"*100,
            "username":"testuser"*100,
            "email":f"{'testuser'*100}@example.com",
            "password":"securepassword123"*100,
        }

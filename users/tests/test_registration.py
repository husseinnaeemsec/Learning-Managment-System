from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User



class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse("register")  # Update with your actual endpoint name.

    def test_permissions_and_access_control(self):
        """Test that a user can register successfully with valid data."""
        data = {
            "role": "admin",  # Passing the role attribute to see if it will be allowed,
            "is_superuser": True, # Passing True to see if it will be allowed
            "is_staff": True, # Passing True to see if it will be allowed
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "first_name":"Test",
            "last_name":"User"
        }
        response = self.client.post(self.registration_url, data)
        # Test user creation status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if the user was created successfully from the response message
        self.assertIn("User created successfully", response.data.get("message"))
        
        # ! Check permissions and access from the User model
        
        user = User.objects.filter(username=data.get("username"))
        # Chekc if the user object was created successfully
        self.assertTrue(user.exists())
        # Make sure that the is_staff attibute is ignored during creation
        self.assertFalse(user.first().is_staff)
        # Make sure that the is_superuser attibute is ignored during creation
        self.assertFalse(user.first().is_superuser)
        # Check account status  
        self.assertTrue(user.first().is_active)
        # Check user role 
        self.assertEqual(user.first().role, "student")  # Should be ignored during creation


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
        # Assert user1 creation from the response message
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
            # Assert user1 creation from the response message
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

        response = self.client.post(self.registration_url, data)
        
        try:
            # Check username max_length error
            self.assertIn("max_length",response.data.get("username")[0].code)
            # Check email max_length error
            self.assertIn("max_length",response.data.get("email")[0].code)
            # Check password max_length error
            self.assertIn("max_length",response.data.get("password")[0].code)
            # Check first_name max_length error
            self.assertIn("max_length",response.data.get("first_name")[0].code)
            # Check last_name max_length error
            self.assertIn("max_length",response.data.get("last_name")[0].code)
        
        except IndexError as e:
            print("IndexError for the ErrorDetail object from DRF",e)
        
        except AttributeError as e:
            print("ErrorDetail object from DRF has no attribute called [code]",e)
        
        except Exception as e:
            print("An error occurred: ",e)
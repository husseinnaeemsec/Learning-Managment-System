from users.models import User
from django.test import TestCase


class UserTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.user.set_password("testpass")
        self.user.save()
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")

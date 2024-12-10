from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from courses.models import Course
from django.urls import reverse

class CourseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()  # Use APIClient, not Client
        # Setup endpoints
        self.create_course_endpoint = reverse("course-list-create")
        self.login_endpoint = reverse("login")
        # Course data 
        self.course_data = {
            "title":"Math 010",
            "description":"Math classification"
        }
        # Create a teacher user
        self.teacher = User.objects.create_user(
            username="teacher1", role="teacher",first_name="Teacher",last_name="Account",email="teacher@example.com"
        )
        self.teacher.set_password("password@TestPassword")
        self.teacher.save()
        
        # Create a student user
        self.student = User.objects.create_user(
            username="student1", role="student",first_name="Student",last_name="Account",email="student@example.com"
        )
        
        self.student.set_password("password@TestPassword")
        self.student.save()
        
        # Login credentials for token authentication
        self.teacher_login_data = {"username": "teacher1", "password": "password@TestPassword"}
        self.student_login_data = {"username": "student1", "password": "password@TestPassword"}

    def authenticate(self, user_login_data):
        # Authenticate and set the token for future requests
        response = self.client.post(self.login_endpoint, data=user_login_data)
        token = response.data.get("access_token")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
        


    def test_course_creation(self):
        

        
        self.authenticate(self.teacher_login_data)
        
        response = self.client.post(self.create_course_endpoint, data=self.course_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get("course"))
        self.assertEqual(response.data.get("message"),"Course Created")

    def test_course_creation_with_student_permissions(self):
        
        self.authenticate(self.student_login_data)
        
        response = self.client.post(self.create_course_endpoint, data=self.course_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        print(response.data)
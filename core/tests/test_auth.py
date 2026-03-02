

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import UserRole


class AuthenticationTest(APITestCase):

 
    # Test 1: User can register successfully
   
    def test_user_registration_success(self):
        url = reverse("register")

        data = {
            "username": "testuser",
            "password": "testpass123",
            "role": "CUSTOMER"
        }

        response = self.client.post(url, data)

        # Check correct response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check user created in database
        self.assertEqual(User.objects.count(), 1)

        # Check role created
        self.assertEqual(UserRole.objects.count(), 1)


    # Test 2: Duplicate username should fail
   
    def test_duplicate_username(self):
        # Create user first
        User.objects.create_user(username="testuser", password="pass")

        url = reverse("register")

        data = {
            "username": "testuser",
            "password": "newpass",
            "role": "CUSTOMER"
        }

        response = self.client.post(url, data)
        print(response.data)
        print(response.status_code)

        # Should return 400 error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        

   
    # Test 3: Login returns token
    
    def test_login_success(self):
        User.objects.create_user(username="testuser", password="testpass123")

        url = reverse("login")

        response = self.client.post(url, {
            "username": "testuser",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Token must exist in response
        self.assertIn("token", response.data)
"""
Module for testing serializers in the 'auth_review' application.

This module contains unit tests for the serializers defined in the
'auth_review' application, specifically the RegisterSerializer and
MyTokenObtainPairSerializer classes. The tests validate the behavior
and functionality of these serializers, ensuring that they correctly
handle user registration and token generation.

"""

from django.test import TestCase  # pylint: disable=E0401
from django.contrib.auth import get_user_model  # pylint: disable=E0401
from rest_framework.exceptions import ValidationError  # pylint: disable=E0401
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer

User = get_user_model()

class RegisterSerializerTest(TestCase):
    """Test case for the RegisterSerializer class.

    This class contains tests to validate the behavior of the RegisterSerializer,
    including successful registrations and various edge cases.
    """

    def test_valid_registration_data(self):
        """Test that valid registration data creates a user successfully."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPassword123!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, data["username"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_admin)

    def test_registration_missing_username(self):
        """Test that registration fails when the username is missing."""
        data = {
            "email": "newuser@example.com",
            "password": "StrongPassword123!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_registration_missing_password(self):
        """Test that registration fails when the password is missing."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_registration_weak_password(self):
        """Test that registration fails when the password does not meet validation criteria."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "123"  # Weak password
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

class MyTokenObtainPairSerializerTest(TestCase):
    """
    Tests to verify token generation
    """
    # pylint: disable=C0103
    def setUp(self):
        """
        Sets up the test environment with mock data before each test.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword"
        )
        self.user.is_verified = True
        self.user.save()

    def test_get_token_with_valid_user(self):
        """Test token generation for verified user"""
        serializer = MyTokenObtainPairSerializer()
        token = serializer.get_token(self.user)
        self.assertEqual(token["username"], self.user.username)
        self.assertTrue(token["is_verified"])

    def test_get_token_with_unverified_user(self):
        """Test token generation for unverified user"""
        self.user.is_verified = False
        self.user.save()

        serializer = MyTokenObtainPairSerializer()
        with self.assertRaises(ValidationError):
            serializer.get_token(self.user)

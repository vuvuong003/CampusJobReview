"""
Module for testing serializers in the 'auth_review' application.

This module contains unit tests for the serializers defined in the
'auth_review' application, specifically the RegisterSerializer and
MyTokenObtainPairSerializer classes. The tests validate the behavior
and functionality of these serializers, ensuring that they correctly
handle user registration and token generation

"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer

User = get_user_model()


class RegisterSerializerTest(TestCase):
    """Test case for the RegisterSerializer class.

    This class contains tests to validate the behavior of the RegisterSerializer,
    including successful registrations and various edge cases.
    """

    def test_valid_registration_data(self):
        """Test that valid registration data creates a user successfully.

        This test checks that when valid registration data is provided,
        a user is created and has the correct attributes.
        """
        data = {
            "username": "newuser",
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
        """Test that registration fails when the username is missing.

        This test checks that if the username is not provided,
        the serializer raises a validation error.
        """
        data = {
            "password": "StrongPassword123!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_registration_missing_password(self):
        """Test that registration fails when the password is missing.

        This test checks that if the password is not provided,
        the serializer raises a validation error.
        """
        data = {
            "username": "newuser"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_registration_duplicate_username(self):
        """Test that registration fails when the username already exists.

        This test checks that if the username already exists in the database,
        the serializer raises a validation error.
        """
        User.objects.create_user(
            username="existinguser",
            password="StrongPassword123!")
        data = {
            "username": "existinguser",
            "password": "AnotherStrongPassword456!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)


class MyTokenObtainPairSerializerTest(TestCase):
    """Test case for the MyTokenObtainPairSerializer class.

    This class contains tests to validate the behavior of the MyTokenObtainPairSerializer,
    including successful token generation and handling of nonexistent users.
    """

    def test_get_token_with_valid_user(self):
        """Test that a token can be obtained for a valid user.

        This test checks that when a valid user is provided, the token
        contains the correct username.
        """
        user = User.objects.create_user(
            username="testuser", password="securepassword")
        serializer = MyTokenObtainPairSerializer()
        token = serializer.get_token(user)

        self.assertIn("username", token)
        self.assertEqual(token["username"], user.username)

    def test_get_token_for_nonexistent_user(self):
        """Test that an error is raised when attempting to get a token for a nonexistent user.

        This test simulates the scenario where a token is requested for a user
        that does not exist, and it checks that a ValidationError is raised.
        """
        with self.assertRaises(ValidationError):
            # This part simulates getting a token for a non-existent user
            serializer = MyTokenObtainPairSerializer()
            serializer.get_token(None)  # Should raise an error

"""
Test module for the User model in the 'auth_review' application.

This module contains unit tests for the User model, verifying
the functionality of user creation methods and ensuring proper
handling of various scenarios, including regular users, superusers,
and error cases for invalid input.
"""
# Import Django's built-in test case class for unit testing
from django.test import TestCase  # pylint: disable=E0401
# Import the function to get the active user model
from django.contrib.auth import get_user_model  # pylint: disable=E0401
# Import IntegrityError for handling database constraint errors
# from django.db.utils import IntegrityError  # pylint: disable=E0401
# Import the Client model from the local 'auth_review' models
# from .models import Client # Import Client model for testing

User = get_user_model() # Set the User variable to reference the active user model


class ClientModelTests(TestCase):
    """Unit tests for validating various behaviors of the User model."""

    def test_create_regular_user(self):
        """Test creating a regular user and verifying default attributes.

        Verifies:
        - Username is set correctly.
        - Default attributes (e.g., is_active, is_staff, is_superuser) are assigned correctly.
        """
        user = User.objects.create_user(
            username="regularuser", password="password123")

        self.assertEqual(user.username, "regularuser") # Check if the username is set as expected
        self.assertTrue(user.is_active) # Regular users should be active by default
        self.assertFalse(user.is_staff) # Regular users should not have staff status
        self.assertFalse(user.is_admin) # Regular users should not be admin
        self.assertFalse(user.is_superuser) # Regular users should not have superuser privileges

    def test_create_superuser(self):
        """Test creating a superuser and verifying superuser-specific attributes.

        Verifies:
        - Username is set correctly.
        - Superuser attributes (is_active, is_staff, is_superuser) are set as expected.
        """
        superuser = User.objects.create_superuser(
            username="adminuser", password="adminpass123")

        self.assertEqual(superuser.username, "adminuser") # Check if username is set correctly
        self.assertTrue(superuser.is_active) # Superusers should be active
        self.assertTrue(superuser.is_staff) # Superusers should have staff status
        self.assertTrue(superuser.is_admin) # Superusers should have admin privileges
        self.assertTrue(superuser.is_superuser) # Superusers should have superuser status

    def test_create_user_without_username(self):
        """Test that creating a user without a username raises an error.

        Expectation:
        - Creating a user with a null username should raise a TypeError.
        """
        with self.assertRaises(TypeError):
            User.objects.create_user(username=None, password="password123")

    def test_create_superuser_without_password(self):
        """Test that creating a superuser without a password raises an error.

        Expectation:
        - Creating a superuser with a null password should raise a TypeError.
        """
        with self.assertRaises(TypeError):
            User.objects.create_superuser(username="adminuser", password=None)

    def test_user_activation(self):
        """Test that a user can be deactivated.

        Steps:
        - Create a user and deactivate them by setting `is_active` to False.
        - Verify that the `is_active` attribute is set to False after saving.
        """
        user = User.objects.create_user(
            username="activeuser", password="password123"
        )
        user.is_active = False # Deactivate the user
        user.save() # Save the user with updated attributes

        self.assertFalse(user.is_active) # Check if the user is inactive

    def test_user_string_representation(self):
        """Test the string representation of the user.

        Expectation:
        - The string representation of the User object should match its username.
        """
        user = User.objects.create_user(
            username="stringuser", password="password123"
        )
        self.assertEqual(str(user), "stringuser") # Verify string representation is username

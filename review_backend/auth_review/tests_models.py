"""
Test module for the User model in the 'auth_review' application.

This module contains unit tests for the User model, verifying
the functionality of user creation methods and ensuring proper
handling of various scenarios, including regular users, superusers,
and error cases for invalid input.
"""
from django.test import TestCase  # pylint: disable=E0401
from django.contrib.auth import get_user_model  # pylint: disable=E0401

User = get_user_model()


class ClientModelTests(TestCase):
    """Unit tests for the User model."""

    def test_create_regular_user(self):
        """Test creating a regular user and verifying default attributes"""
        user = User.objects.create_user(
            username="regularuser", email="regularuser@example.com", password="password123")

        self.assertEqual(user.username, "regularuser")
        self.assertEqual(user.email, "regularuser@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser and verifying superuser-specific attributes"""
        superuser = User.objects.create_superuser(
            username="adminuser", email="adminuser@example.com", password="adminpass123")

        self.assertEqual(superuser.username, "adminuser")
        self.assertEqual(superuser.email, "adminuser@example.com")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_username(self):
        """Test that creating a user without a username raises an error"""
        with self.assertRaises(TypeError):
            User.objects.create_user(username=None, email="user@example.com", password="password123")

    def test_create_superuser_without_password(self):
        """Test that creating a superuser without a password raises an error."""
        with self.assertRaises(TypeError):
            User.objects.create_superuser(username="adminuser", email="adminuser@example.com", password=None)

    def test_user_activation(self):
        """Test that a user can be deactivated."""
        user = User.objects.create_user(
            username="activeuser", email="activeuser@example.com", password="password123"
        )
        user.is_active = False
        user.save()

        self.assertFalse(user.is_active)

    def test_user_string_representation(self):
        """Test the string representation of the user."""
        user = User.objects.create_user(
            username="stringuser", email="stringuser@example.com", password="password123"
        )
        self.assertEqual(str(user), "stringuser")

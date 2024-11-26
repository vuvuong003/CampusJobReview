"""
Module for testing authentication-related functionality in the 'auth_review' application.

This module contains unit tests for user authentication, registration,
and token management in the 'auth_review' application. It uses Django's
APITestCase to simulate HTTP requests and validate responses from the
API endpoints. Each test case is designed to verify specific aspects
of the authentication process, ensuring that the implementation
meets the expected behavior.
"""

from unittest.mock import patch
from django.contrib.auth import get_user_model  # pylint: disable=E0401
from django.urls import reverse  # pylint: disable=E0401
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status  # pylint: disable=E0401
from rest_framework.test import APITestCase  # pylint: disable=E0401

User = get_user_model()


class AuthTests(APITestCase):
    """Test cases for user authentication and registration."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_user = None
        self.register_url = None
        self.token_url = None
        self.token_refresh_url = None
        self.inactive_user = None

    # pylint: disable=C0103
    def setUp(self):
        """Set up the test environment before each test case.

        This method creates a test user and sets up the URLs for the
        registration and token endpoints, ensuring a clean slate for
        each test case.
        """
        self.test_user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="securepassword"
        )
        self.test_user.is_verified = True
        self.test_user.save()
        self.profile_url = reverse("profile")
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")
        self.token_refresh_url = reverse("token_refresh")
        # Create an inactive user for testing
        # self.inactive_user = User.objects.create_user(
        #     username="inactiveuser",
        #     password="securepassword",
        #     is_active=False
        # )

    @patch('auth_review.views.SendGridAPIClient')

    def test_register_new_user_success(self, mock_sendgrid):
        """Test successful registration of a new user.

        This test verifies that a new user can be registered successfully
        and receives a confirmation message.
        """
        # Mock the SendGrid send method
        mock_sendgrid.return_value.send.return_value = True
        # Test successful registration
        data = {"username": "newuser", "email": "newuser@example.com", "password": "newpassword123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["val"])
        self.assertEqual(
            response.data["data"]["detail"],
            "Registration Successful. Please verify your email.")

         # Verify the user was created
        user = User.objects.get(username="newuser")
        self.assertFalse(user.is_verified)
        self.assertEqual(user.email, "newuser@example.com")

        # Verify SendGrid was called
        mock_sendgrid.return_value.send.assert_called_once()

    def test_register_existing_user_error(self):
        """Test registration with an existing username.

        This test checks that an attempt to register with an already
        existing username fails and returns the appropriate error message.
        """
        # Test registration with an existing username
        data = {"username": "testuser",
                "email": "testuser@example.com",
                "password": "newpassword123"}

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["data"]["val"])
        self.assertEqual(response.data["data"]["detail"], "Entered username or email exists")

    def test_token_obtain_pair_success(self):
        """Test successful JWT token generation with valid credentials.

        This test verifies that a valid user can obtain a JWT token by
        providing the correct username and password.
        """
        data = {"username": "testuser", "password": "securepassword"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["val"])
        self.assertIn("tokens", response.data["data"])
        self.assertIn("access", response.data["data"]["tokens"])
        self.assertIn("refresh", response.data["data"]["tokens"])

    def test_token_obtain_pair_invalid_credentials(self):
        """Test token generation with invalid user credentials.

        This test checks that an attempt to generate a token with
        incorrect username or password fails and returns an unauthorized
        error.
        """
        # Test token generation with invalid credentials
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_success(self):
        """Test token refresh"""
        # First get tokens
        login_response = self.client.post(self.token_url, {
            "username": "testuser",
            "password": "securepassword"
        })
        refresh_token = login_response.data["data"]["tokens"]["refresh"]

        # Then refresh
        response = self.client.post(self.token_refresh_url, {
            "refresh": refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_register_user_invalid_password(self):
        """Test registration with an invalid password.

        This test checks that an attempt to register with a weak password
        fails and returns an appropriate error message.
        """
        # Test Registration with invalid password
        data = {"username": "user_with_invalid_pass",
                "email": "invalid@example.com",
                "password": "123"}

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["data"]["val"])
        self.assertIn("password", response.data["data"]["detail"])

    def test_token_obtain_inactive_user(self):
        """Test token generation for an inactive user.

        This test verifies that an inactive user cannot obtain a JWT token
        and receives an unauthorized error.
        """
        # Test Token Generation for Inactive User
        data = {"username": "inactiveuser", "password": "securepassword"}
        response = self.client.post(self.token_url, data, format="json")

        # Assert that the response status is unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_obtain_with_empty_payload(self):
        """Test token generation with an empty payload.

        This test checks that sending an empty payload to the token endpoint
        results in a bad request error.
        """
        # Test Token with Empty Payload
        response = self.client.post(self.token_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_not_allowed_on_token_endpoint(self):
        """Test get not allowed on token 

        This test checks that an attempt to register with a weak password
        fails and returns an appropriate error message.
        """

        # Send a GET request to the token endpoint
        self.token_url = reverse("token_obtain_pair")
        response = self.client.get(self.token_url)

        # Check that the response status code is 405 Method Not Allowed
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED)

        # Check the response message content
        self.assertEqual(response.data, {"msg": "Get not allowed"})

class EmailVerificationTests(APITestCase):
    """
    Tests for the user's email verification feature.
    """
    # pylint: disable=C0103
    def setUp(self):
        """
        Setup the test enviornment before each test case.

        This method creates a test user and sets up the URLs for the
        email verification endpoint, ensuring a clean slate for
        each test case.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.verify_url = reverse("verify_email", kwargs={"uidb64": self.uid, "token": self.token})

    def test_verify_email_success(self):
        """
        Test to verify the email verification success case
        """
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_verify_email_invalid_token(self):
        """
        Test to verify when the token is invalid
        """
        invalid_token_url = reverse("verify_email",
                                    kwargs={"uidb64": self.uid, "token": "invalid-token"})

        response = self.client.get(invalid_token_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_verified)

class ProfileTests(APITestCase):
    """
    Tests for the user's profile feature.
    """
    # pylint: disable=C0103
    def setUp(self):
        """
        Setup the test enviornment before each test case.

        This method creates a test user and sets up the URLs for the
        profile endpoint, ensuring a clean slate for each test case.
        """
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse("profile")

    def test_get_profile(self):
        """
        Test to verify the fetching of user's profile information.
        """
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_profile(self):
        """
        Test to ensure the user's profile information is successfully updated.
        """
        data = {"first_name": "Test", "last_name": "User", "bio": "This is a test bio."}
        response = self.client.put(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.bio, "This is a test bio.")

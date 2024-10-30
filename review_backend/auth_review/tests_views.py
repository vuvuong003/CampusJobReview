"""
Module for testing authentication-related functionality in the 'auth_review' application.

This module contains unit tests for user authentication, registration,
and token management in the 'auth_review' application. It uses Django's
APITestCase to simulate HTTP requests and validate responses from the
API endpoints. Each test case is designed to verify specific aspects
of the authentication process, ensuring that the implementation
meets the expected behavior.
"""

from django.contrib.auth import get_user_model #pylint: disable=E0401
from django.urls import reverse #pylint: disable=E0401
from rest_framework import status #pylint: disable=E0401
from rest_framework.test import APITestCase #pylint: disable=E0401

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

    def set_up(self):
        """Set up the test environment before each test case.

        This method creates a test user and sets up the URLs for the
        registration and token endpoints, ensuring a clean slate for
        each test case.
        """
        self.test_user = User.objects.create_user(
            username="testuser", password="securepassword"
        )
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")
        self.token_refresh_url = reverse("token_refresh")
        # Create an inactive user for testing
        self.inactive_user = User.objects.create_user(
            username="inactiveuser",
            password="securepassword",
            is_active=False
        )

    def test_register_new_user_success(self):
        """Test successful registration of a new user.

        This test verifies that a new user can be registered successfully
        and receives a confirmation message.
        """
        # Test successful registration
        data = {"username": "newuser", "password": "newpassword123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["val"])
        self.assertEqual(
            response.data["data"]["detail"],
            "Registration Successful")

    def test_register_existing_user_error(self):
        """Test registration with an existing username.

        This test checks that an attempt to register with an already
        existing username fails and returns the appropriate error message.
        """
        # Test registration with an existing username
        data = {"username": "testuser", "password": "newpassword123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["data"]["val"])
        self.assertEqual(response.data["data"]["detail"], "Username Exists")

    def test_token_obtain_pair_success(self):
        """Test successful JWT token generation with valid credentials.

        This test verifies that a valid user can obtain a JWT token by
        providing the correct username and password.
        """
        # Test JWT token generation with valid credentials
        data = {"username": "testuser", "password": "securepassword"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["val"])
        self.assertIn("tokens", response.data["data"])
        self.assertIn("tenant_id", response.data["data"]["details"])

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
        """Test successful token refresh with a valid refresh token.

        This test verifies that a user can successfully refresh their JWT
        access token using a valid refresh token.
        """
        # Test refreshing a valid token
        data = {"username": "testuser", "password": "securepassword"}
        login_response = self.client.post(self.token_url, data, format="json")
        refresh_token = login_response.data["data"]["tokens"]["refresh"]
        response = self.client.post(
            self.token_refresh_url, {"refresh": refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_register_user_invalid_password(self):
        """Test registration with an invalid password.

        This test checks that an attempt to register with a weak password
        fails and returns an appropriate error message.
        """
        # Test Registration with invalid password
        data = {"username": "user_with_invalid_pass", "password": "123"}
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
        """Test GET request on the token endpoint.

        This test verifies that sending a GET request to the token endpoint
        is not allowed and returns a method not allowed error.
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

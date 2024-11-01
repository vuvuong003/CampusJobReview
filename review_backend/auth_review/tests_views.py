"""
Module for testing authentication-related functionality in the 'auth_review' application.

This module contains unit tests for user authentication, registration,
and token management in the 'auth_review' application. It uses Django's
APITestCase to simulate HTTP requests and validate responses from the
API endpoints. Each test case is designed to verify specific aspects
of the authentication process, ensuring that the implementation
meets the expected behavior.
"""
# Import function to get the custom User model
from django.contrib.auth import get_user_model  # pylint: disable=E0401
# Import function for reversing URL names
from django.urls import reverse  # pylint: disable=E0401
# Import HTTP status codes for assertions
from rest_framework import status  # pylint: disable=E0401
# Import base class for API test cases
from rest_framework.test import APITestCase  # pylint: disable=E0401

User = get_user_model() # Retrieve the User model dynamically to allow custom User models


class AuthTests(APITestCase):
    """Test cases for user authentication and registration."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_user = None # Placeholder for a test user
        self.register_url = None # Placeholder for the registration URL
        self.token_url = None # Placeholder for the token generation URL
        self.token_refresh_url = None # Placeholder for the token refresh URL
        self.inactive_user = None # Placeholder for an inactive test user

    # pylint: disable=C0103
    def setUp(self):
        """Set up the test environment before each test case.

        This method creates a test user and sets up the URLs for the
        registration and token endpoints, ensuring a clean slate for
        each test case.
        """
        self.test_user = User.objects.create_user(
            username="testuser", password="securepassword"
        )
        self.register_url = reverse("register") # URL for user registration
        self.token_url = reverse("token_obtain_pair") # URL for JWT token generation
        self.token_refresh_url = reverse("token_refresh") # URL for token refresh

    def test_register_new_user_success(self):
        """Test successful registration of a new user.

        This test verifies that a new user can be registered successfully
        and receives a confirmation message.
        """
        data = {"username": "newuser", "password": "newpassword123"} # Sample registration data
        response = self.client.post(self.register_url, data, format="json") # Simulate POST request
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Verify success status
        self.assertTrue(response.data["data"]["val"]) # Confirm registration flag
        self.assertEqual(
            response.data["data"]["detail"],
            "Registration Successful") # Check message

    def test_register_existing_user_error(self):
        """Test registration with an existing username.

        This test checks that an attempt to register with an already
        existing username fails and returns the appropriate error message.
        """
        data = {"username": "testuser", "password": "newpassword123"} # Reuse existing username
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)# Expect error status
        self.assertFalse(response.data["data"]["val"]) # Confirm failure flag
        self.assertEqual(response.data["data"]["detail"], "Username Exists") # Check error message

    def test_token_obtain_pair_success(self):
        """Test successful JWT token generation with valid credentials.

        This test verifies that a valid user can obtain a JWT token by
        providing the correct username and password.
        """
        data = {"username": "testuser", "password": "securepassword"} # Valid login credentials
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verify success status
        self.assertTrue(response.data["data"]["val"]) # Confirm token request flag
        self.assertIn("tokens", response.data["data"]) # Check that tokens are in the response


    def test_token_obtain_pair_invalid_credentials(self):
        """Test token generation with invalid user credentials.

        This test checks that an attempt to generate a token with
        incorrect username or password fails and returns an unauthorized
        error.
        """
        # Test token generation with invalid credentials
        data = {"username": "testuser", "password": "wrongpassword"} # Incorrect password
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Expect auth error

    def test_token_refresh_success(self):
        """Test successful token refresh with a valid refresh token.

        This test verifies that a user can successfully refresh their JWT
        access token using a valid refresh token.
        """
        data = {"username": "testuser", "password": "securepassword"} # Login to obtain tokens
        login_response = self.client.post(self.token_url, data, format="json")
        refresh_token = login_response.data["data"]["tokens"]["refresh"] # Extract refresh token
        response = self.client.post(
            self.token_refresh_url, {"refresh": refresh_token}, format="json") # Request refresh
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Verify success status
        self.assertIn("access", response.data) # Confirm access token in response

    def test_register_user_invalid_password(self):
        """Test registration with an invalid password.

        This test checks that an attempt to register with a weak password
        fails and returns an appropriate error message.
        """
        # Test Registration with invalid password
        data = {"username": "user_with_invalid_pass", "password": "123"} # Weak password
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Expect error status
        self.assertFalse(response.data["data"]["val"]) # Confirm failure flag
        self.assertIn("password", response.data["data"]["detail"]) # Check password error message

    def test_token_obtain_inactive_user(self):
        """Test token generation for an inactive user.

        This test verifies that an inactive user cannot obtain a JWT token
        and receives an unauthorized error.
        """
        # Test Token Generation for Inactive User
        data = {"username": "inactiveuser", "password": "securepassword"} # Inactive
        # user credentials
        response = self.client.post(self.token_url, data, format="json")

        # Assert that the response status is unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Expect auth error

    def test_token_obtain_with_empty_payload(self):
        """Test token generation with an empty payload.

        This test checks that sending an empty payload to the token endpoint
        results in a bad request error.
        """
        # Test Token with Empty Payload
        response = self.client.post(self.token_url, {}, format="json") # Empty request body
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Expect error status

    def test_get_not_allowed_on_token_endpoint(self):
        """Test GET request on the token endpoint.

        This test verifies that sending a GET request to the token endpoint
        is not allowed and returns a method not allowed error.
        """
        self.token_url = reverse("token_obtain_pair") # GET request to token endpoint
        response = self.client.get(self.token_url)

        # Check that the response status code is 405 Method Not Allowed
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED)  # Method not allowed status

        # Check the response message content
        self.assertEqual(response.data, {"msg": "Get not allowed"}) # Confirm error message

    # def test_get_not_allowed_on_token_endpoint(self):
    #     """Test GET request on the token endpoint.

    #     This test verifies that sending a GET request to the token endpoint
    #     is not allowed and returns a method not allowed error.
    #     """
    #     self.token_url = reverse("token_obtain_pair") # GET request to token endpoint
    #     response = self.client.get(self.token_url)
    #     self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    #     Method not allowed status
    #     self.assertEqual(response.data, {"msg": "Get not allowed"}) # Confirm error message

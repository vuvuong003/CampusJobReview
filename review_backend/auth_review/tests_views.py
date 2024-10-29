from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self):
        # Create a user to test the login and token functionality
        self.test_user = User.objects.create_user(
            username="testuser", password="securepassword"
        )
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")
        self.token_refresh_url = reverse("token_refresh")

    def test_register_new_user_success(self):
        # Test successful registration
        data = {"username": "newuser", "password": "newpassword123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["val"])
        self.assertEqual(
            response.data["data"]["detail"],
            "Registration Successful")

    def test_register_existing_user_error(self):
        # Test registration with an existing username
        data = {"username": "testuser", "password": "newpassword123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["data"]["val"])
        self.assertEqual(response.data["data"]["detail"], "Username Exists")

    def test_token_obtain_pair_success(self):
        # Test JWT token generation with valid credentials
        data = {"username": "testuser", "password": "securepassword"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["val"])
        self.assertIn("tokens", response.data["data"])
        self.assertIn("tenant_id", response.data["data"]["details"])

    def test_token_obtain_pair_invalid_credentials(self):
        # Test token generation with invalid credentials
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_success(self):
        # Test refreshing a valid token
        data = {"username": "testuser", "password": "securepassword"}
        login_response = self.client.post(self.token_url, data, format="json")
        refresh_token = login_response.data["data"]["tokens"]["refresh"]
        response = self.client.post(
            self.token_refresh_url, {
                "refresh": refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_register_user_invalid_password(self):
        # Test Registration with invalid password
        data = {"username": "user_with_invalid_pass", "password": "123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["data"]["val"])
        self.assertIn("password", response.data["data"]["detail"])

    def test_token_obtain_inactive_user(self):
        # Test Token Generation for Inactive User
        inactive_user = User.objects.create_user(
            username="inactiveuser",
            password="securepassword",
            is_active=False)
        data = {"username": "inactiveuser", "password": "securepassword"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_obtain_with_empty_payload(self):
        # Test Token with Empty Payload
        response = self.client.post(self.token_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_not_allowed_on_token_endpoint(self):
        # Send a GET request to the token endpoint
        self.token_url = reverse("token_obtain_pair")
        response = self.client.get(self.token_url)

        # Check that the response status code is 405 Method Not Allowed
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED)

        # Check the response message content
        self.assertEqual(response.data, {"msg": "Get not allowed"})

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer

User = get_user_model()

class RegisterSerializerTest(TestCase):
    def test_valid_registration_data(self):
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
        data = {
            "password": "StrongPassword123!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_registration_missing_password(self):
        data = {
            "username": "newuser"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_registration_duplicate_username(self):
        User.objects.create_user(username="existinguser", password="StrongPassword123!")
        data = {
            "username": "existinguser",
            "password": "AnotherStrongPassword456!"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

class MyTokenObtainPairSerializerTest(TestCase):
    def test_get_token_with_valid_user(self):
        user = User.objects.create_user(username="testuser", password="securepassword")
        serializer = MyTokenObtainPairSerializer()
        token = serializer.get_token(user)
        
        self.assertIn("username", token)
        self.assertEqual(token["username"], user.username)

    def test_get_token_for_nonexistent_user(self):
        with self.assertRaises(ValidationError):
            # This part simulates getting a token for a non-existent user
            serializer = MyTokenObtainPairSerializer()
            serializer.get_token(None)  # Should raise an error
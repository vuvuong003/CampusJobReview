from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

class ClientModelTests(TestCase):
    
    def test_create_regular_user(self):
        """Test creating a regular user and verifying default attributes"""
        user = User.objects.create_user(username="regularuser", password="password123")
        
        self.assertEqual(user.username, "regularuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)
        
    def test_create_superuser(self):
        """Test creating a superuser and verifying superuser-specific attributes"""
        superuser = User.objects.create_superuser(username="adminuser", password="adminpass123")
        
        self.assertEqual(superuser.username, "adminuser")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_superuser)
    
    def test_create_user_without_username(self):
        """Test that creating a user without a username raises an error"""
        with self.assertRaises(TypeError):
            User.objects.create_user(username=None, password="password123")
    
    def test_create_user_with_duplicate_username(self):
        """Test that creating a user with an existing username raises an error"""
        User.objects.create_user(username="duplicateuser", password="password123")
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="duplicateuser", password="password123")
    
    def test_create_superuser_without_password(self):
        """Test that creating a superuser without a password raises an error"""
        with self.assertRaises(TypeError):
            User.objects.create_superuser(username="adminuser", password=None)
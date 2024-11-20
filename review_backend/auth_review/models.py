"""
Module for defining custom user models and their management for the application.

This module contains the `Client` model, which customizes user fields and
permissions. It also includes a custom manager, `ClientManager`, for
creating regular users and superusers. The `Client` model is based on
Django's AbstractBaseUser and PermissionsMixin, allowing for flexibility
in user authentication and management.
"""
# Import Django's model base class
from django.db import models  # pylint: disable=E0401
from django.contrib.auth.models import (  # pylint: disable=E0401
    AbstractBaseUser, # Provides basic authentication fields
    BaseUserManager, # Base class for creating custom user managers
    PermissionsMixin, # Base class for creating custom user managers
    Group, Permission
)

# Custom manager for the Client model, responsible for creating regular and super users
class ClientManager(BaseUserManager):
    """
    Custom manager for the Client model.

    This class defines methods for creating regular users and superusers,
    ensuring that necessary fields are validated and set during user creation.

    Methods:
        create_user(username, password=None): Creates a regular user.
        create_superuser(username, password=None): Creates a superuser with
            admin privileges.
    """

    # create a regular user with optional password?

    def create_user(self, username, password=None):
        """
        Create and return a regular user with an encrypted password.

        Args:
            username (str): The username for the user.
            password (str, optional): The password for the user.

        Raises:
            TypeError: If username is None.

        Returns:
            Client: The created user instance.
        """
        if username is None:
            raise TypeError("User should have a username")
        user = self.model(username=username) # Instantiate user with username
        user.set_password(password) # Encrypt and set password

        user.save(using=self._db) # Save user to the database
        return user

    # creates a superuser. Passwords is enforced for superuser accounts
    def create_superuser(self, username, password=None):
        """
        Create and return a superuser with an encrypted password.
        Args:
            username (str): The username for the superuser.
            password (str, optional): The password for the superuser.
        Raises:
            TypeError: If password is None.
        Returns:
            Client: The created superuser instance.
        """
        if password is None:
            raise TypeError("Password should not be none")
        user = self.create_user(username, password) # Reuse create_user method
        user.is_active = True
        user.is_superuser = True # Grant superuser privileges
        user.is_staff = True # Grant staff privileges
        user.is_admin = True # Grant admin privileges
        user.save(using=self._db) # Save superuser to the database
        return user

# pylint: disable=R0903
class Client(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the application.

    This model customizes user fields and permissions, including unique
    usernames and various role-related attributes.

    Attributes:
        is_active (bool): Indicates if the user account is active.
        username (str): Unique username for the user, used as primary key.
        is_admin (bool): Grants admin privileges if True.
        is_staff (bool): Grants staff privileges if True.

    USERNAME_FIELD: The field used for authentication.
    objects: The custom manager for user creation.

    Methods:
        __str__(): Returns the username as the string representation of
                    the Client instance.
    """

    is_active = models.BooleanField(default=True) # Marks user as active
    username = models.CharField(
        max_length=50, primary_key=True, unique=True, blank=False
    ) # Unique username, primary key

    is_admin = models.BooleanField(default=False) # Marks user as admin
    is_staff = models.BooleanField(default=False) # Marks user as staff

    USERNAME_FIELD = "username" # Set 'username' as identifier for authentication
    objects = ClientManager() # Assign custom manager for user creation
    groups = models.ManyToManyField(Group, related_name="client_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="client_permissions", blank=True)


    # pylint: disable=E0307
    def __str__(self):
        """
        Returns the string representation of the Client instance.

        Returns:
            str: The username of the client.
        """
        return self.username

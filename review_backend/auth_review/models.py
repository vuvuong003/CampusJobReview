"""
Module for defining custom user models and their management for the application.

This module contains the `Client` model, which customizes user fields and
permissions. It also includes a custom manager, `ClientManager`, for
creating regular users and superusers. The `Client` model is based on
Django's AbstractBaseUser and PermissionsMixin, allowing for flexibility
in user authentication and management.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.
# Customer manager class for the Client model. This class defines methods for creating regular
# users and superusers


class ClientManager(BaseUserManager):
    """
    Custom manager for the Client model.

    This class defines methods for creating regular users and superusers,
    ensuring that the necessary fields are validated and set during
    user creation.

    Methods:
        create_user(username, password=None, **extra_fields): Creates
                    a regular user with a username and optional password.
        create_superuser(username, password=None, **extra_fields): Creates
                    a superuser with admin privileges and required password.
    """
    # create a regular user with optional password?

    def create_user(self, username, password=None):
        """
        Create and return a regular user with an encrypted password.

        Args:
            username (str): The username for the user.
            password (str, optional): The password for the user.
            **extra_fields: Additional fields for the user.

        Raises:
            TypeError: If username is None.

        Returns:
            Client: The created user instance.
        """
        if username is None:
            raise TypeError("User should have a username")
        user = self.model(username=username)
        # hashes the password before saving the user
        user.set_password(password)

        user.save(using=self._db)
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
        user = self.create_user(username, password)
        user.is_active = True
        user.is_superuser = True
        # are the staff and admin our superusers?
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


# client class allows for customization of user fields and permissions

# Disable the "too-few-public-methods" warning for this class
# since AppConfig subclasses typically require only one or no methods.
class Client(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the application.

    This model allows for customization of user fields and permissions,
    including unique usernames and various role attributes.

    Attributes:
        is_active (bool): Indicates whether the account is active.
        username (str): Unique username for the user, serves as primary key.
        is_admin (bool): Indicates whether the user has admin privileges.
        is_staff (bool): Indicates whether the user has staff privileges.

    USERNAME_FIELD: The field used for authentication.
    objects: The custom manager for creating users and superusers.

    Methods:
        __str__(): Returns the username as the string representation of
                    the Client instance.
    """

    # indication of whether the account is active
    is_active = models.BooleanField(default=True)
    # character field that serves as a primary key and has to be unique
    username = models.CharField(
        max_length=50, primary_key=True, unique=True, blank=False
    )

    # role = models.CharField(choices=ROLE, default=ROLE[0], max_length=50)
    # indication of whether the user has admin privileges
    is_admin = models.BooleanField(default=False)
    # indication of whether the user has staff privileges
    is_staff = models.BooleanField(default=False)

    # username should be used to identify users during the login
    USERNAME_FIELD = "username"
    # allows custom methods for creating users and superusers
    objects = ClientManager()

    # def has_profile(self):
    #     return hasattr(self, 'participantprofile')

    # return the username as a string representation of the Client instance.
    def __str__(self):
        """
        Returns the string representation of the Client instance.

        Returns:
            str: The username of the client.
        """
        return self.username

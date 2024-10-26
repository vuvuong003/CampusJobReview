from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
# Customer manager class for the Client model. This class defines methods for creating regular
# users and superusers
class ClientManager(BaseUserManager):
    # create a regular user with optional password?
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('User should have a username')
        user = self.model(username=username)
        # hashes the password before saving the user
        user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    # creates a superuser. Passwords is enforced for superuser accounts
    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(username, password)
        user.is_active = True
        user.is_superuser = True
        # are the staff and admin our superusers?
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

# client class allows for customization of user fields and permissions 
class Client(AbstractBaseUser, PermissionsMixin):
    # indication of whether the account is active
    is_active = models.BooleanField(default=True)
    # character field that serves as a primary key and has to be unique
    username = models.CharField(max_length=50, primary_key=True, unique=True, blank=False)

    #role = models.CharField(choices=ROLE, default=ROLE[0], max_length=50)
    # indication of whether the user has admin privileges
    is_admin = models.BooleanField(default=False)
    # indication of whether the user has staff privileges
    is_staff = models.BooleanField(default=False)

    # username should be used to identify users during the login
    USERNAME_FIELD = 'username' 
    # allows custom methods for creating users and superusers
    objects = ClientManager()

    # def has_profile(self):
    #     return hasattr(self, 'participantprofile')

    # return the username as a string representation of the Client instance. 
    def __str__(self):
        return self.username

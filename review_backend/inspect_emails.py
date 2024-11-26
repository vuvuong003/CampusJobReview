"""
Module for print all the users with their email ids

This module is to be used just for inspecting the database.
"""

import os
import django
from django.contrib.auth import get_user_model

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'review_backend.settings')
django.setup()

User = get_user_model()

def inspect_emails():
    """
    This method fetches all the users from the database and prints their username and email.

    Only to be used for inspecting.
    """
    users = User.objects.all()
    for user in users:
        print(f'Username: {user.username}, Email: {user.email}')

if __name__ == '__main__':
    inspect_emails()

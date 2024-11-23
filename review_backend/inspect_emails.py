import os
import django
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'review_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def inspect_emails():
    users = User.objects.all()
    for user in users:
        print(f'Username: {user.username}, Email: {user.email}')

if __name__ == '__main__':
    inspect_emails()
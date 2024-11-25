from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate email field for existing users with a default email address and delete user with username "username"'

    def handle(self, *args, **kwargs):
        # Delete user with username "username"
        user_to_delete = User.objects.filter(username='username').first()
        if user_to_delete:
            user_to_delete.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted user with username "username"'))
        
        # Populate email field for existing users
        users = User.objects.filter(Q(email__isnull=True) | Q(email=''))
        for user in users:
            try:
                if not user.email:  # Check if the email is empty or null
                    user.email = f'{user.username}@example.com'  # Use username to create a unique email
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated email for user: {user.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to update email for user {user.username}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('All users have been updated.'))

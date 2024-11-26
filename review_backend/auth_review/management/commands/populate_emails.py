"""
This module contains a command class for populating the email fields
with a default email for existing users. This module was added to solve
the migration issues related to adding email field to the existing database schema.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class Command(BaseCommand):
    """
    Command class to populate for existing users with a default email address
    and delete user with username 'username'
    """
    help = '''Populate email field for existing users with a
    default email address and delete user with username "username"'''

    # pylint: disable=W0718,W0613
    def handle(self, *args, **kwargs):
        """
        This method deletes the user with username 'username' and
        adds a default email to the email field for existing users.
        """
        # Delete user with username "username"
        user_to_delete = User.objects.filter(username='username').first()
        if user_to_delete:
            user_to_delete.delete()
            self.stdout.write(
                self.style.SUCCESS('Successfully deleted user with username "username"')
            )

        # Populate email field for existing users
        users = User.objects.filter(Q(email__isnull=True) | Q(email=''))
        for user in users:
            try:
                if not user.email:  # Check if the email is empty or null
                    # Use username to create a unique email
                    user.email = f'{user.username}@example.com'
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully updated email for user: {user.username}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to update email for user {user.username}: {e}')
                )

        self.stdout.write(self.style.SUCCESS('All users have been updated.'))

"""
This module contains a command for deleting users from the database.

This is called from the command line manually.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    """
    Command class to delete users from the database.

    Methods:
        handle: deletes users
    """
    help = 'Delete specified users from the database'

    # pylint: disable=W0613
    def handle(self, *args, **kwargs):
        """
        This methods deletes the users specified with usernames in `users_to_delete.

        It displays a success message if a user is successfully deleted
        and a warning message if a username is not found in the database.
        """
        users_to_delete = [
            'Khandu',
            'Demon',
            'Zekken',
            'omkarddesai',
            'Rohan',
            'RK',
            'RRK',
            'BADBOYXD01',
            'hpsalway'
        ]

        for username in users_to_delete:
            try:
                user = User.objects.get(username=username)
                user.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully deleted user: {username}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'User not found: {username}')
                )

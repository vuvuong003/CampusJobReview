from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Delete specified users from the database'

    def handle(self, *args, **kwargs):
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
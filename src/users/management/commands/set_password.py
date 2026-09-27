# File: src/users/management/commands/set_password.py
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from users.models import User

class Command(BaseCommand):
    help = 'Resets the password for an existing user.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username to update.')
        parser.add_argument('password', type=str, help='The new password.')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User '{username}' does not exist.")

        user.password = make_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Password for user '{username}' has been reset successfully."))
# File: src/users/management/commands/create_admin.py
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from users.models import User
import getpass

class Command(BaseCommand):
    help = "Creates a new administrator user in the users_user table."

    def handle(self, *args, **options):
        username = input("Username: ")
        email = input("Email: ")
        password = getpass.getpass("Password: ")

        if User.objects.filter(username=username).exists():
            raise CommandError(f"User '{username}' already exists.")

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_admin=True,
            is_active=True,
            is_staff=True,  # IMPORTANT to access /admin/
            is_superuser=True  # IMPORTANT to fully manage Wagtail
        )

        self.stdout.write(self.style.SUCCESS(f"Admin user '{username}' created successfully."))
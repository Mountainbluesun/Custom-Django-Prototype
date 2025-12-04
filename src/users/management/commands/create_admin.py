# Fichier : src/users/management/commands/create_admin.py
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from users.models import User
import getpass

class Command(BaseCommand):
    help = "Crée un nouvel utilisateur administrateur dans la table users_user."

    def handle(self, *args, **options):
        username = input("Nom d'utilisateur : ")
        email = input("Email : ")
        password = getpass.getpass("Mot de passe : ")

        if User.objects.filter(username=username).exists():
            raise CommandError(f"L'utilisateur '{username}' existe déjà.")

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_admin=True,
            is_active=True,
            is_staff=True,  # IMPORTANT pour accéder à /admin/
            is_superuser=True  # IMPORTANT pour gérer Wagtail entièrement
        )

        self.stdout.write(self.style.SUCCESS(f"Utilisateur admin '{username}' créé avec succès."))
# Fichier : src/users/management/commands/set_password.py
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from users.models import User

class Command(BaseCommand):
    help = 'Réinitialise le mot de passe pour un utilisateur existant.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Le nom de l\'utilisateur à modifier.')
        parser.add_argument('password', type=str, help='Le nouveau mot de passe.')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"L'utilisateur '{username}' n'existe pas.")

        user.password = make_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Le mot de passe pour l'utilisateur '{username}' a été réinitialisé avec succès."))
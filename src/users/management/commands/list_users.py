# Fichier : src/users/management/commands/list_users.py
from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Liste les utilisateurs de la base de données avec des filtres optionnels.'

    def add_arguments(self, parser):
        parser.add_argument('--admins', action='store_true', help='Affiche uniquement les administrateurs.')
        parser.add_argument('--active', action='store_true', help='Affiche uniquement les utilisateurs actifs.')

    def handle(self, *args, **options):
        # On commence par récupérer tous les utilisateurs
        users = User.objects.all()

        # On applique les filtres si demandés
        if options['admins']:
            users = users.filter(is_admin=True)
        if options['active']:
            users = users.filter(is_active=True)

        # On affiche le résultat
        if not users:
            self.stdout.write("Aucun utilisateur trouvé avec ces critères.")
            return

        for user in users:
            is_admin_str = " (Admin)" if user.is_admin else ""
            self.stdout.write(f"- {user.username}{is_admin_str}")
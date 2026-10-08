from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Lists users from the database with optional filters.'

    def add_arguments(self, parser):
        parser.add_argument('--admins', action='store_true', help='Show only administrators.')
        parser.add_argument('--active', action='store_true', help='Show only active users.')

    def handle(self, *args, **options):
        # Start by fetching all users
        users = User.objects.all()

        # Apply filters if requested
        if options['admins']:
            users = users.filter(is_admin=True)
        if options['active']:
            users = users.filter(is_active=True)

        # Display the result
        if not users:
            self.stdout.write("No users found matching these criteria.")
            return

        for user in users:
            is_admin_str = " (Admin)" if user.is_admin else ""
            self.stdout.write(f"- {user.username}{is_admin_str}")
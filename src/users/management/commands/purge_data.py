import logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Purges expired user sessions and performs automated database cleanup tasks."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Number of retention days for inactive logs or stale record purging (default: 30 days).",
        )

    def handle(self, *args, **options):
        retention_days = options["days"]
        cutoff_date = timezone.now() - timedelta(days=retention_days)

        self.stdout.write(self.style.NOTICE("Starting automated data cleanup job..."))

        # 1. Purge expired Django sessions
        deleted_sessions_count, _ = Session.objects.filter(
            expire_date__lt=timezone.now()
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {deleted_sessions_count} expired session(s)."
            )
        )

        # Log completion details for audit logs
        logger.info(
            f"Cron Job Execute: Purged {deleted_sessions_count} expired sessions."
        )
        self.stdout.write(self.style.SUCCESS("Data cleanup job completed successfully."))
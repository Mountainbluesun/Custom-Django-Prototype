from pathlib import Path
from typing import List, Dict, Optional
from django.core.management.base import BaseCommand, CommandError
import shutil

from core.json_storage import load_json, save_json
from core.paths import data_dir


class Command(BaseCommand):
    help = "Deletes a JSON user by username (with backup before deletion)."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="Username to delete")
        parser.add_argument("--base-dir", default=None, help="Data folder (default: <project>/data)")
        parser.add_argument("--force", action="store_true", help="Delete without asking for confirmation")

    def handle(self, *args, **options):
        username: str = options["username"].strip()
        base_dir_opt: Optional[str] = options["base_dir"]

        base: Path = Path(base_dir_opt).resolve() if base_dir_opt else data_dir()
        base.mkdir(parents=True, exist_ok=True)

        users_path = base / "users.json"
        if not users_path.exists():
            raise CommandError(f"No users.json file found in {base}")

        users: List[Dict] = load_json(users_path.name, base_dir=base) or []

        if not any(u.get("username") == username for u in users):
            raise CommandError(f"User '{username}' does not exist.")

        # Confirmation if --force is not set
        if not options["force"]:
            confirm = input(f"Are you sure you want to delete '{username}'? (y/N) ").lower()
            if confirm != "y":
                self.stdout.write(self.style.WARNING("Deletion cancelled."))
                return

        # Backup before deletion
        backup_path = users_path.with_suffix(".json.bak")
        shutil.copy(users_path, backup_path)

        # Delete
        new_users = [u for u in users if u.get("username") != username]
        save_json(users_path.name, new_users, base_dir=base)

        self.stdout.write(self.style.SUCCESS(
            f"✅ User '{username}' deleted (backup → {backup_path})"
        ))
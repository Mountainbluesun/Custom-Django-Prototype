from pathlib import Path
from typing import List, Dict, Optional
from django.core.management.base import BaseCommand, CommandError
import shutil

from core.json_storage import load_json, save_json
from core.paths import data_dir


class Command(BaseCommand):
    help = "Supprime un utilisateur JSON par son username (avec backup avant suppression)."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="Nom d'utilisateur à supprimer")
        parser.add_argument("--base-dir", default=None, help="Dossier data (défaut: <projet>/data)")
        parser.add_argument("--force", action="store_true", help="Supprime sans demander confirmation")

    def handle(self, *args, **options):
        username: str = options["username"].strip()
        base_dir_opt: Optional[str] = options["base_dir"]

        base: Path = Path(base_dir_opt).resolve() if base_dir_opt else data_dir()
        base.mkdir(parents=True, exist_ok=True)

        users_path = base / "users.json"
        if not users_path.exists():
            raise CommandError(f"Aucun fichier users.json trouvé dans {base}")

        users: List[Dict] = load_json(users_path.name, base_dir=base) or []

        if not any(u.get("username") == username for u in users):
            raise CommandError(f"L’utilisateur '{username}' n’existe pas.")

        # Confirmation si pas --force
        if not options["force"]:
            confirm = input(f"Voulez-vous vraiment supprimer '{username}' ? (o/N) ").lower()
            if confirm != "o":
                self.stdout.write(self.style.WARNING("Suppression annulée."))
                return

        # Backup avant suppression
        backup_path = users_path.with_suffix(".json.bak")
        shutil.copy(users_path, backup_path)

        # Supprimer
        new_users = [u for u in users if u.get("username") != username]
        save_json(users_path.name, new_users, base_dir=base)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Utilisateur '{username}' supprimé (backup → {backup_path})"
        ))

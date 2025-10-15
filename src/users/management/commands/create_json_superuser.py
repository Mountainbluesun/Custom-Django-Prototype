# src/users/management/commands/create_json_superuser.py
from pathlib import Path
from typing import List, Dict, Optional
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password

from core.json_storage import load_json, save_json
from core.paths import data_dir


def _next_id(users: List[Dict]) -> int:
    return max((int(u.get("id", 0)) for u in users), default=0) + 1


class Command(BaseCommand):
    help = "Crée un utilisateur admin dans data/users.json (sans base de données)."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--email", default="")
        parser.add_argument("--password", required=True)
        parser.add_argument("--base-dir", default=None, help="Dossier data (défaut: <projet>/data)")

    def handle(self, *args, **options):
        username: str = options["username"].strip()
        email: str = options["email"].strip()
        password: str = options["password"]
        base_dir_opt: Optional[str] = options["base_dir"]

        if not username or not password:
            raise CommandError("username et password sont obligatoires.")

        base: Path = Path(base_dir_opt).resolve() if base_dir_opt else data_dir()
        base.mkdir(parents=True, exist_ok=True)

        users_path = base / "users.json"
        users: List[Dict] = load_json(users_path.name, base_dir=base) or []

        if any(u.get("username") == username for u in users):
            raise CommandError(f"L'utilisateur '{username}' existe déjà.")

        user = {
            "id": _next_id(users),
            "username": username,
            "email": email,
            "password": make_password(password),  # ✅ hash sécurisé
            "companies": [],
            "is_admin": True,
            "is_active": True,
        }

        users.append(user)
        save_json(users_path.name, users, base_dir=base)

        self.stdout.write(self.style.SUCCESS(
            f"Admin JSON créé: {username} (id={user['id']}) → {users_path}"
        ))


from django.contrib.auth.hashers import make_password


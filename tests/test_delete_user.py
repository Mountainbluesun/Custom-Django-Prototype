import json
from pathlib import Path
import subprocess
import sys


def test_delete_json_user(tmp_path: Path):
    # Prépare un fichier users.json factice
    users_file = tmp_path / "users.json"
    users = [
        {"id": 1, "username": "alice", "password_hash": "xxx"},
        {"id": 2, "username": "bob", "password_hash": "yyy"},
    ]
    users_file.write_text(json.dumps(users))

    # Appelle la commande via subprocess (comme en vrai)
    result = subprocess.run(
        [
            sys.executable, "manage.py", "delete_json_user",
            "--username", "bob", "--base-dir", str(tmp_path), "--force"
        ],
        capture_output=True, text=True
    )

    # Vérifie que la commande réussit
    assert result.returncode == 0
    assert "supprimé" in result.stdout

    # Vérifie que bob a disparu
    data = json.loads(users_file.read_text())
    usernames = [u["username"] for u in data]
    assert "bob" not in usernames
    assert "alice" in usernames

    # Vérifie que le backup existe
    backup_file = tmp_path / "users.json.bak"
    assert backup_file.exists()

import json
from pathlib import Path
import subprocess
import sys


def test_delete_json_user(tmp_path: Path):
    # Prepare a fake users.json file
    users_file = tmp_path / "users.json"
    users = [
        {"id": 1, "username": "alice", "password": "xxx"},
        {"id": 2, "username": "bob", "password": "yyy"},
    ]
    users_file.write_text(json.dumps(users))

    # Call the command via subprocess (as it would run for real)
    result = subprocess.run(
        [
            sys.executable, "manage.py", "delete_json_user",
            "--username", "bob", "--base-dir", str(tmp_path), "--force"
        ],
        capture_output=True, text=True
    )

    # Check that the command succeeds
    assert result.returncode == 0
    assert "deleted" in result.stdout

    # Check that bob has disappeared
    data = json.loads(users_file.read_text())
    usernames = [u["username"] for u in data]
    assert "bob" not in usernames
    assert "alice" in usernames

    # Check that the backup exists
    backup_file = tmp_path / "users.json.bak"
    assert backup_file.exists()
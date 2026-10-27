import getpass
import hashlib
import json
import os
import secrets
from pathlib import Path


PASSWORD_ITERATIONS = 600_000
TEACHERS_FILE = Path(
    os.environ.get("TEACHERS_FILE", str(Path(__file__).with_name("teachers.json")))
)


def main():
    username = input("Teacher username: ").strip()
    if not username:
        raise SystemExit("Username cannot be empty.")

    password = getpass.getpass("Teacher password: ")
    if not password:
        raise SystemExit("Password cannot be empty.")
    if password != getpass.getpass("Confirm password: "):
        raise SystemExit("Passwords do not match.")

    if TEACHERS_FILE.exists():
        try:
            data = json.loads(TEACHERS_FILE.read_text(encoding="utf-8"))
            teachers = data["teachers"]
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            raise SystemExit("Teacher credentials file is invalid.")
    else:
        data = {"teachers": []}
        teachers = data["teachers"]

    if any(teacher.get("username") == username for teacher in teachers):
        raise SystemExit("That teacher username already exists.")

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    ).hex()
    teachers.append({
        "username": username,
        "salt": salt.hex(),
        "password_hash": password_hash,
    })

    TEACHERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TEACHERS_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    TEACHERS_FILE.chmod(0o600)
    print(f"Added teacher '{username}' to {TEACHERS_FILE}.")


if __name__ == "__main__":
    main()
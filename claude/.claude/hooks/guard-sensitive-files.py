#!/usr/bin/env python3
"""
PreToolUse hook: block edits to files that likely contain secrets or credentials.
Works on Windows, Linux, and macOS without additional dependencies.
Exit code 2 = block the action and show the message to the user.

Matching is on file names and extensions, not substrings, so source files such as
PasswordResetServlet.java or a password-reset component are not blocked.
"""
import json
import os
import re
import sys

# Key and certificate stores: always sensitive, whatever the file is called
SENSITIVE_EXTENSIONS = {".key", ".pem", ".jks", ".p12", ".pfx", ".keystore", ".truststore"}

# Config-style files whose name says they hold secrets (credentials.json, secrets.yaml, password.txt)
SECRET_NAME = re.compile(r"(^|[._-])(credentials?|secrets?|passwords?)([._-]|$)")
CONFIG_EXTENSIONS = {"", ".json", ".yaml", ".yml", ".properties", ".txt", ".cfg", ".conf", ".ini", ".toml", ".xml"}


def sensitive_reason(file_path: str) -> str | None:
    """Return why the file is sensitive, or None when it may be edited."""
    name = os.path.basename(file_path).lower()
    stem, extension = os.path.splitext(name)
    if name == ".env" or name.startswith(".env.") or extension == ".env":
        return "environment file"
    if extension in SENSITIVE_EXTENSIONS:
        return f"'{extension}' key or certificate file"
    if extension in CONFIG_EXTENSIONS and SECRET_NAME.search(stem):
        return "configuration file named as holding secrets"
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    reason = sensitive_reason(file_path)
    if reason:
        print(json.dumps({
            "decision": "block",
            "reason": f"Blocked: '{file_path}' looks like a sensitive file ({reason}). Edit it manually if this is intentional.",
        }))
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()

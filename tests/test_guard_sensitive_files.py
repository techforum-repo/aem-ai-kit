"""Tests for claude/.claude/hooks/guard-sensitive-files.py. Run: python3 -m unittest discover tests"""

import importlib.util
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "claude" / ".claude" / "hooks" / "guard-sensitive-files.py"
spec = importlib.util.spec_from_file_location("guard_sensitive_files", HOOK)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

BLOCKED = [
    ".env",
    ".env.local",
    "config/prod.env",
    "certs/server.key",
    "certs/server.pem",
    "keystore.jks",
    "client.p12",
    "C:\\Users\\dev\\project\\cert.pfx",
    "credentials.json",
    "aws-credentials",
    "secrets.yaml",
    "app.secret.properties",
    "db_password.txt",
]

ALLOWED = [
    "core/src/main/java/com/example/core/servlets/PasswordResetServlet.java",
    "core/src/main/java/com/example/core/services/SecretProviderService.java",
    "core/src/main/java/com/example/core/models/CredentialsForm.java",
    "ui.apps/src/main/content/jcr_root/apps/site/components/password-reset/password-reset.html",
    "ui.frontend/src/components/secret-banner.ts",
    "ui.config/src/main/content/jcr_root/apps/site/osgiconfig/config/com.example.ApiClient.cfg.json",
    "environment.md",
    "docs/keyboard.md",
    "monkey.json",
]


class GuardSensitiveFilesTest(unittest.TestCase):
    def test_blocks_secret_files(self):
        for path in BLOCKED:
            with self.subTest(path=path):
                self.assertIsNotNone(guard.sensitive_reason(path))

    def test_allows_source_files(self):
        for path in ALLOWED:
            with self.subTest(path=path):
                self.assertIsNone(guard.sensitive_reason(path))


if __name__ == "__main__":
    unittest.main()

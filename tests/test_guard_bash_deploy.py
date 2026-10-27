"""Tests for claude/.claude/hooks/guard-bash-deploy.py. Run: python3 -m unittest discover tests"""

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "claude" / ".claude" / "hooks" / "guard-bash-deploy.py"
spec = importlib.util.spec_from_file_location("guard_bash_deploy", HOOK)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

BLOCKED = [
    # autoInstall to a remote host, in every Maven spelling
    "mvn clean install -PautoInstallPackage -Daem.host=stage.example.com",
    "mvn clean install -P autoInstallPackage -Daem.host=stage.example.com",
    "mvn clean install -P autoInstallPackage -D aem.host=stage.example.com",
    "mvn clean install --activate-profiles=autoInstallPackage -Daem.host=stage.example.com",
    "mvn clean install --activate-profiles autoInstallSinglePackage -Daem.host=stage.example.com",
    "mvn clean install -Pfoo,autoInstallBundle -Daem.host=10.0.0.5",
    "mvn clean install -PautoInstallPackagePublish -Daem.publish.host=publish.example.com",
    "./mvnw clean install -PautoInstallPackage -Daem.host=stage.example.com",
    "cd core && mvn install -PautoInstallBundle -Daem.host=stage.example.com",
    'mvn clean install -PautoInstallPackage "-Daem.host=stage.example.com"',
    "MAVEN_OPTS=-Xmx2g mvn install -PautoInstallPackage -Daem.host=stage.example.com",
    # publishing goals
    "mvn deploy",
    "mvn clean deploy",
    "mvn -q clean deploy -DskipTests",
    "mvn deploy:deploy-file -Dfile=x.jar",
    "mvn release:prepare",
    "git pull && mvn release:perform",
]

ALLOWED = [
    "mvn clean install",
    "mvn clean install -DskipTests",
    "mvn clean install -PautoInstallPackage",
    "mvn clean install -PautoInstallPackage -Daem.host=localhost -Daem.port=4502",
    "mvn clean install -P autoInstallPackage -Daem.host=127.0.0.1",
    "mvn test -Dtest=DeployServiceTest",
    "mvn spotless:apply",
    "git log --grep deploy",
    "echo mvn deploy is blocked",
    "npm run deploy",
]


class GuardBashDeployTest(unittest.TestCase):
    def test_blocks_remote_or_publishing_commands(self):
        for command in BLOCKED:
            with self.subTest(command=command):
                self.assertIsNotNone(guard.check(command))

    def test_allows_local_commands(self):
        for command in ALLOWED:
            with self.subTest(command=command):
                self.assertIsNone(guard.check(command))

    def test_hook_protocol(self):
        """The script exits 2 with a block decision on stdout, and 0 otherwise."""
        def run(command):
            payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
            env = {"PATH": "", "AEM_HOST": "localhost"}
            return subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True, env=env)

        blocked = run("mvn clean deploy")
        self.assertEqual(blocked.returncode, 2)
        self.assertEqual(json.loads(blocked.stdout)["decision"], "block")
        self.assertEqual(run("mvn clean install").returncode, 0)


if __name__ == "__main__":
    unittest.main()

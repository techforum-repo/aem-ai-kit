#!/usr/bin/env python3
"""
PreToolUse hook: block Maven commands that could deploy outside the local machine.
- autoInstall profiles targeting a non-localhost AEM instance (shared dev, stage, prod)
- the `deploy` phase and `release:*` goals, which publish artifacts
Exit code 2 = block the action and show the message to the user.
"""
import json
import os
import re
import shlex
import sys

# Hosts that are safe to deploy to without confirmation
LOCALHOST_VALUES = {"localhost", "127.0.0.1", "::1"}

# AEM_HOST env var — if set, used as the default deploy target
DEFAULT_HOST = os.environ.get("AEM_HOST", "localhost")

# Maven properties that select the AEM instance the archetype's autoInstall profiles target
HOST_PROPERTIES = {"aem.host", "aem.publish.host"}

# Shell operators that separate one command from the next
SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")"}


def split_commands(command: str) -> list[list[str]]:
    """Split a shell command line into the argument lists of its individual commands."""
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        # Unbalanced quotes: fall back to a plain split so the command is still inspected.
        tokens = command.split()
    commands, current = [], []
    for token in tokens:
        if token in SEPARATORS:
            if current:
                commands.append(current)
            current = []
        else:
            current.append(token)
    if current:
        commands.append(current)
    return commands


def is_maven(args: list[str]) -> bool:
    """True if the command runs Maven (mvn, mvnw, ./mvnw, mvn.cmd), ignoring leading VAR=value assignments."""
    for arg in args:
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", arg):
            continue
        return bool(re.match(r"^(.*[/\\])?mvnw?(\.cmd)?$", arg, re.IGNORECASE))
    return False


def parse_maven(args: list[str]) -> tuple[list[str], dict[str, str], list[str]]:
    """Return (profiles, -D properties, goals/phases) for a Maven argument list."""
    profiles, properties, goals = [], {}, []
    i = 0
    while i < len(args):
        arg = args[i]
        value = None
        if arg in ("-P", "--activate-profiles", "-D", "--define") and i + 1 < len(args):
            value = args[i + 1]
            i += 1
        if arg in ("-P", "--activate-profiles") or (arg.startswith("-P") and len(arg) > 2):
            profiles += (value if value is not None else arg[2:]).split(",")
        elif arg.startswith("--activate-profiles="):
            profiles += arg.split("=", 1)[1].split(",")
        elif arg in ("-D", "--define") or (arg.startswith("-D") and len(arg) > 2):
            name, _, prop_value = (value if value is not None else arg[2:]).partition("=")
            properties[name] = prop_value
        elif not arg.startswith("-"):
            goals.append(arg)
        i += 1
    return profiles, properties, goals


def check(command: str) -> str | None:
    """Return a block reason for the command, or None when it is allowed."""
    for args in split_commands(command):
        if not is_maven(args):
            continue
        profiles, properties, goals = parse_maven(args)

        publishing = [g for g in goals if g == "deploy" or g.startswith(("deploy:", "release:"))]
        if publishing:
            return f"Blocked: Maven '{' '.join(publishing)}' publishes artifacts and must be run manually."

        if any("autoinstall" in p.lstrip("!-").lower() for p in profiles):
            for name in sorted(HOST_PROPERTIES):
                host = properties.get(name, DEFAULT_HOST if name == "aem.host" else "localhost")
                if host.lower() not in LOCALHOST_VALUES:
                    return (
                        f"Blocked: Maven autoInstall targeting '{host}' ({name}, non-localhost).\n"
                        "Claude may only deploy to localhost."
                    )
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if payload.get("tool_name", "") != "Bash":
        sys.exit(0)

    command = payload.get("tool_input", {}).get("command", "")
    reason = check(command)
    if reason:
        print(json.dumps({
            "decision": "block",
            "reason": f"{reason} Run this command manually if intentional:\n  {command}",
        }))
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()

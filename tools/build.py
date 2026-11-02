#!/usr/bin/env python3
"""Export every Pelican egg (egg-*.yaml, PLCN_v3) in this tree to Pterodactyl's PTDL_v2 JSON.

The YAML files are the source of truth. Run after editing one:

    python3 tools/build.py          # write egg-pterodactyl-*.json next to each egg
    python3 tools/build.py --check  # only validate, exit 1 on problems
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ("name", "author", "uuid", "description", "docker_images", "startup_commands", "config", "scripts", "variables")
ENV_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")


def problems_in(egg, path):
    found = []
    for key in REQUIRED:
        if key not in egg:
            found.append(f"missing key '{key}'")
    if egg.get("meta", {}).get("version") != "PLCN_v3":
        found.append("meta.version must be PLCN_v3")

    startup = egg.get("startup_commands") or {}
    if not startup:
        found.append("no startup command")

    install = egg.get("scripts", {}).get("installation", {})
    for key in ("script", "container", "entrypoint"):
        if not install.get(key):
            found.append(f"scripts.installation.{key} is empty")

    names = set()
    for var in egg.get("variables") or []:
        env = str(var.get("env_variable", ""))
        if not ENV_NAME.match(env):
            found.append(f"bad env_variable '{env}'")
        if env in names:
            found.append(f"duplicate env_variable '{env}'")
        names.add(env)
        if not isinstance(var.get("rules"), list):
            found.append(f"{env}: rules must be a list")

    # every {{VAR}} in the startup line must be a declared variable or a panel built-in
    builtins = {"SERVER_PORT", "SERVER_IP", "SERVER_MEMORY", "SERVER_UUID", "P_SERVER_UUID", "P_SERVER_LOCATION", "TZ"}
    for line in startup.values():
        for ref in re.findall(r"\{\{([A-Z0-9_]+)\}\}", line):
            if ref not in names and ref not in builtins:
                found.append(f"startup uses undeclared {{{{{ref}}}}}")

    return [f"{path.relative_to(ROOT)}: {msg}" for msg in found]


def as_json_string(value):
    if not value:
        return "{}"
    return json.dumps(value, indent=4)


def to_pterodactyl(egg):
    config = egg.get("config", {})
    install = egg["scripts"]["installation"]
    return {
        "_comment": "DO NOT EDIT: FILE GENERATED AUTOMATICALLY BY PTERODACTYL PANEL - PTERODACTYL.IO",
        "meta": {"version": "PTDL_v2", "update_url": None},
        "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "name": egg["name"],
        "author": egg["author"],
        "description": egg["description"],
        "features": list(egg.get("features") or []),
        "docker_images": egg["docker_images"],
        "file_denylist": list(egg.get("file_denylist") or []),
        "startup": next(iter(egg["startup_commands"].values())),
        "config": {
            "files": as_json_string(config.get("files")),
            "startup": as_json_string(config.get("startup")),
            "logs": as_json_string(config.get("logs")),
            "stop": config.get("stop", "^C"),
        },
        "scripts": {
            "installation": {
                "script": install["script"],
                "container": install["container"],
                "entrypoint": install["entrypoint"],
            }
        },
        "variables": [
            {
                "name": var["name"],
                "description": var.get("description", ""),
                "env_variable": var["env_variable"],
                "default_value": "" if var.get("default_value") is None else str(var["default_value"]),
                "user_viewable": bool(var.get("user_viewable", True)),
                "user_editable": bool(var.get("user_editable", True)),
                "rules": "|".join(str(rule) for rule in var["rules"]),
                "field_type": "text",
            }
            for var in sorted(egg["variables"], key=lambda v: v.get("sort", 0))
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate only")
    args = parser.parse_args()

    eggs = sorted(p for p in ROOT.rglob("egg-*.yaml") if "tools" not in p.parts)
    issues = []
    for path in eggs:
        egg = yaml.safe_load(path.read_text(encoding="utf-8"))
        issues += problems_in(egg, path)
        if args.check:
            continue
        target = path.with_name(path.name.replace("egg-", "egg-pterodactyl-", 1)).with_suffix(".json")
        target.write_text(json.dumps(to_pterodactyl(egg), indent=4, ensure_ascii=False) + "\n", encoding="utf-8")

    for issue in issues:
        print(issue, file=sys.stderr)
    print(f"{len(eggs)} eggs, {len(issues)} problems")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())

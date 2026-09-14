#!/usr/bin/env python3
"""Minimal local host discovery; stdout only, no enrollment or system changes."""

import argparse
from datetime import datetime, timezone
import json
import os
import platform
import re
import shutil
import socket


TOOLS = (
    "git", "python3", "ssh", "sudo", "systemctl", "launchctl", "apt-get",
    "brew", "docker", "virsh", "ufw", "tmux", "herdr", "opencode",
    "claude", "code",
)


def host_id(value):
    """A portable logical label, never a path or a machine identity assertion."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", value):
        raise argparse.ArgumentTypeError(
            "host ID must be 1-63 lowercase ASCII letters/digits/hyphens, "
            "starting with a letter or digit"
        )
    return value


def collect_facts(proposed_host_id=None):
    if proposed_host_id is not None:
        host_id(proposed_host_id)
    return {
        "schema_version": 1,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "observed",
        "execution_scope": "local-process-host",
        "proposed_host_id": proposed_host_id,
        "host_binding_confirmed": False,
        "hostname_hint": socket.gethostname(),
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "effective_root": os.geteuid() == 0 if hasattr(os, "geteuid") else None,
        "tools_on_path": {name: shutil.which(name) is not None for name in TOOLS},
        "revalidate": "before any system change or host-profile enrollment",
        "limitations": [
            "Hostname is a hint, not verified identity.",
            "Tool presence does not prove version, health, or permission to use it.",
            "No service, firewall, routing, storage, or remote-host state was collected.",
            "Review output before saving it in an approved private knowledge store.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host-id", type=host_id, help="proposed logical label only")
    args = parser.parse_args()
    print(json.dumps(collect_facts(args.host_id), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
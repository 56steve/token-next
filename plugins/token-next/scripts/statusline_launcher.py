#!/usr/bin/env python3
"""Runs the newest installed token-next status line.

The status line setting points at this file, which is copied to a stable place.
Plugin updates change the folder the script lives in, so this finds the newest
one each time and the setting never goes stale.
"""

import glob
import os
import re
import sys

# The plugin's own folder, then the one it had when it was called token-bar, so a status line
# set up before the rename keeps working until the old plugin is removed.
PATTERNS = (
    "~/.claude/plugins/cache/token-next/token-next/*/scripts/token_next.py",
    "~/.claude/plugins/cache/token-bar/token-bar/*/scripts/token_bar.py",
)


def version_key(path):
    """Sorts install paths by the version folder, so 0.1.10 comes after 0.1.9."""
    version = os.path.normpath(path).split(os.sep)[-3]
    return [int(part) if part.isdigit() else 0 for part in re.split(r"[.\-]", version)]


def newest(paths):
    return max(paths, key=version_key) if paths else None


def find_script():
    """The newest installed copy of the plugin's script, under its own name or its old one. None if neither."""
    for pattern in PATTERNS:
        found = newest(glob.glob(os.path.expanduser(pattern)))
        if found:
            return found
    return None


def main():
    script = find_script()
    if not script:
        print("token-next: plugin not found")
        return 0
    os.execv(sys.executable, [sys.executable, script, "statusline"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

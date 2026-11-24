#!/usr/bin/env python3
"""Write the 3 AM commit message to the output path.

Entrypoint for the make.fun "The 3 AM Commit Message" bounty.
Stdlib only. The output path is resolved from the environment:
  ENTRY_OUTPUT, else OUTPUT_DIR / MAKEFUN_OUTPUT_DIR joined with
  entry.txt, else /output/entry.txt (falling back to this script's
  own directory when /output is not writable).
"""

import os
import sys

MESSAGE = (
    "revert(3am): prod is down, tests still green \u2014 "
    "I wrote them at 3 AM and they believed me"
)


def resolve_output_path():
    env_path = os.environ.get("ENTRY_OUTPUT")
    if env_path:
        return env_path
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    default = os.path.join(os.sep, "output", "entry.txt")
    try:
        parent = os.path.dirname(default)
        if os.path.isdir(parent) and os.access(parent, os.W_OK):
            return default
        os.makedirs(parent, exist_ok=True)
        return default
    except OSError:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "entry.txt"
        )


def main():
    text = MESSAGE.strip()
    if not text:
        raise SystemExit("error: message is empty")
    if len(text) > 200:
        raise SystemExit("error: message exceeds 200 characters")
    if "\n" in text or "\r" in text:
        raise SystemExit("error: message must be a single line")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    data = (text + "\n").encode("utf-8")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        if handle.read() != data:
            raise SystemExit("error: read-back mismatch for %s" % path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

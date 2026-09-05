#!/usr/bin/env python3
"""Generate the desktop cask from the final release DMG."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

TEMPLATE = Path(__file__).with_name("starfarer.rb.in")


def render(tag: str, digest: str, notarized: bool = False) -> str:
    if not re.fullmatch(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", tag):
        raise ValueError("Homebrew requires a stable release tag, such as v1.2.3")
    if not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise ValueError("Homebrew requires the release DMG's SHA-256 digest")
    notice = "" if notarized else (
        "    This preview is not notarized by Apple. If macOS blocks it, use\n"
        "    System Settings > Privacy & Security > Open Anyway.\n\n"
    )
    return (TEMPLATE.read_text().replace("@VERSION@", tag[1:])
            .replace("@SHA256@", digest).replace("@SIGNING_NOTICE@", notice)
            .replace("@NOTARIZED@", "true" if notarized else "false"))


def generate(tag: str, dmg: Path, output: Path, notarized: bool = False) -> None:
    with dmg.open("rb") as artifact:
        digest = hashlib.file_digest(artifact, "sha256").hexdigest()
    cask = render(tag, digest, notarized)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(cask)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--dmg", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--notarized", action="store_true")
    args = parser.parse_args()
    generate(args.tag, args.dmg, args.output, args.notarized)

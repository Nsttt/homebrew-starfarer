#!/usr/bin/env python3
"""Update a tap from Starfarer's published release manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from cask import render


def update(manifest: dict, output: Path) -> bool:
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("macos"), dict):
        raise ValueError("unsupported release manifest")
    release = manifest["macos"]
    tag, digest = release.get("tag"), release.get("sha256")
    if not isinstance(tag, str) or not isinstance(digest, str):
        raise ValueError("release tag and digest are required")
    notarized = release.get("notarized")
    if type(notarized) is not bool:
        raise ValueError("release must declare whether it is notarized")
    content = render(tag, digest, notarized)
    expected = f"https://downloads.starfarer.ai/releases/{tag}/Starfarer-aarch64.dmg"
    if release.get("url") != expected:
        raise ValueError("release URL must identify the versioned Starfarer DMG")
    version = tuple(map(int, tag[1:].split(".")))
    if output.exists():
        existing = output.read_text()
        previous = re.search(r'^  version "([0-9]+\.[0-9]+\.[0-9]+)"$', existing, re.MULTILINE)
        checksum = re.search(r'^  sha256 "([a-f0-9]{64})"$', existing, re.MULTILINE)
        signing = re.search(r'^# notarized: (true|false)$', existing, re.MULTILINE)
        if not previous or not checksum or not signing:
            raise ValueError("existing cask version, digest, or signing mode is invalid")
        current = tuple(map(int, previous[1].split(".")))
        if version < current:
            raise ValueError("refusing to downgrade the tap")
        if version == current:
            if digest != checksum[1]:
                raise ValueError("published release digest changed without a new version")
            if notarized != (signing[1] == "true"):
                raise ValueError("published signing mode changed without a new version")
            if existing == content:
                return False
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    changed = update(json.loads(args.manifest.read_text()), args.output)
    print("Cask updated" if changed else "Cask already matches the published release")

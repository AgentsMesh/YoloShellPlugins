#!/usr/bin/env python3
"""Validate the YoloShell plugin registry.

Every spec lives at Specs/<id>/<version>.json and records the exact plugin
manifest plus the source repository, path, tag and commit. Published version
files are immutable; a change to plugin behavior requires a new version file.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "Specs"
ID = re.compile(r"^[a-z0-9]+(?:\.[a-z0-9-]+)+$")
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")


def add(errors, path, message):
    errors.append("{}: {}".format(path, message))


def load(path, errors):
    try:
        with path.open() as handle:
            data = json.load(handle)
    except Exception as exc:
        add(errors, path.relative_to(ROOT), "invalid JSON: {}".format(exc))
        return None
    if not isinstance(data, dict):
        add(errors, path.relative_to(ROOT), "spec must be a JSON object")
        return None
    return data


def check_source(source, path, errors):
    if not isinstance(source, dict):
        add(errors, path, "source must be an object")
        return
    repository = source.get("repository")
    source_path = source.get("path")
    tag = source.get("tag")
    commit = source.get("commit")
    if not isinstance(repository, str) or not repository.startswith(
        "https://github.com/"
    ):
        add(errors, path, "source.repository must be a GitHub HTTPS URL")
    if (
        not isinstance(source_path, str)
        or not source_path
        or source_path.startswith("/")
        or ".." in Path(source_path).parts
    ):
        add(errors, path, "source.path must be a relative path without ..")
    if not isinstance(tag, str) or not tag:
        add(errors, path, "source.tag must be a non-empty string")
    if not isinstance(commit, str) or not COMMIT.match(commit):
        add(errors, path, "source.commit must be a 40-character lowercase SHA")


def check_manifest(manifest, spec, path, errors):
    if not isinstance(manifest, dict):
        add(errors, path, "manifest must be an object")
        return
    if manifest.get("schema_version") != 1:
        add(errors, path, "manifest.schema_version must be 1")
    for key in ("id", "version", "name", "description"):
        if manifest.get(key) != spec.get(key):
            add(errors, path, "manifest.{} must match the spec".format(key))
    platforms = manifest.get("platforms")
    if not isinstance(platforms, list) or not platforms:
        add(errors, path, "manifest.platforms must be a non-empty list")
    if not manifest.get("startup") and not manifest.get("actions"):
        add(errors, path, "manifest must have startup or actions")


def check_spec(path, errors):
    rel = path.relative_to(ROOT)
    spec = load(path, errors)
    if spec is None:
        return
    for key in ("schema_version", "id", "version", "name", "description",
                "source", "manifest"):
        if key not in spec:
            add(errors, rel, "missing {}".format(key))
    if spec.get("schema_version") != 1:
        add(errors, rel, "schema_version must be 1")
    plugin_id = spec.get("id")
    version = spec.get("version")
    if not isinstance(plugin_id, str) or not ID.match(plugin_id):
        add(errors, rel, "id must be dotted lowercase, for example web.client")
    elif plugin_id.startswith("yolo."):
        add(errors, rel, "the yolo. prefix is reserved for built-ins")
    elif path.parent.name != plugin_id:
        add(errors, rel, "parent directory must equal the plugin id")
    if not isinstance(version, str) or not VERSION.match(version):
        add(errors, rel, "version must be semver such as 0.1.0")
    elif path.stem != version:
        add(errors, rel, "file name must equal the plugin version")
    for key in ("name", "description"):
        if not isinstance(spec.get(key), str) or not spec.get(key):
            add(errors, rel, "{} must be a non-empty string".format(key))
    check_source(spec.get("source"), rel, errors)
    check_manifest(spec.get("manifest"), spec, rel, errors)


def main():
    if not SPECS.is_dir():
        print("Specs directory is missing", file=sys.stderr)
        return 1
    errors = []
    directories = sorted(path for path in SPECS.iterdir() if path.is_dir())
    if not directories:
        errors.append("Specs is empty")
    for directory in directories:
        if not list(directory.glob("*.json")):
            errors.append("{}: no version specs".format(directory.relative_to(ROOT)))
    files = sorted(SPECS.glob("*/*.json"))
    for path in files:
        check_spec(path, errors)
    if errors:
        for error in errors:
            print("ERROR {}".format(error), file=sys.stderr)
        return 1
    print("validated {} plugin spec(s)".format(len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

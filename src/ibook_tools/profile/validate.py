#!/usr/bin/env python3
"""Validate a complete package profile and its cross-file invariants."""
from __future__ import annotations

import argparse
import json
import sys
from importlib.resources import files
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_ROOT = files("ibook_tools.profile").joinpath("schemas")


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _schema(name: str) -> dict[str, Any]:
    return _load(SCHEMA_ROOT / name)


def _relative(root: Path, value: str) -> Path | None:
    candidate = Path(value)
    if candidate.is_absolute() or "\\" in value:
        return None
    try:
        resolved = (root / candidate).resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None
    return resolved


def _schema_errors(value: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    return [f"{label}: {error.message}" for error in validator.iter_errors(value)]


def _map_files(
    profile_root: Path,
    mapping: Any,
    kind: str,
    errors: list[str],
) -> dict[str, tuple[Path, dict[str, Any]]]:
    result: dict[str, tuple[Path, dict[str, Any]]] = {}
    if not isinstance(mapping, dict):
        return result
    for identifier, relative in mapping.items():
        if not isinstance(relative, str):
            errors.append(f"{kind} map entry {identifier}: path must be a string")
            continue
        path = _relative(profile_root, relative)
        if path is None:
            errors.append(f"{kind} map entry {identifier}: unsafe path {relative!r}")
            continue
        if not path.is_file():
            errors.append(f"{kind} map entry {identifier}: file does not exist at {relative}")
            continue
        try:
            value = _load(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{kind} {identifier}: cannot read {relative}: {exc}")
            continue
        result[identifier] = (path, value)
    return result


def _validate_result(profile_root: Path, result_path: Path, errors: list[str]) -> None:
    try:
        result_path.resolve().relative_to(profile_root.resolve())
    except ValueError:
        pass
    else:
        errors.append("result path must be outside PROFILE_ROOT")
    try:
        result = _load(result_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"result: cannot read {result_path}: {exc}")
        return
    errors.extend(_schema_errors(result, _schema("profile-result.schema.json"), "result"))
    if isinstance(result, dict) and result.get("status") == "success":
        warnings = result.get("warnings", [])
        if isinstance(warnings, list) and any(
            isinstance(item, dict) and item.get("requires_review") for item in warnings
        ):
            errors.append("result: success cannot contain a warning requiring review")


def validate_profile(profile_root: Path, before_profile: Path | None = None) -> list[str]:
    """Return sorted invariant errors; return an empty list for a valid profile."""
    errors: list[str] = []
    profile_root = profile_root.resolve()
    manifest_path = profile_root / "manifest.json"
    if not profile_root.is_dir():
        return [f"profile root does not exist: {profile_root}"]
    if not manifest_path.is_file():
        return ["manifest.json: file does not exist"]
    try:
        manifest = _load(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"manifest.json: cannot read: {exc}"]
    errors.extend(_schema_errors(manifest, _schema("profile-manifest.schema.json"), "manifest.json"))
    if not isinstance(manifest, dict):
        return sorted(set(errors))

    source = manifest.get("source", {})
    source_root = source.get("root") if isinstance(source, dict) else None
    if isinstance(source_root, str) and Path(source_root).is_absolute():
        errors.append("source.root must be repository-relative")
    git = source.get("git", {}) if isinstance(source, dict) else {}
    target_sha = git.get("current_hash") if isinstance(git, dict) else None

    profile_files = manifest.get("profile_files", {})
    module_map = profile_files.get("modules", {}) if isinstance(profile_files, dict) else {}
    facet_map = profile_files.get("facets", {}) if isinstance(profile_files, dict) else {}
    modules = _map_files(profile_root, module_map, "module", errors)
    facets = _map_files(profile_root, facet_map, "facet", errors)

    modules_dir = profile_root / "modules"
    facet_dir = profile_root / "facets"
    disk_modules = {path.relative_to(profile_root).as_posix() for path in modules_dir.glob("*.json")} if modules_dir.is_dir() else set()
    disk_facets = {path.relative_to(profile_root).as_posix() for path in facet_dir.glob("*.json")} if facet_dir.is_dir() else set()
    mapped_modules = {relative for relative in module_map.values() if isinstance(relative, str)} if isinstance(module_map, dict) else set()
    mapped_facets = {relative for relative in facet_map.values() if isinstance(relative, str)} if isinstance(facet_map, dict) else set()
    for relative in sorted(disk_modules - mapped_modules):
        errors.append(f"module file {relative} is not listed in manifest profile_files.modules")
    for relative in sorted(mapped_modules - disk_modules):
        errors.append(f"manifest module map path {relative} has no module file on disk")
    for relative in sorted(disk_facets - mapped_facets):
        errors.append(f"facet file {relative} is not listed in manifest profile_files.facets")
    for relative in sorted(mapped_facets - disk_facets):
        errors.append(f"manifest facet map path {relative} has no facet file on disk")

    # Only the four contract output classes may be present in the profile root.
    allowed = {"manifest.json", "coverage.md"} | disk_modules | disk_facets
    for path in profile_root.rglob("*"):
        if path.is_file() and path.relative_to(profile_root).as_posix() not in allowed:
            errors.append(f"unexpected profile output {path.relative_to(profile_root).as_posix()}")
    if not (profile_root / "coverage.md").is_file():
        errors.append("coverage.md: file does not exist")

    module_ids: set[str] = set()
    source_paths: dict[str, str] = {}
    changed_scopes = manifest.get("changed_scopes")
    changed_modules = (
        changed_scopes.get("modules", [])
        if isinstance(changed_scopes, dict)
        else []
    )
    if not isinstance(changed_modules, list):
        changed_modules = []
    for map_id, (path, module) in modules.items():
        errors.extend(_schema_errors(module, _schema("module-profile.schema.json"), f"module {map_id}"))
        if not isinstance(module, dict):
            continue
        module_id = module.get("id")
        if isinstance(module_id, str) and module_id in module_ids:
            errors.append(f"duplicate module id {module_id}")
        if isinstance(module_id, str):
            module_ids.add(module_id)
            if module_id != map_id:
                errors.append(f"module map entry {map_id} contains profile id {module_id}")
        source_path = module.get("path")
        if isinstance(source_path, str):
            previous = source_paths.get(source_path)
            if previous:
                errors.append(f"duplicate module source path {source_path} ({previous} and {map_id})")
            source_paths[source_path] = map_id
        if map_id in changed_modules and target_sha and module.get("source_hash") != target_sha:
            errors.append(f"module {map_id}: source_hash does not match manifest target SHA {target_sha}")

    ignored_paths = manifest.get("ignored_paths", [])
    counts = manifest.get("counts", {})
    if isinstance(ignored_paths, list) and isinstance(counts, dict):
        if counts.get("profiles_ignored") != len(ignored_paths):
            errors.append("ignored-module accounting: counts.profiles_ignored does not match ignored_paths")
        if isinstance(counts.get("modules_discovered"), int) and isinstance(counts.get("modules_profiled"), int):
            expected = counts["modules_profiled"] + len(ignored_paths)
            if counts["modules_discovered"] != expected:
                errors.append("ignored-module accounting: modules_discovered must equal profiled plus ignored")

    for facet_id, (path, facet) in facets.items():
        errors.extend(_schema_errors(facet, _schema("audience-facet.schema.json"), f"facet {facet_id}"))
        if not isinstance(facet, dict):
            continue
        audience = facet.get("audience")
        if audience != facet_id:
            errors.append(f"facet map entry {facet_id} contains audience {audience}")
        references: list[tuple[str, bool]] = []
        concepts = facet.get("concepts", [])
        if not isinstance(concepts, list):
            concepts = []
        for concept in concepts:
            if isinstance(concept, dict):
                module_ids_for_concept = concept.get("module_ids", [])
                if isinstance(module_ids_for_concept, list):
                    references.extend((item, True) for item in module_ids_for_concept if isinstance(item, str))
        featured_modules = facet.get("featured_modules", [])
        if isinstance(featured_modules, list):
            references.extend((item, True) for item in featured_modules if isinstance(item, str))
        hidden_modules = facet.get("hidden_or_internal_modules", [])
        if isinstance(hidden_modules, list):
            references.extend((item, False) for item in hidden_modules if isinstance(item, str))
        for module_id, requires_audience in references:
            if module_id not in module_ids:
                errors.append(f"facet {facet_id}: unknown module {module_id}")
            elif requires_audience:
                module = modules.get(module_id, (None, {}))[1]
                audiences = module.get("audiences", []) if isinstance(module, dict) else []
                if isinstance(audiences, list) and audience not in audiences:
                    errors.append(f"facet {facet_id}: module {module_id} is not a member of audience {audience}")

    if before_profile is not None:
        before_manifest = before_profile / "manifest.json"
        if not before_manifest.is_file():
            errors.append(f"before profile: manifest.json does not exist at {before_profile}")
        else:
            try:
                previous = _load(before_manifest)
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"before profile: cannot read manifest: {exc}")
                previous = {}
            if not isinstance(previous, dict):
                errors.append("before profile manifest must be an object")
                previous_profile_files = {}
            else:
                previous_profile_files = previous.get("profile_files")
                if not isinstance(previous_profile_files, dict):
                    errors.append("before profile profile_files must be an object")
                    previous_profile_files = {}
            previous_map = (
                previous_profile_files.get("modules", {})
                if isinstance(previous_profile_files, dict)
                else {}
            )
            for module_id, relative in previous_map.items() if isinstance(previous_map, dict) else []:
                old_path = _relative(before_profile, relative) if isinstance(relative, str) else None
                new = modules.get(module_id)
                if old_path is None or not old_path.is_file() or new is None:
                    continue
                try:
                    old_module = _load(old_path)
                except (OSError, json.JSONDecodeError):
                    continue
                if isinstance(old_module, dict) and isinstance(new[1], dict) and old_module.get("manual") != new[1].get("manual"):
                    errors.append(f"module {module_id}: manual object was not preserved")

    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile_root", type=Path)
    parser.add_argument("--before-profile", type=Path)
    parser.add_argument("--result", type=Path)
    args = parser.parse_args(argv)
    errors = validate_profile(args.profile_root, args.before_profile)
    if args.result is not None:
        _validate_result(args.profile_root.resolve(), args.result.resolve(), errors)
    if errors:
        for error in sorted(set(errors)):
            print(error, file=sys.stderr)
        return 4
    print(f"Valid profile: {args.profile_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

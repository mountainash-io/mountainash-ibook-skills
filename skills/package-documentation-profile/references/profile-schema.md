# Profile Schema

Use the canonical machine schemas at `../../../src/ibook_tools/profile/schemas/` (relative to this reference) as the validation authority. All schema basenames below refer to that package-owned directory, not a project copy. Keep this reference as the human-readable field guide. A profile is rooted at the invocation's explicit `profile/` output directory; it does not write package state or textbook artifacts.

```text
profile/
├── manifest.json
├── coverage.md
├── modules/
│   └── <module-id>.json
└── facets/
    └── <audience>.json
```

All committed paths are repository-relative, use forward slashes, and must not contain an absolute path or a parent traversal. Profile objects intentionally allow extension fields so language-specific evidence can evolve. The protocol-owned invocation and result envelopes remain closed by their schemas.

## `manifest.json`

Validate with `profile-manifest.schema.json`. Require:

```json
{
  "profile_version": "1.0",
  "generated_at": "ISO-8601 timestamp",
  "source": {
    "root": "repository-relative path",
    "git": {
      "previous_hash": "nullable 40-hex commit hash",
      "current_hash": "40-hex commit hash",
      "branch": "branch name or detached HEAD",
      "working_tree_dirty": false
    }
  },
  "scope": {"include": [], "exclude": [], "package_roots": []},
  "audiences": [],
  "counts": {
    "modules_discovered": 0,
    "modules_profiled": 0,
    "profiles_ignored": 0,
    "facets_written": 0
  },
  "changed_scopes": {"files": [], "modules": [], "facets": []},
  "ignored_paths": [{"path": "relative/path", "reason": "why it is ignored"}],
  "profile_files": {
    "modules": {"package.module": "modules/package.module.json"},
    "facets": {"users": "facets/users.json"}
  }
}
```

`profile_files` is the authoritative index. Every map entry must point to an existing file, and every JSON file in `modules/` or `facets/` must appear exactly once in its map. Map keys must equal the identity stored inside each file. Keep `source.git.current_hash` as the target committed revision. Set `previous_hash` to the prior manifest target during incremental refreshes, or `null` when no trusted ancestry exists.

## `modules/<module-id>.json`

Validate with `module-profile.schema.json`. Require these fields:

```json
{
  "id": "package.module",
  "path": "src/package/module.py",
  "summary": "Short factual summary.",
  "role": "public-api",
  "visibility": "public",
  "stability": "stable",
  "audiences": ["users", "maintainers"],
  "doc_priority": "essential",
  "confidence": "high",
  "public_api": [],
  "key_classes": [],
  "key_functions": [],
  "dependencies": [],
  "dependents": [],
  "extension_points": [],
  "lifecycle_notes": [],
  "documentation_hooks": [],
  "examples": [],
  "tests": [],
  "risks": [],
  "open_questions": [],
  "evidence": [{"kind": "symbol", "path": "src/package/module.py", "detail": "export"}],
  "source_hash": "40-hex commit hash",
  "manual": {
    "notes": "",
    "editorial_status": "",
    "owner": "",
    "manual_summary": ""
  }
}
```

Keep module IDs and source paths unique. Preserve the entire `manual` object by value during refresh, including extension keys not understood by the current producer. Refresh `source_hash` for changed modules and direct dependents; coverage may identify stale untouched profiles.

## `facets/<audience>.json`

Validate with `audience-facet.schema.json`. Require:

```json
{
  "audience": "users",
  "summary": "What this audience needs from the package.",
  "concepts": [
    {
      "name": "Core workflow",
      "module_ids": ["package.module"],
      "recommended_docs": ["guide"],
      "evidence": ["src/package/module.py"]
    }
  ],
  "featured_modules": ["package.module"],
  "hidden_or_internal_modules": [],
  "documentation_plan": [],
  "open_questions": []
}
```

Reference only mapped module IDs. Concept and featured modules must declare the facet audience in their `audiences` array. Hidden/internal modules must exist but may be omitted from audience membership when they are intentionally hidden.

## Invocation parameters

Validate the `parameters` object of `InvocationV1` with `profile-invocation.schema.json`. Require `accepted_source_sha` (40 hex or null), `target_source_sha` (40 hex), `package_roots`, `include`, `exclude`, `audiences`, and `full_refresh_threshold` between zero and one. Keep the protocol envelope in `references/protocol/v1/`; do not copy protocol fields into profile objects.

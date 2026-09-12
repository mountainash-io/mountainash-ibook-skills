# Update Algorithm

Refresh package profiles from explicit invocation inputs while preserving editorial fields. The output root is the caller-supplied `profile/` directory. Never infer a package path, write repository state, or prompt for a subsequent stage.

## Required inputs

Require these invocation parameters (see `../../../src/ibook_tools/profile/schemas/profile-invocation.schema.json`):

- `accepted_source_sha`: the prior accepted target SHA, or `null` for an initial profile;
- `target_source_sha`: the committed revision to profile;
- `package_roots`, `include`, and `exclude`: explicit source boundaries;
- `audiences`; and
- `full_refresh_threshold`, normally `0.3333333333333333`.

For incremental behavior, require an existing manifest with `source.git.current_hash`, `profile_files.modules`, and `scope.package_roots`. If any is absent, choose a conservative full refresh and emit a reviewable warning.

## `REFRESH_SCOPE`

```pseudocode
REFRESH_SCOPE(invocation, profile_path):
  read manifest and verify profile schema
  previous_hash = manifest.source.git.current_hash
  target_hash = invocation.parameters.target_source_sha

  IF invocation.parameters.accepted_source_sha != previous_hash:
    RETURN full_refresh(reason="accepted source does not match profile")
  IF previous_hash is null OR git cat-file -e previous_hash fails:
    RETURN full_refresh(reason="previous hash unavailable")

  changed_committed = git diff --name-only previous_hash target_hash
  changed_uncommitted = parse git status --short under project_root
  changed_files = union(changed_committed, changed_uncommitted.paths)
  changed_modules = map_files_to_modules(changed_files, invocation.package_roots)
  local_dependents = find direct local importers of changed_modules
  topology_changed = package roots, discovery rules, or public export boundaries changed
  changed_facets = audiences declared by changed_modules and local_dependents

  ratio = len(changed_modules) / max(1, modules_in_manifest)
  IF topology_changed OR ratio > invocation.full_refresh_threshold:
    RETURN full_refresh(reason="topology or threshold trigger")
  RETURN incremental(previous_hash, target_hash, changed_files,
                    changed_modules + local_dependents, changed_facets)
```

Use committed differences for provenance and report dirty files separately. Do not claim that a dirty profile corresponds only to the commit. Verify that `target_source_sha` is the expected source revision before writing.

## Refresh rules

- Refresh changed modules and direct local dependents.
- Refresh facets for every affected audience; retain unaffected facet files.
- Re-run discovery, classification, coverage, and manifest checks after each refresh.
- Copy every existing target module's complete `manual` object before replacing computed fields. Preserve unknown manual keys and values exactly.
- Keep untargeted module records and manual objects unchanged. Mark untouched records stale when their `source_hash` differs from the target and mark missing source modules orphaned in coverage.
- Represent every excluded discovery path in `ignored_paths` with a reason and keep `profiles_ignored`, `modules_discovered`, and `modules_profiled` consistent.
- Update only `profile/manifest.json`, `profile/modules/*.json`, `profile/facets/*.json`, and `profile/coverage.md`; write the completion result outside that root.

## Full refresh triggers

Choose full refresh when:

- `accepted_source_sha` is null, previous ancestry is unavailable, or the manifest is incomplete;
- package roots or include/exclude discovery rules changed;
- public export files changed substantially;
- a module boundary was added, removed, split, or joined;
- changed source modules exceed `full_refresh_threshold`; or
- partial coverage reports an orphan, missing profile, or untrusted facet mapping.

When a trigger is used, include a warning code and reason in the completion result. A warning with `requires_review: true` requires result status `warning`, never `success`.

## Deterministic validation

After writes, run the pinned `ibook profile validate PROFILE_ROOT`. It validates every owned JSON schema, exact manifest maps, safe repository-relative paths, unique module IDs and source paths, refreshed source hashes, ignored accounting, facet references and audience membership, and optional preservation evidence against `--before-profile`. Exit `0` only when no invariants fail; exit `4` for invariant failures. Keep any result path outside the profile root.

## Provenance

Set manifest `source.git.current_hash` to the committed target revision. Set `previous_hash` to the prior manifest target for incremental runs. Record `working_tree_dirty` and dirty files without changing the source hash. Hash exact bytes for completion-result input, output, and preserved paths. Return a completion result with profile stage, `package-profile.generate` capability, requested behavior, target module lists, warnings, metrics, and preserved module paths.

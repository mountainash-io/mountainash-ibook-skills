---
name: package-documentation-profile
version: 0.2.0
description: Triggers when a package needs an auditable module profile for user, maintainer, contributor, architecture, or positioning documentation, including full profiling and incremental refreshes.
---

# Package Documentation Profile

Build a documentation-ready inventory before writing prose. Produce evidence-backed module records, audience facets, and a coverage report. Treat the profile as a composable artifact: refresh only the requested scope and preserve editorial data. Do not write textbook state, commit changes, publish releases, or infer a repository path from an unrelated project.

## Contract and boundaries

Accept an explicit invocation. Require `project_root`, `run_root`, source target, behavior (`full` or `incremental`), mode (`interactive` or `orchestrated`), package roots, include/exclude globs, audiences, and the profile output root. Accept an existing profile only as an explicit input. Read `contract.json`, the invocation and completion-result protocol schemas under `references/protocol/v1/`, and the canonical profile schemas at `../../src/ibook_tools/profile/schemas/` before processing. Use protocol schemas at their pinned source digest; do not redefine them. Paths here are relative to this skill directory; schema files belong to the Python package and are not copied into projects.

For a direct user-driven request, use `mode: interactive`; use `mode: orchestrated` only for an explicit orchestrated invocation. In either mode, the invocation's common `targets` object contains empty `concept_ids`, `chapter_slugs` and `enrichment_ids` arrays: profiling does not select textbook targets. Its actual source scope belongs in the existing profile invocation parameters, not invented target fields.

The supplied profile root is the directory containing `manifest.json` (for example, `R/docs-site/profile`), not its parent. In the contract paths below, `profile/` denotes that supplied root; never append a second `profile/` directory. Write only:

```text
profile/manifest.json
profile/modules/<module-id>.json
profile/facets/<audience>.json
profile/coverage.md
```

Write the completion result to the caller-supplied transient result path, outside the profile root. Never write `state.json`, update notes, textbook chapters, or an inferred default path. Keep source paths repository-relative in committed artifacts. Reject an absolute `source.root` in orchestrated output.

Use the pinned `ibook profile validate` command as the machine gate (installation convention in the repository README). Return the declared `CompletionResultV1` envelope unchanged. The packaged `profile-result.schema.json` specializes that envelope for the profile stage; it is not a replacement protocol. Its textbook target arrays are empty and its concept metrics are zero because this skill does not process concepts. Module/facet counts and effective scope remain in the digested manifest (`counts`, `changed_scopes`); requested source scope remains in the digested invocation. Use only `success`, `warning`, or `failed`; set `warning` whenever a warning requires review.

## Modes

### Orchestrated mode

1. Read the complete invocation and every referenced schema. Verify the invocation capability, skill identity, mode, behavior, allowed outputs, and profile target paths.
2. Verify the target source SHA and each expected input digest before scanning. Refuse a mismatched target rather than silently profiling another revision.
3. Load the existing manifest when incremental behavior is requested. Classify full versus incremental scope using the update algorithm and the one-third threshold. Include direct local dependents and topology-triggered changes.
4. Discover, classify, profile, facet, and cover the selected scope. Preserve every existing module's `manual` object by value, including fields unknown to the current schema.
5. Update only the allowed profile paths. Do not ask for approval, ask what to do next, or perform a later textbook stage.
6. Run `ibook profile validate PROFILE_ROOT` with `--before-profile` when an earlier profile is available. Emit inspectable canonical outputs even on a failed run when they can be safely produced.
7. Author the `CompletionResultV1` document at the transient result path, then validate it with `ibook profile validate PROFILE_ROOT --result RESULT_JSON` and the same `--before-profile` when available. `--result` reads and validates this existing file; it does not generate or rewrite it. Return the validated result without conversational next-step prompting.

### Interactive mode

Explain the proposed scope and semantic impact before writing. Ask only questions necessary to resolve an ambiguous package target, audience, or destructive scope; do not ask for approval when the invocation already determines the target. Use the same explicit source, profile, output, validation, preservation, and result boundaries as orchestrated mode. Report the profile path, behavior, changed modules, facets, coverage gaps, and result path when complete.

## Verification gate

Load each external reference and prove it is non-empty before using it:

```pseudocode
LOAD_AND_VERIFY(path, marker):
  content = Read(path)
  IF content is empty or unreadable: halt with the path
  IF marker is absent: halt with the path
  DISPLAY loaded path and marker
```

Load `references/profile-schema.md` before discovering fields, `references/classification-rubric.md` before assigning classifications, and `references/update-algorithm.md` before an incremental decision. Load all JSON schemas before writing JSON. Run the validator after all writes, not before.

## Workflow

### 1. Establish intent and baseline

Read the explicit invocation. Record the requested behavior, package roots, include/exclude rules, audiences, accepted source SHA, target source SHA, and profile root. Inspect repository metadata and record the committed `git.current_hash`, branch or detached state, and dirty-file status. Keep dirty files visible without claiming that the profile represents a clean commit. Detect language, package manager, source layout, tests, examples, configuration, and existing docs under the explicit root.

### 2. Discover modules and evidence

Scan only the included source paths after applying exclusions. Use language-aware boundaries where available. Group files into stable module IDs and record each module's repository-relative source path. Discover exports, public classes/functions/types, commands, routes, plugins, schemas, tests, examples, docs, configuration wiring, and import relationships. Represent every discovered module in a profile or an `ignored_paths` record with a reason.

### 3. Classify with evidence

For each module, assign one primary role (`public-api`, `api-builder`, `protocol`, `backend`, `model`, `orchestration`, `io`, `integration`, `test-support`, `docs-example`, `legacy`, or `experimental`), visibility, stability, audience membership, documentation priority, and confidence. Cite an evidence path, symbol, test, document, configuration entry, or import for non-obvious choices. Record an open question for low-confidence classifications. Do not use promotional language in module summaries.

### 4. Write module profiles

Write `profile/modules/<module-id>.json` with all fields required by the packaged `module-profile.schema.json`: identity and summary, role, visibility, stability, audiences, priority, confidence, public API, key classes/functions, dependencies and dependents, extension points, lifecycle notes, documentation hooks, examples, tests, risks, open questions, evidence, and `source_hash`. Include a `manual` object. During refresh, copy the prior `manual` object by value before replacing computed fields; never merge by dropping unknown manual keys. Refresh changed modules and direct local dependents only in incremental mode.

### 5. Build audience facets

Write an affected facet for each requested audience under `profile/facets/`. Include the audience, summary, ordered concepts, referenced module IDs, recommended docs, evidence, featured modules, hidden/internal modules, documentation plan, and open questions. Reference only existing modules. Require featured and concept modules to declare membership in that audience; use hidden/internal entries only for modules that exist. Keep the required default lenses (`users`, `maintainers`, `backend-architecture`, and `broader-hype`) evidence-based when requested.

### 6. Record manifest and coverage

Write `profile/manifest.json` with `profile_version: "1.0"`, timestamp, relative source root, git provenance, scope, audiences, counts, changed scopes, ignored paths, and exact module/facet file maps. Make each map agree with files on disk. Set `current_hash` to the committed target SHA and record `previous_hash` for incremental refreshes. Write `profile/coverage.md` with missing, stale, orphaned, low-confidence, and audience-coverage findings; do not hide gaps in generated prose.

### 7. Validate and complete

Run:

```text
ibook profile validate PROFILE_ROOT
ibook profile validate PROFILE_ROOT --before-profile BEFORE_ROOT --result RESULT_JSON
```

Fix every invariant error. The validator checks every owned JSON schema, safe repository-relative paths, exact manifest maps, unique IDs and source paths, refreshed source hashes, ignored-module accounting, facet references and audience membership, and manual preservation evidence. Exit with code `0` for a valid profile or `4` for invariant failure. Digest each input, output, and preserved module path in the completion result. Include warnings with `code`, `message`, `path` (or `null`), and `requires_review`; never mark a result successful when review is required.

The agent authors the result, including execution metadata the validator cannot know. Validate the profile first, write the truthful result, then run the `--result` check against that file. If validation fails, correct the result to report failure and the actual errors; never reinterpret a validator exit as a generated completion document.

## Incremental decision

Use `references/update-algorithm.md`. Resolve the previous committed hash from the manifest, compare committed and uncommitted changes, map files to modules, add direct dependents, and map affected audiences. Choose full refresh when ancestry, package roots, discovery rules, public exports, or coverage cannot be trusted, or when changed source modules exceed `full_refresh_threshold` (default one third). Preserve untargeted module records and their manual objects. Mark untouched stale or orphaned records in coverage rather than silently deleting them.

## Handoff to existing-book refresh

The caller selects this skill with `behavior: incremental` and the mode rule above, using the complete existing invocation contract. `mode: incremental-refresh` is not an alias. The accepted source SHA is the existing profile's source revision; the target is the explicitly selected source snapshot. The book's documentation baseline is separate and must not be changed by profiling.

Before replacing an existing profile, the caller retains an inspectable before-profile snapshot or a recoverable profile revision. Use it for preservation validation and retain it for the subsequent content-impact comparison. Keep transient snapshots/results outside the canonical profile root; this does not extend this skill's allowed outputs.

Return the existing completion result with source provenance, digests of the invocation and manifest carrying requested/effective scope, validation and preservation evidence, and unresolved warnings. The caller may resume textbook refresh only after validation succeeds and review-required warnings are resolved. A full-refresh decision here means a full **profile scan**, never book generation. Do not invoke the next skill implicitly or claim textbook refresh succeeded because profiling completed.

## Reporting

Return the structured result, not an invitation to run another stage. In interactive text, summarize profile root, source hash, behavior, module and facet counts, coverage gaps, changed scope, warnings, and transient result path. Keep all claims tied to recorded evidence.
## Data and preservation rules

Treat the manifest as the authoritative index, not as a directory listing suggestion. Keep map keys equal to the `id` or `audience` inside each mapped JSON file, and use normalized forward-slash repository paths. Keep module IDs stable across refreshes whenever the source boundary remains the same. If a source boundary splits or joins, record the topology change in `changed_scopes` and explain resulting stale or orphaned records in coverage.

Hash the exact bytes used for every declared input and output. Use lowercase hexadecimal SHA-256 values with the `sha256:` prefix in completion-result digests. Use the 40-hex committed source revision for git provenance and module source hashes. Preserve unchanged modules byte-for-byte when possible; at minimum preserve their parsed data and manual object exactly. Do not treat a regenerated timestamp or facet ordering as evidence that an untargeted module changed.

When a refresh cannot establish ancestry, do not guess at a diff. Run a conservative full refresh, set `previous_hash` to `null` when appropriate, and emit a reviewable warning. When a module is intentionally excluded, add its path and a useful reason to `ignored_paths`, increment `profiles_ignored`, and keep discovered/profiled/ignored counts internally consistent. Never use an ignored record to conceal a discovery failure.

The profile result must identify the invocation and skill version, report `profile` as its stage and `package-profile.generate` as its capability, and use the requested behavior. Preserve the declared envelope: `targets` contains empty `requested_concept_ids`, `effective_concept_ids`, `chapter_slugs` and `enrichment_ids` arrays; `metrics` contains `active_concepts: 0` and `retired_concepts: 0`. Do not insert module fields into that envelope; report them through the existing invocation and manifest. List every preserved module path in `preserved`, and list only contract paths in `outputs`. If validation fails, include the failure warning and retain inspectable outputs when safe; do not claim success.

## Failure handling

Stop before writing when the invocation, target SHA, schema, or expected input digest is invalid. If discovery or classification is incomplete, write no misleading profile record; instead emit a failed result with a precise warning and offending path. If validation finds drift, identify the exact module, facet, path, or invariant in the warning. Keep the result path outside the profile root so a failed result cannot become an accidental profile artifact. Do not repair source code, alter repository history, or write files outside the explicit output and transient result boundaries.

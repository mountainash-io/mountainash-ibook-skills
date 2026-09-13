---
name: textbook-refresh
description: Detect source code changes since the last textbook generation, identify stale chapters and artefacts, and perform targeted regeneration of only the affected content. Requires an existing textbook site (from init-textbook + chapter-content-generator) and a code profile (from package-documentation-profile).
---

# Textbook Refresh

Incrementally update an intelligent textbook when the underlying source code
changes. Instead of regenerating all chapters, this skill detects what changed,
maps changes to affected chapters via enriched learning graph nodes, and
regenerates only the stale sections.

## Mountainash editorial contract

This skill maintains the existing book; it is not the creation/replacement workflow. Reuse the confirmed `docs-site/editorial-brief.md` and approved `docs-site/chapter-plan.md` when present. If they are absent, preserve the current book's scope, chapter organisation, appendix choices and reader surfaces as the maintenance boundary. Their absence does not authorise creating a new brief, replanning chapters or rebuilding the book. If the source change requires an audience, scope or structural decision, stop and ask the focused question before changing that boundary.

Keep canonical graph, CSV, taxonomy, reports and source mappings internal under `docs-site/`. Do not sync them into the published site. Routine refresh does not remove or relocate an existing reader-facing graph, FAQ, glossary, quiz or runtime asset as migration cleanup. Inventory the actual existing FAQ/glossary paths and formats; do not assume the replacement book's appendix paths. Unsupported FAQ JSON stays untouched unless its own reviewed update is requested. If the required change cannot be completed within these boundaries, report the specific unsupported artifact instead of silently omitting it.

Use `ibook graph reconcile EXISTING PROPOSED CANDIDATE` for deterministic graph updates and CIS recomputation. Resolve identity conflicts explicitly; preserve chapter/source/provenance fields. Do not regenerate an enriched canonical graph with bare CSV conversion. Approved chapter reassignment is an editorial change recorded separately.

Prefer Mermaid. MicroSims are optional when interaction adds value. Do not generate quizzes in the Mountainash workflow. Keep the quiz skill and the engine's existing enrichment support available for separately requested workflows.

Refresh is agent-led and finalized via reviewed PRs. Consumer Actions validate/build/publish prepared content only; they never run interviews, agents, reconciliation or unattended refresh proposals. The existing accepted book remains intact while a replacement is reviewed.

Follow the phases and referenced contracts, adapting to the project's actual layout and editorial intent through the guidance below. An unfamiliar case or absent recipe is not itself a process failure. If a required capability, source fact or authority is missing, or contracts genuinely conflict, pause the dependent operation and identify the precise prerequisite; do not bypass it or substitute whole-book generation. A successful build, profile validation or preselected block patch is component evidence, not proof that the source-to-book skill workflow succeeded.

**Required input:** `source_repo`, the explicit path to the target source
repository or Git worktree. Relative paths are anchored to the invocation
directory, then normalized once. The target must already contain
`docs-site/profile/`, `docs-site/learning-graph/`, and `docs-site/site/`
(the MkDocs project root). This is a skill input, not a new CLI.

**Output:** Updated chapter content, refreshed FAQ entries, updated
`refresh-state.json`, enriched `learning-graph.json`, and a change report.

> **External references:**
> `references/refresh-state-schema.md` | `references/change-classification.md`

> **Related skills:**
> `package-documentation-profile` (produces the code profiles this skill reads)
> `chapter-content-generator` (produces the chapter content this skill updates)
> `learning-graph-generator` (produces the learning graph this skill enriches)
> `faq-generator` (produces the FAQ this skill refreshes)


## Adaptive maintenance

The maintenance agent owns progress across the skills, not just the next-step recommendation. Inspect prerequisites relevant to the next operation and catch cheap blockers before expensive work—for example, conflicting contents of the profile output root before a source scan. Inspect other artifacts when they become relevant; a profile refresh does not require a census of the whole book.

Resolve ordinary choices from the agreed intent and existing conventions. Correct mistakes within authorized outputs without ceremonial approval. Treat existing layouts and manual content as inputs to understand, not defects to normalize.

When alternatives materially affect content, reader experience, ownership, destructive changes or scope, investigate and ask a focused question: what is the issue, what do you recommend, and what would change? Combine related decisions, accept free-form answers and explain consequences proportionately. Keep detailed hashes and provenance in the conversation or existing run/review records, not a new approval checklist. Investigation is not permission to delete; an already authorized routine step does not need fresh approval because it uses another tool.

Choose the disposition from the evidence: preserve, update, relocate, consolidate, retire or defer. An unexpected profile README warrants checking its purpose and references, not automatic removal; keeping it in a disallowed location leaves the validator conflict unresolved. A legacy appendix may need a bounded edit rather than conversion. Propose a contract change separately if the existing permissions or available capabilities cannot support the desired result; user approval alone does not supply a missing converter.

Carry out authorized preparation as maintenance work, without enlarging any component's output permissions. Preserve recoverable originals before destructive changes and protect concurrent edits. Do not hide artifacts or relax validation to obtain a pass. Read-only requests remain read-only: explain and obtain authorization for any transition to writes. In unattended execution, return the unresolved decision to the invoking agent; never infer consent.

After a decision, perform the authorized work, verify it and continue from the earliest still-valid point. Re-evaluate affected inputs and decisions without discarding unrelated progress or repeating an unchanged approval. The invoking agent owns conversations and explicit stage handoffs; a noninteractive component returns actionable evidence under its existing result contract. If the user defers, identify what remains blocked and what would permit resumption, then stop that work rather than asking again.

Distinguish proposed, attempted, verified and accepted work. Preserve separate source, profile and book provenance throughout recovery. Preparation or a newly validated profile is not a refreshed book, and a partial recovery is not publication acceptance.

---

## Data Architecture: Learning Graph as Single Source of Truth

The concept-to-module-to-chapter mapping lives **in the learning graph JSON
itself**, not in a separate index file. Each node in `learning-graph.json`
carries its own source provenance:

```json
{
  "id": 11,
  "label": "Backend Protocol Definition",
  "group": "PROTO",
  "source_module": "mountainash_data.core.protocol",
  "source_path": "src/mountainash_data/core/protocol.py",
  "chapter": "02-backend-protocol",
  "match_confidence": 1.0
}
```

The `metadata` block carries the refresh baseline:

```json
"metadata": {
  "title": "Mountainash Data Concept Graph",
  "description": "...",
  "creator": "Nathaniel Ramm",
  "date": "2026-06-03",
  "version": "1.0",
  "format": "Learning Graph JSON v1.0",
  "schema": "https://raw.githubusercontent.com/dmccreary/learning-graphs/...",
  "license": "CC BY-NC-SA 4.0 DEED",
  "source_commit": "4c077666ebc560f82e9bbd7ef419bdfde2c5f62f",
  "profile_dir": "docs-site/profile"
}
```

`metadata.profile_dir` is relative to the **source repository root**, not the
graph or site directory. It records the fixed profile location; it never
selects the target or redirects reads or writes.

### Why the Learning Graph, Not a Separate File

- **One file, one truth** — no risk of a separate map drifting out of sync
  with the concepts it indexes
- **Already loaded** by every skill in the chain (chapter-generator,
  FAQ-generator, refresh) — no extra file reads
- **Internal provenance** — source mappings support agent review without publishing the graph.
- **CSV stays lean** — the enrichment lives only in the JSON; the CSV
  remains human-editable with just `ConceptID,ConceptLabel,Dependencies,TaxonomyID`

### What Still Lives in refresh-state.json

Ephemeral state that doesn't belong in the learning graph:

- **Chapter content hashes** — detect manual edits before overwriting
- **Refresh history** — audit log of past refreshes with token costs
- **Tool versions** — detect when the generator was upgraded
- **FAQ/learning-graph content hashes** — detect drift

The `refresh-state.json` is a slim operational file, not a knowledge structure.

---

## Verification Gates

Every phase that depends on an external reference must read the file and prove
it was loaded before executing phase logic.

```pseudocode
LOAD_AND_VERIFY(path, proof):
  content = Read(path)
  IF content IS empty OR unreadable:
    HALT "Cannot proceed: {path} not found or empty"
  extracted = proof(content)
  DISPLAY "Loaded {path}: {extracted}"
```

Before writing output, verify:

- The learning graph JSON exists and contains enriched nodes (or is being seeded)
- The source repo is accessible and the baseline commit exists in its history
- The profile directory contains `manifest.json` and module profile JSONs
- Every chapter referenced by a node's `chapter` field still exists on disk

---

## Overview

| Phase | Description | Runs |
|-------|-------------|------|
| **0: Intent** | Determine mode, locate inputs, validate prerequisites | Always |
| **1: Detect** | Diff source repo against baseline commit | Refresh/Check |
| **2: Map** | Cross-reference changed files against enriched learning graph nodes | Refresh/Check |
| **3: Classify** | Categorise each change (signature, new symbol, removal, etc.) | Refresh/Check |
| **4: Plan** | Build a regeneration plan with affected artefacts | Refresh/Check |
| **5: Regenerate** | Update stale chapters, FAQ, learning graph | Refresh only |
| **6: Verify** | Check concept coverage, content hashes, link integrity | Refresh only |
| **7: Update State** | Write updated learning graph + refresh-state.json | Refresh/Seed |

---
## Deterministic packaged operations

`ibook_tools.refresh.patch_engine` is the stdlib-only implementation of the byte-exact parts of Phases 5–6. Install the pinned `mountainash-ibook-tools` revision and matching constraints using the repository README. No skill checkout imports, writable installation or copied helpers are needed.

- `markers.py` -- parses `<!-- concept:N -->` markers and the paired
  `<!-- KIND:ID concepts:N,N --> ... <!-- /KIND:ID -->` enrichment-block
  markers, preserving exact byte offsets and rejecting malformed/nested
  markers.
- `patches.py` -- validates a file's declared base digest against its
  current bytes (rejects a stale/manually-edited target before writing
  anything), splices one or more concept/enrichment blocks, independently
  re-verifies that every byte outside the targeted blocks is unchanged, and
  writes each targeted file atomically. The patch set is not a multi-file transaction; do not claim all-or-nothing rollback.
- `enrichments.py` -- computes a deterministic JSON projection only for
  supported paired-marker FAQs. It does not support the pilot's heading-based
  FAQ Markdown and existing JSON shape; see the FAQ format gate below.

In the commands below, `ibook` means the pinned uvx invocation and `$R` is the validated, normalized `source_repo`. The implementation lives in the Mountainash tool distribution, not in the target repository or the old Hiivmind plugin.

```bash
ibook refresh apply --project-root "$R" \
  --invocation /absolute/run/invocation.json --patch-set /absolute/run/patch-set.json

ibook refresh coverage \
  --graph "$R/docs-site/learning-graph/learning-graph.json" \
  --chapters "$R/docs-site/site/docs/chapters"
```

`faq-export` and `faq-verify` are **marker-format-only** commands. Do not run
them on the existing heading-based FAQ as a validation or replacement step.
The FAQ Refresh section defines the required format detection and preservation
checks before either command may be used.

`invocation.json` declares `project_root` (the same absolute `$R` passed to
`--project-root`), `allowed_outputs`, and `targets` (`concept_ids`/
`enrichment_ids` this run is authorized to change). Patch file paths and
allowlist entries are source-root-relative, for example
`docs-site/site/docs/chapters/04-ibis-backend/index.md`, not `docs/chapters/...`.
List only the exact documentation files approved in the plan; never allow
the repository root, `src/`, `docs-site/profile/`, or a broad wildcard.
Resolve each output and reject traversal or symlinks outside its intended
documentation directory. The same boundary applies to non-helper writes:
canonical artifacts in `docs-site/learning-graph/`, published content in
`docs-site/site/docs/`, and state at `docs-site/site/refresh-state.json`.

`patch-set.json` lists the files and replace/delete/insert_before/insert_after
operations to apply. Both inputs are plain local JSON built by the
human-supervised skill run, not a versioned schema protocol. The engine
retains its stdlib-only, stale-digest rejection, byte-preservation and atomic
write behavior; the skill is responsible for selecting the correct target
and safe allowlist.

The installed-tool verification command is documented in the repository README. The retained suite covers supported marker formats, not heading-based FAQ parity. Ordinary refresh invokes the installed operations; it does not require a skill-local test runner or a writable checkout.

---

## Phase 0: Intent

Determine the operating mode and validate all inputs exist.

```pseudocode
INTENT():
  mode = choose one:
    - "seed"                # first run — enrich learning graph + create refresh-state.json
    - "check"               # dry run — report what's stale without writing
    - "refresh"             # detect + regenerate stale artefacts
    - "force-refresh"       # explicit whole-book request only; never a fallback for a failed gate

  invocation_dir = current working directory at invocation
  REQUIRE explicit source_repo input
  source_repo = normalize_absolute(source_repo, relative_to=invocation_dir)
  R = source_repo
  profile_dir = R/docs-site/profile
  learning_graph_dir = R/docs-site/learning-graph
  textbook_dir = R/docs-site/site

  validate:
    - textbook_dir/mkdocs.yml exists
    - textbook_dir/docs/chapters/ contains at least one chapter directory
    - learning_graph_dir/learning-graph.json exists (canonical copy)
    - profile_dir/manifest.json exists
    - profile_dir/modules/ contains at least one .json file
    - git -C R rev-parse --is-inside-work-tree returns true
    - normalized git -C R rev-parse --show-toplevel equals R
    - git -C R rev-parse --verify HEAD^{commit} succeeds
    - every resolved input/output remains within its intended target directory

  record separately:
    - selected source snapshot and dirty-file status
    - book baseline from graph/state
    - profile source revision and available validation evidence
    - existing book layout and preservation inputs

  REQUIRE the selected committed source revision is HEAD of the explicit worktree
  REQUIRE that commit includes the reported source change
  IF another revision or uncommitted source changes are the intended input:
    STOP; request an explicit worktree at that committed revision
    never switch branches, discard dirty work, or imply HEAD includes uncommitted changes
  preserve unrelated local documentation edits as separate preservation inputs
```

### Input Resolution

The explicit target is the only authority for all four directories above.
Require the repository/worktree root, not a subdirectory within one. Git's
checks accept a worktree whose `.git` is a file; do not require `.git/`.
Missing inputs or invalid targets must report the exact path and stop before
any write. Do not initialize a missing profile or graph, infer the target
from `manifest.json` → `source.root` or MkDocs settings, or search an older
centralized layout. Historical source provenance in a manifest remains
evidence, not a filesystem routing instruction.

The canonical graph is `R/docs-site/learning-graph/learning-graph.json`.
Enrich only an internal reviewed candidate. Never synchronize a graph into the published site. Read `metadata.profile_dir` as provenance (`docs-site/profile`, relative to `R`), not a routing instruction. An approved seed/refresh may correct it on the internal graph; check mode never repairs it.

Inventory existing reader-facing and canonical FAQ Markdown/JSON before planning. Read MkDocs configuration and the actual files to establish their roles; the creation workflow's `docs-site/site/docs/faq.md` is not a required path for an older book. Detect heading/paired-marker format and existing JSON shape. Do not create missing companions, move appendices or overwrite unsupported legacy data. A deliberate appendix migration is separate from routine maintenance.

**Check is read-only:** read inputs, resolve the baseline and detect source changes. Evaluate the profile gate before mapping/classifying or presenting a content-impact plan. A failed gate pauses the dependent analysis and reports the exact prerequisite; investigate and recommend a remedy under Adaptive maintenance, but do not write or produce an authoritative impact plan using stale facts. Once prerequisites pass, map/classify
changes and report the plan. Do not generate invocation/patch JSON files,
write a report to disk, repair metadata or copies, retrofit markers, profile,
build, or update state. If using read-only Python helpers, use `python3 -B`
to avoid bytecode-cache writes. `force-refresh` still validates paths and
baseline availability and requires human approval; ignoring state for
regeneration scope does not authorize resetting provenance.

---

## Phase 1: Detect Source Changes

Identify what changed in the source code since the last refresh.

```pseudocode
DETECT(source_repo, baseline_commit):
  current_commit = git -C source_repo rev-parse HEAD
  IF current_commit == baseline_commit:
    REPORT "No changes since last refresh"
    RETURN empty_changeset

  scope = inspected profile/invocation package_roots, include, exclude
  REQUIRE scope is explicit and its discovery rules are available
  changed_files = git -C source_repo diff --name-only --no-renames baseline_commit..current_commit
  changed_files = apply the profile discovery boundary rules to old and new paths
  # Deleted paths are evaluated against the baseline tree, not current file existence.
  added_files   = filter changed_files where file is new (not in baseline)
  removed_files = filter changed_files where file was deleted
  modified_files = changed_files - added_files - removed_files

  RETURN {
    baseline_commit,
    current_commit,
    added_files,
    removed_files,
    modified_files
  }
```

### Baseline Commit Resolution

The baseline commit is read from `learning-graph.json` → `metadata.source_commit`.
If this field is absent (graph not yet enriched), fall back to
`refresh-state.json` → `baseline.source_commit`. If neither exists, the user
must run seed mode first.

Validate the selected hash with
`git -C "$R" rev-parse --verify "$BASELINE^{commit}"` before detection or
regeneration. Seed uses `manifest.json` → `source.git.current_hash` and must
validate that commit too. An unavailable commit is a hard stop: report the
hash and ask the operator to make the required source history available.
Never substitute HEAD or write refreshed state to conceal a missing baseline.
Keep source commits, tool versions, stable concept IDs, and enrichment
provenance intact unless the existing seed/refresh operation actually updates
them; relocation alone is not a content refresh.

Retain the book baseline throughout profiling and planning. Do not substitute the profile's newer revision or the target HEAD. If graph metadata and refresh state both declare different book baselines, stop and resolve the discrepancy rather than silently selecting one after a partial update.

### Profile freshness and handoff gate

Before mapping, classifying or planning book changes:

```pseudocode
profile_commit = profile_dir/manifest.json → source.git.current_hash
IF profile_commit != current_commit:
  REPORT book baseline, profile_commit, current_commit, and detected source paths
  REPORT "Profile refresh required before content-impact analysis"
  PAUSE content-impact analysis; the maintenance agent owns the explicit profile handoff below
IF profile validation failed, its evidence is unavailable, or review-required warnings remain:
  REPORT the unresolved profile validation/review prerequisite
  PAUSE content-impact analysis; investigate the prerequisite without bypassing it
```

There is no stale-profile override on this maintenance route. `check` never updates the profile, and profiling is a separate explicit component invocation, not an implicit write inside `refresh`. The maintenance agent performs that handoff when the user's maintenance scope authorizes profiling. For a read-only check, explain the proposed transition and obtain authorization before any preparation or profile writes. Do not ask the user to invoke the next skill themselves or repeat permission already granted.

For a stale profile, invoke [package-documentation-profile](../package-documentation-profile/SKILL.md) using its complete existing contract and schemas. For missing validation evidence, validate the existing profile first; for failures or review-required warnings, investigate and resolve the actual prerequisite rather than rescanning by default:

- Use `behavior: incremental`; use `mode: interactive` for a direct user-driven run and `mode: orchestrated` only for an explicit orchestrated invocation. Do not use the unsupported `mode: incremental-refresh`.
- Keep the same explicit source target `R` and selected source snapshot. Supply the existing profile and `R/docs-site/profile` as the explicit profile output, and a caller-owned transient run/result location outside that profile root.
- Set `accepted_source_sha` from the existing profile, not from the book baseline; set `target_source_sha` to the selected committed source revision. Take package roots, inclusion/exclusion rules and audiences from the inspected profile/invocation, not a sibling repository.
- Retain an inspectable before-profile snapshot or recoverable revision for preservation and comparison. Do not overwrite the only copy of the prior facts.
- Require the profile skill's validation and preservation evidence and resolve review-required warnings. A full profile scan, if selected by its update algorithm, is not permission to regenerate the book.

After a validated profile handoff with review-required warnings resolved, re-enter at Phase 0 against the same selected source and unchanged book baseline, reusing unaffected inspection and comparison work. If the source or other relevant inputs changed, re-evaluate the affected prerequisites and plan. Continue to the concrete content-impact approval gate without asking the user to coordinate re-entry. If a decision is deferred or recovery fails, report the remaining prerequisite and completed work truthfully; profiling success alone does not complete any chapter refresh.

---

## Phase 2: Map Changes to Artefacts

Cross-reference changed source files against the enriched learning graph nodes.

### Reading the Map from the Learning Graph

The enriched `learning-graph.json` nodes carry `source_path` and `chapter`
fields. To find which concepts (and therefore chapters) are affected by a
file change:

```pseudocode
MAP(changeset, learning_graph):
  # Build source_path → concepts index
  path_index = {}
  FOR node IN learning_graph.nodes:
    IF node.source_path:
      path_index.setdefault(node.source_path, []).append(node)

  stale_chapters = {}
  stale_api_pages = set()
  unmapped_files = []

  FOR file IN changeset.modified_files + changeset.added_files:
    concepts = path_index.get(file, [])
    IF concepts:
      FOR concept IN concepts:
        chapter = concept.chapter
        stale_chapters.setdefault(chapter, []).append({
          concept_id: concept.id,
          concept_label: concept.label,
          source_module: concept.source_module,
          file: file,
          change_type: "modified" or "added"
        })
        api_page = resolve_api_page(concept.source_module)
        IF api_page:
          stale_api_pages.add(api_page)
    ELSE:
      unmapped_files.append(file)

  FOR file IN changeset.removed_files:
    concepts = path_index.get(file, [])
    FOR concept IN concepts:
      stale_chapters.setdefault(concept.chapter, []).append({
        concept_id: concept.id,
        concept_label: concept.label,
        source_module: concept.source_module,
        file: file,
        change_type: "removed"
      })

  RETURN { stale_chapters, stale_api_pages, unmapped_files }
```

### Enriching the Learning Graph (Seed Mode)

When seeding for the first time, the skill adds `source_module`, `source_path`,
`chapter`, and `match_confidence` to each learning graph node. It also adds
`source_commit` and `profile_dir` to the metadata block.

```pseudocode
ENRICH_LEARNING_GRAPH(learning_graph, profile_dir, chapters_dir):

  # Step 1: Load module profiles
  modules = load all profile_dir/modules/*.json
  # Each has: id, path, public_api, key_classes, key_functions

  # Step 2: Build chapter assignment from chapter index files
  concept_chapter = {}
  FOR chapter_dir IN chapters_dir:
    concept_ids = parse_concept_ids(chapter_dir/index.md)
    FOR cid IN concept_ids:
      concept_chapter[cid] = chapter_dir.name

  # Step 3: Match each concept to its source module
  FOR node IN learning_graph.nodes:
    best_module = None
    best_score = 0
    FOR module IN modules:
      score = match_concept_to_module(node.label, module)
      IF score > best_score:
        best_module = module
        best_score = score

    # Enrich the node
    IF best_score >= 0.6:
      node.source_module = best_module.id
      node.source_path = best_module.path
    ELSE:
      node.source_module = null
      node.source_path = null

    node.chapter = concept_chapter.get(node.id, null)
    node.match_confidence = best_score

  # Step 4: Enrich metadata
  manifest = load profile_dir/manifest.json
  learning_graph.metadata.source_commit = manifest.source.git.current_hash
  learning_graph.metadata.profile_dir = "docs-site/profile"  # relative to source_repo

  RETURN learning_graph
```

### Concept-to-Module Matching Heuristics

```pseudocode
match_concept_to_module(concept_label, module):
  normalised_label = concept_label.lower().replace(" ", "").replace("-", "")

  # Exact: concept label matches a class or function name
  FOR symbol IN module.public_api + [c.name for c in module.key_classes]:
    IF symbol.lower() == normalised_label:
      RETURN 1.0

  # Normalised: remove common suffixes (Class, Protocol, Mixin, Error)
    stripped = symbol.lower()
    FOR suffix IN ("class", "protocol", "mixin", "error", "exception"):
      stripped = stripped.replace(suffix, "")
    IF stripped == normalised_label:
      RETURN 0.8

  # Containment: concept label contains a key class name or vice versa
  FOR cls IN module.key_classes:
    IF cls.name.lower() IN normalised_label OR normalised_label IN cls.name.lower():
      RETURN 0.7

  # Module-name: concept label contains the module's short name
  short_name = module.id.split(".")[-1]
  IF short_name.lower() IN normalised_label:
    RETURN 0.6

  RETURN 0.0
```

### Enriched Node Schema

After enrichment, each learning graph node has these fields:

| Field | Type | Source | Required |
|-------|------|--------|----------|
| `id` | int | learning-graph-generator | yes |
| `label` | string | learning-graph-generator | yes |
| `group` | string | learning-graph-generator | yes |
| `shape` | string | learning-graph-generator | optional |
| `source_module` | string \| null | textbook-refresh (seed) | enriched |
| `source_path` | string \| null | textbook-refresh (seed) | enriched |
| `chapter` | string \| null | textbook-refresh (seed) | enriched |
| `match_confidence` | float | textbook-refresh (seed) | enriched |

Nodes with `source_module: null` are foundational/conceptual concepts that
don't map to a specific source file (e.g. "SQL Databases", "Python Protocols").
This is expected and not an error — typically chapter 1 concepts.

### Enriched Metadata Schema

| Field | Type | Source |
|-------|------|--------|
| `source_commit` | string | textbook-refresh (seed) |
| `profile_dir` | string | textbook-refresh (seed); `docs-site/profile`, source-root-relative |
| All existing fields | — | learning-graph-generator |

---

## Phase 3: Classify Changes

For each stale module, determine the nature of the change by comparing old and
new state. This informs the regeneration strategy.

Establish the comparison inputs explicitly. A saved before-profile is usable as `old_profile` only when its source provenance matches the book baseline. If it does not, recover baseline facts from the source at the book baseline before classification. Never load the newly refreshed profile as both the old and new state. If the baseline facts cannot be recovered, report the gap and stop rather than infer that no documented behaviour changed.

Retain the computed `added`/`removed` symbol sets as `symbol_diffs[module]` alongside the classification string, and pass both to planning. A rename category alone is not enough to populate a graph update.

```pseudocode
CLASSIFY(source_module, changeset, old_profile, new_source):
  IF source file IN changeset.added_files:
    RETURN "new_module"
  IF source file IN changeset.removed_files:
    RETURN "removed_module"

  # Compare old profile against current source
  old_symbols = set(old_profile.public_api)
  new_symbols = extract_public_symbols(new_source)

  added = new_symbols - old_symbols
  removed = old_symbols - new_symbols
  common = old_symbols & new_symbols

  IF added AND NOT removed:
    RETURN "new_symbols"
  IF removed AND NOT added:
    RETURN "removed_symbols"
  IF added AND removed:
    renames = detect_renames(added, removed, old_profile, new_source)
    IF renames:
      RETURN "renamed_symbols"
    RETURN "mixed_changes"
  IF common == old_symbols:
    signature_changed = check_signature_diff(common, old_profile, new_source)
    IF signature_changed:
      RETURN "signature_change"
    RETURN "docstring_only"

  RETURN "internal_refactor"
```

### Change Classification Table

| Classification | Chapter Impact | API Page Impact | Learning Graph Impact |
|---------------|---------------|-----------------|----------------------|
| `new_module` | May need new chapter or new section | New API page needed | May need new concepts + enrichment |
| `removed_module` | Remove/revise sections | Remove API page | May need concept removal |
| `new_symbols` | Add sections for new concepts | Rebuild page | May need new concepts + enrichment |
| `removed_symbols` | Remove/revise sections | Rebuild page | May need concept removal |
| `renamed_symbols` | Find-and-replace in prose | Rebuild page | Update node labels + source_module |
| `mixed_changes` | Regenerate affected sections | Rebuild page | Review concepts |
| `signature_change` | Regenerate code examples | Rebuild page (auto) | No change |
| `docstring_only` | No change | Rebuild page (auto) | No change |
| `internal_refactor` | No change | No change | No change |

---

## Phase 4: Plan Regeneration

Build a concrete plan before writing any files.

```pseudocode
PLAN(stale_chapters, classifications, symbol_diffs, unmapped_files):
  plan = {
    chapters_to_regenerate: [],
    chapters_to_review: [],
    api_pages_to_rebuild: [],
    learning_graph_updates: [],
    faq_stale: false,
    unmapped_new_files: []
  }

  FOR chapter, changes IN stale_chapters:
    actions = []
    FOR change IN changes:
      cls = classifications[change.source_module]
      SWITCH cls:
        "signature_change":
          actions.append({action: "regenerate_code_examples", concept: change.concept_id})
        "new_symbols":
          actions.append({action: "add_new_sections", concept: change.concept_id})
        "removed_symbols":
          actions.append({action: "remove_or_revise_sections", concept: change.concept_id})
        "renamed_symbols":
          actions.append({action: "find_and_replace", concept: change.concept_id})
        "mixed_changes":
          actions.append({action: "regenerate_affected_sections", concept: change.concept_id})
        "docstring_only", "internal_refactor":
          SKIP

    IF actions:
      plan.chapters_to_regenerate.append({
        chapter: chapter,
        actions: actions,
        changed_concepts: [a.concept for a in actions],
        source_modules: unique([c.source_module for c in changes])
      })
      plan.faq_stale = true

  FOR file IN unmapped_files:
    IF file.endswith(".py") AND NOT "__pycache__" IN file:
      plan.unmapped_new_files.append(file)

  # Learning graph node updates for renames
  FOR module, cls IN classifications:
    IF cls == "renamed_symbols":
      plan.learning_graph_updates.append({
        action: "update_node_labels",
        module: module,
        old_symbols: symbol_diffs[module].removed,
        new_symbols: symbol_diffs[module].added
      })

  IF any classification IN ("new_module", "removed_module"):
    plan.learning_graph_updates.append({action: "review_concept_coverage"})

  RETURN plan
```

### Present Plan to User

In **check** mode, present the plan and stop without writing. In **refresh** mode, obtain approval of the concrete plan before proceeding; reuse approval when that same plan and its inputs remain valid. Identify the book baseline, selected source, profile revision/validation, owning skill revision, exact affected concept blocks and appendix entries, proposed changes, preservation boundaries and unresolved mappings. Approval covers that plan only; changes to source or target document hashes require re-evaluation of affected work and renewed approval when the approved changes or their consequences differ. Approval to test a skill is not approval to replace the book or publish it.

```
Textbook Refresh Plan for mountainash-data
==========================================
Source: 4c07766 → a1b2c3d (12 files changed)
Profile: current (matches source HEAD)

Chapters to update:
  04-ibis-backend
    - regenerate_code_examples (concept 22: IbisBackend.connect signature changed)
    - add_new_sections (concept 25: new symbol IbisBackend.create_table)

  06-settings-and-configuration
    - find_and_replace (concept 67: DialectSpec renamed to BackendSpec)

Learning graph updates:
  - Update node 67 label: "DialectSpec" → "BackendSpec"
  - Update node 67 source_module: unchanged

API pages to rebuild: api/backends.md, api/core.md
  (automatic — mkdocstrings reads from source at build time)

FAQ: stale (2 chapters updated) — will regenerate affected questions

Unmapped new files (review manually):
  src/mountainash_data/backends/duckdb/__init__.py

Proceed? (y/n)
```

---

## Phase 5: Regenerate

Execute the plan, updating only stale artefacts.

### Chapter Section Regeneration

Chapters generated by `chapter-content-generator` v0.09+ contain concept
markers: `<!-- concept:42 -->` HTML comments that delimit where each concept's
content begins. These markers enable precise section targeting.

```pseudocode
REGENERATE_CHAPTER(chapter_dir, plan_entry, learning_graph):
  content = Read(chapter_dir/index.md)
  changed_concept_ids = plan_entry.changed_concepts

  FOR concept_id IN changed_concept_ids:
    # Find the section bounded by concept markers
    start = find_marker(content, f"<!-- concept:{concept_id} -->")
    next_marker = find_next_marker(content, start)
    old_section = content[start:next_marker]

    # Look up source info from the learning graph node
    node = learning_graph.nodes[concept_id]
    source_code = Read(source_repo / node.source_path)

    # Regenerate this section
    new_section = generate_concept_section(
      concept_id = concept_id,
      concept_label = node.label,
      source_module = node.source_module,
      source_code = source_code,
      chapter_context = extract_surrounding_context(content, start),
      reading_level = "college",
      action = plan_entry.actions[concept_id]
    )

    content = content[:start] + new_section + content[next_marker:]

  # Update metadata
  update_frontmatter_date(content)
  Write(chapter_dir/index.md, content)
  RETURN { chapter: chapter_dir, words: word_count(content) }
```

In practice, build a `patch-set.json` describing the `replace` operation for
each `concept_id` above and apply it with:

```bash
ibook refresh apply --project-root "$R" \
  --invocation /absolute/run/invocation.json --patch-set /absolute/run/patch-set.json
```

rather than splicing `content` by hand — `ibook refresh apply` rejects a stale
`chapter_dir/index.md` (edited since this run started reading it), rejects
an ambiguous or malformed marker set, and proves every byte outside the
`changed_concept_ids` sections is unchanged before writing anything.

### Fallback: Chapters Without Concept Markers

For chapters generated before concept markers were introduced (pre-v0.09),
fall back to full-section regeneration:

1. Read the chapter's concept list from "## Concepts Covered"
2. Filter to only the changed concepts
3. Read the full chapter content
4. Regenerate the entire chapter body while preserving the structure
   (title, summary, concepts list, prerequisites)

This is more expensive (~3000-5000 words per chapter vs ~300-500 per section)
but correct.

### Find-and-Replace for Renames

For `renamed_symbols` changes, avoid full regeneration:

```pseudocode
RENAME_IN_CHAPTER(chapter_dir, old_name, new_name):
  content = Read(chapter_dir/index.md)
  occurrences = count(old_name, content)
  IF occurrences > 0:
    content = content.replace(old_name, new_name)
    Write(chapter_dir/index.md, content)
    RETURN { chapter: chapter_dir, replacements: occurrences }
```

### Learning Graph Updates

Prepare proposed graph changes from the source-backed plan. Run the pinned `ibook graph reconcile EXISTING PROPOSED CANDIDATE`, then validate the candidate. Reconciliation preserves existing provenance and chapter/source enrichments, recalculating CIS from the proposed topology. It refuses ambiguous labels/IDs and enriched removals; resolve those explicitly on a reviewed copy, never by stripping metadata or guessing from substring matches.

Prepare a separate reviewed graph candidate, preserving source provenance and existing chapter assignments. Do not advance the book baseline or promote the candidate over the canonical graph in this phase. Verify proposed mappings with the candidate content in Phase 6; only Phase 7 records the selected source basis and promotes verified graph/state changes. Do not copy graph data, reports or viewer into `site/docs`.

### FAQ Refresh

If any chapters were updated, refresh only the human-approved affected FAQ
entries, preserving the existing format and canonical/published roles.

**Required format gate, before marker-only export or verification:** read the
FAQ Markdown and canonical JSON and identify their actual structure. Supported
helper input requires valid paired `<!-- faq:ID concepts:N,N -->` /
`<!-- /faq:ID -->` blocks covering every question, plus JSON already using
the helper's `schema_version`/`questions` projection with `id`, `concept_ids`,
`question`, `answer_markdown`, and `source` fields. Marker-looking examples,
missing/malformed blocks, partial coverage, or a different JSON shape do not
establish support.

The pilot uses `##` category headings, `###` question headings, and JSON
`metadata` plus `questions` entries containing `category`, `question`, and
`answer`. It has no question IDs or concept mappings to assume. Keep that
shape and metadata; do not retrofit FAQ markers, invent IDs/mappings, or
convert it to satisfy the helper.

Read the reader-facing FAQ identified in Phase 0 and the current chapters. Identify affected questions through human review, then update only approved answers after verifying source accuracy and input hashes. Preserve question/category order and every untouched answer. Use the confirmed brief when present; otherwise preserve the existing book's reading depth and appendix choices.

Legacy Markdown/JSON in `docs-site/learning-graph/` is a preservation input, not an obligatory mirrored output. Keep unsupported JSON byte-for-byte unchanged unless a separate reviewed migration explicitly authorizes changing its shape/content. Do not write it merely because chapter prose changed. When an existing project explicitly maintains synchronized legacy FAQ artifacts, verify ordered question/category/answer parity and hashes before any separately approved update; unexplained drift stops that update.

Do not introduce an FAQ or companion JSON when the existing maintenance scope does not include one. A new/replacement book's confirmed brief may exclude the appendix; neither route authorises inventing missing copies as a refresh side effect.

The heading-based comparison reads `###` question titles in document order
under their `##` categories; an answer ends at the next question or category.
Compare the ordered question/category list and each answer with canonical
JSON `questions`, trimming surrounding whitespace only. Preserve internal
Markdown, links, question counts, and untouched answers. Compare canonical
and published Markdown bytes, and any already-existing JSON copy. Ambiguous
headings, unexplained differences, or comparisons that cannot establish parity
require human review and resolution before writing state, not a fake pass.

Only for an already-supported marker-format FAQ may these commands be used:

```bash
ibook refresh faq-export \
  --faq "$R/docs-site/site/docs/faq.md"
ibook refresh faq-verify \
  --faq "$R/docs-site/site/docs/faq.md" \
  --json "$R/docs-site/learning-graph/faq-chatbot-training.json"
```

Capture export output for inspection; **never redirect it over an existing
FAQ JSON file**. Before applying any supported projection, confirm the input
contract, preservation of every unaffected question, ordering, answers, and
existing JSON shape. An empty projection of a nonempty FAQ is a hard refusal,
even if the CLI exits successfully. Unsupported export must never be applied.
Use heading-based comparison for this pilot and report the marker helper as
unsupported, not successful. Do not add a converter or CLI wrapper.

### API Pages

API reference pages do not need regeneration — mkdocstrings reads directly
from source at `mkdocs build` time. The refresh plan lists them for
informational purposes so the user knows to rebuild the site.

---

## Phase 6: Verify

After regeneration, verify the textbook is internally consistent.

```pseudocode
VERIFY(textbook_dir, learning_graph, plan):
  issues = []

  # 1. Concept coverage: every concept in the learning graph is still
  #    mentioned in exactly one chapter
  FOR chapter IN all_chapters:
    content = Read(chapter/index.md)
    concept_list = parse_concepts_covered(chapter/index.md)
    FOR concept IN concept_list:
      IF concept.label NOT IN content:
        issues.append(f"Chapter {chapter}: concept '{concept.label}' listed but not in content")

  # 2. Content hashes: recompute and compare to detect unexpected changes
  FOR chapter IN plan.chapters_to_regenerate:
    new_hash = sha256(Read(chapter/index.md))
    old_hash = refresh_state.chapter_state[chapter].content_hash
    IF new_hash == old_hash:
      WARN f"Chapter {chapter} was targeted for update but content unchanged"

  # 3. Concept markers: verify markers are still well-formed
  FOR chapter IN all_chapters:
    content = Read(chapter/index.md)
    markers = find_all("<!-- concept:\\d+ -->", content)
    expected = parse_concepts_covered(chapter/index.md)
    IF len(markers) != len(expected):
      issues.append(f"Chapter {chapter}: {len(markers)} markers but {len(expected)} concepts")

  # 4. Learning graph consistency: every enriched node points to a valid chapter
  FOR node IN learning_graph.nodes:
    IF node.chapter AND NOT chapter_exists(node.chapter):
      issues.append(f"Node {node.id} ({node.label}): chapter '{node.chapter}' not found")

  # 5. Internal links: check chapter cross-references resolve
  FOR chapter IN all_chapters:
    links = extract_markdown_links(chapter/index.md)
    FOR link IN links:
      IF NOT file_exists(resolve_relative(link, chapter)):
        issues.append(f"Chapter {chapter}: broken link {link}")

  REPORT issues
```

For marker-bearing chapters, run the installed helper's `coverage` command shown above against the reviewed graph candidate (or unchanged canonical graph) and candidate chapters; do not reimplement the marker/label cross-check inline. Verify FAQ parity using the applicable format-specific procedure in Phase 5 before Phase 7. Execute affected examples against the selected source, build the site and inspect changed rendered pages. Compare against the pre-refresh snapshot to prove every untargeted block/file remains unchanged. Report failures; do not update source baselines to make a failed run appear current.

---

## Phase 7: Update State

Write the updated learning graph and slim `refresh-state.json`.

### Update Learning Graph

Phase 5 prepared any graph changes without advancing the canonical book baseline. Only after Phase 6 succeeds, set the verified graph candidate's `metadata.source_commit` to the selected source revision and promote it with the updated refresh state. Preserve prior history. These file writes are not a multi-file transaction: report partial failures, and do not claim success if the graph and state disagree.

### Update refresh-state.json

```pseudocode
UPDATE_STATE(textbook_dir, changeset, plan, results):
  state = Read(textbook_dir/refresh-state.json) or new_state()

  state.baseline.source_commit = changeset.current_commit
  state.baseline.refresh_date = today()

  FOR chapter, result IN results:
    state.chapter_state[chapter] = {
      content_hash: sha256(Read(chapter/index.md)),
      word_count: result.words,
      has_concept_markers: count_markers(chapter/index.md) > 0,
      last_generated: today(),
      generator_version: "0.09"
    }

  state.learning_graph_state = {
    concept_count: len(learning_graph.nodes),
    edge_count: len(learning_graph.edges),
    enriched_count: count(n for n in nodes if n.source_module),
    content_hash: sha256(learning_graph_json)
  }

  state.faq_state = {
    question_count: count_faq_questions(),
    content_hash: sha256(faq_md)
  }

  # Append to refresh history
  state.refresh_history.append({
    date: today(),
    from_commit: changeset.baseline_commit,
    to_commit: changeset.current_commit,
    chapters_updated: [ch for ch in results],
    sections_regenerated: sum(len(r.changed_concepts) for r in results),
    faq_questions_updated: count_updated_faq,
    tokens_used: estimated_tokens
  })

  Write(textbook_dir/refresh-state.json, state)
```

---

## Seed Mode

When running for the first time (`mode = "seed"`), the skill:

1. Reads `manifest.json` from the profile directory to get the baseline commit
2. Reads all module profiles to extract symbols, paths, dependencies
3. Reads the learning graph from `R/docs-site/learning-graph/`
4. Reads each chapter's concept list from `R/docs-site/site/docs/chapters/`
5. **Enriches every learning graph node** with `source_module`, `source_path`,
   `chapter`, and `match_confidence`
6. **Adds `source_commit` and `profile_dir`** to the learning graph metadata
7. Writes the reviewed enriched graph only to `R/docs-site/learning-graph/learning-graph.json`; no published graph copy is created
8. Creates `R/docs-site/site/refresh-state.json` with chapter content hashes and tool versions
9. Reports low-confidence matches (< 0.6) for manual review

No chapter regeneration occurs in seed mode — it only enriches the graph and
creates the state file.

---

## Concept Markers

Concept markers are HTML comments embedded in chapter content to enable
precise section targeting during refresh:

```markdown
<!-- concept:42 -->
## The Backend Protocol

The `Backend` protocol defines the universal contract...

<!-- concept:43 -->
## Backend Registration

Registration is handled by...
```

### Marker Placement Rules

- One marker per concept, placed immediately before the heading or paragraph
  that introduces that concept
- Markers use the learning graph concept ID (integer), not the label
- Markers must appear in the same order as the concept coverage list
- The final concept's section extends to either the next `##` heading at the
  same or higher level, or to the "Key Takeaways" section

### Retrofitting Markers

For chapters generated before markers were introduced (pre-v0.09), a one-time
retrofitting pass adds them:

```pseudocode
RETROFIT_MARKERS(chapter_dir, learning_graph):
  content = Read(chapter_dir/index.md)
  concepts = parse_concepts_covered(chapter_dir/index.md)

  # Resolve concept IDs from the learning graph
  FOR concept_name IN concepts:
    concept_id = find_node_by_label(learning_graph, concept_name).id

    # Find where this concept is first substantively discussed
    position = find_concept_introduction(content, concept_name)
    IF position:
      insert_marker(content, position, concept_id)

  Write(chapter_dir/index.md, content)
```

This pass should be run once per project before the first incremental refresh.

---

## Cascade Rules

Changes propagate through the artefact chain. The refresh skill handles
each level, stopping early when no further propagation is needed:

```
Source code change
  │
  ├─► Profile update          (separate skill — package-documentation-profile)
  │
  ├─► API reference pages     (automatic — mkdocstrings reads source at build)
  │
  ├─► Learning graph nodes    (this skill — Phase 5, update labels/paths)
  │
  ├─► Chapter content         (this skill — Phase 5, section regeneration)
  │     │
  │     └─► FAQ entries        (this skill — Phase 5, FAQ refresh)
  │
  └─► Learning graph structure (rare — only when public API surface changes)
        │
        └─► Chapter structure  (rare — only when concepts are added/removed)
```

Most refreshes touch only learning graph node fields, chapter content sections,
and FAQ entries. Learning graph structure changes (new/removed concepts) and
chapter structure changes (new/removed chapters) are rare.

---

## Edge Cases

### Module renamed (file moved)

Phase 1 retains old and new paths as removed/added entries. During mapping, `git diff -M` may supply rename-pair evidence; it does not replace or discard the complete Phase 1 changeset. Confirm the identity match from source before proposing these steps in the approved plan:
1. Finds affected nodes by old `source_path` in the learning graph
2. Updates `source_module` and `source_path` on those nodes
3. Runs find-and-replace for the old module name in chapter content
4. Updates API page references

### Module split into multiple files

Detected as one file deleted + multiple files added. The old module's concepts
may span multiple new modules:
1. Flag for review: "Module X was split into Y and Z"
2. Re-run concept-to-module matching for the affected concepts
3. Update the affected nodes in the learning graph

### Manual edits detected

Before overwriting any chapter, compare its current content hash against the
stored hash:
```pseudocode
IF sha256(current_content) != state.chapter_state[chapter].content_hash:
  WARN "Chapter {chapter} has been manually edited since last refresh"
  ASK "Overwrite manual edits, merge, or skip?"
```

### Tool version mismatch

If `chapter-content-generator` was upgraded since the last refresh:
```pseudocode
IF current_tool_version != state.baseline.tool_versions.chapter_content_generator:
  WARN "Generator version changed ({old} → {new})"
  SUGGEST "Consider force-refresh for consistent output format"
```

### Concept markers missing

If a chapter has no concept markers:
```pseudocode
IF no markers found AND mode == "refresh":
  WARN "Chapter {chapter} has no concept markers — falling back to full regeneration"
  SUGGEST "Run retrofit-markers first for cheaper future refreshes"
```

---

## Cost Estimates

| Scenario | Chapters affected | Tokens (approx) |
|----------|-------------------|-----------------|
| Small refactor (1-2 files) | 1-2 chapters, section-level | 5-15k |
| Moderate change (5-10 files) | 3-5 chapters, section-level | 20-50k |
| Major change (new module) | 1-2 chapters + learning graph review | 50-100k |
| Full force-refresh | All chapters | 300-500k per project |
| Rename only | 1-5 chapters, find-and-replace | 1-3k |
| Seed (first time, no regen) | 0 chapters | 5-10k |

---

## Example Sessions

### Seed Mode

```
User: "Seed textbook-refresh with source_repo=/absolute/path/to/mountainash-data"

Skill:
1. Reads manifest.json → baseline commit 4c07766
2. Loads 22 module profiles (symbols, paths, classes)
3. Loads 100-concept learning graph from R/docs-site/learning-graph/
4. Reads 9 chapter concept lists
5. Enriches all 100 nodes: 82 mapped to modules, 10 foundational (null), 8 low-confidence
6. Adds source_commit + profile_dir to metadata
7. Writes the reviewed enriched learning-graph.json internally only
8. Creates refresh-state.json (content hashes, tool versions)
9. Reports: "8 concepts had low-confidence module matches — review recommended"
```

### Check Mode (Dry Run)

```
User: "Check textbook-refresh with source_repo=/absolute/path/to/mountainash-data"

Skill:
1. Reads learning-graph.json → metadata.source_commit = 4c07766
2. git diff 4c07766..HEAD → 3 files changed
3. Looks up changed paths in learning graph nodes → concepts 22, 25, 67, 68
4. Maps concepts to chapters: ch04 (concepts 22, 25), ch06 (concepts 67, 68)
5. Classifies: signature_change for ibis backend, renamed_symbols for settings
6. Reports plan (no files written)
```

### Refresh Mode

```
User: "Refresh textbook-refresh with source_repo=/absolute/path/to/mountainash-data"

Skill:
1-5. Same as check mode
6. Presents plan, user confirms
7. Updates learning graph node 67: label "DialectSpec" → "BackendSpec"
8. Regenerates 2 sections in ch04 (concepts 22, 25)
9. Find-and-replaces "DialectSpec" → "BackendSpec" in ch06
10. Refreshes 3 FAQ entries related to changed concepts
11. Promotes the reviewed internal graph candidate without publishing it
12. Verifies concept coverage, markers, links
13. Updates refresh-state.json
14. Reports: "2 chapters updated, 4 sections regenerated, ~12k tokens used"
```

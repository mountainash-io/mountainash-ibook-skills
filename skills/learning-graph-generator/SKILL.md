---
name: learning-graph-generator
description: Generate and reconcile an internal concept dependency graph from confirmed editorial intent and package profiles, preserving source mappings and chapter enrichments.
metadata:
  ibook.version: "2.0.0"
---

# Internal learning graph

The graph is a logical backend for chapter planning and refresh, not a published product. Resolve an explicit source repository/worktree. Read its confirmed `docs-site/editorial-brief.md`, profile manifest/modules, coverage report and **all available facets**. If the brief is draft or missing, use the retained `course-description-analyzer` interview first.

## Artifact ownership

Keep `learning-graph.json`, `learning-graph.csv`, concept list, taxonomy/configuration, metadata and reports under `docs-site/learning-graph/`. Do not add them to MkDocs navigation or copy them, their viewer, or maintenance tools into `docs-site/site/docs/`. Read the format reference `vis-network-json-format.md` for data fields; its viewer examples do not authorize publication.

All commands below are the pinned `ibook` uvx invocation documented in the repository README. Install the full skill repository to read its canonical schema at `../../src/ibook_tools/graph/learning-graph-schema.json`. Do not copy Python or shell helpers into projects.

## Concepts and dependencies

1. Enumerate concepts needed by the confirmed brief and current source, with concise unambiguous labels. Prefer Title Case but retain actual API spellings. No arbitrary 200/300/600-concept quota. Review coverage and questionable concepts rather than inflating counts.
2. Retain existing positive integer ConceptIDs for unchanged concepts. Never renumber to close gaps. A rename, split, merge or reused label is a reviewable identity change, not a fuzzy string match.
3. Map prerequisite relationships grounded in explanation order. Edge `{from: 5, to: 1}` means **5 depends on 1**. Do not reverse this convention. No self-dependency, duplicate dependency or nonexistent target. A terminal node has no dependents; an orphan has no edges in either direction.
4. Write CSV columns `ConceptID,ConceptLabel,Dependencies,TaxonomyID`; dependencies are pipe-separated integer IDs. Taxonomy IDs use uppercase letters, as required by the retained Draft 7 schema. Keep concise named categories with clear descriptions; report imbalance for editorial review, not arbitrary automatic reclassification.
5. Keep explicit `taxonomy-names.json`, optional `color-config.json` and source-backed `metadata.json`. Taxonomy-name precedence is built-in names → names embedded in color config → explicit taxonomy names. Preserve notices and source provenance; do not invent licensing permissions.

## Deterministic operations

Use explicit input/output paths; graph outputs must be new candidate files, never existing canonical files.

```text
ibook graph taxonomy concepts.csv categorized.csv --config taxonomy-config.json
ibook graph analyze learning-graph.csv quality-metrics-candidate.md
ibook graph taxonomy-report learning-graph.csv taxonomy-candidate.md --taxonomy-names taxonomy-names.json
ibook graph convert learning-graph.csv proposed.json --colors color-config.json --metadata metadata.json --taxonomy-names taxonomy-names.json
ibook graph validate proposed.json
ibook graph reconcile learning-graph.json proposed.json candidate.json
ibook graph validate candidate.json
```

Only supply optional configuration flags when the files exist. Missing explicit inputs are errors, not permission to fall back silently. For an initial graph, conversion produces the candidate. For any enriched existing graph, **reconcile**, never replace it with bare conversion output.

The packaged converter retains the upstream 1.05 scoring baseline: `CIS(x) = 1 + sum(CIS(d) for d in direct_dependents(x))`. It scores the dependency DAG in reverse topological order; no damping or iteration. Scores are topology-derived and recomputed, not preserved as editorial metadata. Do not infer stale scores solely because all scores equal one: an edgeless graph can legitimately have that result.

## Reconciliation and approval

Reconciliation matches stable IDs and preserves source/module/path/chapter/confidence fields, unknown enrichments and graph provenance. Changed labels under an existing ID, conflicting enrichments, reused labels under new IDs, and removal of enriched concepts/dependencies are conflicts. The command emits no candidate on conflict and never mutates its inputs.

Surface each conflict with its existing and proposed meaning for agent/user resolution. Do not guess identities or strip enrichment to make validation pass. Resolve intentional renames/removals on a separately reviewed copy, retain their provenance and then reconcile. Keep the accepted graph intact until the candidate is reviewed. Promote reviewed artifacts deliberately in the candidate branch, recording the selected source revision.

Preserve chapter assignments during mechanical updates. `book-chapter-generator` may deliberately remap them **after chapter-plan approval**, recorded as an editorial change. Report graph validation, scoring basis, coverage gaps, preservation and unresolved decisions. Do not regenerate the example book or publish graph artifacts as part of tool migration.

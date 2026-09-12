---
name: book-chapter-generator
description: Propose a facet-informed chapter and section plan from a confirmed editorial brief and internal dependency graph; obtain user approval before prose generation.
license:
metadata:
  ibook.version: "2.0.0"
  ibook.preferred-model: "sonnet"
---

# Chapter and section planning

Resolve the explicit source repository/worktree. Read `docs-site/editorial-brief.md`, the profile manifest/coverage/modules and **all available audience facets**, and `docs-site/learning-graph/learning-graph.json`. A brief must have actual user confirmation; a quality score or existing course description is not a substitute.

For a replacement book, read the old prose as potential reuse material, not as the chapter structure to preserve. Keep accepted branches and the current book intact.

## Validate the backbone

Use the pinned `ibook graph validate` command from the repository README. The canonical schema and converter belong to the installed tools, not copied project scripts. Edges point **from dependent to prerequisite**: `{from: 5, to: 1}` means concept 5 requires concept 1. Verify source-backed prerequisite meaning; do not reverse edges just because an advanced-sounding concept has no prerequisite.

Every active concept needs one primary chapter/section explanation. Cross-links may refer to it from other audiences. Prerequisites must appear earlier within the same chapter or in an earlier chapter. Inspect isolated concepts and dependency clusters as editorial issues rather than imposing a fixed number of concepts or chapters.

Read computed `cis` values. If missing or stale relative to changed topology, reconcile the enriched graph into a separate candidate; never regenerate over canonical enrichments. Importance is book-wide: use `cis_max = max(node['cis'] for node in graph['nodes'])` across the **whole book**, never just this chapter. CIS aids elaboration and ordering; it does not determine the editorial structure by itself.

## Propose the plan

Write only the internal `docs-site/chapter-plan.md` while approval is pending. Include:

- Status `proposed`, source/profile/graph basis and the confirmed brief it implements.
- A coverage account for every available facet: where its needs are served, linked, or intentionally excluded by the brief. Consider custom audiences as well as users, maintainers, backend architecture and broader positioning.
- Fresh ordered chapters with stable slugs, reader-facing titles, purpose, audiences served, prerequisites, sections, primary concept IDs, source references and reusable existing material.
- Reasons for each chapter boundary versus keeping material as sections. Neither one chapter per facet nor three rigid audience tracks is required.
- Core depth progression: understand concepts → use the package → understand/modify internals. Readers can enter at the level they need through clear signposts and links to shared explanations.
- Appendix decisions from the brief, chapter/section link destinations, and proposed visuals. Prefer Mermaid; justify any interaction separately. No quizzes or public graph section.
- Per-concept CIS and book-wide elaboration guidance kept internally, plus unresolved ordering/coverage questions.

Present the proposal and obtain user approval **before chapter prose or site outlines are generated**. Do not infer approval from a general request to implement tooling. Record actual approval/date and the approved scope; if scope changes, reopen the affected brief decision first.

## After approval

Record status `approved`. Deliberately update candidate graph chapter mappings to the approved slugs, preserving source fields and unknown enrichments. Record intentional mapping changes separately from mechanical reconciliation. Validate the resulting graph.

Create chapter directories/outlines only for the approved plan under `docs-site/site/docs/chapters/`. Do not count outlines as finished chapters. Keep concept markers and mappings for refresh, but do not publish graph reports or internal planning tables. Coordinate shared navigation edits serially using the installer reference `../book-installer/references/mkdocs-nav-editing.md`; preserve site URL overrides, hooks and branch routing.

Hand the approved plan, confirmed brief, internal graph, current source and chosen reuse material to `chapter-content-generator`. A mascot is optional; if already defined, preserve the project's existing rendered placement rules. Do not alter frozen mascot resources or require a mascot before writing.

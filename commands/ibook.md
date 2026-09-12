---
name: ibook
description: Show the read-only Mountainash documentation runbook and the next unmet artifact or approval gate. Never auto-run a skill.
---

# Mountainash documentation runbook

This is a passive assessment, not the Python `ibook` CLI and not an orchestrator. Read existing artifacts; recommend the next skill and its gate. Do not write files, run generation, commit, install, or publish from this command.

## Establish the target

Use the explicit source repository or worktree, never infer a sibling from the current directory. Its documentation root is `docs-site/`; its MkDocs project is `docs-site/site/`. Resolve relative paths against the invocation directory once.

Read the following artifacts and their recorded source/approval state. File existence is not completion. A draft brief or proposed chapter plan is **awaiting approval**, not missing and not approved. Outdated profiles are **stale**. A chapter outline is **incomplete content**. Never infer approval from a quality score, commit, filename or presence of headings.

| Order | Skill / operation | Artifact | Gate |
|---|---|---|---|
| 1 | `package-documentation-profile` | `docs-site/profile/{manifest.json,modules/,facets/,coverage.md}` | Selected source revision, valid composable profiles, manual fields preserved |
| 2 | `course-description-analyzer` | `docs-site/editorial-brief.md` | User confirms audience/scope, all-facet rationale, depth and appendix decisions |
| 3 | `learning-graph-generator` | `docs-site/learning-graph/` | Internal graph validates; reconciled stable IDs, enrichment and scores; conflicts resolved |
| 4 | `book-chapter-generator` | `docs-site/chapter-plan.md` | User approves fresh chapter/section structure before prose |
| 5 | `chapter-content-generator` | `docs-site/site/docs/chapters/` | Every approved chapter complete, source-backed, correctly ordered |
| 6 | `faq-generator`, `glossary-generator` | `docs-site/site/docs/faq.md`, `glossary.md` | Confirmed appendices complete with verified chapter/section links |
| 7 | `reference-generator`, optional visual skills | Verified references and necessary visuals | Mermaid preferred; included MicroSims actually implemented and visually checked |
| 8 | Strict MkDocs build and review | Candidate site and reviewed PR | No deployed internal graph, course or quiz output; actual browser proof |
| 9 | Existing paired publishing process | Accepted main/develop sites | Explicit content/deployment acceptance; prepared-files publishing only |

Use `book-installer` only when a missing site scaffold or an actually requested feature requires it. Do not replace an existing site configuration. A missing scaffold does not prevent a profile or brief interview.

## Recommend one next action

Report: target, source basis, current stage, the first missing/stale/awaiting-approval artifact, and the one next skill or user decision. Show the ordered runbook. If the brief is draft, recommend confirming that brief, not rerunning profiling or pretending generation can begin. If the plan awaits approval, show the plan's open decisions; do not generate chapters.

## Standing boundaries

- Reader-facing output is chapters plus confirmed appendices. Core depth is concepts → package use → internals, with all available audience facets considered; neither three fixed tracks nor one chapter per facet is mandatory.
- Canonical graph data, viewer, reports, source mappings, brief and chapter plan remain outside `site/docs`. Hiding a navigation link is insufficient.
- Keep all skills. Do not invoke quiz generation in this workflow. MicroSims, media, mascots, analytics and announcements are not mandatory steps.
- Deterministic tools use the pinned uvx installation in the repository README; never copy helpers into books. Frozen `bk` commands remain separate.
- Routine `textbook-refresh` reuses the confirmed brief. Editorial changes reopen only affected questions and require confirmation.
- Agent work is iterative and reviewed through PRs. Actions validate/build/publish prepared files only. Existing accepted books remain unchanged until replacement acceptance.

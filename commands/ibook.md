---
name: ibook
description: Show the read-only Mountainash documentation runbook and the next unmet artifact or approval gate. Never auto-run a skill.
---

# Mountainash documentation runbook

This is a passive assessment, not the Python `ibook` CLI and not an orchestrator. Read existing artifacts; recommend the next skill and its gate. Do not write files, run generation, commit, install, or publish from this command.

## Establish the target

Use the explicit source repository or worktree, never infer a sibling from the current directory. Its documentation root is `docs-site/`; its MkDocs project is `docs-site/site/`. Resolve relative paths against the invocation directory once.

Establish the requested operation before assessing artifacts. Read their source and approval state; existence is not completion. Do not interpret an existing book's missing new-workflow planning files as a request to replace that book.

## Select the operation

| User intent | Route | Boundary |
|---|---|---|
| Source changed; refresh or maintain an existing book | Existing-book refresh below | Preserve its structure and editorial scope |
| Create a book where none exists | Creation below | Confirm brief and chapter plan before prose |
| Redesign or replace an existing book | Creation below, only with explicit replacement intent | Keep the accepted book separate until acceptance |

If intent is materially ambiguous, ask which operation is intended. A source change alone never selects replacement, `seed`, or `force-refresh`.

## Existing-book refresh

The source of truth for phases and stop conditions is [textbook-refresh](../skills/textbook-refresh/SKILL.md), especially its profile freshness gate. The [profile skill](../skills/package-documentation-profile/SKILL.md) owns profiling inputs, preservation and validation. This command routes to those instructions; it neither replaces them nor runs them.

1. Identify the explicit target worktree and selected source snapshot. Read the existing book's baseline from its graph/state and the profile's separate source revision.
2. Recommend `textbook-refresh` in `check` mode. It detects the source delta and checks profile freshness before mapping or classifying book impact.
3. If the profile is stale, the next action is the separate profile skill with `behavior: incremental`, not chapter generation. Use `mode: interactive` for a direct user-driven run; use `mode: orchestrated` only when an explicit orchestrated invocation is supplied. Preserve the earlier profile for comparison. A full-profile-scan decision does not authorise a book rebuild.
4. After the profile skill returns a validated result for the selected source, with review-required warnings resolved, recommend re-entering `textbook-refresh` in `check` mode. It presents the bounded impact plan and stops without writing.
5. Only approval of that concrete impact plan permits `refresh` to generate the affected content, verify preservation and update candidate state. Changed inputs invalidate the plan.
6. Publication remains a separate acceptance decision.

Reuse an existing confirmed brief/plan when present. If absent, preserve the current book's scope, chapter organisation, appendix choices and reader surfaces; do not send the user through creation to perform routine maintenance. Structural changes or insufficient evidence of the intended scope require a focused decision, not an inferred replacement.

## Creation or explicitly requested replacement

A draft brief or proposed chapter plan is awaiting approval, not missing or approved. Never infer approval from a quality score, commit, filename or presence of headings.

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

Report the requested operation, explicit target, book baseline, profile revision, selected source snapshot, the first unmet gate and one next skill or user decision. Cite the owning skill section. For maintenance, a stale profile routes to profiling even if the book lacks a new-workflow brief. Only on the creation/replacement route do a draft brief or unapproved fresh chapter plan select the corresponding approval step. Never silently switch routes.

## Standing boundaries

- The creation/replacement workflow produces chapters plus confirmed appendices. Core depth is concepts → package use → internals, with all available audience facets considered; neither three fixed tracks nor one chapter per facet is mandatory.
- Canonical graph and planning artifacts remain internal. Routine refresh does not migrate or delete an existing book's reader surfaces as cleanup; that is a separate editorial/publishing change.
- Keep all skills. Do not invoke quiz generation in this workflow. MicroSims, media, mascots, analytics and announcements are not mandatory steps.
- Deterministic tools use the pinned uvx installation in the repository README; never copy helpers into books. Frozen `bk` commands remain separate.
- Follow the skill instructions and their handoffs, not an improvised sequence. Report missing or contradictory instructions as a process failure; do not fill the gap silently and call the skill test successful. The README defines workflow acceptance evidence.
- Agent work is iterative and reviewed through PRs. Actions validate/build/publish prepared files only. Existing accepted books remain unchanged until replacement acceptance.

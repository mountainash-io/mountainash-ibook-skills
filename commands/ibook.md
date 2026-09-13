---
name: ibook
description: Guide Mountainash documentation work through the owning skills, focused decisions and authorized continuation. Keep checks read-only and preserve content approval gates.
---

# Mountainash documentation runbook

This is an agent runbook, not the Python `ibook` CLI or a new deterministic orchestrator. Use the owning skills to carry out the requested operation and coordinate authorized handoffs. A bare `/ibook`, request to show the runbook or read-only check authorizes assessment only, not writes. A maintenance request permits routine work within its agreed scope, not unapproved destructive preparation, content generation, commits or publication.

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

The source of truth for phases, adaptation and safety gates is [textbook-refresh](../skills/textbook-refresh/SKILL.md). The [profile skill](../skills/package-documentation-profile/SKILL.md) owns profiling inputs, preservation and validation. Follow those instructions rather than duplicating their contracts here; the invoking agent owns the conversation and explicit stage transitions.

1. Identify the explicit target worktree and selected source snapshot. Read the existing book's baseline from its graph/state and the profile's separate source revision.
2. Assess the source delta and profile gate through `textbook-refresh`'s read-only analysis before mapping or classifying book impact.
3. When profiling is required and authorized, invoke the separate profile skill with `behavior: incremental`, not chapter generation. Use `mode: interactive` for a direct user-driven run; use `mode: orchestrated` only when an explicit orchestrated invocation is supplied. Preserve the earlier profile for comparison. For a check-only request, explain and obtain authorization before leaving read-only assessment. A full-profile-scan decision does not authorise a book rebuild.
4. Investigate a failed prerequisite and recommend a bounded remedy using the refresh skill's Adaptive maintenance guidance. Ask for material choices, not workflow mechanics. After authorized preparation and a validated profile result with review-required warnings resolved, re-enter refresh analysis, reusing still-valid work, and present the bounded impact plan.
5. Only approval of that concrete impact plan permits `refresh` to generate the affected content, verify preservation and update candidate state. Re-evaluate affected work when inputs change; do not repeat unchanged approvals or discard unrelated progress.
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

## Carry the operation forward

Report the requested operation, explicit target, separate book/profile baselines, selected source snapshot and observed gate evidence, with detail proportional to the decision. Continue authorized stages rather than merely recommending the next skill. When a material decision is needed, explain the issue, recommendation and consequences; after the answer, perform and verify the authorized work and resume at the earliest valid point. For read-only assessment, stop with findings and the proposed transition, without writes. For a deferral or genuine missing prerequisite, identify what remains blocked and what permits resumption.

For maintenance, a stale profile routes to profiling even if the book lacks a new-workflow brief. Only on the creation/replacement route do a draft brief or unapproved fresh chapter plan select the corresponding approval step. Never silently switch routes, infer consent in unattended work or claim a profile update completed the book.

## Standing boundaries

- The creation/replacement workflow produces chapters plus confirmed appendices. Core depth is concepts → package use → internals, with all available audience facets considered; neither three fixed tracks nor one chapter per facet is mandatory.
- Canonical graph and planning artifacts remain internal. Routine refresh does not migrate or delete an existing book's reader surfaces as cleanup; that is a separate editorial/publishing change.
- Keep all skills. Do not invoke quiz generation in this workflow. MicroSims, media, mascots, analytics and announcements are not mandatory steps.
- Deterministic tools use the pinned uvx installation in the repository README; never copy helpers into books. Frozen `bk` commands remain separate.
- Follow the owning skills' contracts and adaptive guidance. An unfamiliar situation is not itself a process failure. Investigate and resolve what is safely within scope; pause dependent work for a genuine missing capability, fact, authority or contract conflict. Propose contract changes separately rather than bypassing gates. The README defines workflow acceptance evidence.
- Agent work is iterative and reviewed through PRs. Actions validate/build/publish prepared files only. Existing accepted books remain unchanged until replacement acceptance.

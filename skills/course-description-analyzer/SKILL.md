---
name: course-description-analyzer
description: Establish or review a confirmed internal editorial brief from package profiles and audience facets before chapter planning. Retains the original skill identity without requiring a published course page.
license: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
metadata:
  ibook.version: "2.0.0"
  ibook.preferred-model: "sonnet"
---

# Editorial brief interview

Mountainash adaptation of the retained course-description-analyzer skill. A numerical completeness score is not editorial approval. Do not create a public course description or impose concept-count quotas.

## Inputs

Resolve an explicit source repository/worktree. Read its `docs-site/profile/manifest.json`, coverage report, **every available audience facet**, and the relevant module profiles. Use the existing facet contract, including custom audiences; do not introduce another audience schema. If the profiles are stale, establish their source basis before asserting coverage.

Read an existing `docs-site/editorial-brief.md` or a supplied brief. Use existing answers rather than restarting the interview. The toolchain design interview does not approve an individual book's brief.

## Interview

Present a source-grounded proposal and ask only unresolved editorial questions:

1. What must readers understand and accomplish? Which package capabilities and limitations are in scope, and which are explicitly excluded?
2. How should the book serve conceptual newcomers, package users and people modifying internals? Consider all facets, including architecture and positioning where available; explain included and deferred audience needs. Do not force one primary audience or one chapter per facet.
3. What prerequisite knowledge and explanation depth should each audience need? Readers may enter at their required depth; link shared explanations instead of repeating them.
4. Confirm **FAQ and glossary appendices**, included by default, with links to relevant chapters/sections. Record any requested exclusion explicitly.
5. Confirm the visual policy: simple Mermaid first; MicroSims only where interaction adds distinct explanatory value. No quizzes in the Mountainash workflow.
6. For a replacement, identify accurate prose/examples/appendix entries worth reusing. Propose a fresh structure, not inheritance of the old course outline.

Record the proposed decisions at `docs-site/editorial-brief.md`, outside the published site. Include title/purpose, source revision and dirty-state caveats, profile basis, audience/facet rationale, prerequisites, scope/exclusions, depth progression, reuse policy, appendices, visuals and open questions. Use the retained template under `assets/` as a field guide, not as evidence of approval.

## Confirmation gate

Present the complete brief for confirmation. Record status `draft` until the user confirms it. Then record status `confirmed`, the actual confirmation date and a concise account of what was confirmed. Never manufacture a person's name, date or approval. Do not write a chapter plan or prose before the relevant gate passes.

## Refresh

Routine source changes reuse the persisted confirmed brief. When audience, scope or editorial policy changes, identify the exact affected decisions, ask focused questions and confirm the revision. Preserve prior decisions and meaningful approval history; do not silently rewrite or repeat the entire interview.

## Completion

Return the internal brief path, source/profile basis, decisions confirmed and unresolved gate. Recommend `learning-graph-generator` only after confirmation. Keep accepted books untouched; finalize implementation/content changes through reviewed PRs, not unattended Actions.

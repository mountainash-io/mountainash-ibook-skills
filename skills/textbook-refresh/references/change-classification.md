# Change Classification Reference

Classify source changes from baseline-to-target evidence, then inspect the book's actual teaching. A module can have multiple classifications: API changes do not subsume behavioral changes. The owning skill retains the set plus symbol diffs and source-backed reasons; these are planning judgments, not a new CLI or protocol schema.

## Classification Hierarchy

For added/removed files, use `new_module` / `removed_module`. For modified files, assess both:

- **API shape:** added/removed/renamed symbols and changed signatures, using the actual source revisions. Preserve every applicable symbol/signature finding.
- **Semantic effect:** `behavior_change` when observable behavior changed; `internal_refactor` only when behavior is established as preserved; `review_required` when the effect is unresolved.

Use `docstring_only` only after proving that the changes are limited to nonsemantic formatting, comments or docstrings. An unchanged public API is not that proof. Private helpers can change validation, outputs, ordering, filtering, missing-value handling or dependent callers. Syntax-aware comparison helps identify executable edits but does not establish semantic equivalence. Annotations, decorators and metadata require checking their runtime consumers.

Direct graph mappings are starting points. Check affected dependents and the actual implementation lessons even if their recorded source files did not change. Resolve uncertainty before approving affected content, rather than marking it “no impact.”

## Classifications

### new_module

**Detection:** File path exists in current commit but not in baseline.

**Chapter impact:** High. A new module may introduce concepts not covered by
any existing chapter. The refresh skill flags this for review — the user must
decide whether to:
- Add concepts to the learning graph and assign them to an existing chapter
- Create a new chapter (requires re-running book-chapter-generator)
- Skip (the module is an internal implementation detail not worth teaching)

**API page impact:** A new API reference page should be created.

**Learning graph impact:** May need new concept nodes and dependency edges.

**Automated action:** Flag for manual review. Do not auto-generate content
for unmapped modules.

---

### removed_module

**Detection:** File path exists in baseline but not in current commit.

**Chapter impact:** High. Concepts taught from this module may be orphaned.
The refresh skill identifies which chapters and concepts are affected.

**API page impact:** The corresponding API page should be removed or marked
as deprecated.

**Learning graph impact:** Concepts may need removal or reassignment.

**Automated action:** Flag for manual review. Identify affected chapters and
concepts. Do not auto-delete content — the concepts may still be teachable
from a different angle.

---

### new_symbols

**Detection:** New class or function names appear in `public_api` that were
not in the old profile.

**Chapter impact:** Medium. New sections should be added to the chapter(s)
that cover this module. Use concept markers to insert content at the
appropriate position.

**API page impact:** Automatic (mkdocstrings picks up new symbols).

**Learning graph impact:** New concepts may be needed if the symbols represent
teachable concepts.

**Automated action:** Generate new section content for each new symbol,
inserting after the last related concept marker in the chapter.

---

### removed_symbols

**Detection:** Class or function names from the old `public_api` are absent
in the current source.

**Chapter impact:** Medium. Sections teaching the removed symbol should be
revised or removed. Simply deleting prose can leave gaps — the surrounding
narrative may reference the removed concept.

**API page impact:** Automatic (mkdocstrings drops absent symbols).

**Learning graph impact:** Concepts may need removal.

**Automated action:** Regenerate the sections covering the removed concepts,
using the surrounding context to produce a coherent narrative without the
removed content. Flag the concept for potential removal from the learning
graph.

---

### renamed_symbols

**Detection:** Evidence establishes one-to-one old/new symbol pairs. Similar names, structures or paths suggest candidates; they do not prove identity. Record verified pairs alongside the complete added/removed sets. Classify unmatched additions/removals independently as `new_symbols`, `removed_symbols` or `mixed_changes`, retaining any accompanying signature/behavior findings.

**Chapter impact:** Low. Find-and-replace the old name with the new name
throughout the chapter. No structural changes needed.

**API page impact:** Automatic.

**Learning graph impact:** Propose label changes for verified pairs only; never treat every symbol in a module's added/removed sets as part of a rename.

**Automated action:** Propose bounded replacements for verified pairs. Unmatched additions/removals and accompanying semantic changes remain separate impacts in the same combined content proposal.

---

### mixed_changes

**Detection:** Both unmatched additions and unmatched removals remain after accounting for any verified rename pairs. This classification can coexist with `renamed_symbols`; neither hides the other's changes.

**Chapter impact:** High. Affected sections should be regenerated using the
new source code as context.

**API page impact:** Automatic.

**Learning graph impact:** Review concept coverage.

**Automated action:** Regenerate all sections in the chapter that cover
concepts from this module. This is the most expensive classification short
of full chapter regeneration.

---

### signature_change

**Detection:** The same symbols exist in both old and new versions, but their
signatures differ (different parameters, return types, or method signatures).

**Chapter impact:** Update examples and parameter explanations that use the changed signature. Independently retain any `behavior_change` finding; new errors, ordering or output semantics are not covered by a signature-only edit.

**API page impact:** Automatic.

**Learning graph impact:** None.

**Automated action:** Regenerate the concept sections that contain code
examples for the changed symbols. Focus on code blocks and parameter
explanations rather than conceptual prose.

---

### docstring_only

**Detection:** Source comparison proves only nonsemantic formatting, comments or docstrings changed. Stable symbol names/signatures alone are insufficient. Do not place executable edits here; do not assume type annotation changes are nonsemantic.

**Chapter impact:** No source-driven chapter regeneration. If source inspection reveals independently stale teaching, record it separately rather than disguising an executable change as documentation-only.

**API page impact:** Automatic where mkdocstrings renders those source docstrings.

**Learning graph impact:** None.

**Automated action:** No chapter regeneration for the nonsemantic delta; existing API pages update on the next build.

---

### internal_refactor

**Detection:** Implementation changed, with evidence that observable behavior is preserved. Non-public naming and stable signatures do not establish this.

**Chapter impact:** Review the actual teaching. Update sections that describe the changed algorithm, dependency, helper or implementation example; retain unaffected concepts. An internals-oriented book can require updates even when users observe identical results.

**API page impact:** Review affected references; do not assume private symbols are absent from every project.

**Learning graph impact:** No automatic change.

**Automated action:** Put affected concepts into review until their teaching is compared. Convert demonstrated stale sections into bounded update proposals; skip only where the content remains accurate.

---

### behavior_change

**Detection:** Source-backed comparison establishes changed observable behavior, including return values, errors/validation, ordering, filtering, null/sentinel semantics or effects on callers. Keep this classification alongside any API additions, removals, renames or signature changes.

**Chapter impact:** Update affected explanations and examples. Include concepts reached through unchanged dependents or implementation lessons whose graph mappings do not directly name the changed file.

**API and graph impact:** Review affected references and concept coverage; do not invent new concepts merely because a private helper was added.

**Action:** Propose one bounded update per affected concept, combining overlapping behavioral and API work. Confirm actual source evidence and preservation boundaries before content approval.

---

### review_required

**Detection:** The behavioral effect or documentation scope cannot be established from available evidence. This is not equivalent to `internal_refactor` or “no impact.”

**Action:** Investigate the missing source fact, caller effect or mapping and state the precise unresolved prerequisite if it remains unavailable. Do not approve affected regeneration or book-baseline promotion on an unresolved finding.

---

## Cost by Classification

| Classification | Regeneration Scope | Approx Tokens |
|---------------|-------------------|---------------|
| `internal_refactor` | Review taught implementation; update demonstrated stale sections | Scope-dependent |
| `behavior_change` | Affected explanations and examples, including dependent concepts | Scope-dependent |
| `review_required` | Investigate before approving content work | Unknown |
| `docstring_only` | None for proven nonsemantic edits (API auto-updates) | 0 |
| `renamed_symbols` | String replacement | < 1k |
| `signature_change` | Code examples in 1-3 sections | 3-8k |
| `new_symbols` | 1-3 new sections | 5-15k |
| `removed_symbols` | 1-3 sections revised | 5-15k |
| `mixed_changes` | All sections for affected module | 10-30k |
| `new_module` | Manual review + potential new sections | 15-40k |
| `removed_module` | Manual review + section removal | 5-15k |

## Priority Order

Resolve review requirements first. When multiple classifications affect a chapter, combine overlapping changes into one proposal per concept before applying patches. The following ordering helps compose that proposal; it is not permission for repeated independent rewrites of the same block:

1. `renamed_symbols` — apply string replacements first (cheapest, no conflicts)
2. `removed_symbols` — remove stale content before adding new content
3. `signature_change` — update existing code examples
4. `new_symbols` — add new sections
5. `mixed_changes` and `behavior_change` — update affected explanations and examples, retaining all earlier API findings

Include stale implementation teaching found during `internal_refactor` review in the same bounded proposal. No classification authorizes automatic content writes, chapter replacement or publication.

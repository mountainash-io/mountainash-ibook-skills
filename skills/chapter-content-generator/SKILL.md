---
name: chapter-content-generator
description: Write complete source-backed chapters from a confirmed editorial brief and user-approved chapter plan, using the internal graph for ordering, coverage and refresh markers.
license: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
metadata:
  ibook.version: "2.0.0"
  ibook.preferred-model: "sonnet"
---

# Chapter content generation

## Required gate and inputs

Resolve the explicit source repository/worktree. Read its confirmed `docs-site/editorial-brief.md`, user-approved `docs-site/chapter-plan.md`, profile manifest/all available facets/relevant modules, internal graph under `docs-site/learning-graph/`, and actual source/examples/tests. Missing or draft approval is a stop gate, not permission to infer consent or generate a sample.

Read `references/reading-levels.md` for depth adaptation. For a chosen non-text element, read the applicable format guidance in `references/content-element-types.md`; its legacy interactivity requirements do not override this workflow's Mermaid-first policy. Reuse accurate old explanations/examples deliberately, checking them against current source. Do not inherit the old course outline.

## Ordering and elaboration

Edges point **from dependent to prerequisite**. Build `prereqs[edge['from']].add(edge['to'])`. Every primary explanation follows its prerequisites, within the chapter or in preceding chapters. Link to shared explanations rather than repeating them for each audience.

Use the approved plan's concept IDs and graph `cis` fields. Scores come from the packaged graph operation, not an invented per-chapter calculation. Normalize across the entire book:

```python
import math

def elaboration_score(cis, cis_max):
    if cis_max <= 1:
        return 0.0
    return math.log(cis + 1) / math.log(cis_max + 1)
```

Retain the upstream starting guidance, subject to the brief and actual explanation needs:

| Tier | Book-wide score | Starting words | Treatment |
|---|---|---|---|
| A | >= 0.5 | 500–750 | Worked example and useful diagram/chart/table |
| B | >= 0.2 and < 0.5 | 250–400 | Worked example |
| C | < 0.2 | 120–200 | Precise explanation; example when useful |

Keep this planning table internal. Do not pad to meet quotas or normalize chapter lengths to an identical size. Record justified departures from the guidance. Never make MicroSims compulsory to satisfy an element count. Missing/stale scores require enrichment-preserving reconciliation, not bare CSV replacement. All-one scores alone do not prove staleness.

## Writing

Work chapter by chapter unless the user's execution preference says otherwise. Complete every chapter in the approved plan, not just a sample or placeholder outline.

- Lead with the reader's question and explain concepts before showing their code, table or diagram. Introduce unfamiliar vocabulary and explain key parameters before examples.
- Serve concepts, package use and internals at the depths chosen in the plan; use signposts so readers can enter at the level they need. Consider all selected facets, not only a hardcoded three-audience model.
- Cite actual source/API/example paths. Exercise executable examples in the selected package environment; do not invent outputs or claim unsupported features.
- Use accurate errors, boundaries, tradeoffs and extension points. Separate public API from internal details and describe actual guarantees.
- Put content under `docs-site/site/docs/chapters/<approved-slug>/index.md`. Use one clear page title, ordered section headings, blank lines before lists/tables and stable links.
- Preserve concept boundaries as `<!-- concept:N -->` markers. If several concepts share one atomic explanation, follow the refresh engine's shared-marker format. Verify assigned coverage with `ibook refresh coverage --graph GRAPH --chapters CHAPTERS`.
- Keep internal concept/scoring tables, graph data/reports/viewer, brief and plan outside the site source. Do not publish course-generation artifacts or quizzes.
- If a project already defines a mascot, read its rendered `CONTENT-GENERATION-GUIDE.md` placement rules before using it. Do not modify the frozen canonical renderer/rules or invent a required mascot.

## Visuals and supporting content

Prefer a simple Mermaid diagram when it explains a relationship or process. Use existing MkDocs Mermaid configuration and verify rendered output. Tables and static diagrams are valid explanatory tools.

A MicroSim requires a specific interactive learning benefit beyond a diagram. Check available existing local/reusable assets and their notices before generating one; do not require a developer-specific catalog path or service. If included, implement the real interaction using the retained visual skills and inspect it in a browser. An unimplemented specification or iframe is not finished content.

Generate the FAQ/glossary appendices confirmed in the brief, linking to real chapter/section destinations. Preserve useful existing entries and unsupported FAQ JSON. Verify references through `reference-generator`; do not turn reference creation into automatic network publication.

## Completion and refresh

Check every planned chapter and primary concept, prerequisite order, links, examples and chosen visuals. Build the complete candidate strictly and inspect a representative chapter plus navigation/appendices in the actual browser surface. Report exactly what was exercised and any unresolved content review.

The accepted book stays unchanged until review and acceptance. Finalize candidate changes through PRs. Establish truthful refresh-state hashes/mappings for the new structure while retaining meaningful history. Ordinary future refresh uses the persisted brief and `ibook refresh plan/apply`; editorial changes require focused confirmation first. Consumer Actions only validate/build/publish already prepared content.

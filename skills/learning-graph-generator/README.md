# Internal graph tools

Use the pinned `mountainash-ibook-tools` uvx installation described in the repository README. Maintenance scripts are no longer copied into books or the skill directory.

```text
ibook graph validate /absolute/path/learning-graph.json
ibook graph convert concepts.csv proposed.json --taxonomy-names taxonomy-names.json
ibook graph reconcile accepted.json proposed.json candidate.json
```

The canonical [schema](../../src/ibook_tools/graph/learning-graph-schema.json) uses **JSON Schema Draft 7**. `metadata`, `groups`, `nodes` and `edges` are required; metadata requires a title, nodes require positive integer IDs, labels and group IDs. The command also rejects duplicate IDs/dependencies, dangling dependencies, unknown groups and cycles. Edge direction is dependent → prerequisite. `cis` is computed from topology using the upstream 1.05 algorithm.

Reconciliation preserves chapter/source/unknown enrichments and provenance for stable IDs. It refuses ambiguous identity changes, conflicting enrichments and enriched removals without changing its inputs. Outputs must use new candidate paths. See `SKILL.md` for the review and explicit promotion workflow.

Keep graph data, viewers, reports and planning artifacts outside the published site source. The graph is a backend for chapter organization, not a required public page.

import json
import subprocess
import sys
from copy import deepcopy

import pytest

from ibook_tools.graph.reconcile import ReconciliationConflict, reconcile


def graph():
    return {
        "metadata": {"title": "Rules", "source_commit": "accepted", "custom": {"owner": "editor"}},
        "groups": {"CORE": {"classifierName": "Core", "color": "SteelBlue"}},
        "nodes": [
            {"id": 1, "label": "Expression", "group": "CORE", "cis": 99,
             "source_module": "rules.expression", "source_path": "src/rules.py", "chapter": "01-concepts",
             "match_confidence": 1.0, "editorial": {"notes": ["keep"]}},
            {"id": 2, "label": "Rule", "group": "CORE", "cis": 99},
        ],
        "edges": [{"from": 2, "to": 1, "evidence": "source.py:12"}],
        "provenance": {"review": "accepted"},
    }


def proposal(existing):
    result = deepcopy(existing)
    result["metadata"] = {"title": "Converter default"}
    result["nodes"] = [{k: v for k, v in node.items() if k in {"id", "label", "group"}} for node in result["nodes"]]
    result["edges"] = [{"from": 2, "to": 1}]
    result.pop("provenance")
    return result


def test_reconciliation_keeps_editorial_data_and_recomputes_transitive_scores():
    existing = graph()
    before = deepcopy(existing)
    proposed = proposal(existing)
    proposed["nodes"].append({"id": 3, "label": "Evaluation", "group": "CORE"})
    proposed["edges"].append({"from": 3, "to": 2})
    result = reconcile(existing, proposed)
    assert result["metadata"] == existing["metadata"]
    assert result["provenance"] == existing["provenance"]
    assert result["nodes"][0] == {**existing["nodes"][0], "cis": 3}
    assert [node["cis"] for node in result["nodes"]] == [3, 2, 1]
    assert result["edges"][0]["evidence"] == "source.py:12"
    assert existing == before


@pytest.mark.parametrize("change", ["rename", "remove-enriched", "conflicting-chapter", "reuse-label", "remove-enriched-edge"])
def test_ambiguous_changes_need_resolution(change):
    existing = graph()
    proposed = proposal(existing)
    if change == "rename":
        proposed["nodes"][0]["label"] = "Different identity"
    elif change == "remove-enriched":
        proposed["nodes"].pop(0)
        proposed["edges"] = []
    elif change == "conflicting-chapter":
        proposed["nodes"][0]["chapter"] = "03-internals"
    elif change == "reuse-label":
        proposed["nodes"].append({"id": 3, "label": "Expression", "group": "CORE"})
    else:
        proposed["edges"] = []
    with pytest.raises(ReconciliationConflict):
        reconcile(existing, proposed)


def test_cli_refuses_conflict_and_existing_output_without_changing_inputs(tmp_path):
    existing = graph()
    proposed = proposal(existing)
    proposed["nodes"][0]["label"] = "Renamed"
    old = tmp_path / "accepted.json"
    new = tmp_path / "proposed.json"
    output = tmp_path / "candidate.json"
    old.write_text(json.dumps(existing))
    new.write_text(json.dumps(proposed))
    before = old.read_bytes()
    command = [sys.executable, "-m", "ibook_tools", "graph", "reconcile", str(old), str(new), str(output)]
    assert subprocess.run(command, capture_output=True).returncode == 2
    assert not output.exists()
    new.write_text(json.dumps(proposal(existing)))
    command[-1] = str(old)
    assert subprocess.run(command, capture_output=True).returncode == 2
    assert old.read_bytes() == before

"""Reconcile stable concept IDs without erasing editorial enrichments."""
from copy import deepcopy

from .convert import calculate_cis
from .validate import validate_graph


class ReconciliationConflict(ValueError):
    """The proposed change needs explicit editorial resolution."""


def reconcile(existing: dict, proposed: dict) -> dict:
    """Return a separate candidate; never mutate either input or guess identity."""
    validate_graph(existing)
    validate_graph(proposed)
    old_nodes = {node["id"]: node for node in existing["nodes"]}
    new_nodes = {node["id"]: node for node in proposed["nodes"]}
    computed = {"id", "label", "group", "shape", "cis"}
    conflicts = []
    for identifier, old in old_nodes.items():
        new = new_nodes.get(identifier)
        if new is None:
            if set(old) - computed:
                conflicts.append(f"removed enriched concept {identifier}")
            continue
        if old["label"] != new["label"]:
            conflicts.append(f"changed identity at {identifier}: {old['label']!r} -> {new['label']!r}")
        for key in set(old).intersection(new) - computed:
            if old[key] != new[key]:
                conflicts.append(f"conflicting enrichment {identifier}.{key}")
    old_labels = {node["label"] for node in existing["nodes"]}
    for identifier in new_nodes.keys() - old_nodes.keys():
        if new_nodes[identifier]["label"] in old_labels:
            conflicts.append(f"new ID {identifier} reuses an existing concept label")
    old_edges = {(edge["from"], edge["to"]): edge for edge in existing["edges"]}
    new_edges = {(edge["from"], edge["to"]): edge for edge in proposed["edges"]}
    for key, edge in old_edges.items():
        if key not in new_edges and set(edge) - {"from", "to"}:
            conflicts.append(f"removed enriched dependency {key}")
        elif key in new_edges:
            for field in set(edge).intersection(new_edges[key]) - {"from", "to"}:
                if edge[field] != new_edges[key][field]:
                    conflicts.append(f"conflicting dependency enrichment {key}.{field}")
    # Unknown graph-level fields are provenance too, not converter-owned output.
    for field in set(existing).intersection(proposed) - {"nodes", "edges", "groups", "metadata"}:
        if existing[field] != proposed[field]:
            conflicts.append(f"conflicting graph enrichment {field}")
    if conflicts:
        raise ReconciliationConflict("; ".join(conflicts))

    candidate = deepcopy(existing)
    for field, value in proposed.items():
        if field not in {"nodes", "edges", "groups", "metadata"}:
            candidate[field] = deepcopy(value)
    # Existing provenance wins over converter defaults. Editorial metadata changes
    # are reviewed separately, not smuggled in by a mechanical CSV conversion.
    candidate["metadata"] = {**deepcopy(proposed["metadata"]), **candidate["metadata"]}
    for group, value in proposed["groups"].items():
        candidate["groups"][group] = {**deepcopy(value), **candidate["groups"].get(group, {})}
    candidate["nodes"] = []
    scores = calculate_cis(proposed["nodes"], proposed["edges"])
    for new in proposed["nodes"]:
        old = old_nodes.get(new["id"], {})
        node = deepcopy(new)
        node.update({key: deepcopy(value) for key, value in old.items() if key not in computed})
        node["cis"] = scores[node["id"]]
        candidate["nodes"].append(node)
    candidate["edges"] = [
        {**deepcopy(edge), **deepcopy(old_edges.get((edge["from"], edge["to"]), {}))}
        for edge in proposed["edges"]
    ]
    validate_graph(candidate)
    return candidate

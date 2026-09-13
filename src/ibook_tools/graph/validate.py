"""Draft 7 validation and graph-semantic checks."""
import json
from importlib.resources import files

from jsonschema import Draft7Validator

from .convert import calculate_cis


def validate_graph(graph: dict, schema: dict | None = None) -> None:
    """Reject invalid identities, dependencies, groups and cycles before writing."""
    if schema is None:
        schema = json.loads(files("ibook_tools.graph").joinpath("learning-graph-schema.json").read_text())
    Draft7Validator.check_schema(schema)
    errors = sorted(Draft7Validator(schema).iter_errors(graph), key=lambda error: str(error.path))
    if errors:
        raise ValueError("; ".join(f"{list(error.path)}: {error.message}" for error in errors))
    for node in graph["nodes"]:
        if node["group"] not in graph["groups"]:
            raise ValueError(f"Concept {node['id']} references unknown group {node['group']}")
    calculate_cis(graph["nodes"], graph["edges"])

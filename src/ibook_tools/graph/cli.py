"""Graph operations with explicit inputs and separate candidate outputs."""
import argparse
import json
import sys
from pathlib import Path

from .convert import csv_to_json
from .reconcile import reconcile
from .validate import validate_graph


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8")) if path is not None else None


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ibook graph", description=__doc__)
    operations = parser.add_subparsers(dest="operation", required=True)
    for name in ("convert", "taxonomy", "taxonomy-report", "analyze"):
        command = operations.add_parser(name)
        command.add_argument("input", type=Path)
        command.add_argument("output", type=Path)
        if name == "convert":
            command.add_argument("--colors", type=Path)
            command.add_argument("--metadata", type=Path)
            command.add_argument("--taxonomy-names", type=Path)
        elif name == "taxonomy":
            command.add_argument("--config", type=Path, required=True)
        elif name == "taxonomy-report":
            command.add_argument("--taxonomy-names", type=Path)
    command = operations.add_parser("validate")
    command.add_argument("input", type=Path)
    command.add_argument("--schema", type=Path)
    command = operations.add_parser("reconcile")
    command.add_argument("existing", type=Path)
    command.add_argument("proposed", type=Path)
    command.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.operation == "validate":
            validate_graph(_load(args.input), _load(args.schema))
            print(f"Valid graph: {args.input}")
            return 0
        if args.output.exists() or args.output.is_symlink():
            raise ValueError(f"Output already exists: {args.output}; choose a separate candidate path")
        if args.operation == "convert":
            result = csv_to_json(args.input, _load(args.colors), _load(args.metadata), _load(args.taxonomy_names))
            validate_graph(result)
        elif args.operation == "reconcile":
            result = reconcile(_load(args.existing), _load(args.proposed))
        elif args.operation == "taxonomy":
            from .taxonomy import add_taxonomy_to_csv
            add_taxonomy_to_csv(args.input, args.output, _load(args.config))
            return 0
        elif args.operation == "taxonomy-report":
            from .taxonomy_report import analyze_taxonomy_distribution
            analyze_taxonomy_distribution(args.input, args.output, _load(args.taxonomy_names))
            return 0
        else:
            from .analyze import generate_report
            generate_report(args.input, args.output)
            return 0
        # Exclusive creation protects the canonical graph, including hard-link aliases.
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print(f"Candidate graph: {args.output}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

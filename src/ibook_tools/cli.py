"""Explicit, independently installed documentation operations."""
from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ibook", description=__doc__)
    groups = parser.add_subparsers(dest="group", required=True)
    profile = groups.add_parser("profile", help="Validate package profiles", add_help=False)
    profile.add_argument("operation", choices=["validate"])
    groups.add_parser("graph", help="Internal graph operations", add_help=False)
    groups.add_parser("refresh", help="Targeted document refresh", add_help=False)
    args, remaining = parser.parse_known_args(argv)
    if args.group == "profile":
        from .profile.validate import main as validate
        return validate(remaining)
    if args.group == "graph":
        from .graph.cli import main as graph
        return graph(remaining)
    from .refresh.cli import main as refresh
    return refresh(remaining)
from __future__ import annotations

import argparse
import sys

from .engine import ScriptRunner
from .utils import console


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sikulite", description="Image-based desktop automation")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Run a YAML script")
    run_p.add_argument("script", help="Path to YAML script")
    run_p.add_argument("--templates", default="templates", help="Directory with template images")
    run_p.add_argument("--debug", action="store_true", help="Enable debug logs")
    run_p.add_argument("--dry-run", action="store_true", help="Do not send mouse/keyboard events")

    args = parser.parse_args(argv)

    if args.command == "run":
        runner = ScriptRunner(templates_dir=args.templates, debug=args.debug, dry_run=args.dry_run)
        try:
            runner.run_script(args.script)
            return 0
        finally:
            runner.close()
    else:
        parser.print_help()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Query the three-layer license atlas. Zero dependencies.

Examples
    python tools/licctl.py --layer weights --status no
    python tools/licctl.py --no-license
    python tools/licctl.py --copyleft
    python tools/licctl.py --search state
    python tools/licctl.py --json
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSV_PATH = os.path.join(ROOT, "data", "atlas.csv")

LAYER_COL = {
    "code": ("code_license", "commercial_code"),
    "weights": ("weights_license", "commercial_weights"),
    "data": ("data_license", "commercial_weights"),
}


def load():
    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def render(rows, wide=False):
    if not rows:
        print("(no rows matched)")
        return
    for r in rows:
        if wide:
            print("%-28s %-12s code=%-18s weights=%-38s data=%-30s c=%s/%s copyleft=%s"
                  % (r["project"][:27], r["kind"][:11], r["code_license"][:17],
                     r["weights_license"][:37], r["data_license"][:29],
                     r["commercial_code"], r["commercial_weights"], r["copyleft"]))
        else:
            print("%-28s %-9s code=%-18s weights=%-30s commercial=%s/%s"
                  % (r["project"][:27], r["kind"][:8], r["code_license"][:17],
                     r["weights_license"][:29], r["commercial_code"], r["commercial_weights"]))
        print("    ! %s" % r["key_restriction"][:150])
        print("    > %s  (%s, %s)" % (r["evidence_url"][:110], r["method"], r["checked"]))


def main():
    ap = argparse.ArgumentParser(description="Query the vec-license-atlas three-layer license table.")
    ap.add_argument("--layer", choices=sorted(LAYER_COL), help="which layer's commercial status to filter on")
    ap.add_argument("--status", choices=["yes", "no", "unknown", "yes-with-obligations"], help="commercial status to keep")
    ap.add_argument("--no-license", action="store_true", help="projects whose repository has no LICENSE file")
    ap.add_argument("--copyleft", action="store_true", help="copyleft / share-alike projects")
    ap.add_argument("--search", help="substring match on project or restrictions (case-insensitive)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--wide", action="store_true", help="wider table")
    args = ap.parse_args()

    rows = load()
    if args.layer and args.status:
        col = LAYER_COL[args.layer][1]
        rows = [r for r in rows if r[col] == args.status]
    elif args.status and not args.layer:
        rows = [r for r in rows if args.status in (r["commercial_code"], r["commercial_weights"])]
    if args.no_license:
        rows = [r for r in rows if "none-found" in r["code_license"]]
    if args.copyleft:
        rows = [r for r in rows if r["copyleft"] == "yes"]
    if args.search:
        q = args.search.lower()
        rows = [r for r in rows if q in r["project"].lower()
                or q in r["key_restriction"].lower()
                or q in (r["code_license"] + r["weights_license"] + r["data_license"]).lower()]

    if not rows:
        print("(no rows matched)", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    else:
        render(rows, wide=args.wide)
    return 0


if __name__ == "__main__":
    sys.exit(main())

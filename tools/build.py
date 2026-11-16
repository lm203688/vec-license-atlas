#!/usr/bin/env python3
"""Build data/atlas.json from data/atlas.csv and check invariants.

Usage:
    python tools/build.py            # build JSON + run offline checks
    python tools/build.py --check    # offline checks only (no write)
    python tools/build.py --online   # also HEAD every evidence URL (needs network)

Exit code 0 = all checks passed.
"""
import csv
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSV_PATH = os.path.join(ROOT, "data", "atlas.csv")
JSON_PATH = os.path.join(ROOT, "data", "atlas.json")

FIELDS = [
    "project", "kind", "code_license", "weights_license", "data_license",
    "commercial_code", "commercial_weights", "copyleft", "key_restriction",
    "evidence_url", "method", "confidence", "checked",
]
COMMERCIAL = {"yes", "no", "unknown", "yes-with-obligations"}
TRUTHY = {"yes", "no", "unknown"}
SHARE_ALIKE = ("GPL", "NC-SA", "NonCommercial-ShareAlike")
NON_COMMERCIAL = ("non-commercial", "NC-SA", "NonCommercial", "none-found", "CC-BY-NC")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_rows():
    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    missing = [c for c in FIELDS if rows and c not in rows[0]]
    if missing:
        raise SystemExit("atlas.csv is missing columns: %s" % missing)
    return rows


def check(rows):
    errors = []
    seen = set()
    for i, r in enumerate(rows, start=2):
        p = r["project"]
        if not p:
            errors.append("line %d: empty project name" % i)
            continue
        if p in seen:
            errors.append("line %d: duplicate project %r" % (i, p))
        seen.add(p)
        for col in ("commercial_code", "commercial_weights"):
            if r[col] not in COMMERCIAL:
                errors.append("line %d (%s): %s=%r not in %s" % (i, p, col, r[col], sorted(COMMERCIAL)))
        if r["copyleft"] not in TRUTHY:
            errors.append("line %d (%s): copyleft=%r not in %s" % (i, p, r["copyleft"], sorted(TRUTHY)))
        if not r["evidence_url"].startswith("http"):
            errors.append("line %d (%s): evidence_url must be an http(s) URL" % (i, p))
        if not DATE_RE.match(r["checked"]):
            errors.append("line %d (%s): checked=%r is not YYYY-MM-DD" % (i, p, r["checked"]))

        lic = " ".join([r["code_license"], r["weights_license"], r["data_license"]])
        if any(k in lic for k in SHARE_ALIKE) and r["copyleft"] != "yes":
            errors.append("line %d (%s): share-alike/copyleft license but copyleft=no" % (i, p))
        if r["copyleft"] == "yes" and not any(k in lic for k in SHARE_ALIKE):
            errors.append("line %d (%s): copyleft=yes but no copyleft license in any layer" % (i, p))
        if "none-found" in r["code_license"] and r["commercial_code"] == "yes":
            errors.append("line %d (%s): no license file cannot be marked commercial=yes" % (i, p))
        if any(k in r["weights_license"] + r["data_license"] for k in NON_COMMERCIAL):
            if r["commercial_weights"] == "yes":
                errors.append("line %d (%s): non-commercial layer marked commercial_weights=yes" % (i, p))
    return errors


def head_ok(url, timeout=12):
    req = urllib.request.Request(url, method="HEAD")
    req.add_header("User-Agent", "vec-license-atlas/1.0")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return "%d" % resp.status
    except Exception as exc:  # noqa: BLE001 - report, do not raise
        return "ERR %s" % str(exc)[:60]


def main(argv):
    rows = load_rows()
    errs = check(rows)
    if errs:
        print("FAILED %d invariant(s):" % len(errs))
        for e in errs:
            print("  -", e)
        return 1
    print("OK %d rows, invariants passed" % len(rows))

    if "--online" in argv:
        print("\nHEAD each evidence URL:")
        for r in rows:
            print("  %-4s %-45s %s" % (head_ok(r["evidence_url"]), r["project"][:44], r["evidence_url"][:70]))

    if "--check" not in argv:
        payload = {
            "schema": "vec-license-atlas/1",
            "generated_from": "data/atlas.csv",
            "row_count": len(rows),
            "latest_check": max(r["checked"] for r in rows),
            "rows": rows,
        }
        with open(JSON_PATH, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        print("wrote %s (%d rows)" % (os.path.relpath(JSON_PATH, ROOT), len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# -*- coding: utf-8 -*-
"""Table invariants for vec-license-atlas.

Runs under pytest (`pytest tests/`) *or* plain python (`python tests/test_atlas.py`),
because a reader should not need to install anything to verify the table.
"""
import csv
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
CSV_PATH = os.path.join(ROOT, "data", "atlas.csv")
JSON_PATH = os.path.join(ROOT, "data", "atlas.json")


def rows():
    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def test_row_count_and_columns():
    rs = rows()
    assert len(rs) >= 20, "atlas should cover at least 20 projects"
    for col in ("project", "code_license", "weights_license", "data_license",
                "commercial_code", "commercial_weights", "evidence_url", "method", "checked"):
        assert col in rs[0], "missing column %s" % col


def test_project_names_unique():
    names = [r["project"] for r in rows()]
    assert len(names) == len(set(names)), "duplicate project names"


def test_every_row_has_evidence():
    for r in rows():
        assert r["evidence_url"].startswith("http"), r["project"]
        assert r["method"], r["project"]
        assert r["checked"].count("-") == 2, r["project"]


def test_invariants_via_build():
    """The build script's own checks must pass."""
    proc = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build.py"), "--check"],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_json_matches_csv():
    assert os.path.exists(JSON_PATH), "data/atlas.json missing - run tools/build.py"
    with open(JSON_PATH, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    assert payload["row_count"] == len(rows()), "atlas.json is stale - re-run tools/build.py"


def test_known_corrections_present():
    """The three corrections that motivated this atlas must stay in the table."""
    by = {r["project"]: r for r in rows()}
    assert by["scPerturBench"]["code_license"] == "GPL-3.0"
    assert by["CellVQ"]["code_license"] == "none-found"
    assert "BSD-3-Clause" in by["RF3 (foundry)"]["weights_license"]


def test_competition_data_marked_restricted():
    by = {r["project"]: r for r in rows()}
    r = by["Virtual Embryo Challenge data"]
    assert "research-and-education-only" in r["data_license"]
    assert r["commercial_weights"] == "unknown"


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("ok   %s" % name)
            except AssertionError as exc:
                fails += 1
                print("FAIL %s: %s" % (name, exc))
    print("\n%d failure(s)" % fails)
    sys.exit(1 if fails else 0)

#!/usr/bin/env python3
"""
submission_utils.py — submission format for the lesion-segmentation hackathon
============================================================================

Each team submits ONE csv file for the test images:

    case_id,rle
    test_01,1234 5 1490 7 1746 8
    test_02,
    ...

* one row per test image (all of test_01 ... test_10 must be present)
* ``rle`` = run-length encoding of the predicted binary mask (1 = lesion):
  the 256 x 256 mask is flattened row by row (numpy default, C order),
  pixels are numbered from 1, and the string lists "start length" pairs.
  An empty mask is an empty string.

Students:

    from submission_utils import write_submission
    write_submission({"test_01": mask01, "test_02": mask02, ...}, "team_name.csv")

    # check the file before sending it (no ground truth needed):
    python submission_utils.py check team_name.csv --cases cases.csv

Organisers (scoring):

    from submission_utils import read_submission
    preds = read_submission("team_name.csv", shape=(256, 256))   # {case_id: mask}
"""
from __future__ import annotations

import argparse
import csv
import sys

import numpy as np


def rle_encode(mask) -> str:
    """Binary mask -> 'start length start length ...' (1-indexed, row-major)."""
    m = np.asarray(mask).astype(bool).ravel(order="C").astype(np.int8)
    edges = np.flatnonzero(np.diff(np.concatenate([[0], m, [0]]))) + 1
    edges[1::2] -= edges[::2]
    return " ".join(map(str, edges))


def rle_decode(rle: str, shape) -> np.ndarray:
    """'start length ...' -> binary mask (uint8 0/1) of the given shape."""
    out = np.zeros(int(np.prod(shape)), np.uint8)
    vals = (rle or "").split()
    if len(vals) % 2:
        raise ValueError("RLE must contain pairs of numbers")
    for start, length in zip(map(int, vals[0::2]), map(int, vals[1::2])):
        if start < 1 or length < 1 or start - 1 + length > out.size:
            raise ValueError(f"run ({start}, {length}) is outside the image")
        out[start - 1:start - 1 + length] = 1
    return out.reshape(shape)


def write_submission(masks: dict, path: str) -> None:
    """masks: {case_id: 2-D binary array}. Writes the csv to `path`."""
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "rle"])
        for cid in sorted(masks):
            w.writerow([cid, rle_encode(masks[cid])])


def read_submission(path: str, shape=(256, 256)) -> dict:
    """Returns {case_id: mask}. Raises ValueError on a malformed file."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows or set(rows[0].keys()) != {"case_id", "rle"}:
        raise ValueError("header must be exactly: case_id,rle")
    out = {}
    for r in rows:
        cid = r["case_id"].strip()
        if cid in out:
            raise ValueError(f"{cid} appears twice")
        out[cid] = rle_decode(r["rle"], shape)
    return out


def check_submission(path: str, cases_csv: str) -> bool:
    """Format check against students/cases.csv — does not need the ground truth."""
    with open(cases_csv, newline="") as f:
        cases = [r for r in csv.DictReader(f) if r.get("split", "test") == "test"]
    expected = {r["case_id"] for r in cases}
    shape = (int(cases[0]["rows"]), int(cases[0]["cols"]))
    try:
        preds = read_submission(path, shape)
    except ValueError as e:
        print(f"FAIL: {e}")
        return False
    ok = True
    if missing := sorted(expected - preds.keys()):
        print(f"FAIL: missing cases {missing}"); ok = False
    if extra := sorted(preds.keys() - expected):
        print(f"FAIL: unknown case ids {extra}"); ok = False
    for cid in sorted(expected & preds.keys()):
        n = int(preds[cid].sum())
        note = "  <- empty mask" if n == 0 else ("  <- more than half the image?" if n > preds[cid].size / 2 else "")
        print(f"  {cid}: {n:6d} lesion pixels{note}")
    print("OK — ready to submit" if ok else "Please fix the problems above")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Check a hackathon submission file")
    ap.add_argument("command", choices=["check"])
    ap.add_argument("submission")
    ap.add_argument("--cases", default="cases.csv", help="path to students/cases.csv")
    a = ap.parse_args()
    sys.exit(0 if check_submission(a.submission, a.cases) else 1)

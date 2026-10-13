"""
score.py — the scoring used in the hackathon

Students: the starter notebook calls `evaluate(segment, ...)` to score your method
on the development set. It uses the same Dice function the organisers use on the
test set, so your development score is calculated exactly like your final score.

Organisers: score a team's submission against the hidden test masks with
    python score.py teamname.csv path/to/test_masks
(masks named test_01_mask.npy ... test_10_mask.npy)
"""
from __future__ import annotations

import os
import sys

import numpy as np


def dice(pred, gt) -> float:
    """Dice = 2|P∩G| / (|P|+|G|). 1 = perfect overlap, 0 = no overlap."""
    pred, gt = np.asarray(pred) > 0, np.asarray(gt) > 0
    total = pred.sum() + gt.sum()
    return 1.0 if total == 0 else float(2 * (pred & gt).sum() / total)


def check_mask(mask, shape=(256, 256)) -> np.ndarray:
    """Turn a method's output into a 0/1 mask, with a clear error if it is the wrong shape."""
    mask = np.asarray(mask)
    if mask.shape != shape:
        raise ValueError(f"your method returned shape {mask.shape}, expected {shape}")
    return (mask > 0).astype(np.uint8)


def evaluate(method, load_image, load_mask, ids, load_liver=None):
    """Run `method` on every case in `ids`, print the mean Dice and return {case_id: Dice}.

    Without liver masks the method is called as method(image).
    With `load_liver` given, it is called as method(image, liver); liver may be None
    for a case whose liver mask is missing.
    """
    def predict(cid):
        if load_liver is None:
            return method(load_image(cid))
        return method(load_image(cid), load_liver(cid))

    scores = {cid: dice(check_mask(predict(cid)), load_mask(cid)) for cid in ids}
    print(f"{len(ids)} cases   mean Dice {np.mean(list(scores.values())):.3f}")
    return scores


def score_submission(csv_path, mask_dir):
    """Organisers: score a submission CSV against the hidden masks in `mask_dir`."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # find submission_utils.py next to this file
    from submission_utils import read_submission
    preds = read_submission(csv_path, shape=(256, 256))
    ids = sorted(f[:-len("_mask.npy")] for f in os.listdir(mask_dir) if f.endswith("_mask.npy"))
    scores = {}
    for cid in ids:
        gt = np.load(os.path.join(mask_dir, f"{cid}_mask.npy"))
        scores[cid] = dice(preds.get(cid, np.zeros_like(gt)), gt)   # missing case = empty mask
    return scores


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python score.py teamname.csv path/to/test_masks")
    scores = score_submission(sys.argv[1], sys.argv[2])
    print(f"{'case':<10}{'Dice':>8}")
    for cid, d in scores.items():
        print(f"{cid:<10}{d:>8.3f}")
    print(f"{'MEAN':<10}{np.mean(list(scores.values())):>8.3f}")
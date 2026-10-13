# score.py
"""Scores a predictions folder against ground truth.
Students: run on your own predictions only if you were given ground truth (practice set).
Organisers: run on each team's submitted folder with the private ground truth.
Usage : python score.py predictions organiser_only/ground_truth
Needs : pip install numpy scipy
"""
import sys, glob, os
import numpy as np
from scipy.ndimage import distance_transform_edt, binary_erosion
from starter import normalize_intensity

def dice(gt, pr):
    inter = (gt & pr).sum()
    total = gt.sum() + pr.sum()
    return 2 * inter / total if total else 1.0

def hd95(gt, pr):
    """95th percentile boundary distance in pixels. Empty prediction -> image diagonal."""
    if pr.sum() == 0:
        return float(np.hypot(*gt.shape))
    gt_edge = gt & ~binary_erosion(gt)
    pr_edge = pr & ~binary_erosion(pr)
    d_to_gt = distance_transform_edt(~gt_edge)[pr_edge]
    d_to_pr = distance_transform_edt(~pr_edge)[gt_edge]
    return float(np.percentile(np.hstack([d_to_gt, d_to_pr]), 95))

def score_folder(pred_dir, gt_dir):
    rows = []
    for gt_file in sorted(glob.glob(os.path.join(gt_dir, "*.npy"))):
        name = os.path.basename(gt_file)
        pred_file = os.path.join(pred_dir, name)
        gt = np.load(gt_file).astype(bool)
        gt = normalize_intensity(gt)
        pr = np.load(pred_file).astype(bool) if os.path.exists(pred_file) else np.zeros_like(gt)
        if pr.shape != gt.shape:
            raise ValueError(f"{name}: shape {pr.shape} != {gt.shape}")
        rows.append((name, dice(gt, pr), hd95(gt, pr)))
    return rows

if __name__ == "__main__":
    rows = score_folder(sys.argv[1], sys.argv[2])
    print(f"{'patient':<16}{'Dice':>8}{'HD95(px)':>10}")
    for n, d, h in rows:
        print(f"{n[:-4]:<16}{d:>8.3f}{h:>10.1f}")
    print(f"{'MEAN':<16}{np.mean([r[1] for r in rows]):>8.3f}{np.mean([r[2] for r in rows]):>10.1f}")
# Liver Lesion Segmentation Hackathon

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rrr-uom-projects/MPiCRT-hackathon-segmentations/blob/main/starter.ipynb)

Each image is a coronal CT slice with **exactly one lesion** in the liver. Write code that finds and outlines it automatically.

## Quick start

1. Click **Open in Colab** above.
2. **File → Save a copy in Drive**, so your changes aren't lost.
3. Run the cells from top to bottom. You only write code in the `segment()` cell.

## The data

Every image is a 2D coronal CT slice: 256 × 256 pixels, values in Hounsfield units (HU).

| | Development set | Test set |
|---|---|---|
| Images | 84 | 10 |
| CT image (`.npy`, `.png` preview) | ✓ | ✓ |
| Liver mask | ✓ | ✓ |
| Lesion mask (the answer) | ✓ | ✗ hidden |
| Use it to… | build your method and check your score | make your final submission |

The lesions are synthetic: they were added to real CT scans, which is why we know their exact outline.

## What's in this repo

```
├── starter.ipynb          ← start here: setup → load → look → segment → score → submit
├── score.py               ← Dice scoring, the same code used for the official scores
├── submission_utils.py    ← writes and checks your submission file
├── cases.csv              ← list of all cases, image size and pixel spacing
├── sample_submission.csv  ← an (empty) example of the submission format
└── data/
    ├── dev/images/        ← dev_01.npy … dev_84.npy
    ├── dev/lesion_masks/         ← dev_01_mask.npy … (1 = lesion, 0 = background)
    ├── dev/liver_masks/        ← dev_01_liver.npy … (1 = liver, 0 = elsewhere)
    ├── test/images/       ← test_01.npy … test_10.npy (no lesion masks)
    └── test/liver_masks/       ← test_01_liver.npy …
```

You don't need to edit `score.py` or `submission_utils.py`, the notebook calls them for you.

## Your task

Fill in `segment(img, liver)` in the notebook. It gets one CT image and its liver mask, and must return a 256 × 256 array of 0/1 (1 = lesion). The notebook then:

- **scores it on the development set** with Dice;
- **runs it on the test set**, writes your submission file and checks it.

## Scoring

Your masks are compared with the hidden test answers using the **Dice score**: how well your mask overlaps the true lesion (1 = perfect, 0 = no overlap). Your score is the **mean Dice over the 10 test images**.

## How to submit

1. Set your team name in the last section of the notebook and run it. It writes `<team>.csv` and checks it.
2. Wait for **`OK — ready to submit`**. If you see `FAIL`, fix the problem it describes.
3. Send us **your CSV** (File → Download → .ipynb).

- At most **3 submissions per team**. Your best submission counts.

## Rules

**Your solution must be fully automatic.** The same code must produce every mask:

-  no hand-drawn or hand-edited masks
-  no settings picked for specific images or file names



## Credits

The CT images come from the **TotalSegmentator dataset** (CC BY 4.0):
Wasserthal J. *et al.* TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. *Radiology: Artificial Intelligence* 2023;5(5):e230024. https://doi.org/10.1148/ryai.230024

The lesions were added synthetically by the hackathon team, so they are not real patient findings.
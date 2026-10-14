# Liver Lesion Segmentation Hackathon

Each image is a coronal CT slice of the abdomen with **exactly one lesion** in the liver. Write code that finds and outlines it automatically.

**Slides from the session:** [PowerPoint](hackathonSlides.pptx). They explain the data, the task, Dice scoring and how to submit.

## Getting started (on your own laptop)

1. **Install Python 3 and VS Code**, with the *Python* and *Jupyter* extensions (or use Jupyter Notebook).
2. **Download this repository**: click the green **Code** button above → **Download ZIP**, then unzip it.
   (Or, if you use git: `git clone https://github.com/rrr-uom-projects/MPiCRT-hackathon-segmentations.git`)
3. **Install the packages** in a terminal:
   ```
   pip install numpy pandas matplotlib scipy ipykernel
   ```
4. **Open the unzipped folder in VS Code** (File → Open Folder), open the unzipped folder, then open `starter.ipynb`, choose your Python environment when asked, then **Run All**.
   The first cell should print: `84 development images, 10 test images`.

Your method goes in `segment()`. Add as many helper functions and exploration cells as you like, as long as `segment()` calls your helpers. Loading the data, scoring and making the submission file are done for you.

### Plan B: Google Colab (only if the steps above don't work)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rrr-uom-projects/MPiCRT-hackathon-segmentations/blob/main/starter.ipynb)

1. Click **Open in Colab** above (you need a Google account; a personal one is fine).
2. **File → Save a copy in Drive**, so your changes aren't lost.
3. Run the first cell: it downloads the data for you. Then carry on as above.

Colab deletes files when it disconnects, so download your submission CSV as soon as it's made.

## The data

Every image is a 2D coronal CT slice: 256 × 256 pixels, 1.5 mm per pixel, values in **Hounsfield units (HU)**, roughly −1000 to +3000.

There are **two datasets**:

| | Development set | Test set |
|---|---|---|
| Patients | 84 | 10 |
| CT image | ✓ | ✓ |
| Liver mask (optional) | ✓ | ✓ |
| Lesion mask (the answer) | ✓ | ✗ hidden |
| Use it to… | build your method and check your Dice score as often as you like | run your finished method once: **your score comes only from this set** |


## What's in this repo

```
├── starter.ipynb          ← start here: setup → load → look → segment → score → submit
├── score.py               ← Dice scoring, the same code used for the official scores. You do not need to change anything here.
├── submission_utils.py    ← writes and checks your submission file. You do not need to change anything here.
├── cases.csv              ← list of all cases, image size and pixel spacing
└── data/
    ├── dev/images/        ← dev_01.npy … dev_84.npy
    ├── dev/lesion_masks/  ← dev_01_mask.npy … (1 = lesion, 0 = background)
    ├── dev/liver_masks/   ← dev_01_liver.npy … (1 = liver, 0 = elsewhere)
    ├── test/images/       ← test_01.npy … test_10.npy (no lesion masks)
    └── test/liver_masks/  ← test_01_liver.npy …
```

You don't need to edit `score.py` or `submission_utils.py`: the notebook calls them for you.

## Your task

Fill in `segment(img, liver)` in the notebook. It gets one CT image (and, optionally, its liver mask) and must return a 256 × 256 array of 0s and 1s (1 = lesion). The notebook then:

- **scores it on the development set** with Dice, so you can see how well it works;
- **runs it on the test set**, writes your submission file and checks it.

## Scoring

Your masks are compared with the hidden test answers using the **Dice score**: how well your mask overlaps the true lesion (1 = perfect, 0 = no overlap). Your score is the **mean Dice over the 10 test images**.

The lesions are small (about 1 to 3 cm), so a few pixels make a big difference. An empty mask scores 0.

## How to submit

1. Put your team name in the last cell of the notebook and run it. It runs `segment()` on the 10 test images, writes `<team>.csv` and checks it.
2. Wait for **`OK — ready to submit`**. If you see `FAIL`, read the message and fix the problem.
3. Email **two files** to **<artemis.bouzaki@postgrad.manchester.ac.uk>**, with the subject `Hackathon submission – <team name> – 1` (then 2, 3):
   - your `<team>.csv`
   - your notebook (`starter.ipynb`; in Colab: File → Download → Download .ipynb)

- At most **3 submissions per team**. We reply with your mean Dice. **Your best submission counts.**
- Use the development set to compare ideas; don't spend your submissions experimenting.

## Rules

**Your solution must be fully automatic.** The same code must produce every mask:

- ✗ no hand-drawn or hand-edited masks
- ✗ no settings picked for specific images or file names

## Credits

The CT images come from the **TotalSegmentator dataset** (CC BY 4.0):
Wasserthal J. *et al.* TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. *Radiology: Artificial Intelligence* 2023;5(5):e230024. https://doi.org/10.1148/ryai.230024

The lesions were added synthetically by the hackathon team, so they are not real patient findings.
# Vehicle Body Type Classification Across Viewing Angles

**DS 4002 — Project 3**  
**Team:** The Pink Panthers  
**Members:** Shawn Chen, Zichen Luo  
**Group leader:** Shawn Chen

## Contents of This Repository

This project examines how photo viewing angle affects a model's ability to distinguish sedans, SUVs, and pickup trucks using DVM-CAR images [1], [2].

**Research question:** What effect does the angle of a photo have on how accurately a model can distinguish sedans, SUVs, and pickup trucks?

**Goal:** Build an image classifier that exceeds **33.3% balanced accuracy for each viewpoint** (front, side, and rear) on vehicle models excluded from training. Computations compare performance with exactly 1/3. Balanced accuracy gives each body class equal weight.

**Current status:** MI2 exploratory figures and tables are included. The new metadata-cleaning stage has been run and checked against the actual source CSVs. The Colab workflow for image checking, human review, and model-disjoint splitting is ready. Full image review, final cleaned manifests, training, and test results are **pending**. The original 90-photo audit is preliminary and contains no machine-readable approvals; it is not a fully cleaned dataset.

We follow the folder organization used in the group's [Project 1](https://github.com/camjanada/DS-4002-Projects) and [Project 2](https://github.com/camjanada/DS-4002-Project-2) repositories. All files and instructions here refer to Project 3.

## Section 1: Software and Platform

Run the cleaning notebook using **Python 3 in Google Colab on Linux**, with a CPU runtime and Google Drive for persistent inputs and decisions. The source archive may be uploaded to Drive from macOS or Windows. A GPU is only needed later for model training.

| Package | Purpose |
|---|---|
| pandas | Metadata joins, review records, and manifests |
| numpy | Numerical utilities |
| Pillow | Decode images, check dimensions, hash normalized RGB pixels |
| matplotlib | Exploratory figures |
| ipywidgets | Colab visual review interface |
| google.colab | Drive mounting and widget support; supplied by Colab |

Install cleaning packages using the first notebook cell or `pip install -r requirements.txt`. Supported version ranges are in `requirements.txt`. The notebook saves actual package versions to `OUTPUT/cleaning_environment.json` in its Drive working folder. PyTorch and torchvision will be needed for Zichen's model notebook; its versions and exact instructions will be recorded when added. The cleaning notebook does not train a model.

## Section 2: Map of Documentation

| Location | Contents |
|---|---|
| `README.md` | Project orientation, software, file map, and reproduction steps |
| `LICENSE.md` | MIT license for original project code |
| `.gitignore` | Excludes source archives, image caches, credentials, and model weights |
| `requirements.txt` | Cleaning/review package requirements |
| `SCRIPTS/01_data_cleaning.ipynb` | Self-contained Colab metadata cleaning, image review, finalization, and export |
| `SCRIPTS/extract_review_images.py` | Optional standard-library Mac helper: copy only queued files into a reduced image ZIP |
| `SCRIPTS/data_pipeline.py` | Shared implementation embedded in the cleaning notebook |
| `SCRIPTS/02_verify_handoff.ipynb` | Zichen's checks of the exported images and fixed manifests |
| `SCRIPTS/README.md` | Execution order and notebook maintenance notes |
| `SCRIPTS/tests/test_data_pipeline.py` | Tests of pending-review blocking, triplets, duplicates, and grouped splitting |
| `DATA/README.md` | Source provenance, licensing, dictionary, ethics, and exploratory findings |
| `DATA/DOWNLOAD_DATA.md` | Single source of acquisition instructions for raw and final data |
| `DATA/initial/viewpoint_audit_sample.csv` | Original 90-photo audit selection; review fields are blank |
| `DATA/initial/audit_notes.md` | Qualitative issues observed in the earlier audit |
| `DATA/processed/README.md` | Expected final manifest schemas; no final sample claimed yet |
| `OUTPUT/README.md` | Distinguishes historical EDA, automated cleaning results, and pending model results |
| `OUTPUT/eda/` | The original MI2 PNGs and small CSV summaries, preserved unchanged |
| `OUTPUT/metadata_cleaning/` | New automated metadata counts, missingness, candidate figures, and run configuration |
| `REFERENCES/README.md` | IEEE references |

The raw CSVs and 13.6 GiB image archive are obtained using `DATA/DOWNLOAD_DATA.md`; they are excluded from Git. Final image archives also belong in shared storage rather than Git. Final CSV manifests and the stable archive link/checksum must be added after visual review.

## Section 3: Instructions for Reproducing Results

### Step 1: Obtain the raw data

Follow [DATA/DOWNLOAD_DATA.md](DATA/DOWNLOAD_DATA.md). Use **one** advertisement file, `Ad_table (extra).csv`, plus `Image_table.csv` and `resized_DVM_v2.zip`. The standard ad table is an alternative source, not an additional table to concatenate. To reproduce our counts, use the extra file used in MI2.

Upload only the **two CSVs** into `MyDrive/DS4002_Project3/input/` in Google Drive first. Keep the large source ZIP on your Mac. After Cell 4 creates `review_queue.csv`, download that CSV and `SCRIPTS/extract_review_images.py` into Downloads. Run `python3 ~/Downloads/extract_review_images.py` in Terminal. It copies only queued photos from `~/Downloads/resized_DVM_v2.zip` into a smaller `review_images.zip`. Upload the smaller ZIP to the Drive input folder before Cell 5. This is a byte-copy staging step; validation and review remain in Colab.

If the full archive is already on Drive, skip the helper and set the notebook's `IMAGE_ZIP` path to it. Do not extract the whole dataset or send the large ZIP through Colab's small-file upload dialog.

### Step 2: Open the cleaning notebook

Open [SCRIPTS/01_data_cleaning.ipynb](SCRIPTS/01_data_cleaning.ipynb) in Colab. If the private repo is inaccessible from Colab, download the notebook using GitHub's **Download raw file**, then open it through Colab's **Upload** tab. Save a working copy to Drive. The notebook embeds the implementation and requires no access token.

Use a CPU runtime. Run Cells 1–2 to install dependencies, mount Drive, and check the input paths. Default settings are seed `4002`, up to **10 listings per body type/generic model**, and up to **three alternatives per view**. These are explicit workload settings, not a claim that all eligible source images will be reviewed. Set the listing cap to `0` to review every eligible listing. Freeze sampling choices before modeling.

### Step 3: Clean metadata and check queued images

Run the shared implementation cell, then Cells 4–5. The pipeline strips header/value whitespace; preserves IDs as text; removes exact repeated rows; excludes ambiguous IDs, invalid filename/ID matches, source failure flag `N`, non-target bodies, and non-cardinal predicted angles; and joins on both `Adv_ID` and `Genmodel_ID`.

It retains listings with at least one candidate for each view, then selects the review sample deterministically. It extracts only queued image files, checks that they decode at 300 × 300 pixels, and records SHA-256 hashes of normalized RGB pixels. Missing, unreadable, and ambiguous files cannot be approved.

The new metadata stage yielded **10,565 sedan listings (118 models), 28,127 SUV listings (144 models), and 575 pickup listings (13 models)** before file and visual checks. These differ from MI2's earlier 10,765 / 28,667 / 580 because explicit source-failed images and ambiguous records are now excluded. Do not use either set of counts as final cleaned sample sizes.

### Step 4: Complete visual review

Use Cell 6 to review each selected listing. Approve exactly one complete, correct body-type, correct-view photo per angle. All three must show the same actual vehicle. Reject ambiguous diagonal views, close-ups, fragments, incorrect cars, and images with an open hood/trunk. Reject unused alternatives with a reason. **Save before Next.** Decisions are saved in Drive; rerunning the interface resumes progress.

If a listing lacks a usable view, reject its alternatives and let finalization exclude the listing. Increase the number of alternatives and rerun preparation/extraction if more replacements are needed. Cell 7 reports outstanding reviews. The finalization cell intentionally stops while any readable queued photo has no decision.

### Step 5: Finalize and hand off to Zichen

Run Cell 8 after review. It keeps approved triplets, excludes all listings affected by exact duplicate pixels, then assigns complete `Genmodel_ID` groups approximately 70/15/15 to training/validation/test, stratified by each model's primary retained body type. A model spanning body types still receives one split. The workflow stops if a class lacks sufficient model groups or a split lacks a class.

Outputs are written under `MyDrive/DS4002_Project3/cleaning/`:

- `DATA/processed/clean_manifest.csv`, `train_manifest.csv`, `validation_manifest.csv`, `test_manifest.csv`, and `model_split_assignments.csv`
- `DATA/review_decisions.csv`, `technical_checks.csv`, and `excluded_listings.csv`
- `OUTPUT/clean_split_summary.csv` and `handoff_summary.json`
- `zichen_training_data.zip`, containing the final manifests, approved photos, audit logs, and data attribution

Run Cell 9 to create `cleaning_documentation.zip` separately. Use it to update this repo's final CSVs and counts. Share the image bundle with Zichen through Drive and record its stable link and checksum in `DATA/DOWNLOAD_DATA.md`. Do not upload the image archive to GitHub.

### Step 6: Verify the handoff and perform modeling

Zichen runs [SCRIPTS/02_verify_handoff.ipynb](SCRIPTS/02_verify_handoff.ipynb). It checks files, hashes, matched triplets, class coverage, and model isolation. Zichen then adds the completed training/evaluation notebook.

The planned model is an ImageNet-pretrained ResNet-18 [3], fine-tuned on combined views. Use training-only augmentation and class weights if needed; use validation macro F1 for tuning and early stopping. Preserve the fixed split. Test after model choices are frozen, using the same held-out listings at each angle. Report balanced accuracy, macro F1, macro precision, per-class recall, and normalized confusion matrices. Compare each view's balanced accuracy with 1/3. Model results and full training reproduction instructions are pending.

### Local verification of the cleaning implementation

From the repository root with the requirements installed, run:

```bash
python -m unittest discover -s SCRIPTS/tests -v
```

## Work Assignment

| Member | Responsibility |
|---|---|
| Shawn Chen | Metadata cleaning, visual review, exclusion records, EDA, final manifests, grouped splits, repository documentation |
| Zichen Luo | Handoff verification, ResNet-18 training, validation, held-out evaluation, figures and interpretation |
| Both | Check final sample limitations and prepare the presentation |

## Limitations

The data represent UK used-car listings and standardized, background-removed images. Predicted angles are categories, not measured camera orientations. Review reduces but cannot eliminate labeling errors. Exact pixel hashing does not detect every near duplicate or repeated real-world vehicle. Pickup models are few, making results sensitive to the held-out models. The view comparison is observational and does not establish a causal effect of camera angle.

## References

[1] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, “DVM-CAR: A large-scale automotive dataset for visual marketing research and applications,” in *Proc. IEEE Int. Conf. Big Data*, 2022, pp. 4130–4137.

[2] J. Huang et al., “User manual of DVM-CAR.” [Online]. Available: https://deepvisualmarketing.github.io/site-assets/DVM_user_manual.pdf. Accessed: Nov. 14, 2026.

[3] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit.*, 2016, pp. 770–778.

Additional license and source links are in [REFERENCES/README.md](REFERENCES/README.md).

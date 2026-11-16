# Vehicle Body-Type Classification Across Viewing Angles

**DS 4002 — Data Science Project — Project 3**  
**University of Virginia | Fall 2026 | Section 100010**  
**Team:** The Pink Panthers  
**Members:** Shawn Chen and Zichen Luo  
**Group Leader:** Shawn Chen  
**Professor:** Peter Alonzi  
**Teaching Assistant:** Naman Patel  

## Contents of This Repository

This repository contains the data and code for investigating how viewing
angle affects classification of sedans, SUVs, and pickup trucks using
DVM-CAR images.

**Research question:** What effect does the angle of a photo have on how
accurately a model can distinguish sedans, SUVs, and pickup trucks?

**Performance goal:** Exceed the 33.3% three-class chance baseline in
balanced accuracy for each of the three viewpoints—front, side, and
rear—on vehicle models excluded from training.

Vehicle body-type classification can support automotive inventory
management and online marketplaces. However, the features visible in a
vehicle photograph change with camera angle. Side views reveal the
vehicle's silhouette and cargo-bed shape, while front and rear views
provide different cues. Reporting performance separately by viewpoint
helps identify differences that an overall accuracy score could hide.

Following MI2, the comparison uses matched views: each retained listing
contributes one front, one side, and one rear image. Splitting by vehicle
model keeps related images together and evaluates generalization to
models not seen during training.

**Current status:** Data cleaning, image verification, and fixed
training/validation/test splits are complete. Model training, tuning,
and final evaluation are pending. No classification results or claims
of achieving the performance goal are reported yet.

### Dataset and preparation

The project uses DVM-CAR, which provides vehicle images and associated
advertisement and image metadata [1]. During data establishment, the
advertisement and image tables were linked using listing identifiers.
The target body types were standardized to Sedan, SUV, and Pickup.

The MI2 audit of 90 sampled images identified incorrect viewpoint labels,
incomplete vehicle images, and different vehicles appearing within the
same listing. These findings motivated visual review and the requirement
for three usable exterior views of the same vehicle per retained listing.

The cleaning notebook starts from a prepared candidate archive containing
4,500 images from 1,500 listings and a separate archive of recorded review
decisions. It produces 2,580 cleaned images from 860 listings.

| Split | Listings | Images | Distinct vehicle models |
| --- | ---: | ---: | ---: |
| Training | 595 | 1,785 | 168 |
| Validation | 131 | 393 | 37 |
| Test | 134 | 402 | 36 |
| Total | 860 | 2,580 | 241 |

Every retained listing has one Front, one Side, and one Rear image.
Partitions are grouped by `Genmodel_ID`, with no vehicle-model overlap
between training, validation, and test sets.

The target proportions are 70% training, 15% validation, and 15% test.
Actual proportions differ slightly because model groups remain intact.

### Planned modeling and evaluation

Following the MI1 and MI2 plan, we will fine-tune an ImageNet-pretrained
ResNet-18 classifier with a three-class output layer [2]. One classifier
will be trained using all three viewpoints.

The planned workflow is to:

- Resize images to 224 × 224 pixels and normalize them using ImageNet
  statistics.
- Apply label-preserving augmentation to training images only.
- Use class-weighted cross-entropy to address body-type imbalance.
- Select training settings using the fixed validation partition, with
  early stopping based on validation macro F1.
- Reserve the test partition for final evaluation after model selection.
- Compare front, side, and rear performance on the same held-out listings.

Balanced accuracy is the primary metric because it gives equal weight
to recall for Sedan, SUV, and Pickup. Planned supporting measures are
macro precision, macro F1, per-class recall, and normalized confusion
matrices for each viewpoint. Differences between viewpoints will be
reported in percentage points.

These are planned methods. Final model settings, dependencies, execution
instructions, and results will be documented when the modeling code is added.

### Responsibilities

| Member | Responsibility |
| --- | --- |
| Shawn Chen | Data preparation, visual review, cleaning, model-group splits, and data documentation |
| Zichen Luo | Model development, validation, viewpoint-specific evaluation, and interpretation |

## Section 1: Software and Platform

### Software and platform

The cleaning workflow uses Python 3 in Google Colab on a Linux runtime.

The notebook depends on Colab's interactive upload/download functions
and `/content` paths. Running it locally requires adapting those
functions and paths.

### Packages

| Package | Recorded version | Purpose |
| --- | --- | --- |
| pandas | 2.2.3 | Read manifests, apply review decisions, organize records, and export CSV files |
| NumPy | 2.4.6 | Generate and assess model-group split allocations |
| Pillow | Not recorded | Decode images, verify dimensions, and inspect RGB pixel data |

The pandas and NumPy versions are recorded in
`DATA/split_config.json`. Use those versions when reproducing the saved
split allocation. Python and Pillow versions were not recorded by the
current notebook.

The notebook also uses:

- `google.colab.files` for interactive uploads and downloads
- Python standard-library modules: `pathlib`, `zipfile`, `hashlib`,
  `io`, `unicodedata`, `re`, and `json`

If required, run the following in a separate Colab setup cell before
executing the notebook:

```python
%pip install pandas==2.2.3 numpy==2.4.6 Pillow
```

Restart the runtime if prompted after installation.

Model-training dependencies and versions will be added with the
modeling notebook.

## Section 2: Map of Documentation

The repository is organized as follows. Placeholder `.gitkeep` files
are omitted from this outline.

- `README.md` — project overview and reproduction instructions
- `LICENSE.md` — license for original project code and documentation
- `SCRIPTS/`
  - `Data_Cleaning.ipynb` — cleaning, image verification,
    split generation, and dataset export
- `DATA/`
  - `README.md` — dataset documentation, download instructions, and
    data dictionary
  - `DATA_LICENSE.txt` — dataset attribution and licensing information
  - `clean_manifest.csv` — cleaned image records before split assignment
  - `listing_review.csv` — recorded listing review decisions
  - `manifest_with_splits.csv` — cleaned image records with split assignments
  - `model_split_assignments.csv` — model-level split assignments
  - `train_manifest.csv` — training image records
  - `validation_manifest.csv` — validation image records
  - `test_manifest.csv` — test image records
  - `split_config.json` — split parameters and recorded package versions
  - `split_summary.csv` — counts by split and body type
- `OUTPUT/` — reserved for generated figures, tables, and model results
- `REFERENCES/`
  - `README.md` — dataset and supporting references

### Downloadable data archives

The image archives are attached to the
[MI3 dataset release](https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0).

| Release attachment | Role |
| --- | --- |
| `DVM_Project3_Review_20261114_201843_029683.zip` | Cleaning input: candidate images, `selection_manifest.csv`, and source license information |
| `DVM_Review_Records.zip` | Cleaning input: review archive containing `listing_review.csv` |
| `DVM_Cleaned_Data.zip` | Cleaning output: verified images, cleaned manifests, fixed splits, configuration, and license information |

Download these named attachments under **Assets**, rather than GitHub's
automatically generated **Source code** archives.

Cloning or downloading the repository does not download the release
attachments.

### Data connections

The current cleaning workflow uses CSV manifests and JSON configuration.
No Excel workbook is required.

- `Adv_ID` links image records to listing review decisions.
- `Genmodel_ID` links images to vehicle-model split assignments.
- `Extracted_path` links each cleaned record to its image relative to
  the extracted dataset folder.
- `manifest_with_splits.csv` adds split assignments to the cleaned records.
- The train, validation, and test manifests contain the respective subsets.

Numeric class labels are **Sedan = 0, SUV = 1, and Pickup = 2**.

See [DATA/README.md](DATA/README.md) for the data dictionary.

## Section 3: Instructions for Reproducing Results

### A. Use the prepared dataset

To begin modeling without rerunning cleaning:

1. Open the
   [dataset release](https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0).
2. Download `DVM_Cleaned_Data.zip`.
3. Extract the complete archive into a dataset folder.
4. Keep `Photos/` alongside the extracted CSV, JSON, and license files.
5. Use `train_manifest.csv`, `validation_manifest.csv`, and
   `test_manifest.csv` as provided. Do not randomly split the images again.
6. Resolve each record's `Extracted_path` relative to the extracted
   dataset folder. These paths begin with `Photos/`.

The existing manifests preserve both complete three-view listings and
vehicle-model separation.

### B. Reproduce cleaning and split generation

1. Download these two input archives from the release:
   - `DVM_Project3_Review_20261114_201843_029683.zip`
   - `DVM_Review_Records.zip`
2. Open `SCRIPTS/DS4002_Project_3_Data_Cleaning.ipynb` in Google Colab.
3. Start a fresh runtime and ensure the dependencies in Section 1
   are available.
4. Run the notebook's nine cells in order.
5. At the first upload prompt in cell 2, upload only
   `DVM_Project3_Review_20261114_201843_029683.zip`.
6. Cell 3 reads `selection_manifest.csv` and reports the candidate counts.
7. At the second upload prompt in cell 4, upload only
   `DVM_Review_Records.zip`.
8. Continue through the remaining cells to apply review decisions,
   verify and export images, assign splits, and save the manifests.
9. The final cell creates and downloads `DVM_Cleaned_Data.zip`.

Do not upload the cleaned output ZIP at either input prompt. Its
contents differ from the input archives expected by the notebook.

The notebook reproduces cleaning from the prepared candidate archive
and saved human review decisions. It does not reproduce the earlier
raw-metadata selection process or conduct human visual review automatically.

### C. Understand the cleaning checks

The notebook retains listings with `Review_decision` equal to
`provisional_keep`. Other review decisions are excluded.

It then checks:

- Unique image identifiers and file hashes
- Consistent vehicle model and body type within each listing
- Exactly three images per listing: Front, Side, and Rear
- Agreement between viewpoint metadata and view labels
- No retained image explicitly marked `N` in `Quality_check`
- Matching SHA-256 hashes between source files and manifest records
- Successful image decoding and dimensions of 300 × 300 pixels
- No duplicate decoded RGB pixel hashes
- No unexpected files in the exported image folder

Missing CSV values are initially represented as empty strings. This is
not statistical imputation, and a missing quality flag is not evidence
that an image is usable. The workflow relies on the saved review decisions
and explicit integrity checks.

Failed assertions stop execution rather than silently dropping
additional records.

### D. Understand and verify the splits

The split procedure groups images by `Genmodel_ID`, uses random seed
`4002`, and evaluates `5,000` candidate allocations.

It selects an allocation that minimizes deviation from class-level
listing targets. Model performance is not used to choose the splits.

The notebook checks that:

- Each model belongs to only one split.
- Each listing belongs to only one split.
- Identical file hashes do not cross split boundaries.
- Every split includes Sedan, SUV, and Pickup.

Expected outputs are:

| Check | Expected value |
| --- | ---: |
| Cleaned listings | 860 |
| Cleaned images | 2,580 |
| Images per listing | 3 |
| Training images | 1,785 |
| Validation images | 393 |
| Test images | 402 |
| Vehicle-model overlap between splits | 0 |

Cell 8 should report:
`Passed: complete triplets and no model overlap.`

### E. Locate the generated files

The notebook writes cleaned images and accompanying data files to:

`/content/DVM_Cleaned_Data/`

It writes the final archive to:

`/content/DVM_Cleaned_Data.zip`

The notebook does not automatically write into a cloned repository's
`DATA/` or `OUTPUT/` folders.

For this repository, the exported CSV and JSON files were copied into
`DATA/`, and the complete image archive was attached to the release.
The dataset license file is also included in `DATA/`.

Download generated files before ending the Colab session because runtime
storage is temporary.

### F. Model training and final evaluation — pending

The current cleaning notebook does not train a classifier or generate
classification metrics and confusion matrices.

When the modeling work is added, this section will document:

- The modeling notebook filename and execution order
- Required packages, versions, and hardware
- Dataset loading and preprocessing
- Training settings and validation-based checkpoint selection
- Commands or cells that generate each figure and table
- Exact output locations
- Expected final metrics and the comparison with the 33.3% baseline

Model outputs and figures will be stored in `OUTPUT/`, and the
documentation map will be updated to list the actual files.

### Limitations and interpretation

- The source viewpoint labels are predictions rather than measured
  camera angles. Human review reduces, but cannot guarantee elimination
  of, viewpoint and identity errors.
- The cleaned sample contains unequal numbers of the three body types,
  making class-level reporting important.
- The test split contains 60 pickup images from 20 listings but only
  one pickup vehicle model. Pickup performance therefore provides limited
  evidence about generalization across different pickup models.
- Images come from UK vehicle listings and have undergone background
  removal and resizing. Findings may not generalize to other markets or
  natural photographs taken in traffic or parking lots.
- Model-level separation prevents overlap within this project's
  partitions; it does not establish the composition of the external
  pretraining dataset.
- No claim about which viewpoint performs best can be made until the
  planned evaluation is complete.

### Licensing and processing notes

[LICENSE.md](LICENSE.md) covers original project code and documentation.
It does not relicense DVM-CAR images or other third-party materials.

See [DATA/DATA_LICENSE.txt](DATA/DATA_LICENSE.txt) for dataset attribution
and licensing information.

The release archives retain the original processing note from the
candidate-data stage. The repository copy of `DATA_LICENSE.txt` clarifies
that the cleaned dataset has undergone recorded human review and
automated image checks. This wording update does not change the dataset
license.

### References

[1] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, “DVM-CAR.”
[Online]. Available: https://deepvisualmarketing.github.io/

[2] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for
image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit.,
2016, pp. 770–778.

Additional project references are maintained in
[REFERENCES/README.md](REFERENCES/README.md).

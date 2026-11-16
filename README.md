# Vehicle Body-Type Classification Across Viewing Angles

**DS 4002 — Data Science Project — Project 3**  
**University of Virginia | Fall 2026 | Section 100010**  
**Team:** The Pink Panthers  
**Members:** Shawn Chen and Zichen Luo  
**Group Leader:** Shawn Chen  
**Professor:** Peter Alonzi  
**Teaching Assistant:** Naman Patel  

## Contents of This Repository

This repository contains the metadata preparation, image cleaning,
data exploration, and documentation for classifying sedans, SUVs,
and pickup trucks across front, side, and rear views.

**Research question:** What effect does the angle of a photo have on how
accurately a model can distinguish sedans, SUVs, and pickup trucks?

**Performance goal:** Exceed 33.3% balanced accuracy for each viewpoint
on vehicle models excluded from training.

Vehicle photographs reveal different features depending on camera angle.
Side views show silhouette and cargo-bed shape, while front and rear
views provide different cues. Comparing performance by viewpoint can
identify differences hidden by an overall accuracy score.

Following MI2, each retained listing contributes one front, one side,
and one rear image. Vehicle models are kept in separate training,
validation, and test partitions.

**Current status:** Metadata preparation, recorded visual-review
decisions, image cleaning, fixed splits, and explanatory plots are
available. Model training and evaluation are pending. The code that
originally assembled the 4,500-image review archive is not yet included;
that archive is supplied as an input to the cleaning notebook.

### Data stages

| Stage | Contents |
| --- | --- |
| Source metadata | Ad_table (extra).csv and Image_table.csv from DVM-CAR |
| MI2 candidate pool | 10,765 sedan, 28,667 SUV, and 580 pickup listings with all three predicted views |
| MI2 audit template | 90 candidate images, with blank fields for recording visual-review findings |
| Prepared review archive | 4,500 images from 1,500 listings, provided as a release attachment |
| Final cleaned sample | 2,580 images from 860 listings with recorded review decisions and fixed splits |

The MI2 candidate counts precede final visual cleaning. They should not
be confused with the final dataset used for modeling.

The MI2 visual audit identified incorrect viewpoints, incomplete vehicle
images, and inconsistent vehicle identity within listings. These findings
motivated the matched three-view cleaning criteria.

### Final dataset

| Split | Listings | Images | Distinct vehicle models |
| --- | ---: | ---: | ---: |
| Training | 595 | 1,785 | 168 |
| Validation | 131 | 393 | 37 |
| Test | 134 | 402 | 36 |
| Total | 860 | 2,580 | 241 |

The sample contains 395 sedan, 371 SUV, and 94 pickup listings.
Each listing contributes Front, Side, and Rear images.

Splits are grouped by Genmodel_ID. Target proportions are 70% training,
15% validation, and 15% test; actual proportions differ slightly because
model groups remain intact.

### Planned modeling and evaluation

Following MI1 and MI2, we plan to fine-tune an ImageNet-pretrained
ResNet-18 with a three-class output layer [2].

The planned workflow uses:

- Images from all three viewpoints to train one classifier
- Resizing to 224 × 224 pixels and ImageNet normalization
- Training-only image augmentation
- Class-weighted cross-entropy
- Validation-based tuning and early stopping using macro F1
- Final testing on held-out vehicle models

Balanced accuracy is the primary metric. Supporting measures will include
macro precision, macro F1, per-class recall, and normalized confusion
matrices for each viewpoint.

Each viewpoint will be evaluated on the same held-out listings.
Final implementation details and results will be documented when the
modeling code is added.

### Responsibilities

| Member | Responsibility |
| --- | --- |
| Shawn Chen | Metadata preparation, image review, cleaning, splits, exploration, and data documentation |
| Zichen Luo | Model development, validation, evaluation, and interpretation |

## Section 1: Software and Platform

The notebooks use Python 3 in Google Colab on a Linux runtime.

They use interactive uploads and downloads. Local execution requires
adapting the Colab-specific functions and file paths.

| Package | Purpose | Version information |
| --- | --- | --- |
| pandas | Read, join, filter, summarize, and export metadata | Cleaning: 2.2.3 |
| NumPy | Numerical operations and model-group split allocation | Cleaning: 2.4.6 |
| Pillow | Decode images, inspect dimensions, and calculate RGB hashes | Cleaning version not recorded |
| matplotlib | Generate metadata and cleaned-data plots | Cleaned-data exploration: 3.10.0 |

Cleaning versions are recorded in DATA/split_config.json.
Cleaned-data exploration used pandas 2.2.3 and matplotlib 3.10.0,
as recorded in OUTPUT/exploration_package_versions.txt.
The metadata-preparation notebook does not separately record its
package versions.

The notebooks also use google.colab.files and Python standard-library
modules for paths, ZIP archives, hashes, text handling, and JSON.

If needed, install packages in a separate Colab setup cell:

```python
%pip install pandas numpy Pillow matplotlib
```

For closer reproduction of the cleaning splits, use the recorded
pandas and NumPy versions:

```python
%pip install pandas==2.2.3 numpy==2.4.6 Pillow
```

Restart the runtime if prompted after installation.
Model dependencies and hardware requirements will be added with the
modeling notebook.

## Section 2: Map of Documentation

Placeholder .gitkeep files are omitted.

- README.md
- LICENSE.md
- SCRIPTS/
  - Metadata_Prep.ipynb
  - Data_Cleaning.ipynb
  - Data_Exploration.ipynb
- DATA/
  - README.md
  - DATA_LICENSE.txt
  - candidate_matched_images.csv
  - viewpoint_audit_sample.csv
  - clean_manifest.csv
  - listing_review.csv
  - manifest_with_splits.csv
  - model_split_assignments.csv
  - train_manifest.csv
  - validation_manifest.csv
  - test_manifest.csv
  - split_config.json
  - split_summary.csv
- OUTPUT/
  - ad_missing_values.csv
  - image_missing_values.csv
  - duplicate_summary.csv
  - image_counts_by_view.csv
  - listing_counts_by_view.csv
  - model_counts_by_view.csv
  - matched_listing_summary.csv
  - pickup_model_coverage.csv
  - figure_1_viewpoint_coverage.png
  - figure_2_matched_model_coverage.png
  - cleaned_listings_by_body_type.csv
  - vehicle_models_by_body_type_and_split.csv
  - fig_01_cleaned_listings_by_body_type.png
  - fig_02_vehicle_models_by_split.png
  - exploration_package_versions.txt
- REFERENCES/
  - README.md

### Notebook roles

| Notebook | Inputs | Outputs |
| --- | --- | --- |
| Metadata_Prep.ipynb | Original advertisement and image metadata CSVs | Candidate records, audit template, MI2 tables, and MI2 plots |
| Data_Cleaning.ipynb | Prepared candidate-image ZIP and review-record ZIP | Verified images, cleaned manifests, and model-group splits |
| Data_Exploration.ipynb | split_summary.csv | Two cleaned-data plots, supporting tables, and package versions |

These notebooks document different stages. Metadata_Prep.ipynb does
not itself generate the prepared candidate-image ZIP required by
Data_Cleaning.ipynb.

### Data files

| File | Role |
| --- | --- |
| candidate_matched_images.csv | One candidate image per listing and predicted view in the MI2 matched pool |
| viewpoint_audit_sample.csv | 90-image audit template with blank review fields |
| clean_manifest.csv | Final cleaned image records before split assignment |
| listing_review.csv | Recorded decisions used by the cleaning notebook |
| manifest_with_splits.csv | Cleaned image records with split assignments |
| model_split_assignments.csv | Assignments at vehicle-model level |
| train_manifest.csv | Training image records |
| validation_manifest.csv | Validation image records |
| test_manifest.csv | Test image records |
| split_config.json | Split settings and recorded package versions |
| split_summary.csv | Counts by split and body type |

The audit template is not a substitute for listing_review.csv.
The former has blank review fields; the latter supplies the decisions
used in cleaning.

See [DATA/README.md](DATA/README.md) for provenance, licensing,
ethical considerations, the data dictionary, and explanatory plots.

### Output groups

The MI2 output tables and figures describe metadata quality and
candidate coverage before final visual cleaning.

The files beginning fig_01 and fig_02, their two supporting tables,
and exploration_package_versions.txt describe the final cleaned sample.

Model evaluation outputs are pending.

### Release attachments

Download the archives from the
[dataset release](https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0).

| Archive | Purpose |
| --- | --- |
| DVM_Project3_Review_20261114_201843_029683.zip | Prepared candidate images and selection_manifest.csv |
| DVM_Review_Records.zip | Recorded listing review decisions |
| DVM_Cleaned_Data.zip | Final images, manifests, splits, configuration, and license information |

Download the named attachments under Assets. GitHub's automatic
Source code archives do not contain these attached datasets.
Cloning the repository does not download release attachments.

## Section 3: Instructions for Reproducing Results

### A. Reproduce MI2 metadata preparation

1. Obtain Ad_table (extra).csv and Image_table.csv from the
   [DVM-CAR project website](https://deepvisualmarketing.github.io/).
2. Open SCRIPTS/Metadata_Prep.ipynb in Google Colab.
3. Start a fresh runtime and ensure pandas, NumPy, and matplotlib
   are available.
4. Run the code cells from top to bottom.
5. At the upload prompt, select both metadata CSVs together.
6. The notebook validates and joins records, filters body types and
   viewpoints, counts candidate coverage, and generates two plots.
7. It selects one candidate image per listing and view and creates
   a 90-image audit template.
8. The final cell downloads MI2_Metadata_Results.zip.

Expected matched candidate counts:

| Body type | Listings | Distinct models |
| --- | ---: | ---: |
| Sedan | 10,765 | 118 |
| SUV | 28,667 | 145 |
| Pickup | 580 | 14 |

The exported candidate_matched_images.csv contains 120,036 image records.
The viewpoint_audit_sample.csv contains 90 records with blank review fields.

These counts depend on the source metadata version. The original source
CSV snapshots are not currently stored in this repository.

The notebook writes files to /content/mi2_outputs/ and packages them as
/content/MI2_Metadata_Results.zip.

For the repository, candidate_matched_images.csv and
viewpoint_audit_sample.csv are placed in DATA/. The other ten exported
files are placed in OUTPUT/.

### B. Use the final cleaned dataset

To begin modeling without rerunning preparation or cleaning:

1. Download DVM_Cleaned_Data.zip from the release.
2. Extract the complete archive.
3. Keep Photos/ alongside the extracted CSV and JSON files.
4. Use the provided training, validation, and test manifests.
5. Resolve each Extracted_path relative to the extracted dataset folder.

Do not generate new random splits. The provided assignments preserve
complete three-view listings and model-level separation.

Class labels are Sedan = 0, SUV = 1, and Pickup = 2.

### C. Reproduce cleaning and split generation

1. Download both cleaning inputs from the release:
   - DVM_Project3_Review_20261114_201843_029683.zip
   - DVM_Review_Records.zip
2. Open SCRIPTS/Data_Cleaning.ipynb in Google Colab.
3. Start a fresh runtime and ensure the cleaning dependencies are available.
4. Run all code cells from top to bottom.
5. At the first upload prompt, upload only the candidate-image ZIP.
6. At the second upload prompt, upload only DVM_Review_Records.zip.
7. Continue through filtering, image verification, split assignment,
   and export.
8. Download DVM_Cleaned_Data.zip when the final cell runs.

The notebook reads selection_manifest.csv from the candidate archive
and listing_review.csv from the review archive.

Do not substitute the cleaned output ZIP for either input archive.

### D. Understand the cleaning and split checks

The notebook retains listings whose Review_decision is provisional_keep.
It checks:

- Unique image identifiers and file hashes
- Consistent vehicle model and body type within each listing
- Exactly one Front, one Side, and one Rear image per listing
- Agreement between viewpoint codes and view labels
- No retained Quality_check value explicitly marked N
- Matching source-file SHA-256 hashes
- Successful image decoding and 300 × 300 dimensions
- No duplicate decoded RGB pixel hashes
- No unexpected files in the exported photo folder

Missing CSV values are represented as empty strings. This is not
statistical imputation, and missing quality flags do not establish
image usability.

Failed assertions stop execution rather than silently dropping records.

The split procedure groups by Genmodel_ID, uses seed 4002, and compares
5,000 candidate allocations against class-level listing targets.
Model performance is not used to choose the splits.

Models, listings, and identical file hashes do not cross partitions.
Every partition contains all three body types.

| Check | Expected value |
| --- | ---: |
| Cleaned listings | 860 |
| Cleaned images | 2,580 |
| Images per listing | 3 |
| Training images | 1,785 |
| Validation images | 393 |
| Test images | 402 |
| Vehicle-model overlap between splits | 0 |

The split-export cell should report:
Passed: complete triplets and no model overlap.

Cleaned files are written to /content/DVM_Cleaned_Data/.
The final ZIP is written to /content/DVM_Cleaned_Data.zip.

### E. Reproduce cleaned-data exploration

1. Download DATA/split_summary.csv, or use the regenerated copy from
   DVM_Cleaned_Data.zip.
2. Open SCRIPTS/Data_Exploration.ipynb in Google Colab.
3. Run the code cell.
4. Upload split_summary.csv when prompted.
5. Confirm that both plots display.
6. Download Project3_Exploration_Outputs.zip.

Expected listing counts are 395 Sedan, 371 SUV, and 94 Pickup.

Expected within-class model counts:

| Body type | Training | Validation | Test |
| --- | ---: | ---: | ---: |
| Sedan | 75 | 16 | 16 |
| SUV | 88 | 19 | 19 |
| Pickup | 6 | 2 | 1 |

A Genmodel_ID can span multiple body types. Counts summed across
body types may therefore exceed the overall distinct-model total.

The notebook saves two PNG figures, two supporting CSV tables, and
a package-version record in the runtime's OUTPUT/ folder.

### F. Export and repository locations

Running the notebooks does not update GitHub.

- Metadata preparation exports to /content/mi2_outputs/.
- Cleaning exports to /content/DVM_Cleaned_Data/.
- Cleaned-data exploration exports to the runtime's OUTPUT/ folder.

The relevant files are downloaded and uploaded manually to the DATA/
and OUTPUT/ locations listed in Section 2. Image archives are attached
to the release.

Download generated files before ending the Colab session because runtime
storage is temporary.

### G. Reproducibility boundary

The repository reproduces MI2 metadata preparation from the source CSVs
and final cleaning from the supplied candidate and review archives.

The intermediate code that assembled the specific 4,500-image review
archive is not yet included. Metadata_Prep.ipynb does not perform that
extraction. The supplied archive preserves the input needed to reproduce
the downstream cleaning and splits.

Human visual review is represented by saved decisions and is not
automatically reproduced by executing the notebooks.

### H. Model training and evaluation — pending

Zichen's modeling work will add the training notebook, dependencies,
validation-selected settings, checkpoint information, and test evaluation.

Final documentation will specify how to generate the viewpoint-specific
metrics and confusion matrices, where each result is saved, and whether
the 33.3% balanced-accuracy goal is achieved.

### Limitations

- Predicted viewpoints and source labels may contain errors despite review.
- Body types are imbalanced in the cleaned sample.
- The test pickup class contains 20 listings but only one vehicle model,
  limiting conclusions about generalization across pickup models.
- UK listing images with removed backgrounds may not represent other
  markets or natural photographs.
- Model separation concerns this project's partitions, not the contents
  of the external pretraining dataset.
- No conclusion about the best viewpoint is made before model evaluation.

### Licensing

[LICENSE.md](LICENSE.md) covers original project code and documentation.
DVM-CAR retains its own dataset license; see
[DATA/DATA_LICENSE.txt](DATA/DATA_LICENSE.txt).

Release archives retain the original candidate-stage processing note.
The repository copy clarifies completed cleaning checks without changing
the dataset license.

### References

[1] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, “DVM-CAR.”
[Online]. Available: https://deepvisualmarketing.github.io/

[2] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for
image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit.,
2016, pp. 770–778.

Additional references:
[REFERENCES/README.md](REFERENCES/README.md).

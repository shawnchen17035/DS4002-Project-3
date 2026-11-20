# Data

This folder documents the data used in **Vehicle Body-Type Classification Across Viewing Angles**, conducted by The Pink Panthers for DS 4002 Project 3 at the University of Virginia.

## Data Summary

This project uses DVM-CAR vehicle images to investigate how photographic viewpoint affects the classification of three body types: Sedan, SUV, and Pickup.

The analysis compares three viewpoints: Front, Side, and Rear.

The repository preserves two distinct stages of data preparation:

1. **MI2 candidate metadata:** Images identified from the original DVM-CAR metadata before final visual review and cleaning.
2. **Final cleaned dataset:** Images retained following recorded human review, image validation, and grouped train/validation/test splitting.

These stages must not be treated as the same dataset.

### Final Cleaned Dataset

The final dataset contains **2,580 images from 860 vehicle listings**, with exactly one Front, one Side, and one Rear image for each listing. Images have dimensions of 300 × 300 pixels.

| Split | Listings | Images | Distinct vehicle models |
|---|---:|---:|---:|
| Training | 595 | 1,785 | 168 |
| Validation | 131 | 393 | 37 |
| Test | 134 | 402 | 36 |
| **Total** | **860** | **2,580** | **241** |

The cleaned dataset contains:

| Body type | Listings | Images |
|---|---:|---:|
| Sedan | 395 | 1,185 |
| SUV | 371 | 1,113 |
| Pickup | 94 | 282 |
| **Total** | **860** | **2,580** |

Class identifiers are Sedan = 0, SUV = 1, and Pickup = 2.

The target split proportions were 70% training, 15% validation, and 15% testing. Actual proportions differ slightly because assignments are grouped by `Genmodel_ID`, preventing vehicle models from appearing in multiple partitions.

### MI2 Candidate Metadata

Initial metadata processing identified listings with all three predicted viewpoints.

| Body type | Candidate listings | Distinct vehicle models |
|---|---:|---:|
| Sedan | 10,765 | 118 |
| SUV | 28,667 | 145 |
| Pickup | 580 | 14 |
| **Total** | **40,012** | |

`candidate_matched_images.csv` contains 120,036 candidate-image records, corresponding to three predicted viewpoints per candidate listing.

`viewpoint_audit_sample.csv` contains 90 sampled candidate images. Its additional visual-review columns are blank because the file is a review template, not the completed record of cleaning decisions.

The final cleaned dataset must be used for model training and evaluation. The MI2 candidate files are retained for documentation and reproducibility of earlier preparation.

## Accessing the Data

### Final Dataset and Review Archives

The project's image archives are distributed through the GitHub release:

[Project 3 data-v1.0 release](https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0)

| Archive | Description |
|---|---|
| `DVM_Cleaned_Data.zip` | Final cleaned images, manifests, fixed splits, configuration, and license information |
| `DVM_Project3_Review_20261114_201843_029683.zip` | Prepared 4,500-image review archive and selection manifest |
| `DVM_Review_Records.zip` | Recorded listing-review decisions |

To use the final modeling dataset:

1. Download `DVM_Cleaned_Data.zip` from the release's Assets section.
2. Extract the archive.
3. Preserve the `Photos/` folder alongside the CSV and JSON files.
4. Read `train_manifest.csv`, `validation_manifest.csv`, and `test_manifest.csv`.
5. Resolve image locations using `Extracted_path`.
6. Preserve the provided split assignments rather than generating new random partitions.

GitHub's automatically generated source-code archives do not contain the separate release attachments.

### Original Metadata

The metadata-preparation notebook uses two original DVM-CAR files:

- `Ad_table (extra).csv`
- `Image_table.csv`

These can be obtained through the [DVM-CAR project website](https://deepvisualmarketing.github.io/).

The original source metadata snapshots are not included in this repository. The exported candidate files document the preparation results used for this project.

## Files in This Folder

| File | Description |
|---|---|
| `candidate_matched_images.csv` | Earlier candidate pool containing matched listing-image records |
| `viewpoint_audit_sample.csv` | 90-image candidate audit template with blank review fields |
| `clean_manifest.csv` | Final cleaned image records before split assignment |
| `listing_review.csv` | Recorded human-review decisions |
| `manifest_with_splits.csv` | Cleaned images with assigned data partitions |
| `model_split_assignments.csv` | Vehicle-model-level split assignments |
| `train_manifest.csv` | Training partition |
| `validation_manifest.csv` | Validation partition |
| `test_manifest.csv` | Held-out test partition |
| `split_config.json` | Split parameters, seed, and recorded package versions |
| `split_summary.csv` | Body-type counts across partitions |
| `DATA_LICENSE.txt` | Dataset attribution and licensing information |

## Provenance

The project uses DVM-CAR, developed by Jingmin Huang, Bowei Chen, Lan Luo, Shigang Yue, and Iadh Ounis [1].

DVM-CAR contains vehicle photographs and associated records collected from online sources, including UK used-car advertisements.

The project accessed these data through the DVM-CAR website.

`Ad_table (extra).csv` supplied advertisement identifiers, vehicle-model identifiers, and body-type information. `Image_table.csv` supplied image records and predicted viewpoints. These tables were joined using advertisement and related identifiers.

The source dataset includes photographs that were processed through background removal and resizing. Viewpoint annotations are predictions rather than independently measured camera angles.

Source metadata can contain errors involving vehicle identity, body type, image quality, or viewpoint.

The MI2 visual audit identified incorrect viewpoints, incomplete vehicle images, and inconsistent vehicle identity within listings. These observations informed the cleaning criteria used to construct the final sample.

### Data Preparation Stages

1. **Metadata preparation:** Join source tables, standardize body types, map predicted viewpoints, and identify candidate three-view listings.
2. **Candidate review preparation:** Assemble a 4,500-image review archive from 1,500 listings.
3. **Human review:** Record decisions about image completeness, viewpoint accuracy, and consistent vehicle identity.
4. **Cleaning:** Apply retained review decisions and verify images.
5. **Split construction:** Assign vehicle models to training, validation, and testing partitions without overlap.
6. **Exploration and modeling:** Analyze the cleaned dataset and evaluate ResNet-18 classification performance across viewpoints.

### Reproducibility Boundary

`Metadata_Prep.ipynb` reproduces metadata preparation from the original source CSV files.

`Data_Cleaning.ipynb` reproduces cleaning and split construction from the prepared candidate-image archive and saved review records.

The original intermediate script that assembled the specific 4,500-image review archive is not included. This archive is supplied as a release input.

Human visual review is represented by recorded decisions; running the notebooks does not automatically repeat the human review process.

The modeling notebook uses the supplied final cleaned archive and fixed splits.

## Data License

DVM-CAR is distributed under the Creative Commons Attribution-NonCommercial 4.0 International license [3].

The project's processing includes filtering, sampling, duplicate exclusion, file renaming, and split assignment.

See [DATA_LICENSE.txt](DATA_LICENSE.txt) for attribution and processing information.

The repository's MIT license covers original project code and documentation. It does not replace or override the original dataset license.

## Ethical Statement

The vehicle photographs originate primarily from UK used-car advertisements. Consequently, conclusions may not generalize to vehicles photographed in different countries, lighting conditions, locations, or environments.

The project focuses exclusively on vehicle body-type classification. It does not seek to identify vehicle owners or individuals using license plates or other information.

The final dataset contains substantially fewer Pickup listings than Sedan or SUV listings. Therefore, overall accuracy alone could conceal uneven class performance. Balanced accuracy, macro F1, and class-level performance are reported to address this concern.

Model diversity is also limited. The held-out test partition contains only one Pickup vehicle model, making generalization to unseen pickup models particularly uncertain.

Three photographs belonging to one listing are correlated observations. Grouping by vehicle model prevents direct cross-partition model overlap but does not make observations statistically independent.

Source photographs may contain dealership backgrounds, lighting, cropping, framing, or marketplace-specific information that a classifier could learn as shortcuts.

Human review and integrity checks improve data quality but cannot guarantee the absence of labeling errors.

## Data Dictionary

Identifiers are categorical or string labels rather than numerical measurements.

Column names differ between preparation and cleaning stages.

### Final Cleaned Image Manifests

Each image manifest contains one row per retained image.

| Column | Description |
|---|---|
| `Review_ID` | Identifier linking an image to its reviewed listing |
| `Body_type` | Standardized category: Sedan, SUV, or Pickup |
| `Maker` | Vehicle manufacturer from source metadata |
| `Genmodel` | Vehicle model name |
| `Genmodel_ID` | Vehicle-model identifier used for grouped splitting |
| `Adv_ID` | Source advertisement identifier |
| `View` | Retained Front, Side, or Rear viewpoint |
| `Image_ID` | Source image identifier |
| `Image_name` | Original image filename |
| `Predicted_viewpoint` | Original viewpoint prediction: 0, 90, 180, or 270 |
| `Quality_check` | Source quality indicator |
| `Source_relative_path` | Image location relative to the source dataset |
| `Extracted_path` | Image location in the cleaned archive |
| `File_SHA256` | SHA-256 file hash used for integrity checking |
| `Class_id` | Numeric body-type identifier |
| `Filename` | Exported image filename |
| `Human_review_status` | Recorded review status |
| `Human_reviewer` | Recorded reviewer |
| `Human_review_date` | Recorded review date |
| `Split` | Assigned training, validation, or test partition |

Some fields are unavailable in the earlier candidate metadata because they are generated during review or cleaning.

### Candidate Metadata

`candidate_matched_images.csv` contains:

| Column | Description |
|---|---|
| `Genmodel_ID` | Source vehicle-model identifier |
| `Image_ID` | Source image identifier |
| `Image_name` | Source image filename |
| `Predicted_viewpoint` | Source viewpoint prediction |
| `Quality_check` | Source quality flag |
| `Adv_ID` | Advertisement identifier |
| `Bodytype` | Original body-type information |
| `Body_type` | Standardized body-type category |
| `View` | Derived Front, Side, or Rear viewpoint |
| `Relative_path` | Reconstructed source image location |

`Relative_path` belongs to candidate metadata. It is not interchangeable with `Extracted_path` from the final cleaned archive.

### Viewpoint Audit Template

`viewpoint_audit_sample.csv` preserves the candidate columns and adds:

| Column | Intended purpose |
|---|---|
| `Observed_view` | Viewpoint observed during human inspection |
| `View_label_correct` | Whether the predicted viewpoint agrees with inspection |
| `Body_label_correct` | Whether the recorded body type appears correct |
| `Usable` | Whether the image meets usability criteria |
| `Review_notes` | Additional reviewer observations |

These review columns remain blank in the repository's audit template. Blank entries should not be interpreted as approval.

### Review and Split Records

`listing_review.csv` documents the listing-level decisions used by the cleaning notebook.

Listings marked `provisional_keep` are retained only if subsequent programmatic checks pass.

`model_split_assignments.csv` records assignments using `Genmodel_ID`.

`split_summary.csv` records aggregated listing, image, and model counts by split and body type.

`split_config.json` documents the random seed, candidate-allocation procedure, target proportions, and software versions.

### Relationships Between Files

- `Adv_ID` connects advertisement metadata, images, and listing records.
- `Image_ID` identifies images across preparation and cleaning records.
- `Genmodel_ID` connects image records to model-level partitions.
- `Extracted_path` connects final manifests to the cleaned images.
- `manifest_with_splits.csv` contains the cleaned records with assignments.
- The three partition manifests contain the corresponding subsets.
- `split_summary.csv` supports the cleaned-data exploration notebook.

## Cleaning and Split Construction

The visual-review criteria were:

- A complete and usable exterior image of the vehicle
- A correctly identified Front, Side, or Rear viewpoint
- Consistent vehicle identity across the three photographs of a listing

The cleaning notebook applies recorded human-review decisions and programmatic checks.

The programmatic checks include:

- Unique image identifiers and file hashes
- Consistent vehicle identity and body type within listings
- Exactly one usable Front, Side, and Rear image per listing
- Agreement between retained view labels and viewpoint codes
- Exclusion of explicitly rejected source quality flags
- Source-file SHA-256 integrity verification
- Successful image decoding
- Image dimensions of 300 × 300 pixels
- Duplicate decoded RGB-pixel hash detection
- Zero vehicle-model overlap across data partitions

Missing CSV entries are represented as empty strings where required for processing. This does not constitute statistical imputation.

Assertions stop notebook execution when critical validation requirements fail.

### Grouped Splitting

The split construction uses random seed `4002` and evaluates 5,000 candidate vehicle-model allocations.

Assignments are selected based on class-level listing targets rather than downstream classifier performance.

The resulting partitions prevent identical vehicle models from appearing in multiple splits.

All model evaluation uses the provided partitions, not new random image-level splits.

For complete execution instructions, see [Section 3: Reproducing the Results](../README.md#section-3-reproducing-the-results) in the main README.

## Explanatory Plots

These visualizations represent the **final cleaned dataset**, not the earlier MI2 candidate pool.

### Figure 1. Cleaned Listings by Body Type

![Cleaned listings by body type](../OUTPUT/fig_01_cleaned_listings_by_body_type.png)

The final sample contains 395 Sedan, 371 SUV, and 94 Pickup listings.

Each listing contributes three photographs, so the class imbalance in images follows the same proportions.

Pickup listings are substantially underrepresented relative to the other two categories. This supports reporting balanced accuracy, macro F1, and per-class recall rather than relying on accuracy alone.

Supporting file: [cleaned_listings_by_body_type.csv](../OUTPUT/cleaned_listings_by_body_type.csv)

### Figure 2. Vehicle-Model Coverage by Body Type and Split

![Vehicle-model coverage by split](../OUTPUT/fig_02_vehicle_models_by_split.png)

The model-group splitting procedure preserves separation across training, validation, and testing partitions.

Pickup diversity is particularly limited: six Pickup models appear in training, two in validation, and one in testing.

This limits confidence that the classifier will perform equally well on other unseen Pickup models.

Model identifiers may appear across body-type categories. Consequently, summing distinct model counts by class does not necessarily equal the overall number of distinct model identifiers.

Supporting file: [vehicle_models_by_body_type_and_split.csv](../OUTPUT/vehicle_models_by_body_type_and_split.csv)

### Reproducing the Plots

1. Download `DATA/split_summary.csv`.
2. Open [Data_Exploration.ipynb](../SCRIPTS/Data_Exploration.ipynb) in Google Colab.
3. Upload `split_summary.csv` when prompted.
4. Run the notebook to generate the figures.
5. Download `Project3_Exploration_Outputs.zip`.

The exploration notebook exports two PNG figures, two supporting CSV files, and the package-version record.

Software versions are recorded in [exploration_package_versions.txt](../OUTPUT/exploration_package_versions.txt).

The separate MI2 figures in `OUTPUT/` describe earlier metadata preparation and should not be interpreted as visualizations of the final cleaned dataset.

## References

[1] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, "DVM-CAR." [Online]. Available: https://deepvisualmarketing.github.io/

[2] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, "User manual of DVM-CAR." [Online]. Available: https://deepvisualmarketing.github.io/site-assets/DVM_user_manual.pdf

[3] Creative Commons, "Attribution-NonCommercial 4.0 International." [Online]. Available: https://creativecommons.org/licenses/by-nc/4.0/

Additional project references are available in [REFERENCES/README.md](../REFERENCES/README.md).

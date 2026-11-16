# Vehicle Body-Type Classification Across Viewing Angles

**DS 4002 — Data Science Project — Project 3**  
**University of Virginia | Fall 2026 | Section 100010**  
**Team:** The Pink Panthers  
**Members:** Shawn Chen and Zichen Luo  
**Group Leader:** Shawn Chen  
**Professor:** Peter Alonzi  
**Teaching Assistant:** Naman Patel  

## Contents of This Repository

This repository contains the data, cleaning code, and exploratory outputs
for investigating how viewing angle affects classification of sedans,
SUVs, and pickup trucks using DVM-CAR images.

**Research question:** What effect does the angle of a photo have on how
accurately a model can distinguish sedans, SUVs, and pickup trucks?

**Performance goal:** Exceed the 33.3% three-class chance baseline in
balanced accuracy for each viewpoint—front, side, and rear—on vehicle
models excluded from training.

Vehicle body-type classification supports automotive inventory management
and online marketplaces. However, visible features change with camera
angle. Side views reveal silhouette and cargo-bed shape, while front and
rear views provide different cues. Reporting performance separately by
viewpoint helps identify differences that overall accuracy could hide.

Following MI2, each retained listing contributes one front, one side,
and one rear image. This matched design compares viewpoints using the
same listings. Splitting by vehicle model keeps related images together
and evaluates generalization to models excluded from training.

**Current status:** Data cleaning, image verification, fixed splits, and
cleaned-data exploratory figures are complete. Model training, tuning,
and final evaluation are pending. No classification results or claims
of achieving the performance goal are reported yet.

### Dataset and preparation

The project uses DVM-CAR vehicle images and associated metadata [1].
During data establishment, advertisement and image records were linked
using listing identifiers. Target body types were standardized to
Sedan, SUV, and Pickup.

The MI2 audit of 90 sampled images identified incorrect viewpoints,
incomplete vehicle images, and different vehicles within the same listing.
These findings motivated visual review and the requirement for three
usable exterior views of the same vehicle per retained listing.

The cleaning notebook starts from a prepared candidate archive containing
4,500 images from 1,500 listings and a separate archive of review records.
It exports 2,580 cleaned images from 860 listings.

| Split | Listings | Images | Distinct vehicle models |
| --- | ---: | ---: | ---: |
| Training | 595 | 1,785 | 168 |
| Validation | 131 | 393 | 37 |
| Test | 134 | 402 | 36 |
| Total | 860 | 2,580 | 241 |

Every retained listing has one Front, one Side, and one Rear image.
Partitions are grouped by Genmodel_ID, with no vehicle-model overlap
between training, validation, and test sets.

Target proportions are 70% training, 15% validation, and 15% test.
Actual proportions differ slightly because model groups remain intact.

The cleaned sample contains 395 sedan, 371 SUV, and 94 pickup listings.
The exploratory figures document this imbalance and the limited
vehicle-model diversity of the pickup class.

### Planned modeling and evaluation

Following MI1 and MI2, we plan to fine-tune an ImageNet-pretrained
ResNet-18 with a three-class output layer [2]. One classifier will be
trained using all three viewpoints.

The planned workflow is to:

- Resize images to 224 × 224 pixels and normalize with ImageNet statistics.
- Apply label-preserving augmentation to training images only.
- Use class-weighted cross-entropy to address body-type imbalance.
- Select settings using the fixed validation partition, with early
  stopping based on validation macro F1.
- Reserve the test partition for final evaluation after model selection.
- Compare viewpoints on the same held-out listings.

Balanced accuracy is the primary metric because it gives equal weight
to recall for Sedan, SUV, and Pickup. Supporting measures will include
macro precision, macro F1, per-class recall, and normalized confusion
matrices for each viewpoint. Viewpoint differences will be reported
in percentage points.

These methods remain planned. Final settings, dependencies, execution
instructions, and results will be documented with the modeling code.

### Responsibilities

| Member | Responsibility |
| --- | --- |
| Shawn Chen | Data preparation, visual review, cleaning, model-group splits, exploration, and data documentation |
| Zichen Luo | Model development, validation, viewpoint-specific evaluation, and interpretation |

## Section 1: Software and Platform

### Software and platform

The notebooks use Python 3 in Google Colab on a Linux runtime.

Both notebooks use interactive Colab uploads and downloads. The cleaning
notebook also uses /content paths. Local execution requires adapting
these functions and paths.

### Packages

| Package | Purpose | Version record |
| --- | --- | --- |
| pandas | Read, organize, summarize, and export data | Cleaning: 2.2.3; exploration version recorded separately |
| NumPy | Generate and assess model-group split allocations | Cleaning: 2.4.6 |
| Pillow | Decode images, verify dimensions, and inspect RGB pixels | Not recorded by the cleaning notebook |
| matplotlib | Generate the two exploratory figures | Recorded in exploration_package_versions.txt |

Cleaning versions are recorded in DATA/split_config.json.
Exploration versions are recorded in
OUTPUT/exploration_package_versions.txt.

The cleaning notebook also uses google.colab.files and standard-library
modules pathlib, zipfile, hashlib, io, unicodedata, re, and json.

The exploration notebook also uses google.colab.files and standard-library
modules pathlib, io, shutil, and zipfile.

If needed, install the cleaning dependencies in a separate setup cell:

```python
%pip install pandas==2.2.3 numpy==2.4.6 Pillow
```

For exploration:

```python
%pip install pandas matplotlib
```

Use the recorded versions when reproducing the saved outputs.
Restart the runtime if prompted after installation. Python and Pillow
versions were not recorded by the cleaning notebook.

Model-training dependencies and hardware requirements will be added
with the modeling notebook.

## Section 2: Map of Documentation

Placeholder .gitkeep files are omitted from this outline.

- README.md — project overview and reproduction instructions
- LICENSE.md — license for original project code and documentation
- SCRIPTS/
  - DS4002_Project_3_Data_Cleaning.ipynb
  - DS4002_Project_3_Data_Exploration.ipynb
- DATA/
  - README.md
  - DATA_LICENSE.txt
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
  - fig_01_cleaned_listings_by_body_type.png
  - fig_02_vehicle_models_by_split.png
  - cleaned_listings_by_body_type.csv
  - vehicle_models_by_body_type_and_split.csv
  - exploration_package_versions.txt
- REFERENCES/
  - README.md

### Scripts

| Notebook | Role |
| --- | --- |
| DS4002_Project_3_Data_Cleaning.ipynb | Applies review decisions, verifies images, creates model-group splits, and exports the cleaned dataset |
| DS4002_Project_3_Data_Exploration.ipynb | Reads split_summary.csv and generates two figures and supporting tables |

Run cleaning before exploration when rebuilding the dataset.
Exploration can also run independently using the committed split_summary.csv.

### Data files

| File | Contents |
| --- | --- |
| clean_manifest.csv | Cleaned image records before split assignment |
| listing_review.csv | Recorded listing review decisions |
| manifest_with_splits.csv | Cleaned image records with split assignments |
| model_split_assignments.csv | Model-level split assignments |
| train_manifest.csv | Training image records |
| validation_manifest.csv | Validation image records |
| test_manifest.csv | Test image records |
| split_config.json | Split parameters and recorded package versions |
| split_summary.csv | Counts by split and body type |
| DATA_LICENSE.txt | Dataset attribution, license, and processing note |

See [DATA/README.md](DATA/README.md) for provenance, the data dictionary,
ethical considerations, and explanatory plots.

### Exploratory outputs

| File | Contents |
| --- | --- |
| fig_01_cleaned_listings_by_body_type.png | Counts of cleaned listings for each body type |
| fig_02_vehicle_models_by_split.png | Distinct model counts within each body type and split |
| cleaned_listings_by_body_type.csv | Counts underlying Figure 1 |
| vehicle_models_by_body_type_and_split.csv | Counts underlying Figure 2 |
| exploration_package_versions.txt | pandas and matplotlib versions used for exploration |

These are data-exploration outputs, not classifier performance results.

### Downloadable data archives

Download the named attachments from the
[dataset release](https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0).

| Attachment | Role |
| --- | --- |
| DVM_Project3_Review_20261114_201843_029683.zip | Cleaning input: candidate images, selection_manifest.csv, and source license information |
| DVM_Review_Records.zip | Cleaning input: review archive containing listing_review.csv |
| DVM_Cleaned_Data.zip | Cleaning output: verified images, manifests, fixed splits, configuration, and license information |

The release attachments are separate from GitHub's automatically
generated Source code archives. Cloning the repository does not
download these attachments.

### Connections between files

The workflow uses CSV manifests and JSON configuration.
No Excel workbook is required.

- Adv_ID connects image records to listing review decisions.
- Genmodel_ID connects images to model-level split assignments.
- Extracted_path connects each cleaned record to its image relative
  to the extracted dataset folder.
- manifest_with_splits.csv adds split assignments to cleaned records.
- The train, validation, and test manifests contain the respective subsets.
- split_summary.csv provides the input for the exploration notebook.

Class labels are Sedan = 0, SUV = 1, and Pickup = 2.

## Section 3: Instructions for Reproducing Results

### A. Use the prepared dataset

To begin modeling without rerunning cleaning:

1. Open the dataset release linked above.
2. Download DVM_Cleaned_Data.zip.
3. Extract the entire archive.
4. Keep Photos/ alongside the extracted CSV, JSON, and license files.
5. Use the supplied train_manifest.csv, validation_manifest.csv,
   and test_manifest.csv without generating new splits.
6. Resolve each Extracted_path relative to the extracted dataset folder.
   These paths begin with Photos/.

The provided manifests preserve complete three-view listings and
vehicle-model separation.

### B. Reproduce cleaning and split generation

1. Download both input archives:
   - DVM_Project3_Review_20261114_201843_029683.zip
   - DVM_Review_Records.zip
2. Open SCRIPTS/DS4002_Project_3_Data_Cleaning.ipynb in Google Colab.
3. Start a fresh runtime and ensure the cleaning dependencies are available.
4. Execute the code cells in their displayed order.
5. At the first upload prompt, upload only the candidate archive:
   DVM_Project3_Review_20261114_201843_029683.zip.
6. Run the cell that reads selection_manifest.csv and reports candidate counts.
7. At the second upload prompt, upload only DVM_Review_Records.zip.
8. Continue through review filtering, image verification, split generation,
   and file export.
9. The final cell creates and downloads DVM_Cleaned_Data.zip.

Do not substitute the cleaned output ZIP for either input archive.

This notebook reproduces cleaning from the prepared candidate archive
and saved review decisions. It does not reproduce the earlier raw-metadata
selection process or conduct human visual review automatically.

### C. Check the cleaning outputs

The notebook retains listings marked provisional_keep in the review
records and checks:

- Unique image identifiers and file hashes
- Consistent vehicle model and body type within each listing
- Exactly one Front, one Side, and one Rear image per listing
- Agreement between viewpoint codes and view labels
- No retained image explicitly marked N in Quality_check
- Matching source-file SHA-256 hashes
- Successful image decoding and 300 × 300 dimensions
- No duplicate decoded RGB pixel hashes
- No unexpected files in the exported image folder

Missing CSV values are initially represented as empty strings.
This is not statistical imputation. A missing quality flag does not
establish image usability.

Failed assertions stop execution rather than silently removing
additional records.

### D. Check the splits

The split procedure groups images by Genmodel_ID, uses seed 4002,
and evaluates 5,000 candidate allocations.

It selects an allocation that minimizes deviation from class-level
listing targets without using model performance.

Models, listings, and identical file hashes do not cross partitions.
Each split includes all three body types.

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

### E. Reproduce the explanatory figures

1. Download DATA/split_summary.csv from the repository, or use the
   regenerated copy from the cleaned dataset.
2. Open SCRIPTS/DS4002_Project_3_Data_Exploration.ipynb in Google Colab.
3. Start a fresh runtime and ensure pandas and matplotlib are available.
4. Run the notebook's code cell.
5. When prompted, upload the file named split_summary.csv.
6. Confirm that both figures appear.
7. Download Project3_Exploration_Outputs.zip and extract its five files.

Expected Figure 1 listing counts:

| Body type | Listings |
| --- | ---: |
| Sedan | 395 |
| SUV | 371 |
| Pickup | 94 |

Expected Figure 2 model counts:

| Body type | Training | Validation | Test |
| --- | ---: | ---: | ---: |
| Sedan | 75 | 16 | 16 |
| SUV | 88 | 19 | 19 |
| Pickup | 6 | 2 | 1 |

Model counts in Figure 2 are calculated within each body type.
A Genmodel_ID can span multiple body types, so adding counts across
body types may exceed the distinct model total for a partition.

### F. Locate generated files

The cleaning notebook writes its dataset folder to:

`/content/DVM_Cleaned_Data/`

It writes the complete dataset archive to:

`/content/DVM_Cleaned_Data.zip`

The exploration notebook writes its five generated files to the runtime's
`OUTPUT/` folder and packages them in:

`Project3_Exploration_Outputs.zip`

Neither notebook automatically updates GitHub.

The cleaned CSV and JSON files are copied into the repository's DATA/
folder manually. The complete data archives are attached to the release.
Exploratory figures, supporting tables, and package versions are uploaded
to the repository's OUTPUT/ folder manually.

Download generated files before ending the Colab session because runtime
storage is temporary.

### G. Model training and final evaluation — pending

The current notebooks do not train a classifier or produce classification
metrics and confusion matrices.

When modeling is added, the documentation will include:

- Modeling notebook filename and execution order
- Required packages, versions, and hardware
- Dataset loading and image preprocessing
- Training settings and validation-based checkpoint selection
- Instructions for generating each result table and figure
- Exact output locations
- Expected final metrics and comparison with the 33.3% baseline

Model outputs will be added to OUTPUT/, and the documentation map will
be updated to list the actual files.

### Limitations and interpretation

- Viewpoint labels are predictions rather than measured camera angles.
  Human review reduces, but cannot guarantee elimination of, labeling
  and identity errors.
- The cleaned sample contains unequal numbers of the three body types.
  Balanced accuracy and per-class reporting are therefore important.
- The test split contains 60 pickup images from 20 listings but only
  one pickup vehicle model, limiting conclusions about pickup generalization.
- Images originate from UK vehicle listings and have undergone background
  removal and resizing. Findings may not generalize to other markets
  or natural photographs taken in traffic or parking lots.
- Model-group separation prevents overlap within this project's partitions;
  it does not establish the contents of the external pretraining dataset.
- No conclusion about the best viewpoint can be drawn until the planned
  classification evaluation is complete.

### Licensing and processing notes

[LICENSE.md](LICENSE.md) covers original project code and documentation.
It does not relicense DVM-CAR images or other third-party materials.

See [DATA/DATA_LICENSE.txt](DATA/DATA_LICENSE.txt) for dataset attribution
and licensing information.

The release archives retain the original candidate-stage processing note.
The repository copy clarifies that the cleaned dataset has undergone
recorded human review and automated image checks. This wording update
does not change the dataset license.

### References

[1] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, “DVM-CAR.”
[Online]. Available: https://deepvisualmarketing.github.io/

[2] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for
image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit.,
2016, pp. 770–778.

Additional references are maintained in
[REFERENCES/README.md](REFERENCES/README.md).

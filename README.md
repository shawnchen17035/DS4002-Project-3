# Vehicle Body-Type Classification Across Viewing Angles

**DS 4002 — Project 3**  
**Team:** The Pink Panthers  
**Members:** Shawn Chen and Zichen Luo
**Group Leader:** Shawn Chen
**Professor:** Peter Alonzi  
**Teaching Assistant:** Naman Patel  

## Project Overview

This DS 4002 project investigates classification of sedans, SUVs, and
pickups across front, side, and rear views using DVM-CAR images.

The current repository contains the completed data-cleaning notebook,
review records, cleaned image manifests, and fixed training, validation,
and test splits. Model training and evaluation are pending.

The cleaned dataset contains 2,580 images from 860 vehicle listings.
Each listing has one front, one side, and one rear image.

| Split | Listings | Images | Vehicle models |
| --- | ---: | ---: | ---: |
| Training | 595 | 1,785 | 168 |
| Validation | 131 | 393 | 37 |
| Test | 134 | 402 | 36 |
| Total | 860 | 2,580 | 241 |

Splits are grouped by Genmodel_ID so that vehicle models do not overlap
between partitions. The target proportions are 70% training, 15%
validation, and 15% test; actual proportions differ slightly because
model groups remain intact.

## 1. Software and Platform

The cleaning notebook uses Python 3 in Google Colab.

Third-party packages:
- pandas
- NumPy
- Pillow (imported as PIL)

Other imports:
- google.colab.files for uploads and downloads
- Python standard library: pathlib, zipfile, hashlib, io,
  unicodedata, re, and json

The NumPy and pandas versions used to generate the saved splits are
recorded in DATA/split_config.json. For exact split reproduction,
use those versions.

The notebook uses Colab-specific upload/download functions and /content
paths. Running it locally requires adapting those functions and paths.

## 2. Repository Contents

| Path | Purpose |
| --- | --- |
| README.md | Project overview and reproduction instructions |
| SCRIPTS/DS4002_Project_3_Data_Cleaning.ipynb | Cleaning, image verification, split generation, and export |
| DATA/README.md | Data inventory and download instructions |
| DATA/clean_manifest.csv | Cleaned image records before split assignment |
| DATA/listing_review.csv | Listing review decisions |
| DATA/manifest_with_splits.csv | Cleaned image records with split assignments |
| DATA/model_split_assignments.csv | Model-level split assignments |
| DATA/train_manifest.csv | Training image records |
| DATA/validation_manifest.csv | Validation image records |
| DATA/test_manifest.csv | Test image records |
| DATA/split_config.json | Split parameters and recorded package versions |
| DATA/split_summary.csv | Counts by split and body type |
| DATA/DATA_LICENSE.txt | Dataset licensing information |
| OUTPUT/ | Reserved for generated analysis figures and model results |
| REFERENCES/ | Reserved for project materials and references |

### Release assets

Download the following files from:
https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0

- DVM_Cleaned_Data.zip: completed dataset, images, and split files
- DVM_Project3_Review_20261114_201843_029683.zip:
  candidate images and selection_manifest.csv
- DVM_Review_Records.zip: review archive containing listing_review.csv

The named ZIP attachments are separate from GitHub's automatically
generated Source code archives. Cloning the repository does not
download the release attachments.

## 3. Reproduction Instructions

### A. Use the prepared dataset

1. Download DVM_Cleaned_Data.zip from the release.
2. Extract the complete archive.
3. Keep Photos/ alongside the extracted CSV and JSON files.
4. Use the provided train_manifest.csv, validation_manifest.csv,
   and test_manifest.csv without generating new splits.
5. Resolve each manifest's Extracted_path relative to the extracted
   dataset folder. These paths begin with Photos/.

Class labels are Sedan = 0, SUV = 1, and Pickup = 2.

### B. Reproduce cleaning and split generation

1. Download both input archives:
   DVM_Project3_Review_20261114_201843_029683.zip and
   DVM_Review_Records.zip.
2. Open SCRIPTS/DS4002_Project_3_Data_Cleaning.ipynb in Google Colab.
3. Start a fresh runtime and run the nine cells in order.
4. At the first upload prompt in cell 2, upload only the candidate
   archive: DVM_Project3_Review_20261114_201843_029683.zip.
5. Cell 3 reads selection_manifest.csv from that archive.
6. At the second upload prompt in cell 4, upload only
   DVM_Review_Records.zip.
7. Run the remaining cells to apply the saved review decisions,
   validate images, export the cleaned data, and generate splits.
8. The final cell creates and downloads DVM_Cleaned_Data.zip.

The cleaning starts from the prepared candidate archive and recorded
human review decisions. It does not recreate the original DVM-CAR
candidate-selection process or perform human review automatically.

### Cleaning and validation

The notebook retains listings marked provisional_keep in the review
records and checks:

- Unique image identifiers and file hashes
- Consistent vehicle model and body type within each listing
- Exactly three images per listing: Front, Side, and Rear
- Agreement between viewpoint metadata and view labels
- No retained image with Quality_check equal to N
- Matching image-file SHA-256 hashes
- Readable images with dimensions of 300 by 300 pixels
- No duplicate decoded RGB pixel hashes

The split procedure uses seed 4002 and evaluates 5,000 candidate
model-group allocations. It selects an allocation based on class-level
listing proportions, without using model performance.

Assertions check that models and listings do not cross split boundaries
and that each split contains all three body types.

### Generated file locations

The notebook writes cleaned images and data files to:
`/content/DVM_Cleaned_Data/`

The final archive is written to:
`/content/DVM_Cleaned_Data.zip`

It does not automatically write into a cloned repository's DATA/ or
OUTPUT/ folders. The exported CSV, JSON, and license files are copied
into DATA/ manually, and the complete ZIP is attached to the release.

The current notebook does not generate model results or analysis figures.
OUTPUT/ is reserved for those later deliverables.

### Data format and licensing

The current cleaning workflow uses CSV manifests and JSON configuration.
No Excel workbook is required.

Adv_ID connects listing review records to image records.
Genmodel_ID connects image records to model-level split assignments.

See DATA/DATA_LICENSE.txt for dataset licensing information.

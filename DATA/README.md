# Project 3 Data

This folder contains the cleaned data manifests and saved training,
validation, and test splits for our DVM-CAR vehicle classification project.

## Download the complete dataset

Download `DVM_Cleaned_Data.zip` from:
https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0

Select the named dataset ZIP under Assets, not GitHub's automatically
generated Source code archives.

The dataset ZIP includes the Photos folder and the accompanying CSV,
JSON, and license files. Extract the entire ZIP and preserve its internal
folder structure and filenames.

The images are distributed through the release attachment and are not
included when downloading or cloning the repository itself.

## Files

| File | Contents |
| --- | --- |
| clean_manifest.csv | Cleaned image manifest |
| listing_review.csv | Listing review records |
| manifest_with_splits.csv | Image manifest with split assignments |
| model_split_assignments.csv | Vehicle-model split assignments |
| train_manifest.csv | Training subset |
| validation_manifest.csv | Validation subset |
| test_manifest.csv | Test subset |
| split_config.json | Saved split configuration |
| split_summary.csv | Split summary |
| DATA_LICENSE.txt | Dataset licensing information |

## Using the data

Use the provided split assignments rather than randomly splitting the
images again. These assignments keep vehicle models separated across
training, validation, and test sets.

Keep the extracted Photos folder alongside the extracted manifests.
Preserve the image filenames and subfolders when transferring the dataset.

## Data Dictionary

The image manifests contain one row per image.

| Column | Description |
| --- | --- |
| Review_ID | Identifier linking an image to the reviewed listing |
| Body_type | Vehicle category: Sedan, SUV, or Pickup |
| Maker | Vehicle manufacturer |
| Genmodel | Vehicle model name |
| Genmodel_ID | Vehicle model identifier used to keep models separated across splits |
| Adv_ID | Advertisement/listing identifier linking the three views of a vehicle |
| View | Front, Side, or Rear |
| Image_ID | Original image identifier |
| Image_name | Original image name from the source metadata |
| Predicted_viewpoint | Source viewpoint code: 0 = front, 90 or 270 = side, 180 = rear |
| Quality_check | Source quality flag; the cleaning notebook rejects retained images marked N |
| Source_relative_path | Image path recorded for the source dataset |
| Extracted_path | Image path relative to the extracted dataset folder |
| File_SHA256 | SHA-256 hash of the image file, used to verify file integrity |
| Class_id | Numeric class label: Sedan = 0, SUV = 1, Pickup = 2 |
| Filename | Exported image filename |
| Human_review_status | Review status assigned during cleaned-data export |
| Human_reviewer | Recorded reviewer |
| Human_review_date | Recorded review date |
| Split | train, validation, or test; present in the split-assigned manifests |

### Connections between files

- Adv_ID links image records to listing_review.csv.
- Genmodel_ID links image records to model_split_assignments.csv.
- Extracted_path links each image record to its image in Photos/.
- clean_manifest.csv contains cleaned records before split assignment.
- manifest_with_splits.csv adds the Split column.
- train_manifest.csv, validation_manifest.csv, and test_manifest.csv
  contain the corresponding subsets.

### Applying review decisions

The cleaning notebook reads the saved listing_review.csv and retains
listings whose Review_decision is provisional_keep. Other decisions are
excluded.

For retained listings, the notebook checks that each has exactly three
images covering Front, Side, and Rear; consistent body type and model
identity; compatible viewpoint metadata; and no Quality_check flag of N.

It verifies image hashes, readability, 300-by-300 dimensions, and absence
of duplicate decoded RGB images. Failed assertions stop execution rather
than silently dropping additional records.

Human review decisions are inputs to this notebook. The notebook applies
and validates those decisions; it does not independently assess visual
correctness.

### Evaluation limitation

The test split contains 20 pickup listings and 60 pickup images, but
these represent only one Genmodel_ID. Pickup test performance therefore
has limited coverage of different vehicle models.
The cleaning notebook is located at:
`SCRIPTS/DS4002_Project_3_Data_Cleaning.ipynb`

Refer to DATA_LICENSE.txt for dataset licensing information.

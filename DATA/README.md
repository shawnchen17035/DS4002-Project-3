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

The cleaning notebook is located at:
`SCRIPTS/DS4002_Project_3_Data_Cleaning.ipynb`

Refer to DATA_LICENSE.txt for dataset licensing information.

# Project 3 Data

## Data Summary

This project uses DVM-CAR images to investigate how viewing angle affects
classification of sedans, SUVs, and pickup trucks.

The cleaned dataset contains 2,580 images from 860 listings. Each listing
contributes one Front, one Side, and one Rear image of the vehicle.
Images are 300 × 300 pixels.

| Split | Listings | Images | Distinct vehicle models |
| --- | ---: | ---: | ---: |
| Training | 595 | 1,785 | 168 |
| Validation | 131 | 393 | 37 |
| Test | 134 | 402 | 36 |
| Total | 860 | 2,580 | 241 |

The target split proportions are 70% training, 15% validation, and 15%
test. All images belonging to a vehicle model remain in the same split,
using Genmodel_ID as the grouping variable.

## Provenance

DVM-CAR was created by Jingmin Huang, Bowei Chen, Lan Luo, Shigang Yue,
and Iadh Ounis. It contains vehicle photographs and associated metadata
collected from online sources, including UK used-car advertisements.

Dataset website:
https://deepvisualmarketing.github.io/

During data establishment, we used Ad_table (extra).csv for listing,
model, and body-type information and Image_table.csv for image records
and predicted viewpoints. Advertisement identifiers connect the records.

Source images were processed through background removal and resizing.
Viewpoint labels are predictions rather than measured camera angles.
Body-type labels and listing associations can also contain errors.

Our MI2 audit of 90 sampled photographs identified incorrect viewpoints,
incomplete vehicle images, and different vehicles within the same listing.
These findings motivated visual review and a matched three-view sample.

The current cleaning notebook begins with a prepared candidate archive
containing 4,500 images from 1,500 listings and a separate archive of
recorded review decisions. It applies those decisions, verifies retained
images, and exports the cleaned sample and fixed model-level splits.

## Download Instructions

Download the archives from:
https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0

### To use the cleaned dataset

1. Download DVM_Cleaned_Data.zip under Assets.
2. Extract the entire archive.
3. Keep Photos/ alongside the extracted CSV, JSON, and license files.
4. Preserve the image filenames and folder structure.
5. Use the supplied training, validation, and test manifests.

Each Extracted_path is relative to the extracted dataset folder and
begins with Photos/.

The images are release attachments. They are not included when cloning
the repository or downloading GitHub's automatic Source code archives.

### To reproduce cleaning

Download both input archives:

- DVM_Project3_Review_20261114_201843_029683.zip
- DVM_Review_Records.zip

Run SCRIPTS/DS4002_Project_3_Data_Cleaning.ipynb following the main
repository README. Upload the candidate archive at the first prompt
and the review archive at the second prompt.

The cleaned output ZIP is not a substitute for these input archives.

## File Inventory

| File | Contents |
| --- | --- |
| clean_manifest.csv | Cleaned image records before split assignment |
| listing_review.csv | Recorded listing review decisions |
| manifest_with_splits.csv | Cleaned image records with split assignments |
| model_split_assignments.csv | Vehicle-model split assignments |
| train_manifest.csv | Training image records |
| validation_manifest.csv | Validation image records |
| test_manifest.csv | Test image records |
| split_config.json | Split parameters and recorded package versions |
| split_summary.csv | Counts by split and body type |
| DATA_LICENSE.txt | Dataset attribution, license, and processing note |

## Data Dictionary

The image manifests contain one row per image.

| Column | Description and uncertainty |
| --- | --- |
| Review_ID | Identifier connecting an image to its reviewed listing |
| Body_type | Standardized target category: Sedan, SUV, or Pickup; source labels can contain errors |
| Maker | Vehicle manufacturer recorded in source metadata |
| Genmodel | Vehicle model name recorded in source metadata |
| Genmodel_ID | Model identifier used for splitting; a model identifier may span multiple body styles |
| Adv_ID | Advertisement/listing identifier; source listings may contain inconsistent vehicle images |
| View | Front, Side, or Rear; derived from viewpoint metadata and assessed during review |
| Image_ID | Original image identifier |
| Image_name | Original image name recorded in source metadata |
| Predicted_viewpoint | Predicted angle code: 0 = front, 90 or 270 = side, 180 = rear; predictions may be incorrect |
| Quality_check | Source quality flag; N is rejected, but a missing flag does not establish usability |
| Source_relative_path | Image path recorded for the source dataset |
| Extracted_path | Image path relative to the extracted cleaned dataset folder |
| File_SHA256 | SHA-256 image-file hash used for integrity and duplicate checks |
| Class_id | Numeric target: Sedan = 0, SUV = 1, Pickup = 2 |
| Filename | Exported image filename |
| Human_review_status | Review status assigned during cleaned-data export |
| Human_reviewer | Recorded reviewer |
| Human_review_date | Recorded review date |
| Split | train, validation, or test; present in split-assigned manifests |

The image pixels are the classifier inputs. Background removal,
cropping, lighting, and resolution can affect the visible vehicle features.

### Connections between files

- Adv_ID connects image records to listing_review.csv.
- Genmodel_ID connects image records to model_split_assignments.csv.
- Extracted_path connects image records to files in Photos/.
- manifest_with_splits.csv adds split assignments to the cleaned records.
- The train, validation, and test manifests contain the respective subsets.

The cleaning workflow uses CSV and JSON files. No Excel workbook is required.

## Review and Cleaning

The visual-review criteria established in MI2 are complete exterior views,
correct front/side/rear categories, and consistent vehicle identity within
each listing. Listings without three usable views are excluded from the
matched comparison.

The cleaning notebook applies recorded decisions by retaining listings
whose Review_decision is provisional_keep. Other decisions are excluded.
It does not perform human visual review automatically.

For retained records, it checks:

- Unique image identifiers and file hashes
- Consistent body type and model within each listing
- Exactly one Front, one Side, and one Rear image per listing
- Agreement between viewpoint codes and view labels
- No Quality_check value explicitly marked N
- Matching source-file SHA-256 hashes
- Successful decoding and 300 × 300 image dimensions
- No duplicate decoded RGB pixel hashes

Missing CSV values are represented as empty strings when read.
This is not statistical imputation. Failed assertions stop execution
rather than silently removing additional records.

## Split Construction

The notebook groups records by Genmodel_ID, uses seed 4002, and evaluates
5,000 candidate allocations. The selected allocation minimizes deviation
from class-level listing targets without using model performance.

Models, listings, and identical file hashes do not cross split boundaries.
Every partition contains all three body types.

Use the provided assignments rather than randomly splitting images again.

The exact split configuration and recorded NumPy and pandas versions are
stored in split_config.json.

## Limitations and Ethical Considerations

The source consists of UK vehicle-listing images. Results may not
generalize to other countries, vehicle populations, or photographs taken
in traffic, parking lots, or different lighting conditions.

The cleaned sample is not balanced across body types. Balanced accuracy
and class-level recall are therefore important for interpreting performance.

The test split contains 20 pickup listings and 60 pickup images, but only
one pickup vehicle model. Pickup results have limited model diversity and
may depend strongly on that held-out model.

Human review reduces labeling and identity errors but cannot guarantee
their complete removal. File hashes identify exact file duplicates, and
RGB hashes identify exact decoded-image duplicates; these checks do not
establish the absence of every near-duplicate image.

We use the photographs for vehicle classification and do not use license
plates or other identifying details to identify owners. We retain review
records and source identifiers to make filtering decisions traceable.

## License

DVM-CAR is distributed under the Creative Commons
Attribution-NonCommercial 4.0 International license.

Dataset license:
https://creativecommons.org/licenses/by-nc/4.0/

Dataset attribution and processing information are recorded in
DATA_LICENSE.txt. Project changes include filtering, sampling,
duplicate exclusion, file renaming, and split assignment.

The repository's MIT license covers original project code and
documentation; it does not replace the dataset's license.

The release archives retain the original candidate-stage processing
note. The repository copy of DATA_LICENSE.txt clarifies the completed
cleaning checks without changing the dataset license.

## References

[1] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, “DVM-CAR.”
[Online]. Available: https://deepvisualmarketing.github.io/

[2] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis,
“User manual of DVM-CAR.” [Online]. Available:
https://deepvisualmarketing.github.io/site-assets/DVM_user_manual.pdf

[3] Creative Commons, “Attribution-NonCommercial 4.0 International.”
[Online]. Available: https://creativecommons.org/licenses/by-nc/4.0/

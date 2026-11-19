# Vehicle Body-Type Classification Across Viewing Angles

**DS 4002 — Data Science Project — Project 3**  
**University of Virginia | Fall 2026 | Section 100010**  
**Team:** The Pink Panthers  
**Members:** Shawn Chen and Zichen Luo  
**Group Leader:** Shawn Chen  
**Professor:** Peter Alonzi  
**Teaching Assistant:** Naman Patel

## Project Overview

This repository documents the preparation, cleaning, exploration, and modeling workflow for classifying vehicle body types from different camera viewpoints. The analysis focuses on three classes—Sedan, SUV, and Pickup—and three matched viewpoints—Front, Side, and Rear.

**Research question:** What effect does photo viewpoint have on how accurately a model can distinguish sedans, SUVs, and pickup trucks?

**Performance goal:** Exceed the 33.3% balanced-accuracy chance benchmark for each viewpoint on vehicle models excluded from training.

Each retained listing contributes one Front, one Side, and one Rear image. Splits are grouped by `Genmodel_ID`, so a vehicle model cannot appear in more than one of the training, validation, and test partitions.

**Current status:** Metadata preparation, recorded visual review, image cleaning, fixed model-group splits, exploratory analysis, ResNet-18 fine-tuning, validation-based model selection, and held-out test evaluation are complete. The intermediate code that originally assembled the 4,500-image review archive is not included; the archive is supplied as a release input for downstream cleaning.

## Data Stages

| Stage | Contents |
| --- | --- |
| Source metadata | `Ad_table (extra).csv` and `Image_table.csv` from DVM-CAR |
| MI2 candidate pool | 10,765 Sedan, 28,667 SUV, and 580 Pickup listings with all three predicted views |
| MI2 audit template | 90 candidate images with blank visual-review fields |
| Prepared review archive | 4,500 images from 1,500 listings, supplied as a release attachment |
| Final cleaned sample | 2,580 images from 860 listings with recorded review decisions and fixed splits |

The MI2 candidate counts precede final visual cleaning and should not be confused with the final modeling dataset. The visual audit identified incorrect viewpoints, incomplete vehicle images, and inconsistent vehicle identity within listings. These findings motivated the matched three-view cleaning criteria.

### Final Dataset

| Split | Listings | Images | Distinct vehicle models |
| --- | ---: | ---: | ---: |
| Training | 595 | 1,785 | 168 |
| Validation | 131 | 393 | 37 |
| Test | 134 | 402 | 36 |
| **Total** | **860** | **2,580** | **241** |

The cleaned sample contains 395 Sedan, 371 SUV, and 94 Pickup listings. Target split proportions were 70% training, 15% validation, and 15% test; actual proportions differ slightly because model groups remain intact.

## Model Development

An ImageNet-pretrained ResNet-18 was fine-tuned as a three-class classifier. The modeling workflow used:

- 224 × 224 inputs and ImageNet normalization
- Training-only random augmentation
- Class-weighted cross-entropy to address the smaller Pickup class
- AdamW optimization and a ReduceLROnPlateau learning-rate scheduler
- Full-network fine-tuning
- Random seed 4002
- Validation macro F1 for model-setting selection and checkpointing
- Final testing only after model selection

Two learning rates were compared while weight decay was held at 0.0001:

| Learning rate | Best trial validation macro F1 |
| ---: | ---: |
| **0.001** | **0.8507** |
| 0.0003 | 0.8247 |

The selected learning rate was 0.001. After eight full-network fine-tuning epochs, the saved checkpoint achieved validation macro F1 = 0.8753 and validation balanced accuracy = 0.8510.

## Final Evaluation

| Scope | n | Balanced accuracy | Macro F1 |
| --- | ---: | ---: | ---: |
| **Overall** | **402** | **0.8246** | **0.8492** |
| Front | 134 | 0.5322 | 0.4946 |
| Side | 134 | 0.9649 | 0.9596 |
| Rear | 134 | 0.9766 | 0.9766 |

Overall test accuracy was 0.8682.

### Class-Level Test Results

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Sedan | 0.9321 | 0.8830 | 0.9069 | 171 |
| SUV | 0.7980 | 0.9240 | 0.8564 | 171 |
| Pickup | 0.9524 | 0.6667 | 0.7843 | 60 |

Pickup had high precision but lower recall, indicating that the model predicted Pickup conservatively and missed some true Pickup images.

### Interpretation by Viewpoint

Rear-view performance was strongest, closely followed by Side, while Front was substantially weaker. Side images expose silhouette, ride height, and pickup-bed structure. Rear images in this sample expose tailgate/cargo-bed geometry and vehicle proportions that help distinguish Pickups and SUVs. Front views suppress much of the vehicle-length and cargo-area information, making Sedan-versus-SUV and SUV-versus-Pickup distinctions less identifiable. The overall score therefore masks an important viewpoint-dependent failure mode.

The performance goal was exceeded for the Overall, Side, and Rear evaluations. Front balanced accuracy (0.5322) was above the 0.333 chance benchmark but remained far below the other viewpoints.

### Limitations

- The test set contains only 402 images from 134 matched listings, so viewpoint-specific estimates have substantial uncertainty.
- Pickup is the minority class; its recall is based on only 60 test images.
- The three images from a listing are correlated observations even though model-group splitting prevents cross-partition leakage.
- Dealership backgrounds, framing, lighting, and marketplace conventions may become shortcuts and limit generalization to other image domains.
- Hyperparameter search was limited to two learning rates with fixed weight decay.
- Results apply only to the three retained body-type labels and should not be generalized to excluded or ambiguous classes.

## Responsibilities

| Member | Responsibility |
| --- | --- |
| Shawn Chen | Metadata preparation, visual review, cleaning, fixed splits, exploration, and data documentation |
| Zichen Luo | ResNet-18 development, validation-based setting selection, evaluation, viewpoint confusion matrices, and interpretation |

## Section 1: Software and Platform

The notebooks use Python 3 in Google Colab on a Linux runtime. Model training was run with a T4 GPU. Local execution requires adapting Colab-specific upload/download calls and `/content` paths.

| Package | Purpose |
| --- | --- |
| pandas | Read, join, summarize, and export manifests and results |
| NumPy | Numerical operations and reproducibility controls |
| Pillow | Decode and validate images |
| matplotlib | Training curves and figures |
| seaborn | Confusion-matrix visualization |
| scikit-learn | Balanced accuracy, macro F1, reports, and confusion matrices |
| PyTorch | Model training, checkpointing, and inference |
| torchvision | ResNet-18 weights, datasets, and image transforms |

Google Colab generally provides the required packages. If needed, install them with:

```python
%pip install pandas numpy Pillow matplotlib seaborn scikit-learn torch torchvision
```

Cleaning versions are recorded in `DATA/split_config.json`. Exploration package versions are recorded in `OUTPUT/exploration_package_versions.txt`.

## Section 2: Repository Map

Placeholder `.gitkeep` files are omitted.

```text
DS4002-Project-3/
├── README.md
├── LICENSE.md
├── DATA/
│   ├── README.md
│   ├── DATA_LICENSE.txt
│   ├── candidate_matched_images.csv
│   ├── viewpoint_audit_sample.csv
│   ├── clean_manifest.csv
│   ├── listing_review.csv
│   ├── manifest_with_splits.csv
│   ├── model_split_assignments.csv
│   ├── train_manifest.csv
│   ├── validation_manifest.csv
│   ├── test_manifest.csv
│   ├── split_config.json
│   └── split_summary.csv
├── SCRIPTS/
│   ├── Metadata_Prep.ipynb
│   ├── Data_Cleaning.ipynb
│   ├── Data_Exploration.ipynb
│   └── MI3_ResNet18_Modeling.ipynb
├── OUTPUT/
│   ├── MI2 metadata and cleaned-data exploration outputs
│   ├── validation_tuning_results.csv
│   ├── training_history.csv
│   ├── test_metrics_overall_and_by_view.csv
│   ├── test_predictions.csv
│   ├── classification_report.txt
│   ├── validation_training_curve.png
│   └── confusion_matrices_by_viewpoint.png
└── REFERENCES/
    └── README.md
```

### Notebook Roles

| Notebook | Inputs | Outputs |
| --- | --- | --- |
| `Metadata_Prep.ipynb` | Original advertisement and image metadata CSVs | Candidate records, audit template, MI2 tables, and MI2 plots |
| `Data_Cleaning.ipynb` | Prepared candidate-image ZIP and review-record ZIP | Verified images, cleaned manifests, and model-group splits |
| `Data_Exploration.ipynb` | `split_summary.csv` | Cleaned-data plots, supporting tables, and package versions |
| `MI3_ResNet18_Modeling.ipynb` | `DVM_Cleaned_Data.zip` | Checkpoint, validation history, predictions, test metrics, reports, training curve, and viewpoint confusion matrices |

### Important Data Files

| File | Role |
| --- | --- |
| `clean_manifest.csv` | Final cleaned image records before split assignment |
| `listing_review.csv` | Recorded decisions used by the cleaning notebook |
| `manifest_with_splits.csv` | Cleaned image records with split assignments |
| `model_split_assignments.csv` | Assignments at vehicle-model level |
| `train_manifest.csv` | Training image records |
| `validation_manifest.csv` | Validation image records |
| `test_manifest.csv` | Held-out test image records |
| `split_config.json` | Split settings and recorded cleaning-package versions |
| `split_summary.csv` | Counts by split and body type |

See `DATA/README.md` for provenance, licensing, ethical considerations, the data dictionary, and data-quality details.

## Section 3: Reproducing the Results

### A. Obtain the Final Cleaned Dataset

1. Open the repository's [data-v1.0 release](https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0).
2. Download `DVM_Cleaned_Data.zip` under **Assets**. GitHub's automatic source-code archives do not include release attachments.
3. Do not generate new random splits. Use the supplied training, validation, and test manifests.
4. Keep `Photos/` alongside the extracted CSV and JSON files.

Class labels are Sedan = 0, SUV = 1, and Pickup = 2.

### B. Reproduce Model Training and Evaluation

1. Open `SCRIPTS/MI3_ResNet18_Modeling.ipynb` in Google Colab, or use the [working Colab notebook](https://colab.research.google.com/drive/1dOhkDvE6N4zqR8mDPaf191esTuttbawQ).
2. Select a GPU runtime; the completed run used a T4 GPU.
3. Upload only `DVM_Cleaned_Data.zip` when prompted.
4. Run the MI3 setup, training, and evaluation cells in order.
5. Confirm that the validation search selects learning rate 0.001.
6. Confirm the validation checkpoint metrics and final test tables match the values reported above, allowing for small nondeterministic GPU differences.
7. Download `MI3_results.zip` before the Colab runtime ends.

The notebook writes modeling artifacts to `/content/MI3_OUTPUT/` and packages them as `/content/MI3_results.zip`. Runtime storage is temporary.

### C. Reproduce Cleaning and Split Generation

1. Download `DVM_Project3_Review_20261114_201843_029683.zip` and `DVM_Review_Records.zip` from the data release.
2. Open `SCRIPTS/Data_Cleaning.ipynb` in Google Colab.
3. Run all cleaning cells from top to bottom.
4. Upload only the candidate-image ZIP at the first prompt.
5. Upload only `DVM_Review_Records.zip` at the second prompt.
6. Continue through filtering, image verification, grouped split assignment, and export.
7. Download `DVM_Cleaned_Data.zip`.

The cleaning notebook validates unique image identifiers and hashes, consistent vehicle identity, complete Front/Side/Rear triplets, image decoding, 300 × 300 dimensions, duplicate RGB hashes, and zero model overlap between splits. Failed assertions stop execution instead of silently dropping records.

Expected checks:

| Check | Expected value |
| --- | ---: |
| Cleaned listings | 860 |
| Cleaned images | 2,580 |
| Images per listing | 3 |
| Training images | 1,785 |
| Validation images | 393 |
| Test images | 402 |
| Vehicle-model overlap between splits | 0 |

### D. Reproduce Cleaned-Data Exploration

1. Open `SCRIPTS/Data_Exploration.ipynb` in Google Colab.
2. Upload `DATA/split_summary.csv` when prompted.
3. Run the notebook and confirm both plots display.
4. Download `Project3_Exploration_Outputs.zip`.

Expected listing counts are 395 Sedan, 371 SUV, and 94 Pickup.

## Release Attachments

Download archives from the [data-v1.0 release](https://github.com/shawnchen17035/DS4002-Project-3/releases/tag/data-v1.0):

| Archive | Purpose |
| --- | --- |
| `DVM_Project3_Review_20261114_201843_029683.zip` | Prepared candidate images and `selection_manifest.csv` |
| `DVM_Review_Records.zip` | Recorded listing-review decisions |
| `DVM_Cleaned_Data.zip` | Final images, manifests, fixed splits, configuration, and license information |

Cloning the repository does not download release attachments.

## Reproducibility Boundary

The repository reproduces MI2 metadata preparation from the source CSVs and final cleaning from the supplied candidate and review archives. The intermediate code that assembled the specific 4,500-image review archive is not included. Human visual review is represented by saved decisions and is not automatically reproduced by executing the notebooks.

The modeling workflow is reproducible from `DVM_Cleaned_Data.zip` and the MI3 notebook. CUDA operations can exhibit small nondeterministic differences even with fixed seeds; reported metrics correspond to the completed T4 GPU run.

## License and Data Use

Code and repository documentation are covered by `LICENSE.md`. Dataset-specific licensing information is provided in `DATA/DATA_LICENSE.txt` and the release archive. Users should review the original DVM-CAR terms before redistributing images.

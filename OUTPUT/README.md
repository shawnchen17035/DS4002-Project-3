# Outputs

## Existing results

`eda/` preserves the original MI2 outputs without changing their values:

- `figure_1_viewpoint_coverage.png`, `figure_2_matched_model_coverage.png`
- `ad_missing_values.csv`, `image_missing_values.csv`, `duplicate_summary.csv`
- `image_counts_by_view.csv`, `listing_counts_by_view.csv`, `model_counts_by_view.csv`
- `matched_listing_summary.csv`, `pickup_model_coverage.csv`

These describe metadata candidates before revised failure filtering and visual cleaning.

`metadata_cleaning/` contains the actual new automated run on the source CSVs: missingness, stage counts, candidate coverage, two revised plots, configuration, and local package versions. Revised candidate matched counts are Sedan 10,565 /118 models, SUV 28,127 /144, Pickup 575 /13. They are not final cleaned data. Source file paths recorded in configuration reflect the local verification environment, not Colab.

## Generated after review

The cleaning notebook writes `clean_split_summary.csv` and `handoff_summary.json` after visual review. Add those actual outputs here and final CSV manifests to `DATA/processed/`. The Colab run also records its package versions. Until then, full image validity and final sample sizes are unresolved.

## Pending model results

Zichen will add training/validation history, the selected configuration, per-image test predictions, balanced accuracy/macro F1/macro precision/per-class recall by view, and normalized confusion matrices. There are no trained-model results in this repository yet.

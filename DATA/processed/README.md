# Final Data Manifests — Pending Visual Review

This folder will contain `clean_manifest.csv`, `train_manifest.csv`, `validation_manifest.csv`, `test_manifest.csv`, and `model_split_assignments.csv` exported by `01_data_cleaning.ipynb`. No final CSVs are included yet because the selected image review has not been completed.

One row represents one approved image. There must be exactly three rows per advertisement (one per view), one split per generic model, all classes in each split, unique image IDs, and no duplicate decoded pixels. `Path` is relative to the extracted `zichen_training_data.zip`; class IDs are Sedan=0, SUV=1, Pickup=2. Full column definitions are in `DATA/README.md`.

Use `DATA/DOWNLOAD_DATA.md` for source acquisition and the final image-bundle location. Do not put source ZIPs or image directories in Git. A model-training run must use the frozen manifests rather than create new image-level splits.

# Obtain the Source and Final Data

This file is the single acquisition guide. Raw files and image bundles are not stored in Git.

## Original data

1. Visit the [DVM-CAR project website](https://deepvisualmarketing.github.io/).
2. Under **Part I**, follow **Sales and specification tables (CSV)** to the [Figshare dataset](https://figshare.com/articles/figure/DVM-CAR_Dataset/19586296/2) (DOI: [10.6084/m9.figshare.19586296](https://doi.org/10.6084/m9.figshare.19586296)). Download `Image_table.csv` and the advertisement table with body labels. Our run uses the extra advertisement file saved as `Ad_table (extra).csv`, not the basic model table. If the current release only offers the ordinary ad table, preserve it separately and check that `Bodytype`, `Adv_ID`, and `Genmodel_ID` exist. Exact counts can differ across releases.
3. Under **Part II**, download the full **Car images (13.6 GB)** archive, saved as `resized_DVM_v2.zip`. The front-only archive cannot support this project.
4. Use your existing downloaded copies when available. Do not concatenate the extra and standard ad tables.
5. Upload the two CSVs to Google Drive at `MyDrive/DS4002_Project3/input/`. Keep the large image archive on your Mac. You can also put `viewpoint_audit_sample.csv` from this repo in that folder to include eligible earlier audit listings.
6. Run the cleaning notebook through Cell 4. Download its `review_queue.csv` and this repo's `SCRIPTS/extract_review_images.py` into Downloads. In Mac Terminal run `python3 ~/Downloads/extract_review_images.py`. Upload the resulting smaller `review_images.zip` to the Drive input folder, then run Cell 5. The helper only copies selected bytes; all validation/review is in Colab.
7. Follow `SCRIPTS/01_data_cleaning.ipynb`. Outputs and review decisions persist under `MyDrive/DS4002_Project3/cleaning/`.

The full archive is about 14.6 GB in Finder's decimal units. The recommended Mac helper avoids uploading it again. If it is already in Drive, the notebook can use it directly by changing `IMAGE_ZIP`. Only queued photos are extracted. The code accepts a reduced archive with the same filenames if one is prepared later.

## Final analyzed data — pending review

After review, the notebook creates `zichen_training_data.zip` containing:

- `DATA/clean_manifest.csv` and split-specific manifests
- `DATA/model_split_assignments.csv`
- `images/` with only the approved image files
- `AUDIT/` with human and technical decisions
- `OUTPUT/` with split counts and configuration
- `DATA_LICENSE.txt`

**Current status:** This archive does not exist yet; no final download link or final sample size is claimed. Before MI3 submission, add the final shared download URL, access instructions, file size, and SHA-256 below, and commit the final CSV manifests under `DATA/processed/`. Readers must be able to download the same frozen archive. A local Drive path alone is not a shareable link.

| Final bundle record | Status |
|---|---|
| Stable download URL | Pending |
| File size | Pending |
| Archive SHA-256 | Pending |
| Final listing/model counts | Pending |

To compute the bundle checksum after export on your Mac:

```bash
shasum -a 256 zichen_training_data.zip
```

Code is MIT licensed; DVM-CAR source/derived images and metadata remain **CC BY-NC 4.0**, with attribution to Huang, Chen, Luo, Yue, and Ounis. See [license](https://creativecommons.org/licenses/by-nc/4.0/).

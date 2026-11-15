# Scripts and Execution Order

1. **`01_data_cleaning.ipynb`** — Shawn runs this in Colab. It loads source metadata, prepares a deterministic queue, checks queued files, offers a visual-review interface, and exports approved triplets with fixed model-disjoint splits. CPU is sufficient. See the notebook introduction for Drive setup.
2. **`02_verify_handoff.ipynb`** — Zichen verifies the exported image/manifest package before modeling. It loads `train_df`, `validation_df`, and `test_df`; it does not fit ResNet-18.
3. **Training/evaluation notebook — pending Zichen's work.** Add it here with the next ordered name and record actual outputs and reproduction steps. Do not claim model metrics before running it.

`data_pipeline.py` is the shared cleaning implementation. The cleaning notebook includes a generated identical copy so it works when downloaded from a private repository without authenticating from Colab. If modifying the implementation, update the corresponding notebook implementation cell as well; tests check equality. Never commit a token in notebook code or output.

`tests/test_data_pipeline.py` exercises meaningful pipeline invariants on synthetic data: human approval required, exact duplicates excluded, three matched views per listing, all classes in each split, and model isolation. Run from the repository root:

```bash
python -m unittest discover -s SCRIPTS/tests -v
```

The original MI2 notebook was not supplied in this repository. Its actual exported EDA figures and tables are preserved under `OUTPUT/eda/`. The new cleaning implementation reruns source-to-candidate processing; the original historical EDA is clearly distinguished from the stricter cleaning stage.

`extract_review_images.py` is an optional Python-standard-library helper for the Mac. Download it and the Colab-produced `review_queue.csv` into Downloads, then run `python3 ~/Downloads/extract_review_images.py`. It creates a smaller ZIP containing only queued photos from the existing full archive. It makes no cleaning decisions. If the review queue changes, regenerate the reduced ZIP.

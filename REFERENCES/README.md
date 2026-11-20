# References

This folder documents the primary data source, software documentation, model architecture, and licensing information used in DS 4002 Project 3, **Vehicle Body-Type Classification Across Viewing Angles**.

## Dataset and Data Documentation

[1] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, "DVM-CAR." [Online]. Available: https://deepvisualmarketing.github.io/

[2] J. Huang, B. Chen, L. Luo, S. Yue, and I. Ounis, "User manual of DVM-CAR." [Online]. Available: https://deepvisualmarketing.github.io/site-assets/DVM_user_manual.pdf

[3] Creative Commons, "Attribution-NonCommercial 4.0 International." [Online]. Available: https://creativecommons.org/licenses/by-nc/4.0/

## Modeling and Evaluation

[4] K. He, X. Zhang, S. Ren, and J. Sun, "Deep Residual Learning for Image Recognition," *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2016, pp. 770–778. Available: https://arxiv.org/abs/1512.03385

[5] PyTorch, "ResNet-18 — Torchvision Documentation." [Online]. Available: https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html

[6] PyTorch, "CrossEntropyLoss — PyTorch Documentation." [Online]. Available: https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html

[7] PyTorch, "AdamW — PyTorch Documentation." [Online]. Available: https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html

[8] Scikit-learn, "balanced_accuracy_score — Scikit-learn Documentation." [Online]. Available: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html

[9] Scikit-learn, "f1_score — Scikit-learn Documentation." [Online]. Available: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html

[10] Scikit-learn, "confusion_matrix — Scikit-learn Documentation." [Online]. Available: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html

## Project Documentation

The repository contains the following supporting materials:

- [Main README](../README.md): Research question, methods, results, repository structure, and reproduction instructions.
- [Data README](../DATA/README.md): Data provenance, data dictionary, cleaning criteria, explanatory plots, licensing, and ethical considerations.
- [Dataset License](../DATA/DATA_LICENSE.txt): DVM-CAR attribution and data-use information.
- [Repository License](../LICENSE.md): MIT license for original project code and documentation.
- [Modeling Notebook](../SCRIPTS/MI3_ResNet18_Modeling.ipynb): ResNet-18 implementation, validation-based model selection, and final evaluation.

The original DVM-CAR dataset remains subject to its own license. The repository's MIT license applies only to original project materials and does not change third-party licensing conditions.

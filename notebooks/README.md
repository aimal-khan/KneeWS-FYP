# Notebooks

This directory contains all Jupyter notebooks for the KneeWS project, developed and trained on Kaggle using the RSNA Knee Abnormality Detection dataset.

## Version Progression

| Version | File | Key Contribution | Kaggle Public AUC | OOF AUC (58 gold) | Pred Std |
|:---:|:---|:---|:---:|:---:|:---:|
| V01 | `v01-rsna-knee-2p5d-baseline.ipynb` | Initial 3-plane 2.5D EfficientNet-B0 baseline with flat rule-based weak labels | 0.613 | — | — |
| V02 | `v02-rsna-knee-2p5d-baseline.ipynb` | Fold-safe calibrated soft labels, gold weight 8, no class `pos_weight`, resumable training | — | Collapsed | ~0.05 |
| **V03** | **`v03-rsna-knee-2p5d-baseline.ipynb`** | **Hierarchical pooled state-specific soft-label priors, ordering + margin constraints, collapse diagnostic** | **0.664** | **0.632** | **0.091** |
| V04 | `v04-rsna-knee-2p5d-baseline.ipynb` | DINOv2-S ViT-S/14 backbone, laterality normalization (right knees mirrored), target-specific attention pooling head | — | — | — |

## V01 — Flat Rule Weak Labels

**Architecture:** 3-plane 2.5D EfficientNet-B0 with mean pooling per plane, concatenated features, linear multilabel head.

**Label strategy:** Multilingual report-rule NLP assigns one of three states per finding (explicit positive / explicit negative / unmentioned). All report states receive a flat soft target without calibration against gold labels.

**Outcome:** Kaggle public AUC **0.613**. Identified issues: per-class `pos_weight` caused overprediction; training not resumable across Kaggle sessions.

---

## V02 — Fold-Safe Calibrated Soft Labels *(base-rate collapse)*

**Changes over V01:**
- Fold-safe calibration: only training-fold gold rows calibrate soft targets per fold
- Gold label weight multiplied by 8×
- `pos_weight` removed to fix the V01 overprediction
- Resumable training via `*_last.pt` checkpoints
- Time-guarded session management for Kaggle's 9h runtime limit

**Failure mode (V02 collapse):** Per-label gold counts are tiny (~46 training-gold studies per fold). Shrinking every report state toward the same per-label prevalence produced reversed targets (explicit positive below unmentioned for Medial Meniscus and Effusion) and degenerate zero-support labels (Lateral OA had all three states equal). The model converged to predicting base rates for all studies — mean per-label prediction std ~0.05.

---

## V03 — Hierarchical Calibration *(current best)*

**Changes over V02:**

1. **Hierarchical empirical-Bayes shrinkage:** Each label state is shrunk toward a prior mean pooled *across all 12 labels within that state type* (positive > unmentioned > explicit_negative), not toward per-label prevalence. This stabilizes calibration when per-label gold counts are very small.

2. **Ordering + margin constraints:** Enforces `positive > unmentioned > explicit_negative` with a minimum margin, and asserts validity before training begins.

3. **15% zero-support confidence floor removed:** Zero-support states were arbitrarily given 30% confidence in V02. V03 drops this to 9%, removing false certainty.

4. **Best reference-AUC checkpoint:** In addition to the best soft-loss model, V03 saves the checkpoint maximizing rule-reference-AUC as a diagnostic artifact.

5. **Prediction-spread collapse diagnostic:** Each fold reports mean per-label std. Near-zero spread flags a V02-style collapse before submission.

**Results:** Full five-fold training completed on Kaggle. All 12 labels satisfy state ordering constraints on all 5 folds. 58-study gold OOF: mean ROC-AUC **0.632**, log loss **0.605**, pred-std **0.091**. Five-fold ensemble: Kaggle public AUC **0.664**.

**Per-class notes:** PF OA remains the weakest label (gold AUC 0.415, below chance). Several OA and meniscus labels show low variance. The next step is improving report-derived labels before increasing model capacity.

---

## V04 — DINOv2 Backbone *(implemented, not yet trained)*

**Changes over V03:**
- Backbone: **DINOv2-small (ViT-S/14)** at 224×224 input, following the leading public solutions (pilkwang DINOv2 baseline: 0.809)
- **Laterality normalization:** Right-knee studies mirrored to canonical left-knee orientation before patch embedding
- **Target-specific attention pooling:** Replaces V03's mean-pool-per-plane with a learned attention head per abnormality target, allowing the model to attend to relevant anatomical regions
- V03's weak-label calibration, fold structure, resumable training, OOF pipeline, and submission inference are carried forward unchanged

**Expected next steps:** Train on Kaggle; compare with V03 on 58-gold OOF AUC.

---

## Submission Notebook

`rsna-knee-submission.ipynb` is the shared inference notebook. Set `cfg.model_version` to `v01`, `v02`, or `v03` and attach the corresponding checkpoints. The notebook ensembles all folds from the selected version. V01–V03 share the same 3-plane 2.5D EfficientNet architecture.

---

## Configuration Reference

| Parameter | Default | Description |
|:---|:---:|:---|
| `cfg.img_size` | 320 | Input image size (px) |
| `cfg.n_planes` | 3 | Anatomical planes (Sagittal, Coronal, Axial) |
| `cfg.n_samples_per_plane` | 6 | Slice center positions sampled per plane |
| `cfg.triplet_gap` | 2 | Gap between slices in a 2.5D triplet |
| `cfg.backbone` | `efficientnet_b0` | Timm backbone identifier |
| `cfg.batch_size` | 1 | Per-GPU batch size |
| `cfg.grad_accum` | 4 | Gradient accumulation steps |
| `cfg.epochs` | 4 | Training epochs per fold |
| `cfg.folds_to_train` | `(0,1,2,3,4)` | Folds to train (set to `(0,)` for quick validation) |
| `cfg.runtime_limit_hours` | 9 | Kaggle session time guard |
| `cfg.gold_weight` | 8.0 | Weight multiplier for expert-labelled studies |

---

## Artifact Conventions

| Artifact type | Location |
|:---|:---|
| Trained checkpoints | `models/vNN/vNN_fold_K_best.pt` |
| Resumable checkpoints | `models/vNN/vNN_fold_K_last.pt` |
| Best reference-AUC checkpoint | `models/vNN/vNN_fold_K_best_reference_auc.pt` |
| OOF predictions | `results/vNN/oof_predictions_vNN.csv` |
| Submission file | `results/vNN/submission_vNN.csv` |
| Weak label table | `results/vNN/weak_labels_vNN.csv` |
| Calibration tables | `results/vNN/calibration_fold_K.csv` |

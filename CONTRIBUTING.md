# Contributing to KneeWS

Thank you for your interest in contributing to KneeWS. This document explains the conventions and workflows used in this repository.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Repository Structure](#repository-structure)
- [Branch Naming](#branch-naming)
- [Notebook Versioning](#notebook-versioning)
- [Commit Messages](#commit-messages)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold a respectful and inclusive environment.

---

## Repository Structure

```text
KneeWS/
├── assets/figures/     # Architecture and pipeline diagrams (PNG, read-only)
├── docs/               # Project documentation and proposal decks
├── notebooks/          # Versioned Kaggle notebooks (vNN-rsna-knee-*.ipynb)
├── prototypes/         # Self-contained HTML interactive demos
├── scripts/            # Standalone Python utilities and data tools
├── tests/              # Structural integrity and smoke tests
└── .github/            # CI workflows and issue/PR templates
```

**Key rules:**
- Trained model checkpoints belong under `models/vNN/` (not tracked by Git)
- Non-model outputs (OOF, submissions, calibration tables) belong under `results/vNN/` (not tracked by Git)
- Regenerable path caches and duplicate submissions are never committed

---

## Branch Naming

Use the following prefixes for branch names:

| Type | Pattern | Example |
|:---|:---|:---|
| New feature or model version | `feat/description` | `feat/v04-dinov2-backbone` |
| Bug fix | `fix/description` | `fix/v03-calibration-margin` |
| Documentation | `docs/description` | `docs/update-notebook-readme` |
| Refactoring | `refactor/description` | `refactor/dicom-pipeline` |
| CI / tooling | `ci/description` | `ci/add-lint-workflow` |

---

## Notebook Versioning

Every new model notebook must follow these conventions:

1. **Filename:** `vNN-rsna-knee-2p5d-baseline.ipynb` where `NN` is the zero-padded version number (e.g., `v04`, `v05`)
2. **No stored outputs:** Notebooks must be committed without execution outputs (`Kernel → Restart & Clear Output` before committing)
3. **Version guard at top:** The first code cell must set `MODEL_VERSION = "vNN"` and print it
4. **Backward compatibility:** Each version inherits the fold structure, calibration logic, and inference pipeline from the previous version unless explicitly documented

When adding a new version:
- Document the key change(s) in `notebooks/README.md`
- Update the version table in the root `README.md`
- Add the new version string to the `VALID_VERSIONS` list in `tests/test_smoke.py`

---

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `chore`

Examples:
```
feat(notebooks): add V04 DINOv2-S backbone with laterality normalization
fix(v03): correct margin constraint for zero-support labels
docs(readme): add key results table and architecture diagrams
ci: add notebook validation workflow
```

---

## Submitting a Pull Request

1. Fork the repository and create a branch from `main`
2. Make your changes following the conventions above
3. Ensure notebooks are committed without stored outputs
4. Run the test suite locally: `pytest tests/`
5. Run the linter: `ruff check . && black --check .`
6. Fill in the pull request template completely
7. Request a review from a team member

---

## Reporting Issues

Use the GitHub Issue tracker. Please select the appropriate template:

- **Bug report** — unexpected behavior in a script, notebook, or CI workflow
- **Feature request** — new model version, data tool, or documentation improvement

Before opening an issue, search existing issues to avoid duplicates.

---

## Questions

For questions about the project methodology or FYP process, contact the team via the GitHub Discussions tab or raise an issue with the `question` label.

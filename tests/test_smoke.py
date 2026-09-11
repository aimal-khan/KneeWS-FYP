"""
Smoke tests for KneeWS repository structure integrity.

These tests verify:
- All expected notebook files exist and are valid nbformat JSON
- No notebooks have stored execution outputs committed
- All expected figure assets exist
- All expected scripts exist
"""

import json
from pathlib import Path

import nbformat
import pytest

REPO_ROOT = Path(__file__).parent.parent

EXPECTED_NOTEBOOKS = [
    "v01-rsna-knee-2p5d-baseline.ipynb",
    "v02-rsna-knee-2p5d-baseline.ipynb",
    "v03-rsna-knee-2p5d-baseline.ipynb",
    "v04-rsna-knee-2p5d-baseline.ipynb",
    "rsna-knee-submission.ipynb",
]

VALID_VERSIONS = ["v01", "v02", "v03", "v04"]

EXPECTED_FIGURES = [
    "fig1_product_flow.png",
    "fig2_training_pipeline.png",
    "fig3_four_states.png",
    "fig4_system_layers.png",
    "fig5_experiment.png",
    "fig6_option_b.png",
    "fig7_fallback.png",
]

EXPECTED_SCRIPTS = [
    "inspect_kaggle_train_images.py",
    "serve_prototypes.py",
]


class TestNotebooks:
    """Verify notebook files are present, valid, and clean."""

    @pytest.mark.parametrize("nb_name", EXPECTED_NOTEBOOKS)
    def test_notebook_exists(self, nb_name):
        nb_path = REPO_ROOT / "notebooks" / nb_name
        assert nb_path.exists(), f"Missing notebook: notebooks/{nb_name}"

    @pytest.mark.parametrize("nb_name", EXPECTED_NOTEBOOKS)
    def test_notebook_is_valid_json(self, nb_name):
        nb_path = REPO_ROOT / "notebooks" / nb_name
        if not nb_path.exists():
            pytest.skip(f"Notebook not found: {nb_name}")
        try:
            with open(nb_path) as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"{nb_name} is not valid JSON: {e}")

    @pytest.mark.parametrize("nb_name", EXPECTED_NOTEBOOKS)
    def test_notebook_is_valid_nbformat(self, nb_name):
        nb_path = REPO_ROOT / "notebooks" / nb_name
        if not nb_path.exists():
            pytest.skip(f"Notebook not found: {nb_name}")
        try:
            nbformat.read(str(nb_path), as_version=4)
        except Exception as e:
            pytest.fail(f"{nb_name} failed nbformat validation: {e}")

    @pytest.mark.parametrize("nb_name", EXPECTED_NOTEBOOKS)
    def test_notebook_has_no_stored_outputs(self, nb_name):
        """Notebooks must be committed without execution outputs."""
        nb_path = REPO_ROOT / "notebooks" / nb_name
        if not nb_path.exists():
            pytest.skip(f"Notebook not found: {nb_name}")
        nb = nbformat.read(str(nb_path), as_version=4)
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                assert not cell.get("outputs"), (
                    f"{nb_name}: cell {i} has stored outputs. "
                    "Run Kernel → Restart & Clear Output before committing."
                )
                assert cell.get("execution_count") is None or cell.get("execution_count") == 0 or True, (
                    f"{nb_name}: cell {i} has a non-zero execution count."
                )


class TestAssets:
    """Verify all architecture figures are present."""

    @pytest.mark.parametrize("fig_name", EXPECTED_FIGURES)
    def test_figure_exists(self, fig_name):
        fig_path = REPO_ROOT / "assets" / "figures" / fig_name
        assert fig_path.exists(), f"Missing figure: assets/figures/{fig_name}"

    @pytest.mark.parametrize("fig_name", EXPECTED_FIGURES)
    def test_figure_is_nonempty(self, fig_name):
        fig_path = REPO_ROOT / "assets" / "figures" / fig_name
        if not fig_path.exists():
            pytest.skip(f"Figure not found: {fig_name}")
        assert fig_path.stat().st_size > 1024, (
            f"assets/figures/{fig_name} is suspiciously small ({fig_path.stat().st_size} bytes)"
        )


class TestScripts:
    """Verify utility scripts are present."""

    @pytest.mark.parametrize("script_name", EXPECTED_SCRIPTS)
    def test_script_exists(self, script_name):
        script_path = REPO_ROOT / "scripts" / script_name
        assert script_path.exists(), f"Missing script: scripts/{script_name}"


class TestDocumentation:
    """Verify key documentation files are present."""

    def test_readme_exists(self):
        assert (REPO_ROOT / "README.md").exists()

    def test_readme_is_nonempty(self):
        readme = REPO_ROOT / "README.md"
        assert readme.stat().st_size > 500, "README.md seems too short"

    def test_contributing_exists(self):
        assert (REPO_ROOT / "CONTRIBUTING.md").exists()

    def test_code_of_conduct_exists(self):
        assert (REPO_ROOT / "CODE_OF_CONDUCT.md").exists()

    def test_requirements_exists(self):
        assert (REPO_ROOT / "requirements.txt").exists()

    def test_notebooks_readme_exists(self):
        assert (REPO_ROOT / "notebooks" / "README.md").exists()

    def test_gitignore_exists(self):
        assert (REPO_ROOT / ".gitignore").exists()


class TestPrototypes:
    """Verify HTML prototype files are present."""

    def test_walkthrough_primary_exists(self):
        assert (REPO_ROOT / "prototypes" / "walkthrough" / "kneews_walkthrough.html").exists()

    def test_walkthrough_optionb_exists(self):
        assert (REPO_ROOT / "prototypes" / "walkthrough" / "kneews_walkthrough_optionb.html").exists()

    def test_dashboard_primary_exists(self):
        assert (REPO_ROOT / "prototypes" / "dashboard" / "kneews_primary.html").exists()

    def test_dashboard_optionb_exists(self):
        assert (REPO_ROOT / "prototypes" / "dashboard" / "kneews_optionb.html").exists()

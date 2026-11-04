from pathlib import Path
import nbformat

notebook_path = Path("notebooks/04_lead_model_Day6_Enhanced_v2.ipynb")

if notebook_path.exists():
    raise FileExistsError(
        f"STOP: {notebook_path} already exists. Nothing was overwritten."
    )

cells = [
    nbformat.v4.new_markdown_cell("""# Day 6 — Enhanced Lead Model Evaluation

**Status:** Synthetic demonstration only; business validation pending.

## Objectives
- Compare classification models.
- Examine class imbalance and probability calibration.
- Evaluate threshold sensitivity.
- Generate demonstration-only scores and a priority queue.

## Important limitations
The available prospect dataset has no verified conversion outcome.
Randomly generated labels and their metrics are synthetic demonstrations,
not actual NexziByte business performance.

A production threshold cannot be approved without validated outcomes
and documented business cost assumptions.

## Data protection
Use the Day 5 v2 feature dataset. Do not modify source or cleaned CSV files.
Use new, versioned filenames to preserve existing Day 6 deliverables.
"""),
    nbformat.v4.new_code_cell("""from pathlib import Path
import sys
import numpy as np
import pandas as pd
import sklearn
from IPython.display import display

PROJECT_ROOT = Path.cwd()
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "Day5_Feature_Dataset_v2.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "synthetic"
REPORT_DIR = PROJECT_ROOT / "reports"

print("Python:", sys.version.split()[0])
print("scikit-learn:", sklearn.__version__)
print("Dataset exists:", DATA_PATH.exists())
print("Synthetic output folder exists:", OUTPUT_DIR.exists())
print("Report folder exists:", REPORT_DIR.exists())

assert DATA_PATH.exists(), f"Required dataset not found: {DATA_PATH}"
assert OUTPUT_DIR.exists(), f"Output folder not found: {OUTPUT_DIR}"
assert REPORT_DIR.exists(), f"Report folder not found: {REPORT_DIR}"

EXPECTED_FEATURES = [
    "Industry / Sub-industry",
    "Target Customers / B2B or B2C",
    "Founded Year (Standardized)",
    "Employee Count (Numeric)",
    "Company Age (Years)",
]

df = pd.read_csv(DATA_PATH)
missing = [column for column in EXPECTED_FEATURES if column not in df.columns]
assert not missing, f"Missing expected features: {missing}"

print("Dataset shape:", df.shape)
print("Expected feature validation: PASS")
display(df[EXPECTED_FEATURES].head())
""")
]

notebook = nbformat.v4.new_notebook(
    cells=cells,
    metadata={
        "kernelspec": {
            "display_name": "Python (NexziByte BI)",
            "language": "python",
            "name": "nexzibyte-bi",
        },
        "language_info": {"name": "python"},
    },
)

nbformat.validate(notebook)
notebook_path.parent.mkdir(parents=True, exist_ok=True)
nbformat.write(notebook, notebook_path)

print("Notebook created:", notebook_path)
print("Cell count:", len(notebook.cells))
print("Notebook validation: PASS")

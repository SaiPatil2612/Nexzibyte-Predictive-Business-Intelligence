from pathlib import Path
import nbformat

NOTEBOOK_PATH = Path("notebooks/04_lead_model_Day6_Enhanced_v2.ipynb")
BACKUP_PATH = Path("notebooks/04_lead_model_Day6_Enhanced_v2_PreExtension.ipynb")
SCRIPT_PATH = Path("build_day6_workflow.py")

OUTPUT_FILES = [
    Path("data/synthetic/Day6_Enhanced_v2_Model_Comparison.csv"),
    Path("data/synthetic/Day6_Enhanced_v2_Calibration_Assessment.csv"),
    Path("data/synthetic/Day6_Enhanced_v2_Threshold_Analysis.csv"),
    Path("data/synthetic/Day6_Enhanced_v2_Scored_Output.csv"),
    Path("data/synthetic/Day6_Enhanced_v2_Priority_Queue.csv"),
    Path("models/Day6_Enhanced_v2_Demo_Model.joblib"),
    Path("reports/Day6_Enhanced_v2_Lead_Model_Evaluation.md"),
]

if not NOTEBOOK_PATH.exists():
    raise FileNotFoundError(f"Notebook not found: {NOTEBOOK_PATH}")

if not BACKUP_PATH.exists():
    raise FileNotFoundError(f"Verified backup not found: {BACKUP_PATH}")

notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
backup = nbformat.read(BACKUP_PATH, as_version=4)
nbformat.validate(notebook)
nbformat.validate(backup)

if len(notebook.cells) != 2:
    raise RuntimeError("Expected exactly two existing notebook cells.")

if len(backup.cells) != 2:
    raise RuntimeError("Backup does not have the expected two cells.")

if notebook.cells != backup.cells:
    raise RuntimeError("Notebook differs from backup. Stop for review.")

if not Path("data/processed/Day5_Feature_Dataset_v2.csv").exists():
    raise FileNotFoundError("Day 5 v2 feature dataset is missing.")

if not all(path.parent.exists() for path in OUTPUT_FILES):
    raise FileNotFoundError("One or more output directories are missing.")

existing_outputs = [str(path) for path in OUTPUT_FILES if path.exists()]
if existing_outputs:
    raise FileExistsError(
        "Refusing to overwrite existing deliverables: "
        + ", ".join(existing_outputs)
    )

print("Workflow-builder preflight: PASS")
print("Notebook and backup match.")
print("Day 5 v2 dataset exists.")
print("All output directories exist.")
print("All seven planned output paths are available.")
print("No project deliverables have been changed.")

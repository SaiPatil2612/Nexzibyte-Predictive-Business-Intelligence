from pathlib import Path
import nbformat

notebook_path = Path("notebooks/04_lead_model_Day6_Enhanced_v2.ipynb")
backup_path = Path("notebooks/04_lead_model_Day6_Enhanced_v2_PreExtension.ipynb")

if not notebook_path.exists():
    raise FileNotFoundError(f"Notebook not found: {notebook_path}")

if backup_path.exists():
    raise FileExistsError(
        f"Backup already exists: {backup_path}. Nothing was overwritten."
    )

notebook = nbformat.read(notebook_path, as_version=4)
nbformat.validate(notebook)

if len(notebook.cells) != 2:
    raise RuntimeError(
        f"Expected exactly 2 existing cells; found {len(notebook.cells)}. "
        "Stop and inspect before extending."
    )

if notebook.cells[0].cell_type != "markdown":
    raise RuntimeError("Expected the first cell to be Markdown.")

if notebook.cells[1].cell_type != "code":
    raise RuntimeError("Expected the second cell to be code.")

if "Day5_Feature_Dataset_v2.csv" not in notebook.cells[1].source:
    raise RuntimeError("The expected Day 5 v2 dataset reference was not found.")

print("Preflight checks passed.")
print("Notebook:", notebook_path)
print("Current cells:", len(notebook.cells))
print("Backup destination:", backup_path)
print("No files have been changed.")

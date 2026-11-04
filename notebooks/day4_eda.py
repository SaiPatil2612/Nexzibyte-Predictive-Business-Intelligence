from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "clean" / "Day3_Prospects_Clean.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "Day4_EDA_Summary.csv"
METADATA_FILE = ROOT / "data" / "processed" / "Day4_EDA_Metadata.json"

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Clean dataset not found: {INPUT_FILE}")

# Record the input hash so we can verify the source remains unchanged.
input_hash_before = hashlib.sha256(INPUT_FILE.read_bytes()).hexdigest()

df = pd.read_csv(INPUT_FILE)
df.columns = df.columns.str.strip()

def find_column(candidates):
    normalized = {str(c).strip().lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    return None

def add_metric(rows, category, metric, value, count=None, notes=""):
    rows.append({
        "category": category,
        "metric": metric,
        "value": value,
        "count": count,
        "notes": notes,
    })

summary = []

# General dataset profile
add_metric(summary, "dataset", "record_count", len(df))
add_metric(summary, "dataset", "column_count", len(df.columns))
add_metric(
    summary, "dataset", "rows_with_any_missing_value",
    int(df.isna().any(axis=1).sum())
)
add_metric(
    summary, "dataset", "duplicate_full_rows",
    int(df.duplicated().sum())
)

# Identify key columns using the dataset's existing names.
score_col = find_column([
    "Prospect Score", "prospect_score", "Total Score", "total_score"
])
classification_col = find_column([
    "Prospect Classification", "prospect_classification", "Classification"
])
industry_col = find_column([
    "Industry/Subindustry", "Industry / Subindustry",
    "industry_subindustry", "Industry"
])
employee_col = find_column([
    "Employee Count", "employee_count", "Employees"
])

component_candidates = [
    "Company Size Score",
    "B2B Fit Score",
    "Technology Signal Score",
    "Business Need Score",
    "Recent Business Signal Score",
    "Decision-Maker Score",
]

component_cols = []
for candidate in component_candidates:
    col = find_column([candidate])
    if col:
        component_cols.append(col)

# Prospect score distribution
if score_col:
    scores = pd.to_numeric(df[score_col], errors="coerce")
    valid_scores = scores.dropna()

    for metric, value in [
        ("minimum", valid_scores.min()),
        ("maximum", valid_scores.max()),
        ("mean", valid_scores.mean()),
        ("median", valid_scores.median()),
        ("q1", valid_scores.quantile(0.25)),
        ("q3", valid_scores.quantile(0.75)),
        ("standard_deviation", valid_scores.std()),
    ]:
        add_metric(
            summary, "prospect_score", metric,
            round(float(value), 4) if pd.notna(value) else None,
            count=len(valid_scores)
        )

    add_metric(
        summary, "prospect_score", "missing_or_non_numeric_count",
        int(scores.isna().sum()), count=len(df)
    )

    for value, count in scores.value_counts().sort_index().items():
        add_metric(
            summary, "score_frequency", str(value),
            int(count), count=int(count)
        )
else:
    print("WARNING: Prospect score column was not identified.")

# Classification counts and score summaries
if classification_col:
    for label, count in (
        df[classification_col].fillna("Missing").astype(str).value_counts().items()
    ):
        add_metric(
            summary, "classification", label,
            int(count), count=int(count)
        )

    if score_col:
        working = df[[classification_col, score_col]].copy()
        working[score_col] = pd.to_numeric(working[score_col], errors="coerce")

        for label, group in working.groupby(classification_col, dropna=False):
            values = group[score_col].dropna()
            label = "Missing" if pd.isna(label) else str(label)

            add_metric(
                summary, "classification_score", f"{label}_count",
                int(len(group)), count=int(len(group))
            )
            if not values.empty:
                add_metric(
                    summary, "classification_score", f"{label}_mean_score",
                    round(float(values.mean()), 4), count=len(values)
                )
                add_metric(
                    summary, "classification_score", f"{label}_median_score",
                    round(float(values.median()), 4), count=len(values)
                )
                add_metric(
                    summary, "classification_score", f"{label}_minimum_score",
                    float(values.min()), count=len(values)
                )
                add_metric(
                    summary, "classification_score", f"{label}_maximum_score",
                    float(values.max()), count=len(values)
                )

# Industry summaries. Original industry labels are preserved.
if industry_col:
    industry = df[industry_col].fillna("Missing").astype(str)
    add_metric(
        summary, "industry", "distinct_original_labels",
        int(industry.nunique()), count=len(df),
        notes="Original labels preserved; no taxonomy standardization applied."
    )

    industry_frame = pd.DataFrame({
        "industry": industry,
        "score": pd.to_numeric(df[score_col], errors="coerce")
        if score_col else float("nan"),
    })

    counts = industry_frame["industry"].value_counts()
    for label, count in counts.items():
        group_scores = industry_frame.loc[
            industry_frame["industry"] == label, "score"
        ].dropna()

        add_metric(
            summary, "industry_count", label,
            int(count), count=int(count)
        )
        if not group_scores.empty:
            add_metric(
                summary, "industry_score",
                f"{label} | mean_score",
                round(float(group_scores.mean()), 4),
                count=len(group_scores)
            )
            add_metric(
                summary, "industry_score",
                f"{label} | median_score",
                round(float(group_scores.median()), 4),
                count=len(group_scores)
            )

    small_categories = int((counts < 3).sum())
    small_category_records = int(counts[counts < 3].sum())
    add_metric(
        summary, "industry", "labels_with_fewer_than_3_records",
        small_categories, count=small_category_records,
        notes="Exploratory small-category count."
    )

# Employee count bands and score summaries
if employee_col:
    employees = pd.to_numeric(df[employee_col], errors="coerce")
    add_metric(
        summary, "employee_count", "missing_or_non_numeric_count",
        int(employees.isna().sum()), count=len(df)
    )
    add_metric(
        summary, "employee_count", "negative_count",
        int((employees < 0).sum()), count=len(df)
    )

    bins = [-float("inf"), 50, 200, 1000, float("inf")]
    labels = ["1-50", "51-200", "201-1000", "1001+"]
    bands = pd.cut(
        employees, bins=bins, labels=labels, right=True,
        include_lowest=True
    )

    for band in labels:
        mask = bands == band
        count = int(mask.sum())
        band_scores = (
            pd.to_numeric(df.loc[mask, score_col], errors="coerce").dropna()
            if score_col else pd.Series(dtype=float)
        )

        add_metric(
            summary, "employee_band", f"{band}_employees_count",
            count, count=count
        )
        if not band_scores.empty:
            add_metric(
                summary, "employee_band", f"{band}_employees_mean_score",
                round(float(band_scores.mean()), 4), count=len(band_scores)
            )
            add_metric(
                summary, "employee_band", f"{band}_employees_median_score",
                round(float(band_scores.median()), 4), count=len(band_scores)
            )

# Component score distributions and exploratory low-signal indicators
for col in component_cols:
    values = pd.to_numeric(df[col], errors="coerce").dropna()
    if values.empty:
        continue

    add_metric(
        summary, "component_score", f"{col} | mean",
        round(float(values.mean()), 4), count=len(values)
    )
    add_metric(
        summary, "component_score", f"{col} | median",
        round(float(values.median()), 4), count=len(values)
    )
    add_metric(
        summary, "component_score", f"{col} | minimum",
        float(values.min()), count=len(values)
    )
    add_metric(
        summary, "component_score", f"{col} | maximum",
        float(values.max()), count=len(values)
    )
    add_metric(
        summary, "component_score",
        f"{col} | count_at_maximum",
        int((values == values.max()).sum()), count=len(values)
    )

recent_col = find_column(["Recent Business Signal Score"])
decision_col = find_column(["Decision-Maker Score"])

if recent_col and decision_col:
    recent = pd.to_numeric(df[recent_col], errors="coerce")
    decision = pd.to_numeric(df[decision_col], errors="coerce")

    recent_low = recent <= 5
    decision_low = decision <= 4
    both_low = recent_low & decision_low

    add_metric(
        summary, "low_signal_review", "recent_signal_score_le_5",
        int(recent_low.sum()), count=len(df),
        notes="Exploratory threshold; not an official rule."
    )
    add_metric(
        summary, "low_signal_review", "decision_maker_score_le_4",
        int(decision_low.sum()), count=len(df),
        notes="Exploratory threshold; not an official rule."
    )
    add_metric(
        summary, "low_signal_review", "both_conditions",
        int(both_low.sum()), count=len(df),
        notes="Exploratory indicator; not a validated risk label."
    )

    if classification_col:
        for label, group in df.groupby(classification_col, dropna=False):
            label = "Missing" if pd.isna(label) else str(label)
            group_index = group.index
            add_metric(
                summary, "low_signal_by_classification",
                f"{label} | both_conditions",
                int(both_low.loc[group_index].sum()),
                count=len(group)
            )

# Export summary metrics
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary_df = pd.DataFrame(
    summary, columns=["category", "metric", "value", "count", "notes"]
)
summary_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

input_hash_after = hashlib.sha256(INPUT_FILE.read_bytes()).hexdigest()
metadata = {
    "input_file": str(INPUT_FILE.relative_to(ROOT)),
    "output_file": str(OUTPUT_FILE.relative_to(ROOT)),
    "input_sha256_before": input_hash_before,
    "input_sha256_after": input_hash_after,
    "input_unchanged_during_run": input_hash_before == input_hash_after,
    "record_count": int(len(df)),
    "column_count": int(len(df.columns)),
    "summary_metric_rows": int(len(summary_df)),
    "generated_by": "notebooks/day4_eda.py",
    "interpretation_note": (
        "Descriptive EDA only. No conversion outcomes are available to validate "
        "predictive performance. Low-signal thresholds are exploratory."
    ),
}
METADATA_FILE.write_text(
    json.dumps(metadata, indent=2), encoding="utf-8"
)

print("Day 4 EDA script completed.")
print(f"Input records: {len(df)}")
print(f"Input columns: {len(df.columns)}")
print(f"Summary rows: {len(summary_df)}")
print(f"Summary CSV: {OUTPUT_FILE}")
print(f"Metadata JSON: {METADATA_FILE}")
print(f"Input unchanged during run: {input_hash_before == input_hash_after}")
print("\nFirst 15 summary rows:")
print(summary_df.head(15).to_string(index=False))

"""
Day 5 â€” Feature Engineering
NexziByte Predictive Business Intelligence & Growth Engine

Purpose:
    Build a reproducible feature dataset and feature catalogue from the
    cleaned Day 3 dataset.

Safeguards:
    - Never modifies raw or cleaned source CSV files.
    - Preserves existing Day 5 outputs.
    - Writes new versioned output files only when they do not already exist.
    - Verifies the source hash before writing outputs.
    - Does not invent conversion labels or predictive metrics.
    - Blocks model training when a verified conversion target is unavailable.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


# =========================================================
# 1. PATHS AND CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_PATH = (
    PROJECT_ROOT
    / "data"
    / "clean"
    / "Day3_Prospects_Clean.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

FEATURE_DATASET_PATH = (
    OUTPUT_DIR / "Day5_Feature_Dataset_v2.csv"
)

FEATURE_CATALOGUE_PATH = (
    OUTPUT_DIR / "Day5_Feature_Catalogue_v2.csv"
)

READINESS_AUDIT_PATH = (
    OUTPUT_DIR / "Day5_Baseline_Readiness_Audit_v2.csv"
)

METADATA_PATH = (
    OUTPUT_DIR / "Day5_Feature_Engineering_Metadata.json"
)

REFERENCE_DATE = pd.Timestamp("2026-08-22")


# =========================================================
# 2. SOURCE FEATURE REQUIREMENTS
# =========================================================

REQUIRED_COLUMNS = [
    "Company Name",
    "Industry / Sub-industry",
    "Founded Year (Standardized)",
    "Target Customers / B2B or B2C",
    "Employee Count (Numeric)",
    "Company Size Score",
    "B2B Fit Score",
    "Technology Signal Score",
    "Business Need Score",
    "Recent Business Signal Score",
    "Decision-Maker Score",
    "Data Quality Status",
    "Employee Validation",
]

CATALOGUE_COLUMNS = [
    "Source Feature",
    "Business Definition",
    "Feature Type",
    "Modeling Notes",
]


# =========================================================
# 3. UTILITY FUNCTIONS
# =========================================================

def sha256_file(path: Path) -> str:
    """Calculate a file's SHA-256 hash without changing the file."""

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def classify_customer_segment(value: object) -> str:
    """
    Create a transparent text-derived customer-segment group.

    This function classifies wording in the source label.
    It does not independently verify the company's market strategy.
    """

    if pd.isna(value):
        return "Needs review"

    text = str(value).strip().upper()

    if not text:
        return "Needs review"

    if "B2B2C" in text:
        return "B2B2C mentioned"

    if "B2B" in text and "B2C" in text:
        return "B2B and B2C mentioned"

    if text.startswith("B2B"):
        return "B2B-led label"

    if text.startswith("B2C"):
        return "B2C-led label"

    return "Needs review"


def build_catalogue() -> pd.DataFrame:
    """Document the source and engineered features."""

    rows = [
        (
            "Company Name",
            "Company identifier used for reporting and traceability.",
            "Identifier",
            "Exclude from predictive model inputs.",
        ),
        (
            "Industry / Sub-industry",
            "Industry category supplied in the cleaned source dataset.",
            "Categorical",
            "Preserve the original label. Industry Code is nominal, not ordinal.",
        ),
        (
            "Founded Year (Standardized)",
            "Standardized company founding year.",
            "Numeric",
            "Check plausibility and source evidence.",
        ),
        (
            "Target Customers / B2B or B2C",
            "Source description of the company's target customer market.",
            "Categorical/text",
            "Preserve original wording. Derived grouping is heuristic.",
        ),
        (
            "Employee Count (Numeric)",
            "Reported numeric employee count.",
            "Numeric",
            "Employee evidence remains incomplete for four Needs Review records.",
        ),
        (
            "Company Size Score",
            "Existing company-size component score.",
            "Existing score",
            "Existing scoring input. Derivation and predictive validity require review.",
        ),
        (
            "B2B Fit Score",
            "Existing B2B-fit component score.",
            "Existing score",
            "Existing scoring input. Derivation and predictive validity require review.",
        ),
        (
            "Technology Signal Score",
            "Existing technology component score.",
            "Existing score",
            "Existing scoring input. Derivation and predictive validity require review.",
        ),
        (
            "Business Need Score",
            "Existing business-need component score.",
            "Existing score",
            "Existing scoring input. Derivation and predictive validity require review.",
        ),
        (
            "Recent Business Signal Score",
            "Existing recent-business-signal component score.",
            "Existing score",
            "No historical time series is available to calculate a trend.",
        ),
        (
            "Decision-Maker Score",
            "Existing decision-maker component score.",
            "Existing score",
            "Existing scoring input. Derivation and predictive validity require review.",
        ),
        (
            "Data Quality Status",
            "Indicates source-record quality-review status.",
            "Quality flag",
            "Audit/filtering only by default. Exclude from predictive features unless justified.",
        ),
        (
            "Employee Validation",
            "Indicates employee-data validation status.",
            "Quality flag",
            "Audit/review only by default. It is not a conversion outcome.",
        ),
        (
            "Company Age (Years)",
            "Approximate company age using the configured reference year.",
            "Derived numeric",
            "Calculated as reference year minus founding year; exact founding date is unavailable.",
        ),
        (
            "Company Age Validation",
            "Flags missing or implausible founding years.",
            "Validation flag",
            "Audit-only field; not a conversion outcome.",
        ),
        (
            "Employee Count Log1p",
            "Natural logarithm of one plus employee count.",
            "Derived numeric",
            "Reduces right-skew. Does not validate the employee-count evidence.",
        ),
        (
            "Industry Code",
            "Integer identifier for each distinct sorted industry label.",
            "Categorical encoding",
            "Nominal code only. Never interpret code magnitude as industry ranking.",
        ),
        (
            "Customer Segment Group",
            "Heuristic grouping based on wording in the customer-market label.",
            "Derived categorical",
            "Text-derived only; does not verify actual market positioning.",
        ),
        (
            "Customer Segment Code",
            "Integer identifier for each distinct sorted derived segment group.",
            "Categorical encoding",
            "Nominal code only. Never interpret code magnitude as a market ranking.",
        ),
    ]

    return pd.DataFrame(
        rows,
        columns=CATALOGUE_COLUMNS,
    )


# =========================================================
# 4. MAIN FEATURE-ENGINEERING PIPELINE
# =========================================================

def main() -> None:

    # -----------------------------------------------------
    # 4.1 Check source and output paths
    # -----------------------------------------------------

    if not SOURCE_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned source dataset not found: {SOURCE_PATH}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_paths = [
        FEATURE_DATASET_PATH,
        FEATURE_CATALOGUE_PATH,
        READINESS_AUDIT_PATH,
        METADATA_PATH,
    ]

    existing_outputs = [
        str(path)
        for path in output_paths
        if path.exists()
    ]

    if existing_outputs:
        raise FileExistsError(
            "Refusing to overwrite existing output files:\n"
            + "\n".join(existing_outputs)
            + "\nInspect or back up these files before proceeding."
        )

    # -----------------------------------------------------
    # 4.2 Capture source hash and read the source
    # -----------------------------------------------------

    source_hash_before = sha256_file(SOURCE_PATH)

    source_df = pd.read_csv(SOURCE_PATH)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in source_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required source columns are missing: {missing_columns}"
        )

    if source_df.empty:
        raise ValueError(
            "The cleaned source dataset is empty."
        )

    if source_df["Company Name"].isna().any():
        raise ValueError(
            "Company Name contains missing values."
        )

    if source_df["Company Name"].duplicated().any():
        raise ValueError(
            "Company Name is not unique in the cleaned source."
        )

    # -----------------------------------------------------
    # 4.3 Validate numeric and categorical inputs
    # -----------------------------------------------------

    employee_count = pd.to_numeric(
        source_df["Employee Count (Numeric)"],
        errors="raise",
    )

    if employee_count.isna().any():
        raise ValueError(
            "Employee Count contains missing values."
        )

    if (employee_count < 0).any():
        raise ValueError(
            "Employee Count contains negative values."
        )

    industry = source_df["Industry / Sub-industry"]

    if industry.isna().any():
        raise ValueError(
            "Industry labels contain missing values."
        )

    customer_labels = source_df[
        "Target Customers / B2B or B2C"
    ]

    if customer_labels.isna().any():
        raise ValueError(
            "Customer segment descriptions contain missing values."
        )

    # -----------------------------------------------------
    # 4.4 Load and validate the existing feature dataset
    # -----------------------------------------------------

    existing_feature_path = (
        OUTPUT_DIR / "Day5_Feature_Dataset.csv"
    )

    if existing_feature_path.exists():

        existing_df = pd.read_csv(
            existing_feature_path
        )

        if len(existing_df) != len(source_df):
            raise ValueError(
                "Existing feature dataset row count differs "
                "from the cleaned source."
            )

        if (
            existing_df["Company Name"].tolist()
            != source_df["Company Name"].tolist()
        ):
            raise ValueError(
                "Company names or row ordering differ between "
                "the existing features and cleaned source."
            )

        # Verify existing company-age values.
        if (
            "Company Age (Years)" in existing_df.columns
            and "Founded Year (Standardized)" in existing_df.columns
        ):
            expected_age = (
                REFERENCE_DATE.year
                - pd.to_numeric(
                    existing_df["Founded Year (Standardized)"],
                    errors="raise",
                )
            )

            actual_age = pd.to_numeric(
                existing_df["Company Age (Years)"],
                errors="raise",
            )

            if not expected_age.equals(actual_age):
                raise ValueError(
                    "Existing company-age values do not match "
                    "the documented reference-year calculation."
                )

        features_df = existing_df.copy()

    else:

        initial_columns = [
            "Company Name",
            "Industry / Sub-industry",
            "Founded Year (Standardized)",
            "Target Customers / B2B or B2C",
            "Employee Count (Numeric)",
            "Company Size Score",
            "B2B Fit Score",
            "Technology Signal Score",
            "Business Need Score",
            "Recent Business Signal Score",
            "Decision-Maker Score",
            "Data Quality Status",
            "Employee Validation",
        ]

        features_df = source_df[
            initial_columns
        ].copy()

        founding_year = pd.to_numeric(
            features_df["Founded Year (Standardized)"],
            errors="coerce",
        )

        features_df["Company Age (Years)"] = (
            REFERENCE_DATE.year - founding_year
        )

        features_df["Company Age Validation"] = np.where(
            founding_year.isna()
            | (founding_year < 1800)
            | (founding_year > REFERENCE_DATE.year),
            "Needs Review",
            "Valid",
        )

    # -----------------------------------------------------
    # 4.5 Engineer employee-count transformation
    # -----------------------------------------------------

    features_df["Employee Count Log1p"] = np.log1p(
        employee_count.to_numpy()
    )

    # -----------------------------------------------------
    # 4.6 Encode industry labels deterministically
    # -----------------------------------------------------

    industry_labels = sorted(
        industry.astype(str).unique().tolist()
    )

    industry_mapping = {
        label: code
        for code, label in enumerate(industry_labels)
    }

    features_df["Industry Code"] = (
        industry.astype(str)
        .map(industry_mapping)
        .to_numpy()
    )

    # -----------------------------------------------------
    # 4.7 Create and encode customer-segment groups
    # -----------------------------------------------------

    segment_groups = customer_labels.map(
        classify_customer_segment
    )

    segment_labels = sorted(
        segment_groups.unique().tolist()
    )

    segment_mapping = {
        label: code
        for code, label in enumerate(segment_labels)
    }

    features_df["Customer Segment Group"] = (
        segment_groups.to_numpy()
    )

    features_df["Customer Segment Code"] = (
        segment_groups
        .map(segment_mapping)
        .to_numpy()
    )

    # -----------------------------------------------------
    # 4.8 Build catalogue and readiness audit
    # -----------------------------------------------------

    catalogue_df = build_catalogue()

    outcome_candidates = [
        "Conversion Outcome",
        "Converted",
        "Lead Status",
        "Opportunity Won",
        "Quote Accepted",
        "Revenue",
    ]

    available_outcomes = [
        column
        for column in outcome_candidates
        if column in source_df.columns
    ]

    readiness_rows = [
        {
            "Check": "Verified conversion outcome available",
            "Result": (
                "PASS"
                if available_outcomes
                else "BLOCKED"
            ),
            "Details": (
                ", ".join(available_outcomes)
                if available_outcomes
                else (
                    "No documented conversion outcome column "
                    "exists in the cleaned source."
                )
            ),
        },
        {
            "Check": "Historical engagement or time series available",
            "Result": "BLOCKED",
            "Details": (
                "The current dataset is a single snapshot. "
                "Reliable recency, frequency, engagement and trend "
                "features cannot be derived."
            ),
        },
        {
            "Check": "Existing Prospect Score used as conversion target",
            "Result": "PASS",
            "Details": (
                "Prospect Score and Prospect Classification are not "
                "treated as verified conversion outcomes."
            ),
        },
        {
            "Check": "Quality flags excluded by default from model inputs",
            "Result": "PASS",
            "Details": (
                "Data Quality Status, Employee Validation and "
                "Company Age Validation are audit fields."
            ),
        },
        {
            "Check": "Leakage review and approved target definition",
            "Result": "BLOCKED",
            "Details": (
                "A documented business outcome and its timestamp "
                "must be approved before supervised model training."
            ),
        },
    ]

    readiness_df = pd.DataFrame(
        readiness_rows
    )

    # -----------------------------------------------------
    # 4.9 Validate the engineered dataset
    # -----------------------------------------------------

    if features_df.empty:
        raise ValueError(
            "The engineered feature dataset is empty."
        )

    if features_df["Company Name"].duplicated().any():
        raise ValueError(
            "Company Name is not unique in the engineered dataset."
        )

    if features_df.isna().any().any():

        missing_summary = (
            features_df.isna()
            .sum()
        )

        missing_summary = (
            missing_summary[missing_summary > 0]
            .to_dict()
        )

        raise ValueError(
            f"Missing values found in engineered features: "
            f"{missing_summary}"
        )

    expected_rows = len(source_df)

    if len(features_df) != expected_rows:
        raise ValueError(
            f"Row count mismatch: expected {expected_rows}, "
            f"received {len(features_df)}."
        )

    expected_log = np.log1p(
        employee_count.to_numpy()
    )

    if not np.allclose(
        features_df["Employee Count Log1p"].to_numpy(),
        expected_log,
    ):
        raise ValueError(
            "Employee Count Log1p validation failed."
        )

    expected_industry_codes = (
        industry.astype(str)
        .map(industry_mapping)
        .to_numpy()
    )

    if not np.array_equal(
        features_df["Industry Code"].to_numpy(),
        expected_industry_codes,
    ):
        raise ValueError(
            "Industry Code validation failed."
        )

    expected_segment_codes = (
        segment_groups
        .map(segment_mapping)
        .to_numpy()
    )

    if not np.array_equal(
        features_df["Customer Segment Code"].to_numpy(),
        expected_segment_codes,
    ):
        raise ValueError(
            "Customer Segment Code validation failed."
        )

    # -----------------------------------------------------
    # 4.10 Verify source integrity BEFORE writing outputs
    # -----------------------------------------------------

    source_hash_after = sha256_file(
        SOURCE_PATH
    )

    if source_hash_before != source_hash_after:
        raise RuntimeError(
            "Cleaned source hash changed during processing. "
            "No output files were written."
        )

    # -----------------------------------------------------
    # 4.11 Prepare metadata
    # -----------------------------------------------------

    metadata = {
        "created_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "source_file": str(
            SOURCE_PATH.relative_to(PROJECT_ROOT)
        ),
        "source_sha256_before": source_hash_before,
        "source_sha256_after": source_hash_after,
        "source_unchanged": (
            source_hash_before == source_hash_after
        ),
        "source_rows": int(len(source_df)),
        "feature_dataset_rows": int(len(features_df)),
        "feature_dataset_columns": int(
            len(features_df.columns)
        ),
        "feature_columns": features_df.columns.tolist(),
        "industry_code_mapping": industry_mapping,
        "customer_segment_code_mapping": segment_mapping,
        "reference_date": REFERENCE_DATE.date().isoformat(),
        "conversion_outcome_columns_found": available_outcomes,
        "model_training_status": (
            "BLOCKED: no verified conversion outcome is available."
            if not available_outcomes
            else (
                "Requires approved target definition and leakage "
                "review before training."
            )
        ),
        "limitations": [
            "Industry and customer-segment codes are nominal, not ordinal.",
            "Customer-segment groups are heuristic text-derived labels.",
            "No historical time series is available for recency, frequency, engagement or trends.",
            "No verified conversion outcome is available for supervised baseline evaluation.",
            "Existing component scores have not been validated as conversion predictors.",
            "Quality flags should not be used as predictive features by default.",
            "No predictive baseline metrics are calculated by this script.",
        ],
    }

    # -----------------------------------------------------
    # 4.12 Recheck output paths immediately before writing
    # -----------------------------------------------------

    existing_outputs = [
        str(path)
        for path in output_paths
        if path.exists()
    ]

    if existing_outputs:
        raise FileExistsError(
            "Output files appeared during processing. "
            "No outputs were written:\n"
            + "\n".join(existing_outputs)
        )

    # -----------------------------------------------------
    # 4.13 Write versioned outputs
    # -----------------------------------------------------

    features_df.to_csv(
        FEATURE_DATASET_PATH,
        index=False,
    )

    catalogue_df.to_csv(
        FEATURE_CATALOGUE_PATH,
        index=False,
    )

    readiness_df.to_csv(
        READINESS_AUDIT_PATH,
        index=False,
    )

    METADATA_PATH.write_text(
        json.dumps(
            metadata,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # -----------------------------------------------------
    # 4.14 Print completion summary
    # -----------------------------------------------------

    print("\nDay 5 feature engineering completed.")
    print("-" * 55)

    print(f"Source rows: {len(source_df)}")
    print(f"Feature dataset shape: {features_df.shape}")
    print(f"Catalogue shape: {catalogue_df.shape}")
    print(f"Readiness audit shape: {readiness_df.shape}")

    print(
        "Source unchanged: "
        f"{source_hash_before == source_hash_after}"
    )

    print("\nGenerated files:")

    print(f"Feature dataset: {FEATURE_DATASET_PATH}")
    print(f"Feature catalogue: {FEATURE_CATALOGUE_PATH}")
    print(f"Readiness audit: {READINESS_AUDIT_PATH}")
    print(f"Metadata: {METADATA_PATH}")

    print("\nModel training status:")
    print(
        "BLOCKED until a verified conversion outcome "
        "and approved target definition are available."
    )


if __name__ == "__main__":
    main()

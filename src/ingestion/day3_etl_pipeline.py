
"""
Day 3 â€” Reusable ETL and Data-Quality Pipeline
Project: NexziByte Predictive Business Intelligence & Growth Engine

Reads the original scored CSV without modifying it.
Cleans derived records, validates data, and creates QA outputs.
"""

import csv
import hashlib
import json
import sys

from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


# ---------------------------------------------------------
# 1. PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "NexziByte_Final_Scored.csv"
)

CLEAN_FILE = (
    PROJECT_ROOT
    / "data"
    / "clean"
    / "Day3_Prospects_Clean.csv"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "Day3_Data_Quality_Report.csv"
)

EXCEPTIONS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "Day3_Review_Exceptions.csv"
)

RUN_REPORT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "Day3_ETL_Run_Metadata.json"
)


# ---------------------------------------------------------
# 2. COLUMN DEFINITIONS
# ---------------------------------------------------------

SCORE_COLUMNS = [
    "Company Size Score",
    "B2B Fit Score",
    "Technology Signal Score",
    "Business Need Score",
    "Recent Business Signal Score",
    "Decision-Maker Score",
]

REQUIRED_COLUMNS = [
    "Company Name",
    "Website / Domain",
    "Date Verified",
    *SCORE_COLUMNS,
    "Prospect Score",
    "Data Quality Status",
]

CLEAN_EXTRA_COLUMNS = [
    "ETL Website Format Valid",
    "ETL Company Name Unique",
    "ETL Score Consistent",
]

REPORT_HEADERS = [
    "Check",
    "Result Count",
    "Acceptance Rule",
]

# These headers MUST match the existing exception CSV.
EXCEPTION_HEADERS = [
    "Company Name",
    "Employee Count (Numeric)",
    "Employee Validation",
    "Website Validation",
    "Data Quality Status",
    "Review Reason",
    "Recommended Action",
    "Review Outcome",
    "Day 3 Resolution",
]


# ---------------------------------------------------------
# 3. CSV HELPERS
# ---------------------------------------------------------

def read_csv(path):
    """Read a CSV file without modifying it."""

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(
                f"CSV has no header: {path}"
            )

        return list(reader.fieldnames), list(reader)


def write_csv(path, headers, rows):
    """Write a derived CSV file."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=headers,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path):
    """Return the SHA-256 hash of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


# ---------------------------------------------------------
# 4. DATA VALIDATION HELPERS
# ---------------------------------------------------------

def valid_website(value):
    """
    Validate URL format only.

    This does not establish whether the website is live
    or whether its content is accurate.
    """

    value = (value or "").strip()

    if not value:
        return False

    if any(char.isspace() for char in value):
        return False

    try:
        parsed = urlparse(value)
        host = parsed.hostname

        return (
            parsed.scheme.lower() in {"http", "https"}
            and bool(host)
            and "." in host
        )

    except ValueError:
        return False


def valid_date(value):
    """Validate dates in DD-MM-YYYY format."""

    value = (value or "").strip()

    try:
        datetime.strptime(
            value,
            "%d-%m-%Y",
        )
        return True

    except ValueError:
        return False


def normalized_name(value):
    """Normalize a company name for comparisons."""

    return (value or "").strip().casefold()


def score_is_consistent(row):
    """
    Verify that Prospect Score equals the sum of
    the six component scores.
    """

    try:
        component_total = sum(
            int(row[column].strip())
            for column in SCORE_COLUMNS
        )

        prospect_score = int(
            row["Prospect Score"].strip()
        )

        return component_total == prospect_score

    except (
        KeyError,
        TypeError,
        ValueError,
        AttributeError,
    ):
        return False


def exact_row_key(row, headers):
    """Create a key for exact duplicate-row detection."""

    return tuple(
        row.get(header, "") or ""
        for header in headers
    )


# ---------------------------------------------------------
# 5. LOAD EXISTING REVIEW EXCEPTIONS
# ---------------------------------------------------------

def load_existing_exceptions():
    """
    Load existing exception records by normalized
    company name.

    Preserve existing review explanations and outcomes.
    """

    if not EXCEPTIONS_FILE.exists():
        return {}

    headers, rows = read_csv(EXCEPTIONS_FILE)

    if not headers:
        return {}

    return {
        normalized_name(
            row.get("Company Name", "")
        ): row
        for row in rows
    }


# ---------------------------------------------------------
# 6. MAIN ETL PIPELINE
# ---------------------------------------------------------

def main():

    # -----------------------------------------------------
    # A. Verify source availability
    # -----------------------------------------------------

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Source CSV not found: {SOURCE_FILE}"
        )

    # Record the source hash before processing.
    source_hash_before = sha256_file(SOURCE_FILE)

    source_headers, source_rows = read_csv(SOURCE_FILE)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in source_headers
    ]

    if missing_columns:
        raise ValueError(
            "Required source columns are missing: "
            + ", ".join(missing_columns)
        )

    if not source_rows:
        raise ValueError(
            "The source CSV contains no data records."
        )

    # -----------------------------------------------------
    # B. Source data-quality checks
    # -----------------------------------------------------

    row_keys = [
        exact_row_key(row, source_headers)
        for row in source_rows
    ]

    exact_duplicate_rows = (
        len(row_keys) - len(set(row_keys))
    )

    missing_value_count = sum(
        1
        for row in source_rows
        for column in source_headers
        if not (row.get(column) or "").strip()
    )

    names = [
        normalized_name(
            row.get("Company Name", "")
        )
        for row in source_rows
    ]

    name_counts = Counter(
        name
        for name in names
        if name
    )

    # Count distinct company names that repeat.
    # Do not delete duplicate records automatically.
    repeated_company_names = sum(
        1
        for count in name_counts.values()
        if count > 1
    )

    # -----------------------------------------------------
    # C. Create cleaned derived records
    # -----------------------------------------------------

    clean_rows = []

    for source_row in source_rows:

        # Copy the record; never edit source_rows.
        row = dict(source_row)

        row["Company Name"] = (
            row.get("Company Name") or ""
        ).strip()

        row["Website / Domain"] = (
            row.get("Website / Domain") or ""
        ).strip()

        row["Date Verified"] = (
            row.get("Date Verified") or ""
        ).strip()

        name_key = normalized_name(
            row["Company Name"]
        )

        website_ok = valid_website(
            row["Website / Domain"]
        )

        score_ok = score_is_consistent(row)

        # Flag repeated names without deleting records.
        if name_key and name_counts[name_key] > 1:
            row["Duplicate Flag"] = "Yes"

        row["ETL Website Format Valid"] = str(
            website_ok
        )

        row["ETL Company Name Unique"] = str(
            bool(name_key)
            and name_counts[name_key] == 1
        )

        row["ETL Score Consistent"] = str(
            score_ok
        )

        # Preserve existing business validation fields
        # and Data Quality Status.
        clean_rows.append(row)

    # -----------------------------------------------------
    # D. Validate the cleaned records
    # -----------------------------------------------------

    invalid_websites = sum(
        not valid_website(
            row.get("Website / Domain", "")
        )
        for row in clean_rows
    )

    date_failures = sum(
        not valid_date(
            row.get("Date Verified", "")
        )
        for row in clean_rows
    )

    score_failures = sum(
        not score_is_consistent(row)
        for row in clean_rows
    )

    needs_review_rows = [
        row
        for row in clean_rows
        if (
            row.get("Data Quality Status") or ""
        ).strip() == "Needs Review"
    ]

    # -----------------------------------------------------
    # E. Preserve existing exception explanations
    # -----------------------------------------------------

    existing_exceptions = load_existing_exceptions()

    exceptions = []

    for row in needs_review_rows:

        name = (
            row.get("Company Name") or ""
        ).strip()

        existing = existing_exceptions.get(
            normalized_name(name),
            {},
        )

        exceptions.append({
            "Company Name": name,

            "Employee Count (Numeric)": row.get(
                "Employee Count (Numeric)",
                "",
            ),

            "Employee Validation": row.get(
                "Employee Validation",
                "",
            ),

            "Website Validation": row.get(
                "Website Validation",
                "",
            ),

            "Data Quality Status": row.get(
                "Data Quality Status",
                "",
            ),

            # Correct existing CSV column names:
            "Review Reason": existing.get(
                "Review Reason",
                "Existing record is marked Needs Review.",
            ),

            "Recommended Action": existing.get(
                "Recommended Action",
                "Review supporting evidence before changing the status.",
            ),

            "Review Outcome": existing.get(
                "Review Outcome",
                "Retained for review; no unsupported change made.",
            ),

            "Day 3 Resolution": existing.get(
                "Day 3 Resolution",
                "Existing review status preserved.",
            ),
        })

    # -----------------------------------------------------
    # F. Build the data-quality report
    # -----------------------------------------------------

    report_rows = [
        {
            "Check": "Input row count",
            "Result Count": len(source_rows),
            "Acceptance Rule": "Informational",
        },
        {
            "Check": "Output row count",
            "Result Count": len(clean_rows),
            "Acceptance Rule": "Must equal input",
        },
        {
            "Check": "Missing values in source",
            "Result Count": missing_value_count,
            "Acceptance Rule": "Review",
        },
        {
            "Check": "Exact duplicate source rows",
            "Result Count": exact_duplicate_rows,
            "Acceptance Rule": "Review",
        },
        {
            "Check": "Invalid website formats",
            "Result Count": invalid_websites,
            "Acceptance Rule": "Review",
        },
        {
            "Check": "Repeated company names",
            "Result Count": repeated_company_names,
            "Acceptance Rule": "Review; flag without deleting",
        },
        {
            "Check": "Score inconsistencies",
            "Result Count": score_failures,
            "Acceptance Rule": "Must be zero",
        },
        {
            "Check": "Date parsing failures",
            "Result Count": date_failures,
            "Acceptance Rule": "Review",
        },
        {
            "Check": "Existing Needs Review records",
            "Result Count": len(needs_review_rows),
            "Acceptance Rule": "Preserve and investigate",
        },
    ]

    # -----------------------------------------------------
    # G. Prepare clean output headers
    # -----------------------------------------------------

    clean_headers = list(source_headers)

    for column in CLEAN_EXTRA_COLUMNS:
        if column not in clean_headers:
            clean_headers.append(column)

    # -----------------------------------------------------
    # H. Integrity checks before writing
    # -----------------------------------------------------

    if len(clean_rows) != len(source_rows):
        raise RuntimeError(
            "Row-count integrity check failed."
        )

    if score_failures != 0:
        raise RuntimeError(
            "Score consistency check failed."
        )

    if date_failures != 0:
        raise RuntimeError(
            "Date validation failed."
        )

    # -----------------------------------------------------
    # I. Write derived outputs only
    # -----------------------------------------------------

    write_csv(
        CLEAN_FILE,
        clean_headers,
        clean_rows,
    )

    write_csv(
        REPORT_FILE,
        REPORT_HEADERS,
        report_rows,
    )

    write_csv(
        EXCEPTIONS_FILE,
        EXCEPTION_HEADERS,
        exceptions,
    )

    # -----------------------------------------------------
    # J. Verify source integrity
    # -----------------------------------------------------

    source_hash_after = sha256_file(SOURCE_FILE)

    source_unchanged = (
        source_hash_before == source_hash_after
    )

    metadata = {
        "pipeline": "day3_etl_pipeline.py",
        "pipeline_version": "1.1.0",
        "schema_version": "day3_prospects_v1",
        "source_file": str(SOURCE_FILE.relative_to(PROJECT_ROOT)),
        "source_format": "CSV",
        "clean_file": str(CLEAN_FILE.relative_to(PROJECT_ROOT)),
        "quality_report_file": str(REPORT_FILE.relative_to(PROJECT_ROOT)),
        "exceptions_file": str(EXCEPTIONS_FILE.relative_to(PROJECT_ROOT)),
        "source_row_count": len(source_rows),
        "output_row_count": len(clean_rows),
        "source_sha256_before": source_hash_before,
        "source_sha256_after": source_hash_after,
        "source_unchanged": source_unchanged,
        "transformations": [
            "Normalize source field values",
            "Validate website URL formats",
            "Validate date parsing",
            "Check company-name uniqueness",
            "Validate prospect score consistency",
            "Preserve existing data-quality statuses and review details",
        ],
        "checks": {
            "missing_values_in_source": missing_value_count,
            "exact_duplicate_source_rows": exact_duplicate_rows,
            "invalid_website_formats": invalid_websites,
            "repeated_company_names": repeated_company_names,
            "score_inconsistencies": score_failures,
            "date_parsing_failures": date_failures,
            "needs_review_records": len(needs_review_rows),
        },
    }

    RUN_REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RUN_REPORT_FILE.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    # -----------------------------------------------------
    # K. Print the execution summary
    # -----------------------------------------------------

    print("\nDay 3 ETL pipeline completed.")
    print(f"Input records: {len(source_rows)}")
    print(f"Output records: {len(clean_rows)}")
    print(
        f"Needs Review records: {len(needs_review_rows)}"
    )
    print(f"Score inconsistencies: {score_failures}")
    print(f"Date parsing failures: {date_failures}")
    print(f"Invalid website formats: {invalid_websites}")
    print(
        f"Repeated company names: {repeated_company_names}"
    )
    print(f"Source unchanged: {source_unchanged}")
    print(f"Source SHA-256: {source_hash_after}")
    print(f"Clean output: {CLEAN_FILE}")
    print(f"Quality report: {REPORT_FILE}")
    print(f"Exceptions: {EXCEPTIONS_FILE}")
    print(f"Run metadata: {RUN_REPORT_FILE}")

    if not source_unchanged:
        raise RuntimeError(
            "Source hash changed unexpectedly. "
            "Investigate immediately."
        )


# ---------------------------------------------------------
# 7. SCRIPT ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":

    try:
        main()

    except Exception as exc:
        print(
            f"ETL pipeline failed: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

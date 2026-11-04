import csv
import os
from datetime import datetime
from pathlib import Path

import psycopg2


ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data" / "clean" / "Day3_Prospects_Clean.csv"


def text_or_none(value):
    value = value.strip() if value else ""
    return value or None


def int_or_none(value):
    value = text_or_none(value)
    return int(value) if value is not None else None


def date_or_none(value):
    value = text_or_none(value)
    if value is None:
        return None
    return datetime.strptime(value, "%d-%m-%Y").date()


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Clean CSV not found: {CSV_PATH}")

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        expected_columns = {
            "Company Name",
            "Website / Domain",
            "Industry / Sub-industry",
            "HQ Location (City, State)",
            "Founded Year (Standardized)",
            "Products/Services",
            "Target Customers / B2B or B2C",
            "Technology Signals",
            "Recent Business Signal",
            "Decision-Maker (Name + Title)",
            "Source(s) Used",
            "Date Verified",
            "Employee Count (Numeric)",
            "Website Validation",
            "Employee Validation",
            "Duplicate Flag",
            "Data Quality Status",
            "Company Size Score",
            "B2B Fit Score",
            "Technology Signal Score",
            "Business Need Score",
            "Recent Business Signal Score",
            "Decision-Maker Score",
            "Prospect Score",
            "Prospect Classification",
        }

        if not reader.fieldnames or not expected_columns.issubset(reader.fieldnames):
            raise ValueError("CSV headers do not match the expected clean-layer schema.")

        rows = list(reader)

    if len(rows) != 180:
        raise ValueError(f"Expected 180 source records; found {len(rows)}.")

    names = [
        (row.get("Company Name") or "").strip().casefold()
        for row in rows
    ]

    if any(not name for name in names):
        raise ValueError("A record has a missing company name.")

    if len(names) != len(set(names)):
        raise ValueError("Duplicate normalized company names found; load aborted.")

    conn = psycopg2.connect(
        dbname="nexzibyte_bi_test",
        user="postgres",
        host="localhost",
        port=5432,
    )

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        (SELECT COUNT(*) FROM company),
                        (SELECT COUNT(*) FROM prospect_assessment)
                """)
                existing_company_count, existing_assessment_count = cur.fetchone()

                if existing_company_count != 0 or existing_assessment_count != 0:
                    raise RuntimeError(
                        "Target tables are not empty. Load aborted to avoid "
                        "duplicates or mixing with existing records."
                    )

                for row in rows:
                    cur.execute("""
                        INSERT INTO company (
                            company_name,
                            website_domain,
                            industry_subindustry,
                            hq_location,
                            founded_year,
                            products_services,
                            target_customer_segment,
                            technology_signals,
                            recent_business_signal,
                            decision_maker_text,
                            source_text,
                            date_verified,
                            employee_count,
                            website_validation_status,
                            employee_validation_status,
                            duplicate_flag,
                            data_quality_status
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        RETURNING company_id
                    """, (
                        (row.get("Company Name") or "").strip(),
                        text_or_none(row.get("Website / Domain")),
                        text_or_none(row.get("Industry / Sub-industry")),
                        text_or_none(row.get("HQ Location (City, State)")),
                        int_or_none(row.get("Founded Year (Standardized)")),
                        text_or_none(row.get("Products/Services")),
                        text_or_none(row.get("Target Customers / B2B or B2C")),
                        text_or_none(row.get("Technology Signals")),
                        text_or_none(row.get("Recent Business Signal")),
                        text_or_none(row.get("Decision-Maker (Name + Title)")),
                        text_or_none(row.get("Source(s) Used")),
                        date_or_none(row.get("Date Verified")),
                        int_or_none(row.get("Employee Count (Numeric)")),
                        text_or_none(row.get("Website Validation")),
                        text_or_none(row.get("Employee Validation")),
                        text_or_none(row.get("Duplicate Flag")),
                        text_or_none(row.get("Data Quality Status")),
                    ))

                    company_id = cur.fetchone()[0]

                    cur.execute("""
                        INSERT INTO prospect_assessment (
                            company_id,
                            assessed_at,
                            company_size_score,
                            b2b_fit_score,
                            technology_signal_score,
                            business_need_score,
                            recent_business_signal_score,
                            decision_maker_score,
                            prospect_score,
                            prospect_classification,
                            scoring_model_version
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s
                        )
                    """, (
                        company_id,
                        date_or_none(row.get("Date Verified")),
                        int_or_none(row.get("Company Size Score")),
                        int_or_none(row.get("B2B Fit Score")),
                        int_or_none(row.get("Technology Signal Score")),
                        int_or_none(row.get("Business Need Score")),
                        int_or_none(row.get("Recent Business Signal Score")),
                        int_or_none(row.get("Decision-Maker Score")),
                        int_or_none(row.get("Prospect Score")),
                        text_or_none(row.get("Prospect Classification")),
                        None,
                    ))

                cur.execute("""
                    SELECT
                        (SELECT COUNT(*) FROM company),
                        (SELECT COUNT(*) FROM prospect_assessment)
                """)
                company_count, assessment_count = cur.fetchone()

                if company_count != 180 or assessment_count != 180:
                    raise RuntimeError(
                        f"Unexpected final counts: companies={company_count}, "
                        f"assessments={assessment_count}"
                    )

        print("DATABASE LOAD SUCCESS")
        print(f"Source records: {len(rows)}")
        print(f"Companies inserted: {company_count}")
        print(f"Prospect assessments inserted: {assessment_count}")
        print("Each assessment is linked to its company by company_id.")
        print("Transaction committed successfully.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()

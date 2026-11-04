# Day 3 — ETL and Data Quality Report

## 1. Project Information

- **Project:** NexziByte Predictive Business Intelligence & Growth Engine
- **Day:** 3
- **Workstream:** ETL Pipeline and Data Quality Framework
- **Status:** Technical implementation complete; business validation pending.

## 2. Objective

Implement a repeatable ETL pipeline that reads the original prospect dataset, performs defined cleaning and data-quality checks, produces a clean derived dataset, and records exceptions without making unsupported business-data corrections.

## 3. Source Data

- **Source file:** `data/raw/NexziByte_Final_Scored.csv`
- **Input records:** 180
- **Source columns:** 25
- **Source modification:** None intended or performed by the ETL pipeline.
- **Source integrity:** The SHA-256 hash after execution matched the previously recorded baseline.

## 4. Implementation

The pipeline is implemented in:

`src/ingestion/day3_etl_pipeline.py`

The pipeline performs the following operations:

1. Reads the original CSV without modifying it.
2. Cleans selected text fields in the derived output.
3. Validates website URL formats.
4. Validates dates using the expected `DD-MM-YYYY` format.
5. Checks whether prospect component scores sum to the recorded Prospect Score.
6. Checks for missing source values, exact duplicate rows, and repeated company names.
7. Preserves existing `Data Quality Status` values.
8. Preserves documented explanations for records requiring review.
9. Writes the cleaned dataset, quality report, exception report, and execution metadata.

## 5. Generated Deliverables

| Deliverable | Location |
|---|---|
| ETL pipeline | `src/ingestion/day3_etl_pipeline.py` |
| Automated tests | `tests/test_day3_etl_pipeline.py` |
| Cleaned dataset | `data/clean/Day3_Prospects_Clean.csv` |
| Data-quality report | `data/processed/Day3_Data_Quality_Report.csv` |
| Review-exception report | `data/processed/Day3_Review_Exceptions.csv` |
| ETL execution metadata | `data/processed/Day3_ETL_Run_Metadata.json` |

Pre-execution backups are stored in:

`data/processed/day3_backup_before_etl/`

## 6. Data Quality Results

| Check | Result | Interpretation |
|---|---:|---|
| Input records | 180 | Source record count |
| Output records | 180 | All input records retained |
| Missing source values | 0 | No missing values detected by the implemented check |
| Exact duplicate source rows | 0 | No exact duplicate rows detected |
| Invalid website formats | 0 | All website values passed the implemented format check |
| Repeated company names | 0 | No repeated names detected by the implemented normalization |
| Score inconsistencies | 0 | No component-score sum mismatches detected |
| Date parsing failures | 0 | No date parsing failures detected |
| Existing records marked `Needs Review` | 4 | Preserved for further investigation |

### Output status distribution

| Data Quality Status | Records |
|---|---:|
| Valid | 176 |
| Needs Review | 4 |
| Total | 180 |

## 7. Exception Handling

Four existing records remain marked `Needs Review`:

- PayU India
- Wingify
- Facilio
- SpotDraft

The employee count for each record is 100, but the supplied dataset does not establish a defensible employee-count range or supporting evidence.

The exception report preserves the existing review reason, recommended action, review outcome, and Day 3 resolution.

No unsupported employee-count corrections were made, and the existing quality status was not upgraded without evidence.

## 8. Automated Testing

Automated tests were implemented in:

`tests/test_day3_etl_pipeline.py`

Command executed:

`& .\.conda-env\python.exe -m unittest discover -s tests -v`

**Observed result:**

- Tests run: 13
- Failures: 0
- Errors: 0
- Overall result: `OK`

The tests cover website-format validation, date validation, company-name normalization, and prospect-score consistency.

## 9. Source Integrity

The SHA-256 hash recorded before the ETL run was:

`1E9DB0D66D4BB45C2CBF0113A6D2207A9D0FED3C3275895C8E2A59473B29E68B`

The post-run hash matched this baseline.

The execution metadata also reported that the source remained unchanged.

## 10. Limitations and Pending Validation

1. **Employee-count evidence:** The four exception records require independent supporting evidence.
2. **Website reachability:** Website validation checks URL format only. It does not establish live reachability or verify website content.
3. **Business validation:** Business stakeholders have not yet confirmed the flagged records or approved any corrections.
4. **Automated test scope:** The 13 tests cover selected validation functions; they do not replace complete integration testing or business acceptance testing.

## 11. Completion Assessment

### Technical implementation

The ETL pipeline executed successfully, produced the expected output files, retained all 180 records, and passed all 13 automated tests.

### Business validation

Pending. The four records requiring employee-count evidence remain unresolved.

### Day 3 status

**Technical implementation complete — business validation pending.**

Final business acceptance and assignment sign-off should remain pending until the required review is completed.
## PostgreSQL Database Load and Validation

**Execution status:** PASS  
**Validation date:** 2026-10-30  
**Database:** `nexzibyte_bi_test`

### Data Load Results

| Metric | Result |
|---|---:|
| Clean CSV source records | 180 |
| Companies inserted | 180 |
| Prospect assessments inserted | 180 |
| Transaction | Committed successfully |

### Database Validation Results

| Check | Failed records | Status |
|---|---:|---|
| Missing company names | 0 | PASS |
| Duplicate normalized company names | 0 | PASS |
| Negative employee counts | 0 | PASS |
| Missing website validation statuses | 0 | PASS |
| Missing prospect scores or score components | 0 | PASS |
| Inconsistent prospect score totals | 0 | PASS |
| Orphaned prospect assessments | 0 | PASS |
| Companies without assessments | 0 | PASS |
| Missing assessment classifications | 0 | PASS |
| Companies with multiple assessments | 0 | PASS |

### Data Quality Summary

| Status | Records | Percentage |
|---|---:|---:|
| Valid | 176 | 97.78% |
| Needs Review | 4 | 2.22% |
| Total | 180 | 100% |

The four records requiring review were retained. Their supporting employee-count evidence remains subject to verification. Database structural integrity checks do not independently verify the factual accuracy of business information.

### Day 3 Sign-off

**Technical implementation:** Complete.  
**ETL and database validation:** Complete for the checks documented above.  
**Business validation:** Pending.  
**Outstanding review items:** Verify supporting evidence for the four records marked `Needs Review`.


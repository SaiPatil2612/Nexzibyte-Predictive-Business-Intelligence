# Day 4 — Exploratory Data Analysis Report

## 1. Objective

Explore the Day 3 cleaned prospect dataset to understand its structure, score distribution, industry coverage, company-size segments, and potential limitations in the scoring model.

## 2. Dataset Overview

- Input file: `data/clean/Day3_Prospects_Clean.csv`
- Records analyzed: 180
- Columns: 28
- Blank values reported by the initial profile: 0
- Prospect classifications:
  - High Potential: 129 (71.67%)
  - Medium Potential: 51 (28.33%)
- Data quality status:
  - Valid: 176
  - Needs Review: 4

The original raw CSV was not modified during this analysis.

## 3. Prospect Score Distribution

| Metric | Result |
|---|---:|
| Minimum | 55 |
| Maximum | 100 |
| Mean | 79.31 |
| Median | 80.00 |
| First quartile (Q1) | 74.00 |
| Third quartile (Q3) | 84.00 |
| Interquartile range (IQR) | 10.00 |

The score distribution is concentrated toward the higher end of the observed range. The score 84 occurs 39 times (21.67% of the dataset).

Other frequent scores include:
- 80: 18 prospects (10.00%)
- 76: 16 prospects (8.89%)
- 79: 15 prospects (8.33%)
- 69: 13 prospects (7.22%)
- 100: 9 prospects (5.00%)

These patterns warrant further investigation into the scoring rules and component combinations.

## 4. Classification Analysis

| Classification | Count | Mean score | Median score | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| High Potential | 129 | 83.83 | 84.00 | 75 | 100 |
| Medium Potential | 51 | 67.86 | 69.00 | 55 | 74 |

The observed classifications align with a score boundary at 75 in this dataset. The official business rule should be confirmed before the threshold is treated as an approved policy.

These classifications are not verified conversion probabilities. No outcome-based validation was performed during this EDA.

## 5. Industry Analysis

| Industry | Count | Mean score | Median score | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| B2B SaaS / Enterprise Software | 72 | 83.26 | 83.50 | 60 | 100 |
| AI / ML / GenAI | 52 | 74.29 | 76.00 | 55 | 90 |
| FinTech / Payments | 39 | 74.28 | 77.00 | 56 | 84 |

The three largest industry categories contain 163 of 180 prospects (90.56%).

B2B SaaS / Enterprise Software has the highest average score among these categories. This is a descriptive association and does not establish that industry causes a higher score.

The dataset contains 19 distinct original industry labels. Seventeen records belong to categories with fewer than three records. Comparisons involving these small groups should be treated cautiously.

Industry labels contain mixed and overlapping terminology. Preserve the original labels and consider a separately documented taxonomy-mapping process in future work.

## 6. Company-Size Analysis

| Employee-count range | Count | Mean score | Median score |
|---|---:|---:|---:|
| 1–50 | 0 | N/A | N/A |
| 51–200 | 35 | 74.94 | 76.00 |
| 201–1,000 | 93 | 80.22 | 80.00 |
| 1,001+ | 52 | 80.62 | 79.50 |

All 180 records were assigned to a company-size group. No missing, invalid, or negative employee counts were reported by this check.

The 201–1,000 employee group is the largest segment, containing 93 prospects. The 1,001+ group has the highest mean score, but its mean is close to that of the 201–1,000 group.

These results do not establish a causal relationship between company size and prospect score. Employee-count evidence still requires appropriate verification.

## 7. Component Score Analysis

| Component | Maximum possible score | Mean | Records at maximum |
|---|---:|---:|---:|
| Company Size Score | 20 | 17.78 | 115 (63.89%) |
| B2B Fit Score | 20 | 17.39 | 126 (70.00%) |
| Technology Signal Score | 20 | 18.38 | 136 (75.56%) |
| Business Need Score | 15 | 13.97 | 156 (86.67%) |
| Recent Business Signal Score | 15 | 6.39 | 25 (13.89%) |
| Decision-Maker Score | 10 | 5.40 | 42 (23.33%) |

Technology Signal Score has the highest mean among the six components. Business Need Score reaches its maximum for 86.67% of records.

Recent Business Signal Score and Decision-Maker Score have lower means and substantially fewer records at their maximum values.

## 8. Low-Signal Investigation

For this investigation, low-signal thresholds were defined as:
- Recent Business Signal Score <= 5
- Decision-Maker Score <= 4

These thresholds are exploratory analysis criteria, not approved business rules.

| Finding | Count | Percentage |
|---|---:|---:|
| Recent Business Signal Score <= 5 | 155 | 86.11% |
| Decision-Maker Score <= 4 | 138 | 76.67% |
| Both conditions in the same record | 137 | 76.11% |

Classification breakdown for records meeting both conditions:

| Classification | Records meeting both conditions | Total in classification |
|---|---:|---:|
| High Potential | 89 | 129 |
| Medium Potential | 48 | 51 |

A substantial proportion of records meet both low-signal criteria, including 89 High Potential prospects.

This finding warrants reviewing the scoring rubric, the availability of supporting evidence, and the relative contribution of individual components. It does not, by itself, prove that the existing scores are incorrect.

## 9. Data Quality and Limitations

The Day 3 data-quality framework reported:
- 180 input records and 180 cleaned output records.
- Four records classified as Needs Review.
- Zero score inconsistencies detected by the documented checks.
- Zero date parse failures.
- Zero invalid website formats.
- Zero repeated company names under the implemented check.

Website validation was syntactic HTTP/HTTPS format checking, not independent verification that each website or business detail is accurate.

The four Needs Review records are PayU India, Wingify, Facilio, and SpotDraft. Their employee counts require defensible supporting evidence. These values were not changed during EDA.

Additional limitations:
- No historical conversion outcomes were analyzed.
- No predictive performance metrics were calculated.
- High Potential and Medium Potential should not be interpreted as probabilities of conversion.
- Industry categories are not fully standardized.
- Observed score patterns may reflect the existing scoring rules and available evidence.

## 10. Recommendations

1. Obtain business confirmation of the prospect classification threshold.
2. Verify employee counts and other unsupported business claims for the four Needs Review records.
3. Review the scoring rubric, particularly the high frequency of maximum Business Need Scores and the concentration of overall scores at 84.
4. Investigate whether low recent-business and decision-maker signals should affect prioritization differently.
5. Develop a documented industry taxonomy while preserving the original source labels.
6. Obtain historical prospect outcomes before evaluating predictive accuracy or conversion probabilities.
7. Continue preserving the original raw CSV and keep data-quality review separate from business approval.

## 11. Day 4 Status

- Dataset profiling: Complete.
- Prospect score analysis: Complete.
- Industry analysis: Complete.
- Company-size analysis: Complete.
- Scoring-pattern investigation: Complete.
- EDA report preparation: Complete.
- Business validation: Pending.
- Final assignment sign-off: Pending.

Day 4 documents descriptive findings from the cleaned dataset. It does not independently validate the underlying business evidence or prove predictive performance.


## 12. Reproducible EDA Execution and Verification

### Execution

The reproducible EDA script was created at:
- `notebooks/day4_eda.py`

The script was executed using the project's local Python environment:
- Python executable: `.conda-env/python.exe`
- Pandas version: 3.1.0

Command executed:
`.\.conda-env\python.exe .\notebooks\day4_eda.py`

### Generated Artifacts

| Artifact | Location | Verification |
|---|---|---|
| EDA Python script | `notebooks/day4_eda.py` | Executed successfully |
| EDA summary CSV | `data/processed/Day4_EDA_Summary.csv` | File exists; 88 metric rows |
| EDA metadata JSON | `data/processed/Day4_EDA_Metadata.json` | File exists; metadata inspected |

### Execution Results

- Input records processed: 180.
- Input columns: 28.
- Summary metrics generated: 88.
- High Potential prospects: 129.
- Medium Potential prospects: 51.
- Rows with missing values reported by the script: 0.
- Duplicate full rows reported by the script: 0.
- Input integrity check: Passed.

The SHA-256 hash recorded before execution matches the hash recorded after execution. This confirms that the cleaned input file was unchanged during this script run.

### Interpretation and Limitations

The generated summary is intended to make descriptive EDA results reproducible. It does not independently verify business claims, establish the correctness of the scoring methodology, or demonstrate predictive performance.

Business validation remains pending, including confirmation of classification rules and supporting evidence for the four records identified for review.

### Day 4 Technical Status

- Descriptive EDA analysis: Complete.
- Reproducible script execution: Complete.
- Summary CSV generation and verification: Complete.
- Metadata and input-integrity verification: Complete.
- Business validation: Pending.
- Final assignment sign-off: Pending.

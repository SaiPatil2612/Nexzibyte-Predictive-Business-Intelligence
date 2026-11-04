# Day 4 — Exploratory Data Analysis Report

**Project:** NexziByte Predictive Business Intelligence & Growth Engine  
**Status:** Preliminary findings — analysis and validation ongoing

## 1. Dataset Overview

- Records analyzed: 180
- Columns: 28
- Missing values: 0
- Exact duplicate rows: 0
- Duplicate company names: 0
- Valid records: 176
- Records needing review: 4

## 2. Prospect Classification

| Classification | Companies | Percentage |
|---|---:|---:|
| High Potential | 129 | 71.7% |
| Medium Potential | 51 | 28.3% |

These classifications reflect the existing scoring system, not verified conversion probabilities.

## 3. Prospect Score Distribution

| Statistic | Value |
|---|---:|
| Mean | 79.31 |
| Median | 80 |
| Minimum | 55 |
| 25th percentile | 74 |
| 75th percentile | 84 |
| Maximum | 100 |

## 4. Score Component Findings

| Component | Mean | Maximum |
|---|---:|---:|
| Company Size Score | 17.78 | 20 |
| B2B Fit Score | 17.39 | 20 |
| Technology Signal Score | 18.38 | 20 |
| Business Need Score | 13.97 | 15 |
| Recent Business Signal Score | 6.39 | 15 |
| Decision-Maker Score | 5.40 | 10 |

Component scales differ, so comparisons must consider each component's maximum score.

## 5. Industry Distribution

There are 19 distinct industry labels. Fifteen labels contain only one company.

| Industry | Companies | Average Prospect Score |
|---|---:|---:|
| B2B SaaS / Enterprise Software | 72 | 83.26 |
| AI / ML / GenAI | 52 | 74.29 |
| FinTech / Payments | 39 | 74.28 |

The three largest labels represent 90.6% of the dataset. Industry standardization may be useful after reviewing category definitions.

These scores describe the existing scoring system, not actual sales performance.

## 6. Source Information

All 180 records contain source descriptions. Each description is distinct and may contain multiple source types, including official company pages, LinkedIn, and company-size sources.

Source standardization is needed before defensible source-level comparisons can be performed.

## 7. Scoring Consistency and Leakage Risk

All 180 Prospect Scores equal the sum of their six component scores.

High Potential scores range from 75 to 100; Medium Potential scores range from 55 to 74.

Using Prospect Score or its component scores to predict a classification derived from those scores would introduce target leakage.

## 8. Business Outcome Data Limitations

The dataset does not contain explicit historical sales conversion outcomes, quote results, revenue history, or customer-retention records.

Therefore, validated lead conversion, quote win, revenue forecasting, churn, and customer lifetime value models require additional historical business data.

## 9. Preliminary Conclusion

The dataset supports descriptive prospect analysis, score distribution analysis, and limited industry comparisons. Predictive business models must be based on appropriate historical outcome data.

**Report status:** Preliminary. Complete the remaining EDA analyses and validation before final Day 4 sign-off.
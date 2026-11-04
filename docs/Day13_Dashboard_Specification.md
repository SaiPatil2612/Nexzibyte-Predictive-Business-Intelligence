# Day 13 — Power BI Dashboard Specification

**Project:** NexziByte Predictive Business Intelligence & Growth Engine  
**Report:** `powerbi/NexziByte_Executive_Dashboard.pbix`  
**Status date:** 4 November 2026

## 1. Purpose
Provide management, Sales/BD, Operations, Delivery and Finance with a unified decision-support view across prospects, quotations, projects, customers and revenue. This is a prototype. Observed source data must be distinguished from synthetic demonstration outputs.

## 2. Seven-page specification

| Page | Purpose | Confirmed scope/content | Interpretation notes |
|---|---|---|---|
| Executive Command Center | Management overview | KPI cards and customer/quotation summary visuals; earlier project evidence recorded Won 118, Lost 137, Pending 45 across 300 synthetic quotations | Reconcile values under the current report filters before publication. Do not present synthetic results as actual NexziByte performance. |
| Sales Intelligence | Lead quality, pipeline and sales action prioritization | Page exists and was reported by the owner as working | Exact visual/field inventory should be reconciled against the saved PBIX. |
| Proposal Intelligence | Quote value, outcome, price bands, loss reasons and win risk | Total quotation value; won/lost/pending counts; proposal win rate; status analysis; price bands; loss reasons; risk review; win-probability distribution; average predicted win probability; driver coefficients | Probability and driver outputs are synthetic demonstration data. Coefficients are associations, not causal effects. |
| Project Health | Delivery delay and margin risk | Total projects, delayed projects, average delay risk, average forecast gross margin; delay and margin risk distributions; project detail table | Project-risk dataset is synthetic demonstration data. |
| Customer 360 | Customer profile, segments and growth/risk signals | Customer 360 and customer-segment datasets are included; page reported as working | Preserve source definitions and readiness limitations for recency/frequency, CLV and churn outputs. |
| Forecast & Scenarios | Expected revenue and scenario ranges | Forecast & scenario page exists and was reported as working | Use Day 8 forecast outputs, backtests and documented scenario assumptions. Do not invent actual revenue history. |
| Data & Model Health | Data readiness, model inventory, validation and lineage | Data Quality Check Results; Model Inventory & Deployment Readiness; Model Calibration & Validation Results; Model Explainability & Feature Contributions; Customer Data Readiness Audit; Data Lineage & Source Trust | Audit tables are not automatically a composite data-quality score, drift metric or live monitoring system. |

A Project Details drill-through destination is also present in the report tabs and was previously reported as tested.

## 3. Proposal Intelligence definitions and limitation
Sources include `Day11_Quotation_Anomaly_Report`, `Day7_Synthetic_Quote_Win_Probability` and `Day7_Synthetic_Quote_Driver_Analysis`.

`Proposal Win Rate` is Won Quotations divided by Won plus Lost Quotations; Pending quotations are excluded from the denominator.

**Service-category limitation:** The quotation dataset does not contain a standardized quotation-level service-category field. The prospect dataset has `Products/Services` as free text and `Industry / Sub-industry` as a company-level classification. A verified quotation-to-prospect mapping was not established. No service-category visual was fabricated. Add a standardized `Service_Category` field and validated company/quotation relationship before implementing this requirement.

Probability bands are reporting groupings, not validated commercial thresholds. Synthetic model outputs must be labeled as demonstration data.

## 4. Interactions and formatting
The assignment expects relevant slicers, cross-filtering, drill-through, page navigation, tooltip details and refresh validation. The owner reports the pages/visuals working and previously reported Project Details drill-through tested. Exact slicer inventory, tooltip configuration, cross-filter settings and refresh evidence were not fully captured here; confirm them in the validation report.

Use business-friendly titles, consistent number/percentage formats and visible synthetic-data disclosures. Do not infer causality from feature-importance values or standardized coefficients.

## 5. Outstanding requirements
1. Standardized quotation-level `Service_Category` and validated mapping.
2. Confirm whether a calculated data-quality score and explicit missingness analysis exist; the imported Day 3 report exposes `Acceptance Rule`, `Check`, `Result Count`.
3. Confirm model version and latest training date. The displayed model inventory fields did not confirm a training timestamp.
4. Confirm drift/watch indicators and prediction coverage; these were not confirmed in the imported fields shown.
5. Capture screenshots of all seven pages and the Project Details drill-through.
6. Complete relationship, DAX reconciliation, slicer/cross-filter and refresh checks.

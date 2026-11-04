# Day 13 — Dashboard Validation Report

**Project:** NexziByte Predictive Business Intelligence & Growth Engine  
**Report:** `powerbi/NexziByte_Executive_Dashboard.pbix`  
**Status date:** 4 November 2026

## 1. Summary
The project owner confirmed that the PBIX was saved and all report pages were checked and working. Proposal Intelligence and Data & Model Health were built during the current work. This report distinguishes owner-reported functional checks from independently evidenced numerical reconciliation.

## 2. Validation status

| Item | Status | Evidence / note |
|---|---|---|
| PBIX saved | Pass — owner confirmed | `powerbi/NexziByte_Executive_Dashboard.pbix` |
| Seven required pages exist | Pass — owner confirmed | Executive Command Center, Sales Intelligence, Proposal Intelligence, Project Health, Customer 360, Forecast & Scenarios, Data & Model Health |
| Pages/visuals open and work | Pass — owner confirmed | Owner stated all pages were checked and validated |
| Project Details drill-through | Previously reported tested | Reconfirm in current PBIX before submission |
| Proposal status counts | Source sample evidence available | Earlier record showed Won 118, Lost 137, Pending 45 across 300 synthetic quotation rows; recheck current filter context for formal reconciliation |
| Proposal Win Rate definition | Defined | Won / (Won + Lost), Pending excluded |
| Win-probability chart | Screenshot evidence | Synthetic demonstration probabilities |
| Proposal driver chart | Screenshot evidence | Standardized coefficients; association, not causation |
| Project Health | Screenshot evidence | Synthetic project-risk output |
| Data Quality Check Results | Screenshot evidence | Check and Result Count; no composite quality score confirmed |
| Model Inventory | Screenshot evidence | Displayed records indicate synthetic data and not-approved/business-validation states |
| Calibration table | Screenshot evidence | Displayed records are marked synthetic demonstration only |
| Explainability table | Imported and visual created | Interpret with Data_Status and method |
| Customer readiness table | Imported and visual created | Audit output, not proof of live customer-system readiness |
| Data Lineage & Source Trust | Imported with promoted headers and visual created | Trust levels are provisional |
| Service-category performance | Not implemented — documented limitation | No standardized quotation-level service category; prospect mapping unverified |
| All-page DAX reconciliation | Pending evidence | Compare measures with source tables under identical filters |
| Relationship/cardinality audit | Pending evidence | Inspect Model view and record relationship properties |
| Slicer/cross-filter audit | Pending evidence | Confirm expected interactions per page |
| Tooltip audit | Pending evidence | Confirm tooltip details where required |
| Refresh validation | Pending evidence | Run Refresh and record successful completion |
| Full screenshot pack | Pending | Save all required page screenshots |

## 3. Limitations to disclose
1. Quotation probability and driver outputs use synthetic demonstration data.
2. Project risk and forecast demonstration outputs must retain their source synthetic labels.
3. `Day11_Quotation_Anomaly_Report` contains `Company_ID`, but the prospect data has company names and uniqueness flags; verified Company_ID mapping was not established.
4. Quotation data has no standardized `Service_Category`. Prospect `Products/Services` is free text and `Industry / Sub-industry` is company-level; neither is a safe substitute without validated mapping.
5. Data lineage trust levels are provisional.
6. A composite data-quality score, explicit drift indicator, latest model training timestamp and prediction coverage KPI were not confirmed in the imported fields/screenshots.

## 4. Final technical checks
- [ ] Record every relationship, key, cardinality, cross-filter direction and active status from Model view.
- [ ] Check key uniqueness, unmatched keys and unintended many-to-many joins.
- [ ] Reconcile every displayed KPI to source data under matching filters.
- [ ] Test slicers and cross-filter behavior on every page.
- [ ] Re-test Project Details drill-through.
- [ ] Confirm business-friendly titles and number formats.
- [ ] Run Refresh and record success/date.
- [ ] Capture full-page screenshots of all seven pages and drill-through destination.
- [ ] Confirm synthetic-data disclosures are visible.

## 5. Screenshot evidence list
Save under `powerbi/screenshots/`:
- `01_Executive_Command_Center.png`
- `02_Sales_Intelligence.png`
- `03_Proposal_Intelligence.png`
- `04_Project_Health.png`
- `05_Customer_360.png`
- `06_Forecast_and_Scenarios.png`
- `07_Data_and_Model_Health.png`
- `08_Project_Details_Drillthrough.png`

## 6. Sign-off decision
**Current status:** PBIX saved and pages reported functionally checked by the owner. Four documentation drafts prepared. Do not mark the full Day 13 acceptance gate fully closed until relationship inspection, KPI reconciliation, interaction checks, refresh evidence and screenshot capture are recorded.

**Owner confirmation:** Report saved; all pages reported working and validated.  
**Outstanding:** Evidence-backed technical checks and screenshot pack.

# Day 13 — Data Model Documentation

**Project:** NexziByte Predictive Business Intelligence & Growth Engine  
**Report:** `powerbi/NexziByte_Executive_Dashboard.pbix`  
**Status date:** 4 November 2026

## 1. Evidence scope
This document records tables/fields confirmed during the Day 13 Power BI work. It does not claim a complete star schema. Exact relationship cardinality, filter direction, active status and join columns must be read from the saved PBIX Model view before final physical-model sign-off.

## 2. Confirmed imported tables

| Power BI table | Confirmed fields / purpose | Report use |
|---|---|---|
| `Day11_Quotation_Anomaly_Report` | Quote_ID, Company_ID, Quote_Date, Accepted_Date, Quote_Value, Quote_Status, Loss_Reason, Discount_Pct, Revision_Count, Engagement_Count, anomaly/review flags, Data_Status, Data_Use, Synthetic_Data_Flag | Proposal Intelligence |
| `Day7_Synthetic_Quote_Win_Probability` | Quote_ID, Quote_Value, Discount_Pct, Revision_Count, Engagement_Count, Quote_Status, Actual_Outcome, Predicted_Win_Probability, Predicted_Outcome, Synthetic_Data_Flag; calculated `Win Probability Band` | Win probability |
| `Day7_Synthetic_Quote_Driver_Analysis` | Feature, Standardized_Coefficient, Direction, Absolute_Coefficient, Dataset | Proposal driver chart |
| `Day3_Data_Quality_Report` | Acceptance Rule, Check, Result Count | Data quality checks |
| `Day12_Model_Inventory` | Model_ID, Model_Type, Use_Case, Target, Probability_Output, Calibration_Status, Explainability_Method, Production_Recommendation, Data_Type, Project_Day, Reason, Notebook | Model inventory |
| `Day12_Probability_Calibration_Checks` | Model_ID, Brier_Score, Log_Loss, Mean_Predicted_Probability, Observed_Positive_Rate, Test_Records, Data_Status, Interpretation | Calibration table |
| `Day12_Model_Explainability` | Model_ID, Feature, Explanation_Method, Explanation_Value, Value_Type, Interpretation, Data_Status | Explainability table |
| `Day10_Customer_Data_Readiness_Audit` | File, Dataset_Type, File_Exists, Data_Status, Rows, Columns, Customer_Relevant_Columns | Customer data readiness |
| `Day2_Data_Lineage_Source_Trust_FINAL` | Data Domain, Fields / Entities, Source, Source System Availability, Provisional Trust Level, Access and Validation Status, Current Evidence, Proposed Source Owner, Required Follow-up | Data lineage and trust |
| `Day10_Customer_360` | Customer-level analytical output; full field inventory not captured here | Customer 360 |
| `Day10_Customer_Segments` | Customer segment output; full field inventory not captured here | Customer segmentation |
| `Day11_Customer_Recommendations` | Customer recommendation output | Recommendations |
| `Day6_Enhanced_v2_Priority_Queue` | Lead priority output | Sales prioritization |
| `Day6_Enhanced_v2_Scored_Output` | Lead scoring output | Sales scoring |
| `Day8_Forward_Revenue_Scenarios_3M` / `_6M` / `_12M` | Forecast scenario outputs | Forecast & Scenarios |
| `Day8_Synthetic_Revenue_Forecast_3M` | Synthetic forecast output | Forecast & Scenarios |
| `Day9_Synthetic_Project_Risk_Dataset` / `Day9_Project_Risk_Register` | Project risk outputs; screenshot fields included Project_ID, Delay_Risk_Level, Delay_Days, Delay_Risk_Probability, Effort_Risk_Level, Margin_Risk_Level, Forecast_Gross_Margin_Pct, Reason_Codes | Project Health |

This is a confirmed working inventory, not necessarily every table in the PBIX.

## 3. Relationship and join constraints
- A `Customer 360`–`Customer Segments` relationship was previously reported as created. Exact key, cardinality and filter direction are not established in the current evidence; verify in Model view.
- `Day11_Quotation_Anomaly_Report` contains `Company_ID`; synthetic quotation IDs include values such as `SYN-C-0001`.
- `Day3_Prospects_Clean.csv` contains company names and `ETL Company Name Unique`. The latter is a uniqueness flag, not a Company_ID mapping.
- A verified mapping between synthetic Company_ID values and prospect company records was not established. Do not join by row order or assume sequential synthetic IDs map to prospect rows.
- No quotation-to-service-category relationship was established.

## 4. Lineage and synthetic-data controls
`Day2_Data_Lineage_Source_Trust_FINAL` documents domains, entities, sources, source-system availability, provisional trust, validation status and follow-up. Trust levels are provisional. Quotation probability, quote-driver, project-risk and forecast demonstration outputs must retain synthetic-data disclosures.

## 5. Model-view sign-off checklist
Record every relationship as from-table/column → to-table/column, cardinality, cross-filter direction and active status. Check key uniqueness, unmatched keys, unintended many-to-many relationships and double counting. Keep synthetic outputs separate from actual prospect source data unless a validated key exists.

**Current status:** Table inventory and known join constraints documented; complete relationship diagram and properties still require direct PBIX Model-view evidence.

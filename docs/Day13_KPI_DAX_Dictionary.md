# Day 13 — KPI & DAX Dictionary

**Project:** NexziByte Predictive Business Intelligence & Growth Engine  
**Report:** `powerbi/NexziByte_Executive_Dashboard.pbix`  
**Status date:** 4 November 2026

## 1. Scope
This dictionary records exact DAX measures and calculated columns retained in the project work notes. Other KPI families are not given invented formulas: their existing PBIX DAX and business definitions must be inspected and copied before publication.

## 2. Confirmed quotation measures

Table: `Day11_Quotation_Anomaly_Report`

### Total Quotation Value
```dax
Total Quotation Value =
SUM('Day11_Quotation_Anomaly_Report'[Quote_Value])
```
Sum of quote values in the current filter context.

### Won Quotations
```dax
Won Quotations =
CALCULATE(
    DISTINCTCOUNT('Day11_Quotation_Anomaly_Report'[Quote_ID]),
    'Day11_Quotation_Anomaly_Report'[Quote_Status] = "Won"
)
```

### Lost Quotations
```dax
Lost Quotations =
CALCULATE(
    DISTINCTCOUNT('Day11_Quotation_Anomaly_Report'[Quote_ID]),
    'Day11_Quotation_Anomaly_Report'[Quote_Status] = "Lost"
)
```

### Pending Quotations
```dax
Pending Quotations =
CALCULATE(
    DISTINCTCOUNT('Day11_Quotation_Anomaly_Report'[Quote_ID]),
    'Day11_Quotation_Anomaly_Report'[Quote_Status] = "Pending"
)
```

### Proposal Win Rate
```dax
Proposal Win Rate =
DIVIDE(
    [Won Quotations],
    [Won Quotations] + [Lost Quotations],
    0
)
```
Won quotations divided by decided quotations (Won + Lost). Pending is excluded. Format as percentage.

### Lost Quotation Value
```dax
Lost Quotation Value =
CALCULATE(
    SUM('Day11_Quotation_Anomaly_Report'[Quote_Value]),
    'Day11_Quotation_Anomaly_Report'[Quote_Status] = "Lost"
)
```

### Average Quotation Value
```dax
Average Quotation Value =
AVERAGE('Day11_Quotation_Anomaly_Report'[Quote_Value])
```

### Total Quotations
```dax
Total Quotations =
DISTINCTCOUNT('Day11_Quotation_Anomaly_Report'[Quote_ID])
```

### Average Discount %
```dax
Average Discount % =
AVERAGE('Day11_Quotation_Anomaly_Report'[Discount_Pct])
```
Average source discount. Source values observed (e.g. 19.22) are already percentage-point-like; do not multiply by 100. Confirm the visual format in PBIX.

### Average Revisions
```dax
Average Revisions =
AVERAGE('Day11_Quotation_Anomaly_Report'[Revision_Count])
```

### Average Engagement
```dax
Average Engagement =
AVERAGE('Day11_Quotation_Anomaly_Report'[Engagement_Count])
```

`High Value Quotations` and `High Discount Quotations` were also created using 75th-percentile descriptive thresholds. Their exact full DAX text was not retained in the evidence; preserve the PBIX implementation rather than recreating from this summary. These are sample-relative flags, not approved commercial thresholds.

## 3. Confirmed calculated columns

### Quotation Price Band
Table: `Day11_Quotation_Anomaly_Report`
```dax
Quotation Price Band =
SWITCH(
    TRUE(),
    ISBLANK('Day11_Quotation_Anomaly_Report'[Quote_Value]), "Unknown",
    'Day11_Quotation_Anomaly_Report'[Quote_Value] < 50000, "Below 50K",
    'Day11_Quotation_Anomaly_Report'[Quote_Value] < 100000, "50K–100K",
    'Day11_Quotation_Anomaly_Report'[Quote_Value] < 250000, "100K–250K",
    "250K and Above"
)
```
Fixed reporting bands, not approved external pricing tiers.

### Win Probability Band
Table: `Day7_Synthetic_Quote_Win_Probability`
```dax
Win Probability Band =
SWITCH(
    TRUE(),
    ISBLANK('Day7_Synthetic_Quote_Win_Probability'[Predicted_Win_Probability]), "Unknown",
    'Day7_Synthetic_Quote_Win_Probability'[Predicted_Win_Probability] < 0.30, "Low (Below 30%)",
    'Day7_Synthetic_Quote_Win_Probability'[Predicted_Win_Probability] < 0.60, "Medium (30–60%)",
    'Day7_Synthetic_Quote_Win_Probability'[Predicted_Win_Probability] < 0.80, "High (60–80%)",
    "Very High (80%+)"
)
```
Descriptive bands for synthetic probabilities; cutoffs are not validated business thresholds.

## 4. Model output fields (not DAX measures)
| Field | Table | Meaning |
|---|---|---|
| `Predicted_Win_Probability` | `Day7_Synthetic_Quote_Win_Probability` | Synthetic model probability output |
| `Standardized_Coefficient` | `Day7_Synthetic_Quote_Driver_Analysis` | Standardized model coefficient |
| `Brier_Score` | `Day12_Probability_Calibration_Checks` | Calibration/evaluation metric |
| `Log_Loss` | `Day12_Probability_Calibration_Checks` | Probability prediction loss metric |
| `Mean_Predicted_Probability` | `Day12_Probability_Calibration_Checks` | Mean predicted probability in evaluation bin/group |
| `Observed_Positive_Rate` | `Day12_Probability_Calibration_Checks` | Observed positive rate in evaluation bin/group |
| `Test_Records` | `Day12_Probability_Calibration_Checks` | Test records represented |

## 5. KPI families requiring PBIX inspection
The assignment includes executive, sales, proposal, project, customer and forecast KPIs such as total customers, pipeline value, lead conversion, opportunity probability, on-time delivery, project margin, customer recency/frequency, CLV, churn risk, expected revenue, forecast variance and pipeline coverage. Exact formulas/definitions for these must be taken from existing PBIX measures and source definitions; no unsupported DAX is supplied here.

## 6. Calculation controls
- Use distinct entity counts where appropriate.
- Proposal Win Rate denominator is Won + Lost; Pending excluded.
- Avoid multiplying already percentage-scaled source values by 100.
- Label synthetic outputs clearly.
- Do not interpret standardized coefficients as causal effects.
- Reconcile measures against source data under matching filter context.

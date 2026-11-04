# Day 10 — Customer Intelligence Report

## 1. Executive summary

Day 10 developed a synthetic Customer 360 quotation activity profile,
descriptive customer segments, an illustrative expansion-candidate list,
and churn and Customer Lifetime Value (CLV) feasibility assessments.

**Overall status:** Technical demonstration completed; business validation pending.

**Data limitation:** The available quotation dataset is synthetic. Results must
not be represented as actual customer performance, verified churn, collected
revenue, or validated CLV.

## 2. Data readiness

- Source quotation dataset: `data/synthetic/Day7_Synthetic_Quotation_Dataset.csv`
- Quotation records: 300
- Unique companies: 300
- Quotation date range: 2026-01-02 to 2026-08-27
- Won quotations: 118
- Lost quotations: 137
- Pending quotations: 45
- Companies with multiple quotations: 0
- Verified churn outcomes: unavailable
- Actual collected revenue and customer-level cost data: unavailable

The prospect dataset does not establish verified customer transaction history.
Synthetic quotation values are not actual revenue.

## 3. Customer 360

Output: `data/processed/Day10_Customer_360.csv`

- Customer profiles: 300
- Unique company IDs: 300
- Duplicate company IDs: 0
- Missing values: 0
- Assessment date used for the inactivity proxy: 2026-10-19

The profile contains quotation count, first and last quotation dates,
quoted value summaries, quotation status counts, recency, and a provisional
180-day inactivity proxy.

Every company has one quotation. Therefore, repeat-purchase behavior and
customer retention patterns cannot be measured from this dataset.

The inactivity proxy is descriptive and is not a verified churn outcome.

## 4. Descriptive customer segmentation

Output: `data/processed/Day10_Customer_Segments.csv`

- **Inactive Quote:** 137 companies
- **Standard / Review:** 87 companies
- **Recent Activity:** 44 companies
- **High Quote Value:** 32 companies

Segments are rule-based demonstrations using quoted value and recency.
They have not been validated by business stakeholders.

## 5. Expansion candidates

Output: `data/processed/Day10_Expansion_Candidates.csv`

- Expansion candidates identified: 2
- Rule: high quoted value, a Won quotation, and quotation activity within
  the preceding 90 days of the assessment date.

These are candidates for illustrative review only. A Won quotation does not
prove that payment was collected, a service was delivered, or an upsell
opportunity exists.

## 6. Churn feasibility

Output: `data/processed/Day10_Churn_Model_Feasibility_Audit.csv`

A validated predictive churn model was not trained because:

- No company has multiple quotations in the current dataset.
- Verified churn or retention labels are unavailable.
- The current inactivity proxy is derived directly from quotation recency.
- Using that same recency calculation to predict the proxy would introduce
  target leakage.
- The data does not provide a validated future 180-day churn outcome.

The correct next step for a real model is to obtain dated longitudinal
customer activity and an approved outcome definition.

## 7. Customer Lifetime Value feasibility

Output: `data/processed/Day10_CLV_Feasibility_Assessment.csv`

A validated predictive CLV estimate cannot be calculated from the available
data. Missing inputs include actual transaction history, collected revenue,
customer-level costs, retention outcomes, a defined estimation horizon, and
an approved discount-rate assumption where required.

Quoted value may be used as a descriptive monetary proxy only. It must not be
labelled as actual CLV or collected revenue.

## 8. Deliverable validation

- PASS — Customer 360 rows match unique companies
- PASS — No duplicate company IDs
- PASS — Customer 360 has no missing values
- PASS — Segment row count matches Customer 360
- PASS — Expansion candidates follow defined rule

Missing or empty files: None

Validation checklist: `data/processed/Day10_Deliverable_Validation.csv`

## 9. Business decisions and approvals pending

1. Confirm the definition and business use of customer inactivity.
2. Obtain real customer, transaction, revenue, cost, and retention data.
3. Confirm the business-approved customer segmentation rules.
4. Validate expansion-candidate criteria with the business team.
5. Obtain Finance approval for the CLV definition and assumptions.
6. Reassess churn and CLV modelling after suitable data becomes available.

## 10. Final status

Day 10 technical demonstration deliverables are complete if all required
files and content checks pass. Business validation and production-ready
churn/CLV modelling remain pending.

All synthetic results are for demonstration only and are not evidence of
real business performance.

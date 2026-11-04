# Day 11: Recommendation and Anomaly Detection Report

## 1. Executive Summary

Day 11 implemented a rule-based customer recommendation engine,
quotation anomaly screening, project-risk anomaly screening, and a
business alert-rules catalogue.

All nine required CSV deliverables were present during the final
file audit. The outputs were generated using synthetic demonstration
data and provisional business-review rules.

**Status:** Technical deliverables completed; business validation and
threshold approval remain pending.

## 2. Scope and Objectives

- Recommend a next action for each customer profile.
- Screen quotation records for unusual values and business-rule conditions.
- Screen project records for potential delivery, effort, resource,
  margin, and delay concerns.
- Define alert conditions, severity, recommended action, and escalation.
- Save outputs and verify that required files exist.

## 3. Customer Recommendation Engine

The recommendation engine produced **300 customer
recommendation records**.

The rule-based actions include:
- Explore expansion opportunities.
- Follow up on pending quotations.
- Review customer re-engagement.
- Explore relevant follow-on services.
- Review customer needs and quotation history.

### Recommendation action counts

| Review customer re-engagement | 117 |
| Review customer needs and quotation history | 75 |
| Explore relevant follow-on services | 61 |
| Follow up on pending quotation | 45 |
| Explore expansion opportunity | 2 |

Recommendations are illustrative and depend on the available synthetic
quotation and customer-profile fields. They are not verified commercial
recommendations for real customers.

## 4. Quotation Anomaly Detection

The quotation anomaly report contains **300 records**.

### Statistical screening

The interquartile-range (IQR) screening identified
**0 quotations** as statistical outliers across the
four inspected metrics: quote value, discount percentage, revision count,
and engagement count.

No IQR flags does not prove that all records are normal or correct.
The IQR method only identifies observations outside its calculated
bounds.

### Provisional business-rule screening

- Quotations flagged by at least one business rule:
  **144**
- Quotations with no business-rule flags:
  **156**

| Business rule | Quotations flagged |
|---|---:|
| High_Discount_Review | 68 |
| High_Revisions_Review | 55 |
| Zero_Engagement_Review | 30 |
| High_Quote_Value_Review | 15 |

The business rules screen for high discounts, repeated revisions,
zero engagement, and high quotation values. Rule counts can overlap;
they must not be summed to calculate unique flagged quotations.

A review flag is not evidence of fraud, error, or a lost sale. All
thresholds are provisional and all quotation records are synthetic.

## 5. Project Risk Anomaly Detection

The project anomaly report contains **300 synthetic project
records**.

- Projects flagged by at least one proposed rule:
  **203**
- Projects with no proposed rule triggered:
  **97**

| Project anomaly rule | Projects flagged |
|---|---:|
| High_Delay_Anomaly | 62 |
| High_Effort_Overrun_Anomaly | 86 |
| High_Resource_Utilization_Anomaly | 61 |
| Low_Forecast_Margin_Anomaly | 46 |
| High_Change_Request_Anomaly | 8 |
| High_Dependency_Delay_Anomaly | 81 |
| High_Client_Delay_Anomaly | 71 |

The proposed rules screen for:
- Significant delivery delays.
- High effort overruns.
- High resource utilization.
- Low forecast gross margin.
- Multiple change requests.
- Dependency delays.
- Client-related delays.

Counts overlap because a project can trigger multiple rules. These new
anomaly flags are distinct from the existing Day 9 project-risk labels.

The thresholds are provisional business-review criteria, not approved
company policies. Flagged projects require human review.

## 6. Business Alert Rules

The alert-rules catalogue contains **11 rules**:
**5 High** and
**6 Medium**.

The catalogue includes:
- Alert ID and name.
- Data source and trigger condition.
- Severity.
- Recommended action.
- Escalation path.
- Threshold approval status.
- Synthetic-data limitation.

These rows define proposed alert conditions; they do not implement
live monitoring, automated notifications, or escalation workflows.
Business owners must approve thresholds and escalation responsibilities
before operational use.

## 7. Deliverables

The following 12 files were present and readable during the final audit:

| File | Purpose |
|---|---|
| `Day11_Customer_Recommendations.csv` | Customer-level next-action recommendations |
| `Day11_Recommendation_Summary.csv` | Recommendation summary |
| `Day11_Quotation_Anomaly_Report.csv` | Detailed quotation review flags |
| `Day11_Quotation_Anomaly_Rule_Summary.csv` | Quotation rule counts |
| `Day11_Quotation_Anomaly_Overall_Summary.csv` | Overall quotation screening counts |
| `Day11_Project_Anomaly_Report.csv` | Detailed project review flags |
| `Day11_Project_Anomaly_Rule_Summary.csv` | Project rule counts |
| `Day11_Project_Anomaly_Overall_Summary.csv` | Overall project screening counts |
| `Day11_Business_Alert_Rules.csv` | Proposed business alert catalogue |
| `Day11_Finance_Anomaly_Report.csv` | Monthly finance anomaly flags and explanations |
| `Day11_Finance_Anomaly_Rule_Summary.csv` | Finance anomaly counts by rule |
| `Day11_Finance_Anomaly_Overall_Summary.csv` | Overall finance screening summary and provisional thresholds |

## Finance Anomaly Detection

The finance demonstration analysed 36 monthly revenue records. All
36 records are synthetic demonstration data and are not verified actual
NexziByte financial results.

| Measure | Result |
|---|---:|
| Months analysed | 36 |
| Revenue-amount anomalies flagged | 0 |
| Month-over-month change anomalies flagged | 1 |
| Months with at least one anomaly | 1 |
| Months without a flagged anomaly | 35 |
| Provisional revenue lower fence | 361704.50 |
| Provisional revenue upper fence | 898707.62 |
| Provisional monthly-change lower fence | -13.40% |
| Provisional monthly-change upper fence | 16.36% |

**Month flagged for review:** May 2023.

- Revenue: 516770.21.
- Previous month's revenue: 602216.94.
- Month-over-month change: -14.19%.
- Review reason: the monthly revenue change fell below the provisional
  lower IQR fence of -13.40%.

The revenue amount itself was not flagged by the configured revenue
IQR rule. The month was flagged because its percentage change fell
outside the provisional monthly-change bounds.

This is a review candidate, not proof of an error, fraud, business
failure, or cause of the revenue movement. The thresholds are
provisional and require finance-owner review and approval before
operational use.

## 8. Limitations and Business Validation

1. The quotation, project, and finance datasets are synthetic demonstration data.
2. The customer recommendations are rule-based, not experimentally
   validated or proven to increase revenue.
3. Anomaly flags indicate review candidates, not confirmed errors,
   fraud, or operational failures.
4. The thresholds require review and approval by the relevant business
   stakeholders.
5. The alert catalogue does not send live notifications.
6. Real operational use requires validated source data, approved
   definitions, appropriate access controls, and monitoring.
7. Business impact and predictive performance have not been established
   by this demonstration.

## 9. Final Status

**Technical status:** Day 11 outputs generated and required-file audit
passed.

**Business status:** Validation pending. Threshold approval and review
of recommendations remain outstanding.

**Data status:** Synthetic demonstration data; not verified real-business
results.

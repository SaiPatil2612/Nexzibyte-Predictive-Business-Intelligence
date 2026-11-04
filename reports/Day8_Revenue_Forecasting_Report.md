# Day 8 ? Revenue Forecasting Report

## 1. Executive Summary

Day 8 completed a revenue-data readiness screening, synthetic monthly revenue
demonstration, comparison of three forecasting baselines, rolling-origin
backtesting, empirical error diagnostics, and 3-, 6-, and 12-month forecast
and scenario outputs.

**Data integrity statement:** All model evaluation and forecast results in this
report are synthetic demonstrations. They are not actual NexziByte revenue,
validated business forecasts, or approved financial guidance.

**Technical status:** Forecasting demonstration and documented evaluation are
complete, subject to final deliverable verification. Business validation and
production approval remain pending.

## 2. Revenue Data Readiness

- The keyword-based readiness audit reviewed 24 CSV files.
- No potential revenue source was identified by the audit's filename and
  column-name matching rules.
- The prospect datasets do not contain verified realized-revenue measures.
- Quotation values must not be treated as realized revenue.
- Actual historical revenue data and business-approved definitions remain
  outstanding.

The audit is a screening exercise, not proof that revenue data does not exist
in other files, databases, accounting systems, or business applications.

## 3. Synthetic Dataset

- Frequency: Monthly
- Historical period: January 2023 through December 2025
- Observations: 36
- Latest historical month: December 2025
- Latest synthetic revenue: 788,869.17
- Data status: Synthetic demonstration only

The synthetic series supports pipeline development and methodological
demonstration only. It cannot establish the actual revenue level, trend,
seasonality, or forecast accuracy of the business.

## 4. Initial Six-Month Holdout Comparison

The initial evaluation used a training period of 30 months and a final
six-month test period from July through December 2025.

| Model | MAE | RMSE |
|---|---:|---:|
| Naive Forecast | 48,010.66 | 53,655.16 |
| Linear Trend Forecast | 53,156.25 | 59,105.72 |
| Seasonal Naive Forecast | 101,617.12 | 104,278.08 |

On this synthetic holdout, the naive forecast had the lowest MAE and RMSE.
This is a limited single-holdout result and should not be treated as proof of
performance on real business revenue.

## 5. Rolling-Origin Backtest

A rolling-origin evaluation was subsequently performed using an initial
training window of 24 monthly observations. Forecasts were evaluated for the
following 12 months, from January through December 2025. The training window
expanded as each new forecast origin became available.

Each model therefore has 12 rolling forecast origins. Results remain synthetic.

| Model | Forecast Origins | MAE | RMSE |
|---|---:|---:|---:|
| Naive Forecast | 12 | 31,945.63 | 40,879.47 |
| Linear Trend Forecast | 12 | 46,405.07 | 52,485.06 |
| Seasonal Naive Forecast | 12 | 100,682.28 | 104,139.27 |

The naive forecast has the lowest MAE and RMSE in this rolling-origin
demonstration. It is the leading baseline for this synthetic dataset, not a
validated model selection for actual NexziByte revenue.

## 6. Empirical Forecast-Error Diagnostics

The following diagnostics summarize absolute errors across the 12 rolling
forecast origins for each model.

| Model | Origins | MAE | Median Absolute Error | 95th-Percentile Absolute Error | Maximum Absolute Error |
|---|---:|---:|---:|---:|---:|
| Linear Trend Forecast | 12 | 46,405.07 | 50,411.94 | 77,363.58 | 81,349.48 |
| Naive Forecast | 12 | 31,945.63 | 29,555.43 | 73,724.06 | 93,441.88 |
| Seasonal Naive Forecast | 12 | 100,682.28 | 94,667.09 | 135,938.78 | 137,691.11 |

The empirical 95th-percentile absolute error describes the upper part of the
observed error distribution in this small synthetic backtest sample. It is
not, by itself, a calibrated 95% prediction interval or a guarantee of future
coverage.

Only 12 forecast origins are available per model. The observed errors may not
represent future forecast errors, and the assessment must be repeated with
sufficient, verified business history.

## 7. Forecast Horizons and Scenario Analysis

Forecast outputs are provided separately for 3, 6, and 12 months. They begin
in January 2026, following the synthetic history ending in December 2025.

The selected demonstration forecast is the naive baseline. Its point forecast
holds revenue at the latest historical value of 788,869.17 per month.

Scenario assumptions:

- **Base:** Revenue remains at the latest observed synthetic level.
- **Best-case:** Illustrative upside based on historical variation.
- **Worst-case:** Illustrative downside based on historical variation, bounded
  at zero.

These are simplifying assumptions for demonstration. They are not
business-approved targets, probability-weighted plans, or causal estimates.

## 8. Forecast Interval Limitations

Forecast CSVs contain `Approx_Lower_95` and `Approx_Upper_95` fields. The
intervals are approximate residual-based ranges that widen with forecast
horizon. They are explicitly marked as not formally calibrated or validated.

The rolling-origin absolute-error diagnostics provide additional evidence about
the size of observed errors, but they do not establish calibrated 95% coverage.
The empirical 95th percentile is estimated from only 12 forecast origins per
model and should not be presented as a statistically guaranteed prediction
interval.

Before operational use, prediction intervals should be evaluated and calibrated
using verified revenue data and an appropriate time-series validation method.

## 9. Key Limitations and Risks

1. No verified historical revenue dataset was identified by the readiness
   screening.
2. All model comparisons and forecasts use synthetic data.
3. Synthetic evaluation results are not evidence of actual business
   forecasting performance.
4. The naive model assumes the latest observed value remains constant.
5. Scenario assumptions are illustrative and do not establish causal drivers.
6. Trend and seasonality require assessment on real revenue observations.
7. Error and interval estimates are based on a limited demonstration sample.
8. Revenue definitions, currency, date fields, granularity, aggregation rules,
   and treatment of adjustments must be confirmed by the business owner.
9. Business validation and production approval have not been granted.

## 10. Deliverables

### Readiness and initial evaluation

- `data/processed/Day8_Revenue_Data_Readiness_Audit.csv`
- `data/synthetic/Day8_Naive_Forecast_Backtest.csv`
- `data/synthetic/Day8_Naive_Forecast_Metrics.csv`
- `data/synthetic/Day8_Seasonal_Naive_Forecast_Backtest.csv`
- `data/synthetic/Day8_Linear_Trend_Forecast_Backtest.csv`
- `data/synthetic/Day8_Forecast_Model_Comparison.csv`

### Rolling-origin evaluation

- `data/synthetic/Day8_Rolling_Origin_Backtest.csv`
- `data/synthetic/Day8_Rolling_Origin_Metrics.csv`

### Synthetic dataset, forecasts, and scenarios

- `data/synthetic/Day8_Synthetic_Monthly_Revenue.csv`
- `data/synthetic/Day8_Synthetic_Revenue_Forecast_3M.csv`
- `data/synthetic/Day8_Synthetic_Revenue_Forecast_6M.csv`
- `data/synthetic/Day8_Synthetic_Revenue_Forecast_12M.csv`
- `data/synthetic/Day8_Forward_Revenue_Scenarios_3M.csv`
- `data/synthetic/Day8_Forward_Revenue_Scenarios_6M.csv`
- `data/synthetic/Day8_Forward_Revenue_Scenarios_12M.csv`

### Report and notebook

- `reports/Day8_Revenue_Forecasting_Report.md`
- `notebooks/06_revenue_forecast.ipynb`

## 11. Conclusion and Next Actions

The synthetic forecasting implementation demonstrates a complete workflow:
readiness screening, baseline comparison, rolling-origin backtesting,
empirical error diagnostics, multiple forecast horizons, and illustrative
scenarios.

The naive model is the leading baseline on the current synthetic evaluation.
No claim is made that it is the best model for actual business revenue.

Next actions:

1. Obtain verified historical revenue records from an approved source.
2. Confirm revenue definitions, currency, date field, and aggregation rules.
3. Validate data quality and chronology on actual observations.
4. Re-run model comparison and rolling-origin backtesting on real data.
5. Assess and calibrate prediction intervals with adequate validation history.
6. Review results and assumptions with the business owner.
7. Obtain explicit business validation and production approval before
   operational use.

**Status:** Technical demonstration documented; business validation pending;
production approval pending.

# Day 12 — Preliminary Fairness Assessment

## 1. Overall Status

**Assessment plan documented; preliminary lead-model group evaluation completed; broader fairness validation pending.**

The lead model was evaluated using its existing synthetic test predictions. Preliminary group-level metrics were generated for Industry / Sub-industry and customer type.

The datasets contain synthetic labels and predictions. These results cannot establish fairness in real business operations. No model is approved for production use.

## 2. Assessment Approach

1. Confirm valid group definitions and their business justification.
2. Verify sample sizes and outcome availability for each group.
3. Evaluate prediction rates and relevant error metrics by group.
4. Investigate material differences instead of assuming that a difference proves unfairness.
5. Document uncertainty, limitations, and the business owner's review.

## 3. Lead Model — Preliminary Results

### 3.1 Industry / Sub-industry

Output file: `data/processed/Day12_Lead_Model_Group_Fairness.csv`

The assessment covered seven industry/sub-industry groups in the 45-record synthetic test set.

Key observations:

- **AI / ML / GenAI:** 14 records; recall was 0.00, with four false negatives.
- **B2B SaaS / Enterprise Software:** 14 records; recall was 0.00, with five false negatives.
- **FinTech / Payments:** 13 records; recall was 0.25, with three false negatives and one false positive.
- The remaining three groups contained only one record each, so their group-level metrics are not reliable for comparison.

These results indicate that positive cases were frequently missed in some groups in this particular synthetic test set. They do not establish that the model discriminates unfairly against any real-world industry.

### 3.2 Customer Type

Output file: `data/processed/Day12_Lead_Model_Customer_Type_Fairness.csv`

The customer-type assessment produced 44 groups from only 45 test records. Nearly all groups contained one record, making meaningful group comparisons impossible.

The customer-type results are therefore **exploratory and inconclusive**. More observations and a business-approved grouping strategy are required before interpreting differences.

## 4. Current Limitations

- The lead dataset and labels are synthetic.
- The lead-model test set contains only 45 records.
- Most customer-type groups have insufficient observations for stable metrics.
- Small groups can produce extreme or undefined error rates.
- The quotation dataset requires verified mapping before company attributes can be joined.
- Suitable project comparison groups have not yet been approved.
- No protected-group fairness conclusion has been established.
- No model is approved for production use.

## 5. Decisions Still Required

- Approve appropriate comparison groups and evaluation criteria.
- Define minimum sample-size requirements for group comparisons.
- Investigate the lead model's low recall across the observed industry groups.
- Link each test prediction to the correct original record.
- Obtain suitable, authorized data for any real-world fairness review.
- Complete the quotation and project-risk fairness assessments when appropriate data and group definitions are available.
- Obtain business-owner review before drawing operational conclusions.

## 6. Assessment Register

| Model | Comparison group | Status |
|---|---|---|
| DAY6_LEAD_MODEL | Industry / Sub-industry | Preliminary synthetic evaluation completed; interpretation limited |
| DAY6_LEAD_MODEL | B2B versus B2C | Output generated; groups too small for meaningful comparison |
| DAY7_QUOTE_LOGISTIC | Industry / customer type | Blocked pending data mapping |
| DAY9_PROJECT_DELAY_RF | Relevant operational project groups | Pending group definition |
| DAY9_EFFORT_OVERRUN_LOGISTIC | Relevant operational project groups | Pending group definition |

## 7. Conclusion

The lead model has undergone a preliminary group-level assessment using synthetic test predictions. Low recall was observed in several groups, while the customer-type grouping was too granular to support meaningful comparisons.

These findings should be treated as diagnostic signals, not proof of unfairness or fairness. Additional data, approved comparison groups, and business review are required.

**Day 12 fairness status: Preliminary lead-model evaluation completed; overall fairness validation pending.**
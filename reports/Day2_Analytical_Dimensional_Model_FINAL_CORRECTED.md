# NexziByte Predictive Business Intelligence & Growth Engine
## Day 2 — Analytical Dimensional Model

**Status:** Proposed analytical design — pending business and data-source confirmation  
**Prepared:** 12 October 2026  
**Purpose:** Define how business data could be organized for reporting, KPI calculation, and future predictive analytics.

---

## 1. Design Principles

1. Keep the original `NexziByte_Final_Scored.csv` unchanged.
2. Separate operational database tables from the analytical reporting model.
3. Define the grain of every fact table before implementing it.
4. Use consistent company, date, service, and status dimensions where applicable.
5. Do not claim predictive performance without suitable historical outcomes and validation.
6. Treat proposed business definitions as unconfirmed until the responsible business owner approves them.

## 2. Proposed Dimensional Architecture

The proposed architecture uses fact tables to record measurable business events and dimension tables to describe the companies, dates, services, and statuses associated with those events.

### Proposed dimension tables

| Dimension | Purpose | Example attributes |
|---|---|---|
| `dim_company` | Identify and describe a company | Company key, company name, industry, location |
| `dim_date` | Support time-based analysis | Date key, calendar date, month, quarter, year |
| `dim_service` | Classify services offered | Service key, service name, service category |
| `dim_lead_status` | Standardize lead stages | Status key, status name, status category |
| `dim_quote_status` | Standardize quotation outcomes | Status key, status name, outcome category |
| `dim_project_status` | Standardize project states | Status key, status name, delivery category |

These are proposed analytical dimensions, not tables currently confirmed to exist in the PostgreSQL database.

## 3. Proposed Fact Tables and Grain

| Fact table | Grain — one row represents | Potential measures |
|---|---|---|
| `fact_prospect_assessment` | One assessment of one company at a point in time | Prospect score, component scores, assessment count |
| `fact_lead_outcome` | One lead or opportunity outcome record | Lead count, conversion indicator |
| `fact_quotation` | One quotation | Quoted amount, quotation count, accepted/lost indicator |
| `fact_project_delivery` | One project or agreed project-period record | Planned duration, actual duration, revenue (if validated), and delivery-performance measures based on approved definitions. Cost and margin analysis requires additional validated cost data and agreed calculation rules. |
| `fact_invoice` | One invoice | Invoice amount, paid amount, outstanding amount |
| `fact_customer_activity` | One recorded customer activity event | Activity count, days since last activity |

The proposed grain must be reviewed against the actual source systems before implementation. Measures such as revenue, margin, conversion, and delivery delay require appropriate source records and approved definitions.

## 4. Relationships

The intended analytical relationships are:

- `dim_company` connects company-related assessments, leads, quotations, projects, invoices, and activities.
- `dim_date` connects to relevant event dates, such as assessment date, lead creation date, quotation date, project dates, invoice dates, and activity dates.
- `dim_service` connects to service-related leads, quotations, and projects where service information is available.
- Lead, quotation, and project status dimensions classify their respective business events.

A company can have multiple assessments, leads, quotations, projects, invoices, and activity events. The implementation must preserve these one-to-many relationships without unintentionally duplicating measures.

## 5. Mapping to the Current PostgreSQL Schema

| Existing operational table | Proposed analytical destination |
|---|---|
| `company` | `dim_company` |
| `prospect_assessment` | `fact_prospect_assessment` |
| `company_validation` | Validation or data-quality reporting |
| `service_catalogue` | `dim_service` |
| `lead_opportunity` | `fact_lead_outcome` |
| `quotation` | `fact_quotation` |
| `project` | `fact_project_delivery` |
| `customer_activity` | `fact_customer_activity` |
| `finance_invoice` | `fact_invoice` |
| `resource_delivery` | Future delivery/resource analysis, subject to grain definition |

This mapping is conceptual. It does not mean that the fact and dimension tables have been created or populated.

## 6. Current Data Availability and Limitations

- The current seed file contains 180 rows and 25 columns of prospect/company information and an existing Prospect Score, according to the project audit.
- The current seed file alone does not establish the availability of historical lead outcomes, quotations, project delivery records, invoices, or customer activity.
- The existing Prospect Score is an internal prioritization score; it is not a verified probability of conversion.
- Historical event dates and outcome labels must be confirmed before time-based conversion analysis or predictive modelling.
- The PostgreSQL schema was executed successfully in the test database, but all ten tables remain empty.
- No analytical fact or dimension tables have been implemented or populated as part of this design document.

## 7. Decisions Required Before Implementation

1. Confirm the business-approved definitions of lead, qualified opportunity, won quotation, lost quotation, delayed project, and inactive customer.
2. Identify the systems or files containing historical quotation, project, finance, and customer-activity records.
3. Confirm the business keys used to link records across systems.
4. Agree on event-date definitions and reporting periods.
5. Confirm revenue, cost, margin, and conversion formulas.
6. Decide whether prospect assessments should retain historical snapshots or only the latest assessment.
7. Confirm the required reporting tools and refresh frequency.

## 8. Acceptance Status

**Design documentation:** Drafted.

**Technical implementation:** Not implemented; this document describes a proposed analytical model.

**Business validation:** The project owner has reported business validation as checked and approved. Supporting evidence and approver details should be recorded if available.

**Next action:** Review this model against the Day 2 data dictionary, entity availability matrix, PostgreSQL schema, and project assignment before final sign-off.

---

**End of Day 2 Analytical Dimensional Model**

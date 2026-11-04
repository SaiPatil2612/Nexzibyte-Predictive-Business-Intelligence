-- NexziByte Predictive Business Intelligence & Growth Engine
-- Day 3: Data Quality Validation Queries
-- Purpose: Validate loaded prospect data after ETL.
-- Prerequisite: Day 2 PostgreSQL schema must be deployed.
-- Important: These queries inspect data; they do not modify records.

-- 1. Company records missing required company names
SELECT *
FROM company
WHERE company_name IS NULL
   OR BTRIM(company_name) = '';

-- 2. Duplicate company names ignoring case and surrounding spaces
SELECT
    LOWER(BTRIM(company_name)) AS normalized_company_name,
    COUNT(*) AS record_count
FROM company
GROUP BY LOWER(BTRIM(company_name))
HAVING COUNT(*) > 1;

-- 3. Invalid employee counts
SELECT
    company_id,
    company_name,
    employee_count
FROM company
WHERE employee_count < 0;

-- 4. Invalid or missing website validation status
SELECT
    company_id,
    company_name,
    website_domain,
    website_validation_status
FROM company
WHERE website_validation_status IS NULL
   OR BTRIM(website_validation_status) = '';

-- 5. Prospect assessments with missing score components
SELECT *
FROM prospect_assessment
WHERE company_size_score IS NULL
   OR b2b_fit_score IS NULL
   OR technology_signal_score IS NULL
   OR business_need_score IS NULL
   OR recent_business_signal_score IS NULL
   OR decision_maker_score IS NULL
   OR prospect_score IS NULL;

-- 6. Prospect score totals inconsistent with their components
SELECT
    assessment_id,
    company_id,
    prospect_score,
    company_size_score
        + b2b_fit_score
        + technology_signal_score
        + business_need_score
        + recent_business_signal_score
        + decision_maker_score AS calculated_score
FROM prospect_assessment
WHERE prospect_score IS NOT NULL
  AND company_size_score IS NOT NULL
  AND b2b_fit_score IS NOT NULL
  AND technology_signal_score IS NOT NULL
  AND business_need_score IS NOT NULL
  AND recent_business_signal_score IS NOT NULL
  AND decision_maker_score IS NOT NULL
  AND prospect_score <>
      company_size_score
      + b2b_fit_score
      + technology_signal_score
      + business_need_score
      + recent_business_signal_score
      + decision_maker_score;

-- 7. Lead opportunities referencing missing company records
SELECT l.*
FROM lead_opportunity AS l
LEFT JOIN company AS c
    ON c.company_id = l.company_id
WHERE c.company_id IS NULL;

-- 8. Quotations with invalid negative monetary values
SELECT *
FROM quotation
WHERE quote_value < 0
   OR discount_amount < 0;

-- 9. Projects with actual end dates earlier than start dates
SELECT *
FROM project
WHERE start_date IS NOT NULL
  AND actual_end_date IS NOT NULL
  AND actual_end_date < start_date;

-- 10. Invoices where collected amount exceeds billed amount
SELECT *
FROM finance_invoice
WHERE billed_amount IS NOT NULL
  AND collected_amount IS NOT NULL
  AND collected_amount > billed_amount;

-- 11. Summary counts for the main tables
SELECT 'company' AS table_name, COUNT(*) AS record_count
FROM company
UNION ALL
SELECT 'prospect_assessment', COUNT(*)
FROM prospect_assessment
UNION ALL
SELECT 'lead_opportunity', COUNT(*)
FROM lead_opportunity
UNION ALL
SELECT 'quotation', COUNT(*)
FROM quotation
UNION ALL
SELECT 'project', COUNT(*)
FROM project;
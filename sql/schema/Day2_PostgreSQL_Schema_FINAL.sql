-- NexziByte Predictive Business Intelligence & Growth Engine
-- Day 2 FINALIZED DESIGN BASELINE
-- Scope: Current scored-prospect snapshot and future-state operational entities.
-- Status: Executed in the test database; structural verification completed for
-- the reviewed tables, columns, relationships, constraints, and indexes.
-- Business-rule validation and final documentation reconciliation remain pending.
-- Production readiness has not been established.
-- Historical quote/project/invoice/activity/resource records are not in the supplied CSV.
-- Do not fabricate them. Keep the raw source CSV immutable.

BEGIN;

CREATE TABLE company (
    company_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_name TEXT NOT NULL,
    website_domain TEXT,
    industry_subindustry TEXT,
    hq_location TEXT,
    founded_year SMALLINT,
    products_services TEXT,
    target_customer_segment TEXT,
    technology_signals TEXT,
    recent_business_signal TEXT,
    decision_maker_text TEXT,
    source_text TEXT,
    date_verified DATE,
    employee_count INTEGER,
    website_validation_status TEXT,
    employee_validation_status TEXT,
    duplicate_flag TEXT,
    data_quality_status TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_company_name UNIQUE (company_name),
    CONSTRAINT ck_company_founded_year CHECK (founded_year IS NULL OR founded_year BETWEEN 1800 AND 2100),
    CONSTRAINT ck_company_employee_count CHECK (employee_count IS NULL OR employee_count >= 0)
);

-- A row is one assessment/snapshot of a prospect score, allowing scores to be versioned.
CREATE TABLE prospect_assessment (
    assessment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    assessed_at DATE,
    company_size_score SMALLINT,
    b2b_fit_score SMALLINT,
    technology_signal_score SMALLINT,
    business_need_score SMALLINT,
    recent_business_signal_score SMALLINT,
    decision_maker_score SMALLINT,
    prospect_score SMALLINT,
    prospect_classification TEXT,
    scoring_model_version TEXT,
    CONSTRAINT ck_prospect_score_sum CHECK (
        prospect_score IS NULL OR
        (company_size_score IS NOT NULL AND b2b_fit_score IS NOT NULL
         AND technology_signal_score IS NOT NULL AND business_need_score IS NOT NULL
         AND recent_business_signal_score IS NOT NULL AND decision_maker_score IS NOT NULL
         AND prospect_score = company_size_score + b2b_fit_score + technology_signal_score
                           + business_need_score + recent_business_signal_score + decision_maker_score)
    )
);

CREATE TABLE company_validation (
    validation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    validation_type TEXT NOT NULL,
    validation_status TEXT NOT NULL,
    evidence_reference TEXT,
    validated_at DATE,
    reviewer TEXT,
    notes TEXT
);

CREATE TABLE service_catalogue (
    service_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    service_name TEXT NOT NULL,
    category TEXT,
    typical_client_segment TEXT,
    technology_tags TEXT,
    project_complexity_band TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_service_name UNIQUE (service_name)
);

CREATE TABLE lead_opportunity (
    lead_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    service_id BIGINT REFERENCES service_catalogue(service_id),
    source TEXT,
    created_date DATE,
    stage TEXT,
    budget NUMERIC(14,2),
    owner TEXT,
    interactions INTEGER,
    meetings INTEGER,
    response_time_hours NUMERIC(10,2),
    last_activity DATE,
    outcome TEXT,
    CONSTRAINT ck_lead_budget CHECK (budget IS NULL OR budget >= 0),
    CONSTRAINT ck_lead_interactions CHECK (interactions IS NULL OR interactions >= 0),
    CONSTRAINT ck_lead_meetings CHECK (meetings IS NULL OR meetings >= 0)
);

CREATE TABLE quotation (
    quote_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lead_id BIGINT NOT NULL REFERENCES lead_opportunity(lead_id),
    service_id BIGINT REFERENCES service_catalogue(service_id),
    quote_date DATE,
    quote_value NUMERIC(14,2),
    discount_amount NUMERIC(14,2),
    revision_count INTEGER,
    response_time_hours NUMERIC(10,2),
    status TEXT,
    accepted_date DATE,
    loss_reason TEXT,
    CONSTRAINT ck_quote_value CHECK (quote_value IS NULL OR quote_value >= 0),
    CONSTRAINT ck_quote_discount CHECK (discount_amount IS NULL OR discount_amount >= 0),
    CONSTRAINT ck_quote_revisions CHECK (revision_count IS NULL OR revision_count >= 0)
);

CREATE TABLE project (
    project_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    quote_id BIGINT REFERENCES quotation(quote_id),
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    service_id BIGINT REFERENCES service_catalogue(service_id),
    start_date DATE,
    target_end_date DATE,
    actual_end_date DATE,
    planned_effort_hours NUMERIC(12,2),
    actual_effort_hours NUMERIC(12,2),
    change_requests INTEGER,
    dependencies TEXT,
    milestones TEXT,
    defects INTEGER,
    status TEXT,
    revenue NUMERIC(14,2),
    CONSTRAINT ck_project_effort CHECK (
        (planned_effort_hours IS NULL OR planned_effort_hours >= 0)
        AND (actual_effort_hours IS NULL OR actual_effort_hours >= 0)
    ),
    CONSTRAINT ck_project_defects CHECK (defects IS NULL OR defects >= 0)
);

CREATE TABLE customer_activity (
    activity_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    interaction_date DATE,
    channel TEXT,
    interaction_type TEXT,
    meeting_count INTEGER,
    support_count INTEGER,
    renewal_expansion_event TEXT,
    CONSTRAINT ck_activity_counts CHECK (
        (meeting_count IS NULL OR meeting_count >= 0)
        AND (support_count IS NULL OR support_count >= 0)
    )
);

CREATE TABLE finance_invoice (
    invoice_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id BIGINT REFERENCES project(project_id),
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    invoice_date DATE,
    billed_amount NUMERIC(14,2),
    collected_amount NUMERIC(14,2),
    due_date DATE,
    payment_delay_days INTEGER,
    outstanding_amount NUMERIC(14,2),
    CONSTRAINT ck_invoice_amounts CHECK (
        (billed_amount IS NULL OR billed_amount >= 0)
        AND (collected_amount IS NULL OR collected_amount >= 0)
        AND (outstanding_amount IS NULL OR outstanding_amount >= 0)
    )
);

CREATE TABLE resource_delivery (
    resource_delivery_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES project(project_id),
    role TEXT,
    planned_hours NUMERIC(12,2),
    actual_hours NUMERIC(12,2),
    allocation_pct NUMERIC(5,2),
    utilization_pct NUMERIC(5,2),
    start_date DATE,
    end_date DATE,
    CONSTRAINT ck_resource_hours CHECK (
        (planned_hours IS NULL OR planned_hours >= 0)
        AND (actual_hours IS NULL OR actual_hours >= 0)
    ),
    CONSTRAINT ck_allocation_pct CHECK (allocation_pct IS NULL OR allocation_pct BETWEEN 0 AND 100),
    CONSTRAINT ck_utilization_pct CHECK (utilization_pct IS NULL OR utilization_pct BETWEEN 0 AND 100)
);

-- Basic indexes for common joins/filtering. Review query plans after real data is loaded.
CREATE INDEX ix_prospect_assessment_company ON prospect_assessment(company_id);
CREATE INDEX ix_lead_company ON lead_opportunity(company_id);
CREATE INDEX ix_lead_stage ON lead_opportunity(stage);
CREATE INDEX ix_quotation_lead ON quotation(lead_id);
CREATE INDEX ix_project_company ON project(company_id);
CREATE INDEX ix_activity_company_date ON customer_activity(company_id, interaction_date);
CREATE INDEX ix_invoice_company_date ON finance_invoice(company_id, invoice_date);
CREATE INDEX ix_resource_project ON resource_delivery(project_id);

COMMIT;

-- Analytics design note:
-- Operational tables above are normalized source/landing structures.
-- For reporting, build a star schema after grain and business definitions are approved:
-- dimensions: dim_company, dim_service, dim_date, dim_source, dim_owner
-- facts: fact_prospect_assessment, fact_lead_outcome, fact_quotation,
--        fact_project_delivery, fact_customer_activity, fact_invoice,
--        fact_resource_allocation.
-- These are logical recommendations, not implemented tables in this script.
-- Unknown business rules (stage taxonomy, revenue recognition, delay definition,
-- churn/renewal meaning, score thresholds) must be confirmed before KPI publication.

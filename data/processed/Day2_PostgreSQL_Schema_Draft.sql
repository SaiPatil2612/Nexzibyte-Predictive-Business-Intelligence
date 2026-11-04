-- NexziByte Predictive BI & Growth Engine
-- Day 2: Initial PostgreSQL relational schema draft
-- Status: Design draft; business validation pending
-- No live database changes performed.

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
    employee_count INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prospect_assessment (
    assessment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    date_verified DATE,
    company_size_score SMALLINT,
    b2b_fit_score SMALLINT,
    technology_signal_score SMALLINT,
    business_need_score SMALLINT,
    recent_business_signal_score SMALLINT,
    decision_maker_score SMALLINT,
    prospect_score SMALLINT NOT NULL,
    prospect_classification TEXT,
    assessment_source TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE company_validation (
    validation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    website_validation_status TEXT,
    employee_validation_status TEXT,
    duplicate_flag TEXT,
    data_quality_status TEXT,
    review_notes TEXT,
    validation_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Future entities: create only after source data and business rules are confirmed.
-- lead_opportunity
-- quotation
-- project
-- customer_activity
-- finance_invoice
-- resource_delivery
-- service_catalogue

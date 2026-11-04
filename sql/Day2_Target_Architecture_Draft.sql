-- NexziByte Predictive BI & Growth Engine
-- Day 2: Expanded target architecture draft
-- Status: Proposed design; business validation pending
-- Not executed against a database.
-- Tables requiring additional source data are future-state designs.

CREATE TABLE company (
    company_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_name TEXT NOT NULL,
    website_domain TEXT,
    industry_subindustry TEXT,
    hq_location TEXT,
    founded_year SMALLINT,
    employee_count INTEGER
);

CREATE TABLE service_catalogue (
    service_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    service_name TEXT NOT NULL,
    category TEXT,
    typical_client_segment TEXT,
    technology_tags TEXT,
    project_complexity_band TEXT
);

CREATE TABLE lead_opportunity (
    lead_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    source TEXT,
    created_date DATE,
    service_interest TEXT,
    stage TEXT,
    budget NUMERIC(14,2),
    owner TEXT,
    interactions INTEGER,
    meetings INTEGER,
    response_time NUMERIC(10,2),
    last_activity DATE,
    outcome TEXT
);

CREATE TABLE quotation (
    quote_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lead_id BIGINT NOT NULL REFERENCES lead_opportunity(lead_id),
    service_id BIGINT REFERENCES service_catalogue(service_id),
    quote_date DATE,
    quote_value NUMERIC(14,2),
    discount NUMERIC(8,2),
    revision_count INTEGER,
    response_time NUMERIC(10,2),
    status TEXT,
    accepted_date DATE,
    loss_reason TEXT
);

CREATE TABLE project (
    project_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    quote_id BIGINT REFERENCES quotation(quote_id),
    service_id BIGINT REFERENCES service_catalogue(service_id),
    start_date DATE,
    target_end_date DATE,
    actual_end_date DATE,
    planned_effort NUMERIC(12,2),
    actual_effort NUMERIC(12,2),
    change_requests INTEGER,
    dependencies TEXT,
    milestones TEXT,
    defects INTEGER,
    status TEXT,
    revenue NUMERIC(14,2)
);

CREATE TABLE customer_activity (
    activity_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES company(company_id),
    interaction_date DATE,
    channel TEXT,
    interaction_type TEXT,
    meeting_count INTEGER,
    support_count INTEGER,
    renewal_expansion_event TEXT
);

CREATE TABLE finance_invoice (
    invoice_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id BIGINT REFERENCES project(project_id),
    company_id BIGINT REFERENCES company(company_id),
    invoice_date DATE,
    billed_amount NUMERIC(14,2),
    collected_amount NUMERIC(14,2),
    due_date DATE,
    payment_delay_days INTEGER,
    outstanding_amount NUMERIC(14,2)
);

CREATE TABLE resource_delivery (
    resource_delivery_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES project(project_id),
    role TEXT,
    planned_hours NUMERIC(12,2),
    actual_hours NUMERIC(12,2),
    allocation_pct NUMERIC(5,2),
    utilization NUMERIC(5,2),
    start_date DATE,
    end_date DATE
);

-- Existing prospect_assessment and company_validation tables
-- remain part of the initial schema draft.
--
-- IMPORTANT:
-- These tables define a proposed target architecture.
-- Historical records and business rules must be sourced and validated
-- before implementation. Do not fabricate missing historical data.

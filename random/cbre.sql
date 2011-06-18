create table employees (
    id serial,
    email text,
    password text,
    fname text,
    lname text
);

create table transactions (
    id serial,
    client_id integer,
    company_id integer,
    division_id integer,
    region_id integer,
    area_id integer,
    trans_manager integer,
    property_id integer,
    survey_id integer,
    client_trans_manager text,
    trans_type text,
    engage_date date,
    rebc_entry_date date,
    survey_sent date
);

create table new_lease (
    id serial,
    trans_id integer,
    old_sqft integer,
    new_sqft integer,
    value_add integer,
    average_base_rent decimal,
    market_survey_date date,
    lease_execution_date date,
    notes text,
    market_survey bool,
    rfp_on_time bool
);

create table lease_extension (
    id serial,
    trans_id integer,
    old_sqft integer,
    new_sqft integer,
    value_add integer,
    average_base_rent decimal,
    market_survey_date date,
    lease_execution_date date,
    notes text,
    market_survey bool,
    rfp_on_time bool
);

create table purchase (
    id serial,
    trans_id integer,
    old_sqft integer,
    new_sqft integer,
    value_add integer,
    purchase_price decimal,
    market_survey_date date,
    purchase_close_date date,
    notes text,
    market_survey bool
);


create table sub_lease (
    id serial,
    trans_id integer,
    sqft integer,
    bov_expected_timing integer,
    bov_actual_timing integer,
    expected_recovery decimal,
    actual_recovery decimal,
    bov_date date,
    sublease_execution_date date,
    notes text,
    bov_ontime bool
);

create table lease_termination (
    id serial,
    trans_id integer,
    sqft integer,
    bov_expected_timing integer,
    bov_actual_timing integer,
    expected_savings decimal,
    actual_savings decimal,
    bov_date date,
    ltd_execution_date date,
    notes text,
    bov_ontime bool
);

create table sale (
    id serial,
    trans_id integer,
    sqft integer,
    bov_expected_timing integer,
    bov_actual_timing integer,
    expected_sale_price decimal,
    sale_price decimal,
    bov_date date,
    sale_closing_date date,
    notes text,
    bov_ontime bool
);


--OLD
create table acquisition (
    id serial,
    trans_id integer,
    old_sqft integer,
    new_sqft integer,
    value_add integer,
    average_base_rent decimal,
    purchase_price decimal,
    engage_date date,
    loi_date date,
    lease_execution_date date,
    market_survey_date date,
    rebc_entry_date date,
    rfp_on_time bool,
    market_survey bool
)
--OLD
create table disposition (
    id serial,
    trans_id integer,
    sale_sqft integer,
    sublease_sqft integer,
    expected_timing integer,
    actual_timing integer,
    expected_recovery decimal,
    actual_recovery decimal,
    lease_termination_sqft integer,
    total_savings decimal,
    sale_price decimal,
    engage_date date,
    loi_date date,
    sale_closing_date date,
    execution_date date,
    rebc_entry_date date,
    ltd_execution_date date,
    bov_date date,
    bov bool,
    bov_ontime bool,
    meet_timing bool,
    meet_expected_recovery bool
);


create table company (
    id serial,
    client_id integer,
    title text
);

create table divisions (
    id serial,
    company_id integer,
    title text
);

create table regions (
    id serial,
    division_id integer,
    title text
);


create table clients (
    id serial,
    email text,
    password text,
    fname text,
    lname text,
    title text
);

create table clientproperties (
    id serial,
    address text,
    city text,
    state text,
    zipcode text,
    sqft integer
)




create table zoomerang (
    id serial,
    email text,
    submit_date date,
    avg_score integer,
    client_id integer,
    employee_id integer
);


create table zoomqa (
    id serial,
    question text,
    answer text,
    z_id integer
);

-- Table: test.employee

DROP TABLE IF EXISTS test.employee;

CREATE TABLE IF NOT EXISTS test.employee
(
    employee_id bigint NOT NULL,
    employee_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    country_id bigint,
    employee_type bigint,
    employee_status bigint
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS test.employee
    OWNER to postgres;
-- Table: test.country

DROP TABLE IF EXISTS test.country;

CREATE TABLE IF NOT EXISTS test.country
(
    country_id bigint NOT NULL,
    country_name character varying(50) COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS test.country
    OWNER to postgres;
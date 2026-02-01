-- Ejecuta esto en tu terminal de Postgres o en un Query Tool
CREATE TABLE lake_raw_data_int (
    id BIGSERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    value BIGINT NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE lake_raw_data_float (
    id BIGSERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    payload TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT now()
);
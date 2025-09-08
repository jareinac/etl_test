-- DDL compatible with Redshift / DuckDB
CREATE TABLE dim_user (
  user_id VARCHAR(64) PRIMARY KEY,
  email VARCHAR(255),
  created_at DATE,
  country VARCHAR(8)
);

CREATE TABLE dim_product (
  sku VARCHAR(64) PRIMARY KEY,
  name VARCHAR(255),
  category VARCHAR(100),
  price DECIMAL(12,2)
);

CREATE TABLE fact_order (
  order_id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64),
  amount DECIMAL(12,2),
  currency VARCHAR(8),
  created_at TIMESTAMP,
  total_qty INTEGER,
  created_date DATE
);

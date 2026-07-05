---
title: Data Warehouse Schema Design - Star, Snowflake, and Data Vault
description: Compares star, snowflake, and data vault warehouse schemas and fact table types (transaction, periodic snapshot, accumulating snapshot) with tradeoffs.
tags:
  - concept
---

# Data Warehousing - Schema Design

Data warehouses are optimized for analytical reads, not transactional writes. Schema design priorities flip: denormalization is deliberate, redundancy is accepted for query speed.

## Star Schema

The simplest and most common warehouse schema. One central **fact table** surrounded by **dimension tables**. Looks like a star.

```
            dim_customer
                 |
dim_product --- fact_sales --- dim_date
                 |
            dim_store
```

**Fact table** - stores measurable events/metrics. Has foreign keys to all dimensions + numeric measures.

```sql
CREATE TABLE fact_sales (
    sale_id       BIGINT PRIMARY KEY,
    customer_key  INT REFERENCES dim_customer(customer_key),
    product_key   INT REFERENCES dim_product(product_key),
    date_key      INT REFERENCES dim_date(date_key),
    store_key     INT REFERENCES dim_store(store_key),
    quantity      INT,
    revenue       DECIMAL(12,2),
    discount      DECIMAL(12,2)
);
```

**Dimension table** - descriptive attributes for slicing/filtering facts. Denormalized (all attributes flat, no further joins needed).

```sql
CREATE TABLE dim_customer (
    customer_key  INT PRIMARY KEY,         -- surrogate key
    customer_id   VARCHAR(50),             -- natural/business key
    name          VARCHAR(200),
    city          VARCHAR(100),
    country       VARCHAR(100),
    segment       VARCHAR(50),
    valid_from    DATE,
    valid_to      DATE,
    is_current    BOOLEAN
);
```

### Query pattern

```sql
-- total revenue by country and product category, last quarter
SELECT
    c.country,
    p.category,
    SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_product  p ON f.product_key  = p.product_key
JOIN dim_date     d ON f.date_key     = d.date_key
WHERE d.quarter = 'Q1-2024'
  AND c.is_current = true
GROUP BY c.country, p.category
ORDER BY total_revenue DESC;
```

### Pros and cons

Pros: fast queries (few joins), simple for BI tools, easy to understand.

Cons: dimension tables can be wide and denormalized (some redundancy), harder to maintain if the same attribute appears in multiple dimensions.

---

## Snowflake Schema

Extends star schema by normalizing dimension tables into sub-dimensions. Dimensions have their own foreign keys.

```
dim_city --- dim_customer --- fact_sales --- dim_product --- dim_category
```

```sql
CREATE TABLE dim_city (
    city_key   INT PRIMARY KEY,
    city       VARCHAR(100),
    country    VARCHAR(100),
    region     VARCHAR(100)
);

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id  VARCHAR(50),
    name         VARCHAR(200),
    city_key     INT REFERENCES dim_city(city_key)   -- normalized
);
```

### Pros and cons

Pros: less storage (no repeated city/country in every customer row), easier to update a shared attribute (e.g., country name change).

Cons: more joins per query, slower reads, more complex for BI tools to navigate.

**Rule of thumb:** Use star schema unless storage is genuinely a constraint or the dimension hierarchy is reused across many dimensions. Most modern columnar stores (Redshift, BigQuery, Snowflake) make the extra joins cheap enough that the simplicity of star schema wins.

---

## Data Vault

Designed for enterprise DWH where sources are many, schemas change frequently, and full auditability is required. More complex than star/snowflake but very resilient to schema change.

Three object types:

**Hub** - business keys. One hub per core business concept.

```sql
CREATE TABLE hub_customer (
    customer_hkey  CHAR(32) PRIMARY KEY,    -- hash of business key
    customer_id    VARCHAR(50),             -- business key
    load_date      TIMESTAMP,
    record_source  VARCHAR(100)             -- which source system loaded this
);
```

**Link** - relationships between hubs (many-to-many).

```sql
CREATE TABLE link_sales (
    sales_hkey    CHAR(32) PRIMARY KEY,
    customer_hkey CHAR(32) REFERENCES hub_customer,
    product_hkey  CHAR(32) REFERENCES hub_product,
    date_hkey     CHAR(32) REFERENCES hub_date,
    load_date     TIMESTAMP,
    record_source VARCHAR(100)
);
```

**Satellite** - descriptive attributes for a hub or link, with full history.

```sql
CREATE TABLE sat_customer_details (
    customer_hkey CHAR(32) REFERENCES hub_customer,
    load_date     TIMESTAMP,
    end_date      TIMESTAMP,
    city          VARCHAR(100),
    segment       VARCHAR(50),
    hash_diff     CHAR(32),                 -- hash of all attributes, detect changes
    record_source VARCHAR(100),
    PRIMARY KEY (customer_hkey, load_date)
);
```

### Pros and cons

Pros: handles schema changes gracefully (new attributes = new satellite, no ALTER TABLE), full auditability baked in, parallel loading (hubs/links/satellites load independently), works well with multiple source systems.

Cons: very verbose (many tables), complex queries require many joins through hubs and links, not intuitive for analysts. Usually queried via a "business vault" or "information mart" layer on top.

**When to use:** Large enterprise DWH with many source systems, strict audit/compliance requirements, frequent schema changes from upstream. Overkill for most startups.

---

## Fact Table Types

Not all facts are the same shape:

**Transaction fact** - one row per event. Most common. Examples: orders, clicks, payments.

**Periodic snapshot** - one row per entity per time period. Examples: account balance at end of each month, inventory level at end of each day.

```sql
-- snapshot: balance per account per month-end
INSERT INTO fact_account_snapshot
SELECT account_id, LAST_DAY(CURRENT_DATE), balance
FROM accounts;
```

**Accumulating snapshot** - one row per business process instance, updated as it progresses through stages. Examples: order fulfillment (order -> pick -> ship -> deliver). Each stage has its own date key column.

```sql
CREATE TABLE fact_order_pipeline (
    order_key          INT,
    order_date_key     INT,
    pick_date_key      INT,    -- NULL until picked
    ship_date_key      INT,    -- NULL until shipped
    deliver_date_key   INT,    -- NULL until delivered
    order_amount       DECIMAL(12,2)
);
```

## Schema Comparison

| | Star | Snowflake | Data Vault |
|---|------|-----------|------------|
| Query performance | Best | Moderate | Worst (many joins) |
| Storage | High (redundancy) | Medium | High (history + metadata) |
| Schema change handling | Hard | Moderate | Excellent |
| Auditability | Limited | Limited | Full |
| Complexity | Low | Medium | High |
| Best for | Small/medium DWH, BI | Storage-sensitive | Enterprise, multi-source |

## See Also
- [Slowly Changing Dimensions (SCD) and MERGE](scd.md)
- [Database Normalization](normalization.md)
- [Databricks Platform](../../databricks/fundamentals/ch4.md)

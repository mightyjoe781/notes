# Database Partitioning

### What is Partitioning

![](assets/Pasted%20image%2020250925195707.png)

- Split a large table into multiple smaller tables called as partitions (contain metadata, cutting query costs).
- Trick to avoid querying 1M records is to not query 1 M records :)
#### Vertical vs Horizontal Partitioning

- Horizontal Partitioning splits rows into partitions
    - Range or List
- Vertical Partitioning Splits columns partitions
    - Large column (blob) that you can store in a slow access drive in its own tablespace

### Partitioning Types

- By Range
    - Dates, ids (e.g. by logdate or customer_id from to)
- By List
    - Discrete Values (eg CA, AL, etc) or zip codes
- By Hash
    - Hash functions (Consistent Hashing) (Used in Cassandra)

### Horizontal Partitioning vs Sharding

- HP splits big table into multiple tables in the same database, client is agnostic
- Sharding splits big table into multiple tables across multiple database servers
- HP table name changes (or schema)
- Sharding everything is the same but server changes.

### Preparing : Postgres, Database, Tables, Indexes

Spinning up a PostgreSQL container :

```bash
# container creation in detached mode
docker run --name pgmain -d -e POSTGRES_PASSWORD=postgres postgres
docker ps

# exec into the container
docker exec -it pgmain bash

# login
psql -U postgres
```

```postgresql
-- table creation
create table grades_org (id serial not null, g int not null);

-- insert into grades_org, 10 M records
insert into grades_org(g) select floor(random() * 100) from generate_series(0, 10000000);

-- create index 
create index grades_org_index on grades
```
#### Execute Multiple Queries on the Tables

```postgresql
select count(*) from grades_org where g = 30;

explain analyze select count(*) from grades_org where g between 50 and 80;
```

#### Populate the Partitions and Create Indexes

```postgresql
create table grades_parts (id serial not null, g int not null) partition by range(g);

-- manual index creations
create table g00035 (like grades_parts including indexes);
create table g5660 (like grades_parts including indexes);
create table g6080 (like grades_parts including indexes);
create table g80100 (like grades_parts including indexes);

-- atach the partitions to main table
alter table grades_parts attach partition g0035 for values from (0) to (35);
alter table grades_parts attach partition g5660 for values from (35) to (60);
alter table grades_parts attach partition g6080 for values from (60) to (80);
alter table grades_parts attach partition g80100 for values from (80) to (100);

-- explain tables
\d grades_parts
\d g0035

-- insert values
insert into grades_parts select * from grades_org;

-- query the count
select count(*) from grades_parts;

select max(g) from grades_parts;
select count(*) from g0035; -- random
select max(g) from g0035; -- 35

-- let's create indexes
create index grades_parts_idx on grades_parts(g); -- creates on all partitions

\d grades_part
\d g0035

```

#### Check size of partitions

```postgresql
-- faster and queries g = 30 from g0035 table
explain analyze select count(*) from grades_parts where g = 30;

-- another query
explain analyze select count(*) from grades_parts where g between 50 and 80;

-- find size of pg_relation_size
select pg_relation_size(oid), relname from pg_class order by pg_relation_size(oid) desc;
```

NOTE: Enable partition pruning, or else it will scan all partitions and partitions are useless.

```postgresql
show ENABLE_PARTITION_PRUNING;
```
### Advantages of Partitioning

- Improves query performance when accessing a single partitions
- Sequential scan vs scattered index scan
- Easy bulk loading (attach partition)
- archive old data that are barely accessed into cheap storage

### Disadvantages in Partitioning

- updates that move rows from a partition to another (slow or fail sometimes)
- inefficient queries could accidentally scan all partitions resulting in slower performance
- Schema changes can be challenging (DBMS could manage it though)

### Automatic Partitioning in Postgres


```plsql
-- PL/pgSQL table population tool
-- Configurable script to populate any table with test data

DO $
DECLARE
    -- Configuration variables - modify these as needed
    table_name TEXT := 'customers';
    column_name TEXT := 'name';
    data_generator TEXT := 'random()::text';  -- PostgreSQL expression for generating data
    
    -- Size configuration
    total_records INTEGER := 1000000000;  -- 1 billion
    batch_size INTEGER := 10000000;       -- 10 million per batch
    
    -- Control options
    verbose BOOLEAN := TRUE;              -- Set to FALSE to minimize output
    show_progress_every INTEGER := 10;    -- Show progress every N batches
    
    -- Working variables
    i INTEGER := 0;
    total_batches INTEGER;
    insert_sql TEXT;
BEGIN
    -- Calculate total batches
    total_batches := total_records / batch_size;
    
    -- Build dynamic SQL
    insert_sql := format('INSERT INTO %I(%I) (SELECT %s FROM generate_series(1, $1))', 
                        table_name, column_name, data_generator);
    
    -- Start message
    IF verbose THEN
        RAISE NOTICE 'Populating % with % records...', table_name, total_records;
    END IF;
    
    -- Main insertion loop
    FOR i IN 0..(total_batches - 1) LOOP
        -- Execute batch insert
        EXECUTE insert_sql USING batch_size;
        
        -- Progress reporting
        IF verbose AND ((i + 1) % show_progress_every = 0) THEN
            RAISE NOTICE 'Progress: %/% records (%.1%)',
                        ((i + 1) * batch_size), total_records,
                        (((i + 1)::NUMERIC / total_batches) * 100);
        END IF;
        
        -- Commit after each batch
        COMMIT;
    END LOOP;
    
    -- Completion message
    IF verbose THEN
        RAISE NOTICE 'Completed: % records inserted into %', total_records, table_name;
    END IF;
END $;

```


Or a python version

```python
#!/usr/bin/env python3
"""
Database table population tool
Configurable script to populate any table with test data
"""

import psycopg2
import sys

# Configuration variables - modify these as needed
CONFIG = {
    # Database connection
    'host': 'smk',
    'port': 5432,
    'database': 'customers',
    'user': 'postgres',
    'password': 'postgres',
    
    # Table and data configuration
    'table_name': 'customers',
    'column_name': 'name',
    'data_generator': 'random()::text',  # PostgreSQL expression for generating data
    
    # Size configuration
    'total_records': 1_000_000_000,  # 1 billion
    'batch_size': 10_000_000,        # 10 million per batch
    
    # Performance options
    'verbose': True,  # Set to False to minimize output
    'show_progress_every': 10  # Show progress every N batches
}

def populate_table(config=None):
    """
    Populates a database table with generated data
    
    Args:
        config (dict): Configuration dictionary, uses CONFIG if None
    """
    if config is None:
        config = CONFIG
    
    total_batches = config['total_records'] // config['batch_size']
    
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        if config['verbose']:
            print(f"Populating {config['table_name']} with {config['total_records']:,} records...")
        
        insert_sql = f"""
            INSERT INTO {config['table_name']}({config['column_name']}) (
                SELECT {config['data_generator']} 
                FROM generate_series(1, %s)
            )
        """
        
        for i in range(total_batches):
            cursor.execute(insert_sql, (config['batch_size'],))
            
            if config['verbose'] and (i + 1) % config['show_progress_every'] == 0:
                completed = (i + 1) * config['batch_size']
                print(f"Progress: {completed:,}/{config['total_records']:,} records ({((i+1)/total_batches)*100:.1f}%)")
        
        if config['verbose']:
            print(f"Completed: {config['total_records']:,} records inserted into {config['table_name']}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    populate_table()
```
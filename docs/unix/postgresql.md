# PostgreSQL

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Object-relational database. ACID-compliant, supports JSON, full-text search, and advanced indexing.

### Installation

```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl enable --now postgresql
sudo -u postgres psql                # connect as postgres superuser
```

macOS:

```bash
brew install postgresql@16
brew services start postgresql@16
```

### Connect

```bash
psql -U username -d dbname
psql -h 127.0.0.1 -U username -d dbname
psql postgresql://username:password@host:5432/dbname
```

### psql Meta-commands

| Command | Description |
|---|---|
| `\l` | list databases |
| `\c dbname` | connect to database |
| `\dt` | list tables |
| `\d tablename` | describe table (columns, indexes) |
| `\di` | list indexes |
| `\du` | list roles/users |
| `\x` | toggle expanded output |
| `\timing` | show query execution time |
| `\e` | open query in editor |
| `\q` | quit |
| `\! cmd` | run shell command |

### Database and User Management

```sql
CREATE DATABASE mydb;
DROP DATABASE mydb;
CREATE USER alice WITH PASSWORD 'secret';
GRANT ALL PRIVILEGES ON DATABASE mydb TO alice;
REVOKE ALL PRIVILEGES ON DATABASE mydb FROM alice;
ALTER USER postgres WITH PASSWORD 'newpassword';
```

### Tables

```sql
CREATE TABLE users (
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL,
    email   TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE users ADD COLUMN active BOOLEAN DEFAULT true;
ALTER TABLE users DROP COLUMN active;
DROP TABLE users;
TRUNCATE TABLE users;                -- delete all rows, keep structure
```

### CRUD

```sql
-- Insert
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES
    ('Bob', 'bob@example.com'),
    ('Charlie', 'charlie@example.com');

-- Select
SELECT * FROM users;
SELECT name, email FROM users WHERE id = 1;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
SELECT * FROM users WHERE name ILIKE '%ali%';  -- case-insensitive

-- Update
UPDATE users SET email = 'new@example.com' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
```

### Indexes

```sql
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_created ON users (created_at DESC);
CREATE UNIQUE INDEX idx_users_email_unique ON users (email);
DROP INDEX idx_users_email;
```

### Transactions

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Rollback on error
BEGIN;
-- ...
ROLLBACK;
```

### Useful Queries

```sql
-- Active connections
SELECT pid, usename, datname, state, query
FROM pg_stat_activity WHERE state != 'idle';

-- Kill a connection
SELECT pg_terminate_backend(12345);

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(oid))
FROM pg_class WHERE relkind = 'r' ORDER BY pg_total_relation_size(oid) DESC;

-- Slow queries (requires pg_stat_statements)
SELECT query, mean_exec_time, calls
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;

-- Explain query plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';
```

### Backup and Restore

```bash
# Dump single database
pg_dump -U username dbname > backup.sql
pg_dump -U username -Fc dbname > backup.dump   # custom format (faster restore)

# Restore
psql -U username dbname < backup.sql
pg_restore -U username -d dbname backup.dump

# Dump all databases
pg_dumpall -U postgres > all.sql
```

### Configuration

Edit `/etc/postgresql/<version>/main/postgresql.conf`:

```
max_connections = 100
shared_buffers = 256MB
work_mem = 4MB
log_statement = 'all'
```

Edit `pg_hba.conf` for access control:

```
# TYPE  DATABASE  USER  ADDRESS       METHOD
host    all       all   127.0.0.1/32  md5
host    all       all   192.168.1.0/24 md5
```

```bash
sudo systemctl reload postgresql
```

### Tips

- Use connection pooling (PgBouncer) for high-concurrency apps
- `EXPLAIN ANALYZE` shows actual vs estimated row counts - mismatches indicate stale stats, run `ANALYZE`
- Prefer `TIMESTAMPTZ` over `TIMESTAMP` to avoid timezone issues
- Use `COPY` instead of `INSERT` for bulk data loading (much faster)

### See Also

- [Redis](redis.md) for caching
- [SQLite](sqlite.md) for embedded/lightweight use
- Also: MySQL/MariaDB, TimescaleDB (time-series on Postgres), pgvector (vector search)

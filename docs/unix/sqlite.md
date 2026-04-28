# SQLite

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Serverless, file-based SQL database. Great for local apps, scripts, mobile, and development. The database is a single `.db` file.

### Installation

```bash
sudo apt install sqlite3
sqlite3 --version

# macOS (pre-installed)
sqlite3 --version
```

### Getting Started

```bash
sqlite3 mydb.db                      # open or create database
sqlite3 :memory:                     # in-memory database (lost on exit)

# Basic usage
sqlite3 mydb.db "SELECT * FROM users;"
sqlite3 mydb.db < schema.sql          # run SQL file
```

### sqlite3 Shell Meta-commands

| Command | Description |
|---|---|
| `.tables` | list tables |
| `.schema tablename` | show CREATE statement |
| `.headers on` | show column headers |
| `.mode column` | aligned column output |
| `.mode csv` | CSV output |
| `.output file.csv` | redirect output to file |
| `.import file.csv table` | import CSV |
| `.read file.sql` | run SQL from file |
| `.dump` | dump entire database as SQL |
| `.exit` | quit |

### SQL Reference

```sql
-- Create table
CREATE TABLE users (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    email   TEXT UNIQUE,
    created TEXT DEFAULT (datetime('now'))
);

-- Insert
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Select
SELECT * FROM users;
SELECT * FROM users WHERE name LIKE '%Ali%';
SELECT * FROM users ORDER BY created DESC LIMIT 10;

-- Update and Delete
UPDATE users SET email = 'new@example.com' WHERE id = 1;
DELETE FROM users WHERE id = 1;

-- Indexes
CREATE INDEX idx_email ON users (email);
DROP INDEX idx_email;

-- Transactions
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- ROLLBACK;
```

### JSON Support

```sql
-- Store JSON
INSERT INTO events (data) VALUES ('{"type":"login","user":"alice"}');

-- Query JSON fields
SELECT json_extract(data, '$.user') FROM events;
SELECT * FROM events WHERE json_extract(data, '$.type') = 'login';
```

### Advanced Features

```sql
-- Views
CREATE VIEW active_users AS
    SELECT * FROM users WHERE active = 1;

-- Triggers
CREATE TRIGGER update_ts AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Full-text search (FTS5)
CREATE VIRTUAL TABLE docs USING fts5(title, body);
INSERT INTO docs VALUES ('Hello', 'world content here');
SELECT * FROM docs WHERE docs MATCH 'hello';

-- Window functions
SELECT name, salary,
    RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
```

### Backup and Export

```bash
# Dump to SQL
sqlite3 mydb.db ".dump" > backup.sql

# Restore from dump
sqlite3 newdb.db < backup.sql

# Export table to CSV
sqlite3 -header -csv mydb.db "SELECT * FROM users;" > users.csv

# Compressed backup
sqlite3 mydb.db ".dump" | gzip > backup_$(date +%F).sql.gz

# Online backup (safe for live databases)
sqlite3 mydb.db ".backup backup.db"
```

### Encryption (SQLCipher)

```bash
sudo apt install sqlcipher
sqlcipher encrypted.db
PRAGMA key = 'mysecretpassword';
CREATE TABLE test (id INTEGER PRIMARY KEY);
```

### Performance

```sql
-- Write-Ahead Logging (better concurrency)
PRAGMA journal_mode = WAL;

-- Reduce fsync calls (faster, slightly less safe)
PRAGMA synchronous = NORMAL;

-- In-memory temp tables
PRAGMA temp_store = MEMORY;

-- Increase cache
PRAGMA cache_size = -64000;         -- 64MB

-- Check integrity
PRAGMA integrity_check;

-- Explain query plan
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'alice@example.com';
```

### Tips

- Use `WAL` mode for any concurrent read/write use case
- SQLite is single-writer; for high write concurrency, use PostgreSQL
- File permissions are the security boundary: `chmod 600 mydb.db`
- Use `VACUUM` to reclaim space after large deletes
- [Litestream](https://litestream.io) enables continuous S3 replication for SQLite

### See Also

- [PostgreSQL](postgresql.md) for multi-user server deployments
- Also: DuckDB (analytics on SQLite-style files), libSQL (SQLite fork with replication)

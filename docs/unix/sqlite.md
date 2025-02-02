# SQLite3

[:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

Debian/Ubuntu

````bash
sudo apt update
sudo apt install sqlite3
sqlite3 --version
````

macOS

````bash
# usually sqlite is preinstalled
sqlite3 --version
# or 
brew install sqlite
````

### Setup

````bash
# creating a database
sqlite3 mydb.db

# exit the sqlite shell
.exit

# import data from CSV
CREATE TABLE mytable (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);  
.mode csv  
.import data.csv mytable

# Export data to CSV
.headers on  
.mode csv  
.output data.csv  
SELECT * FROM mytable;  

````

### Security

#### File Permissions

SQLite databases are files. Use file system permissions to restrict access

````bash
chmod 600 mydb.db
````

#### Encryption

We can use extensions like SQLCipher for encryption

````bash
sqlcipher mydb.db
PRAGMA key = mysecretkey
````

#### Backup

````bash
sqlite3 mydb ".dump" > backup.sql
````

### Meta-Commands

````sqlite
# list tables
.tables

# describe a table
.schema users

# export data
.mode csv  
.output users.csv  
SELECT * FROM users;

# import data
.mode csv  
.import users.csv users  
````

### Advanced Features

#### Transaction

````bash
BEGIN;  
UPDATE users SET email = 'new@example.com' WHERE id = 1;  
COMMIT;  
````

#### Indexes

```bash
CREATE INDEX idx_users_email ON users (email);
```

#### Views

````bash
CREATE VIEW active_users AS SELECT * FROM users WHERE active = 1;
````

#### Triggers

Automate actions with triggers

````bash
CREATE TRIGGER update_timestamp AFTER UPDATE ON users  
BEGIN  
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;  
END;  
````

### Troubleshooting

````bash
# check database integrity
PRAGMA integrity_check

# recover data from `.dump` to recover data from a corrupted database
sqlite3 corrupted.db ".dump" | sqlite3 new.db

# debug queries
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'john@example.com';
````

### Tips

````bash
# use in-memory databases
sqlite3 :memory:

# backup automatically
sqlite3 mydb.db ".dump" | gzip > backup_$(date +%F).sql.gz

# optimizations
RAGMA journal_mode = WAL;  # Write-Ahead Logging  
PRAGMA synchronous = NORMAL;
````

### Resources

* https://www.sqlitetutorial.net
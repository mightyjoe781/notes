# PostgreSQL

[:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

Debian/Ubuntu

````bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# check service status
sudo systemctl status postgresql
````

macOS

````bash
brew install postgresql

# start the service
brew services start postgresql
````

### Setup

NOTE: Ideally you should not expose your database to public network.

Edit `pg_hba.conf` (usually located at `/etc/postgresql/<version>/main/pg_hba.conf`)

````bash
host    all             all             0.0.0.0/0               md5
````

Edit `postgresql.conf` to listen on all interfaces

````bash
listen_addresses = "*"
````

````bash
sudo systemctl restart postgresql
````

### Security

* Change default password

````bash
ALTER USER postgres WITH PASSWORD 'newpassword';
````

* Restrict Access: Use `pg_hba.conf` to control access

````bash
# Allow only specific IPs  
host    all             all             192.168.1.0/24          md5  
````

* Enable SSL: Edit `postgresql.conf`

````bash
ssl = on
ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'  
ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'
````

* Audit Logging

````bash
log_statement = 'all'  
log_directory = 'pg_log'  
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
````

* Regular Backup: Use `pg_dump` for backup

````bash
pg_dump -U myuser -d mydb -f mydb_backup.sql
````



### Useful Commands

#### 1. Connecting to PostgreSQL

````postgresql
# login
psql -U username -d dbname

# switching database
\c dbname

# list databases
\l
````

#### 2. Managing a Database

````postgresql
# creation
CREATE DATABASE dbname;

# deletion
DROP DATABASE dbname;

# Backup a Database
pg_dump -U username -d dbname -f backup.sql

# Restoring a Backup
psql -U username -d dbname -f backup.sql
````

#### 3. Managing Tables

````postgresql
CREATE TABLE users (  
    id SERIAL PRIMARY KEY,  
    name TEXT NOT NULL,  
    email TEXT UNIQUE  
);  

# list tables
\dt

# describe a table
\d tablename

# delete a table
DROP TABLE tablename;
````

#### 4. Querying Data

````postgresql
SELECT * FROM users;  

SELECT * FROM users WHERE id = 1;  

SELECT * FROM users ORDER BY name ASC;  

SELECT * FROM users LIMIT 10;
````

#### 5. Inserting and Updating and Deleting Data

````postgresql
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');

UPDATE users SET email = 'john.doe@example.com' WHERE id = 1;

DELETE FROM users WHERE id = 1;
````

#### 6. Indexes

````postgresql
CREATE INDEX idx_users_email ON users (email);

# list indices
\di

# dropping indices
DROP INDEX idx_users_email;
````

#### 7. User and Permission

````postgresql
# create a user
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
REVOKE ALL PRIVILEGES ON DATABASE dbname FROM username;

# list users
\du
````

#### 8. Troubleshooting

````postgresql
# check active connections
SELECT * FROM pg_stat_activity;  

# kill a connection
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid = 12345;

# check locks
SELECT * FROM pg_locks;
````

#### 9. Exporting and Importing Data

````postgresql
# export
\copy (SELECT * FROM users) TO 'users.csv' CSV HEADER;

# import 
\copy users FROM 'users.csv' CSV HEADER; 
````

#### 10. Transactions

````postgresql
BEGIN;  
UPDATE users SET email = 'new@example.com' WHERE id = 1;  
COMMIT; 
````

#### 11. Analyzing Query Performance

````postgresql
EXPLAIN ANALYZE SELECT * FROM users WHERE id = 1;
````


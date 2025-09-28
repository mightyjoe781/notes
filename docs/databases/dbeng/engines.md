# Database Engines


### What is Database Engine ?

-   Library that takes care of the on disk storage and CRUD
    - Can be as simple as key-value store
    - Or as rich and complex as full support ACID and transactions with foreign keys
- DBMS can use the database engine and build features on top (server, replication, isolation, stored procedures, etc ...)
- Want to write a database ? Don't start from scratch use an engine.
- Sometimes referred as Storage Engine or embedded database.
- Its called engine because traditionally, engines in a car hide away the complexity of technical design of generating power which maybe too low level to be picked by other relevant parts of the car & their designers.
- Some DBMS gives you the flexibility to switch engines like MySQL & MariaDB
- Some DBMS comes with a built-in engine that you can't change (Postgres)

Article : https://www.uber.com/en-IN/blog/postgres-to-mysql-migration/

### MyISAM

- Stands for Indexed Sequential Access Method
- B-Tree (Balanced Tree) indexes point to the rows directly
- No Transaction support
- Open Source & Owned by Oracle
- Inserts are fast, updates and deleted are problematic (fragments)
- Databases Crashes corrupt tables (have to repaired manually)
- Table level locking
- MySQL, MariaDB, Percona (MySQL forks) supports MyISAM
- Used to be default engine for MySQL

### InnoDB

- B+ tree - with indexes point to primary key and the PK points to the row
- Replaces MyISAM
- Default for MySQL & MariaDB
- ACID compliant transactions support
- Foreign keys
- Tablespaces
- Row level locking
- Spatial Operations
- Owned by Oracle :|

### XtraDB

- Fork of InnoDB
- Was the default for MariaDB until 10.1
- In MariaDB 10.2 switched the default for InnoDB
- XtraDB couldn't be kept up to date with the latest features of InnoDB and cannot be used
- System tables in MariaDB starting with 10.4 are all Aria

### SQLite

- Designed by D Richard Hipp in 2000
- Very populate embedded database for local data
- B-Tree (LSM as extension)
- Postgres-like syntax
- Full ACID & table locking
- Concurrent read & writes
- Web SQL in browsers uses it
- Included in many Operating Systems by default

### Aria

- Created by Michael Widenius
- Very similar to MyISAM
- Crash-safe unlike MyISAM
- Not owned by Oracle
- Designed specifically for MariaDB (mySQL Fork)
- In MariaDB 10.4 all system tables are Aria

### Berkeley DB

- Developed by Sleepycat Software in 1994 (owned by Oracle)
- Key-Value embedded database
- Supports ACID transactions, locks, replication etc.
- Used to be used in bitcoin core (switched to LevelDB)
- Used MemcacheDB
### LevelDB

- Written by Jeff and Sanjay from Google in 2011 (read the article *friendship that made google*)
- Log structured merge tree (LSM) (great for high insert and SSD)
- No Transactions
- Inspired by Google BigTable
- Levels of files
    - Memtable
    - Level 0 (young level)
    - Level 1 - 6
- As files grow large levels are merged
- Used in bitcoin core blockchain, AutoCad, Minecraft

### RocksDB

- facebook forked LevelDB in 2012 to become RocksDB (Dhruba Borthakur, prodigy in field of databases)
- Transactional
- High Performance, Multi-threaded Compaction
- Many features not in LevelDB
- MyRocks for MySQL, MariaDB and Percona
- MongoRocks for MongoDB
- Many many more use it !

### Popular Database Engines

![](assets/Pasted%20image%2020250926230416.png)

### Demo (switching Engines with MySQL)

```bash
docker run --name ms1 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password mysql:8

docker exec -it ms1 bash

# inside container
mysql -u root -ppassword
```

```mysql
create database test;

use database test;

create table employees_myisam(id int primary key auto_increment, name text) engine = myisam;

show engines;

create table employees_innodb(id int primary key auto_increment, name text) engine = innodb;

select * from employees_myisam;
select * from employees_innodb;
```

`server.js`

```javascript
const mysql = require('mysql2/promise');

connectInnoDB();
async function connectInnoDB(){

    try {
        const con = await mysql.createConnection({
            "host": "proton",
            "port": 3306,
            "user": "root",
            "password": "password",
            "database": "test"
        })
       await con.beginTransaction();
       await con.query(
           "INSERT INTO employees_innodb (name) values (?)",
            ["Hussein"])

       const [rows, schema] = await con.query(
           "select * from employees_innodb"
       )
       console.table(rows);

       await con.commit();
       await con.close();
       console.log(result)
    }
    catch(ex){
        console.error(ex)
    }
    finally{

    }

}

async function connectMyISAM(){

    try {
        const con = await mysql.createConnection({
            "host": "husseinmac",
            "port": 3306,
            "user": "root",
            "password": "password",
            "database": "test"
        })
       await con.beginTransaction();
       await con.query(
           "INSERT INTO employees_myisam (name) values (?)",
            ["Hussein"])
       
       await con.commit();
       await con.close();
       console.log(result)
    }
    catch(ex){
        console.error(ex)
    }
    finally{

    }

}
```

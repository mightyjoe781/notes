# Databases Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: databases
This is part 1 of 1 parts

---

## File: databases/index.md

## Database

A database is an organized collection of data stored and accessed electronically. *Small databases* can be stored on a file system, while *large databases* are hosted on computer clusters or cloud storage. 

The design of databases spans formal techniques and practical considerations including data modeling, efficient data representation and storage, query languages, security and privacy of sensitive data, and distributed computing issues including supporting concurrent access and fault tolerance.

A database management system (DBMS) is the software that interacts with end users, applications, and the database itself to capture and analyze the data. The DBMS software additionally encompasses the core facilities provided to administer the database. The sum total of the database, the DBMS and the associated applications can be referred to as a database system.

### Tutorials

### Notes

- [SQL](sql/index.md)
- [PostgreSQL](postgresql/index.md)



---

## File: databases/postgresql/index.md

## PostgreSQL







### Resources

[Online PostgreSQL Queries](https://pg-sql.com)

### Notes



#### Setup on MacOS

NOTE : remove any already existing installation of postgresql.

Visit [Postgres.app](https://postgresapp.com) and download the app.

After that download [PG Admin 4](https://www.pgadmin.org/download/) , a web based tool to manage and inspect a Posters database. Can connect to local or remote server.

- Open Postgres.app connect/initialize a database
- Open PGAdmin 4 and in server -> register
  - set general name as localhost
  - set connection address localhost
  - set username as local mac username (for mac `whoami`)

#### PostgresSQL Complex Datatypes

Data Types Available : Numbers, Date/Time, Geometric, boolean, Currency, Character, Range, XML, Binary, JSON, Arrays, UUID.

Type Number can many types : smallint, integer, bigint, small serial, serial, big serial, decimal, numeric, real, double precision, float.

Type Character : CHAR (5), VARCHAR, VARCHAR(40), TEXT

Boolean Type : TRUE (`true, yes, on, 1, t, y`) , FALSE(`false, no, off, 0, f, n`), NULL.

Date Type : Date, Time, Time with Time Zone, Timestamps, Interval

#### Database-Side Validation Constraints

We usually create validation at a web-server level/interface and ensure integrity of data. For example if someonw inserts an item 	with negative price, certainly its implying we are going to pay the user.

PGAdmin 4 directly connects to table there is no validation web server present. So whatever we execute is going to happen in the database. We could add validation at a database level.

Create a new database in PGAdmin4 with name validation. Right select validation and select Query tool.

````postgresql
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR (40),
	department VARCHAR(40),
	price INTEGER NOT NULL,
	weight INTEGER
);
INSERT INTO products (name,department,price,weight)
VALUES
	('Shirt','Clothes','20','1');
````

Certainly we could also try to put `NULL` in the INSERT.

To implement some level of validation we can use NOT NULL Keyword to the database. If you already created the table and want to update the table.

````sql
ALTER TABLE products
ALTER COLUMN price
SET NOT NULL;
````

NOTE : If this price already have some null value you have to remove it before applying new constraint otherwise alter table won’t work.

Alternatively we can update all null values to some value 99999 and then apply ALTER.

````sql
UPDATE products
SET price = 99999
WHERE price IS NULL;
````

**Default Column Values**

````sql
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR (40) NOT NULL,
	department VARCHAR(40) NOT NULL,
	price INTEGER DEFAULT 9999,
	weight INTEGER
);
````

**Uniqueness Constraint**

````sql
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR (40) NOT NULL UNIQUE,
	department VARCHAR(40) NOT NULL,
	price INTEGER DEFAULT 9999,
	weight INTEGER
);
````

````sql
ALTER TABLE products
ADD UNIQUE(name)
````

Again you can’t apply unique constraint unless you clean up all duplicate values. To remove constraints you can use ALTER TABLE.

````sql
ALTER TABLE products
DROP CONSTRAINT products_name_key;
````

**Validation Check**

````sql
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR (40) NOT NULL UNIQUE,
	department VARCHAR(40) NOT NULL,
	price INTEGER CHECK (price > 0),
	weight INTEGER CHECK (weight > 10)
);
````

````sql
ALTER TABLE products
ADD CHECK (price > 0);
````

Checking multiple columns

````postgresql
CREATE TABLE orders (
	id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  est_delivery TIMESTAMP NOT NULL,
  CHECK (created_at < est_delivery)
);
````

If you have a webserver like nodejs or golang, where should we add validation ?

Generally use spread validation everywhere :)

You get 2 very important benifits

- We are certain that data is always correct when inside table.
- If say some data does get through web server and reaches the Database and database takes care of data.

### Database Design Patterns

Working with Many Tables requires *schema designer*, its easy and nice to document db structure. Few examples are dbdiagram.io, drawsql.app, sqldm.com, quickdatabasediagrams, ondras.zarovi.cz/sql/demo. Last one is an open source and quite good schema designer.

Instagram Database Design. 

#### Design Like System

We want to implement a like system.

Rules

- Each user can like a specific post a single time
- A user should be able `unlike` a post
- Need to be able to figure out how many users like a given post
- Need to be able to who likes a given post.
- Something aside a post like comments can be liked as well
- Keep track of dislike or reactions system

**DO NOT**

- Adding a ‘likes’ columns to Posts

**DO**

- Add a third table likes which has 2 columns such that it will relate user_id with post_id
- Add a unique constraint to (user_id, post_id) -> one player only likes one post.

**Polymorphic Association**

Not recommended but they are still in use. We will have a likes table with column id, user_id, liked_id, liked_type (posts, comments).

But there is an issue with above approach, user_id is consistently checked by postgres at insertion to make sure the user with inserted id exists. But in case of liked_id there is no such consistency check.

**An alternative design using polymorphic association**

So we will now change likes table to have id, user_id, post_id, comment_id such that only one row at a time will have either set post_id or comment_id.

````sql
CHECK (
  COALESCE ((post_id)::BOOLEAN::INTEGER, 0) + 
  COALESCE((comment_id)::BOOLEAN::INTEGER,0)) = 1;
````

Another solution we will create 2 tables posts_likes and comments_like and separate likes :) Only downside is we will have to create like for each new thing, but good thing is the consistency constraints.

#### Building a `Mention` System

Additional Features that are caption to post and adding location of the photo, we can also tagging people in the post.

Caption and location are obvious and easy to add but tagging the photo will require us to create a new table with id, user_id, post_id, x, y (for location of tag on the photo).

What about tags on caption ? we could set both x and y as null and it will represent tags inside caption or we can create new table which is called tags_caption, both solution are equally good.

Usually deciding factor is that if we are running too many queries for tags in caption then we should break into new tables.

#### Building a HashTag System

Hashtags are present in comments, posts, captions, users bio. We can certainly break it into 3 hashtag tables for each type.

But if generally notice the usage of hashtag which is in search feature, and there it is only searched across captions only so we can certainly get away with one hashtag table.

For performance reasons we cannot store every hashtag into the same hashtags table, we will split up and create a table with id, hashtag_id(foreign key), post_id where hashtag_id links id to title of tags in another separate table.

#### Adding more user data

We can add few more details about user, we can add Biography column, avatar url, phone number, emails , password (hashed), status (online/active/recently).

Why no posts, followers, following ?? We could certainly store them as simple numbers. But we can easily query of number of posts, and followers :). This concept is called as derived data and generally we dont’ store it unless its costly or difficult write query out.

We can create a simple table for followers id, user_id, follower_id with constraints like user never follows himself and can’t follow a person more than once.

````sql
CHECK (leader_id <> follower_id)
UNIQUE (leader_id, follower_id)
````

#### Implementing Database Design Patterns

Now course of action is realisation of above explained database design. Create a new db using PGAdmin. Open up the Query Tool and insert following Table creation.

````sql
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	username VARCHAR(30) NOT NULL,
	bio VARCHAR(400),
	avatar VARCHAR(200),
	phone VARCHAR(25),
	email VARCHAR(40),
	password VARCHAR(50),
	status VARCHAR(15),
	CHECK(COALESCE(phone, email) IS NOT NULL)
);
````

````sql
CREATE TABLE posts(
	id SERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  url VARCHAR(200) NOT NULL,
  caption VARCHAR(240),
  lat REAL CHECK(lat IS NULL OR (lat >= -90 AND lat <= 90)),
  lng REAL CHECK(lng IS NULL OR (lng >= -180 AND lng <= 180)),
	user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
````

````sql
CREATE TABLE comments (
	id SERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  contents VARCHAR(240) NOT NULL,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE
);
````

````sql
CREATE TABLE likes (
	id SERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  -- polymorphic association
  post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
  comment_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,
  -- either post or comments id defined, not both and not none (xor)
  CHECK(
  	COALESCE((post_id)::BOOLEAN::INTEGER,0)
    + 
    COALESCE((comment_id)::BOOLEAN::INTEGER,0)
    = 1
  ),
  UNIQUE(user_id, post_id, comment_id)
);
````

````sql
CREATE TABLE photo_tags (
	id SERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  UNIQUE(user_id, post_id)
);
CREATE TABLE caption_tags (
	id SERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  UNIQUE(user_id, post_id)
);
````

````sql
CREATE TABLE hashtags (
	id SERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  title VARCHAR(20) NOT NULL UNIQUE
);
CREATE TABLE hashtags_posts (
	id SERIAL PRIMARY KEY,
  hashtag_id INTEGER NOT NULL REFERENCES hashtags(id) ON DELETE CASCADE,
  post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  UNIQUE(hashtag_id, post_id)
);
CREATE TABLE followers (
	id SERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  leader_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  follower_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE(leader_id, follower_id)
);
````

**Inserting Fake Data**

Download this data [Link](https://att-c.udemycdn.com/2020-10-17_23-26-27-15aa9966355bf380cf0e5cb4ceec6ca7/original.sql?response-content-disposition=attachment%3B+filename%3Dig.sql&Expires=1650612712&Signature=Rj3YRtp6VrNRy7CpQKoMFR9NKX-5YwVb8GTCj5xaxlY5KzbX70UND12ObaGwVGEaNWxBhnk~Jh~UvX9HAtQTmlXL0MIAMjws43ds5jDU8zVfg1-9LEUu-Hn0Mrg2bQW~XDh~TSztnkb0LTVSjnkBjEeYCdu-ruR0evgnvHUV4kBDJg4hP1V9~II8e5dePI6bId~6HjBjU~gLLFCzPoyyXUThwtwvD4WkzYH3d5kXgDyz52rC0Smx-PEoLFt8MnBpzgpf7eup0dn50yCHOy0qirztH1LzSXOMRhyPJ7XoDypFrI5r9NXFMDge~N4wH16wSI72LvdDDhyXOV1jLMXlxw__&Key-Pair-Id=APKAITJV77WS5ZT7262A)

Right click database on PGAdmin 4 and restore. Then locate the file and select these 4 restore option : Only data, owner, Single Transaction, Trigger, verbose messages

Some execises 

- Find the 3 users with highest id number
- join users and posts table show the username of user id 200 and captions of all the post they created.
- Show each username and the number of `likes` that they have created.

### Internals of PostgreSQL

#### Where Does Postgres Store Data ?

`SHOW data_directory;` shows directory where postgres is storing data.

To see the folder where our database is stored.

```sql
SELECT oid, datname FROM pg_database;
```

If you see the corresponding folder you see a lots of file but why so many files ? To see the usage of all objects execute

```sql
SELECT * FROM pg_class;
```

#### Heaps, Blocks, and Tuples

Heap File : File that contains all the data about (rows) of our table.

Tuple or Item : Individual row from the table

Block or Page : The heap file is divided into different # of pages/blocks. 8k large.

Refer to this link for more details [Link](https://www.postgresql.org/docs/current/storage-page-layout.html).

#### A Look at Indexes for performance

````sql
SELECT * FROM users
WHERE username = 'smk'.
````

Steps that happen when u execute the query.

- Postgresql loads up heap file on RAM
- Full Table scan ( PG has to load many (or all) rows from the heap file to memory).
- Index : Data Structure that efficiently tells us what block/index a record is stored. Helps improve performance and remove the need of Full table scan.

Extract only the property we want to do fast lookup by and the block/index for each. To further improve performance for searching we can sort those indexes in some meaningful way. Usually we organize data into a tree data structure that evenly distributes the values in the leaf nodes.

Creating an Index for username table

````sql
CREATE INDEX ON users (username);
-- removing Indexes
DROP INDEX users_username_idx;
````

To benchmark a query try running following query after and before creating index

````sql
EXPLAIN ANALYZE SELECT *
FROM users
WHERE username = 'Emil30';
````

#### Downside of Indexes

For all index data there is a map storage is being utilised to house that index. For printing size of a table.

````sql
SELECT pg_size_pretty(pg_relation_size('users'));
````

- can be large
- expensive and slow insert/update/down - the index has to be updated
- index might not actually get used !

**Types of Index**

By default postgresql uses BTree Indexes, others are Hash, GiST, SP-GiST, GIN, BRIN.

#### Automatically Generated Indexes

Postgres by default creates indexes for

- primary keys
- Unique keys

These are not listed under ‘indexes’ in PGAdmin ! To check you can execure the following query.

````sql
SELECT relname, relking
FROM pg_class
WHERE relkind = 'i';
````

#### Query Tuning

<img src="index.assets/image-20220422232446091.png" alt="image-20220422232446091" style="zoom:50%;" />

Query we write goes to a Parser, Rewriter, Planner and then Executer.

Parser : processing of query, mostly validation and then creates query tree.

Rewriter : decompose views into underlying table references.

Planner : look at various plans and chooses most efficient plan. (this is point of optimisation )

Executer : actually runs the query !!

##### Planner Step :

 EXPLAIN : Build a query plan and display information about it.

EXPLAIN ANALYZE : Build a query plan, run it, and info about it.

Never use these in production.

````sql
EXPLAIN SELECT username, contents
FROM users
JOIN comments ON comments.user_id = users.id
WHERE username = 'Alyson14';
````

There is also a explain analyze builtin PGAdmin.

Every Query Node has a cost associated with it.  Query Planner is able to execute and plan because it has information about the table.

````sql
SELECT * FROM pg_stats WHERE tablename = 'users';
````

Cost : Amount of time to execute some part of our query plan.

Note : Loading data from random spots off a hard drive usually takes more time than loading data sequentially. So indexes use random fetch of maybe 2 pages while direct searching is doing fetch of 100 pages sequentially. So it may seem quantity wise that indexes are more efficient but random fetch comes with its own penalty.

$ cost = (\# pages)*1.0 + (\#rows)*0.01$

a row costs like 1 % of the how much 1 page costs.

To get more details about costs of different factors while runtime query use this [link](https://postgresql.org/docs/current/runtime-config-query.html)

Again planner decides the best course of action for the query we execute :)

#### Common Table Expression

A simple way to write sql queries more clearly.

Ques : Show the username of users who were tagged in a caption or photo before Jan 7th, 2010.

A simple option is take union of boths tags tables and then do join on username.

````sql
SELECT username, tags.created_at
FROM users
JOIN (
	SELECT user_id, created_at FROM caption_tags
  UNION ALL
  SELECT user_id, created_at FROM photo_tags
) AS tags ON tags.user_id = users.id
WHERE tags.created_at < '2010-01-07';
````

CTE Format.

````sql
WITH tags AS (
  SELECT user_id, created_at FROM caption_tags
  UNION ALL
  SELECT user_id, created_at FROM photo_tags
)
SELECT username, tags.created_at
FROM users
JOIN tags AS tags ON tags.user_id = users.id
WHERE tags.created_at < '2010-01-07';
````

#### Recursive CTEs

Useful anytime we have a tree or graph data structure. Must use a ‘union’ keyword. Its very very challanging concept.

````sql
WITH RECURSIVE countdown(val) AS (
	SELECT 10 AS val -- Intial, Non-recursive query
  UNION
  SELECT val-1 FROM countdown WHERE val > 1 -- recursive query
)
SELECT *
FROM countdown;
````

Ques - find the 2-3 degree contacts in our instagram app

````sql
WITH RECURSIVE suggestions(leader_id, follower_id, depth) (
	SELECT leader_id, follower_id, 1 AS depth
	FROM follwers
  WHERE follower_id = 1000
  UNION
  SELECT follower.leader_id, follwers.follower_id, depth+1
  from followers
  JOIN suggestions ON suggesions.leader_id = follwers.follower_id
  WHERE depth < 3
)
SELECT DISTINCT users.id, users.username
FROM suggestions
JOIN users ON users.id = suggestions.leader_id
WHERE depth > 1
LIMIT 30;
````

### Views

Ques : Find the most popular user ? A simple solution would be :

````sql
SELECT
FROM users
JOIN (
	SELECT user_id FROM photo_tags
  UNION ALL
  SELECT user_id FROM caption_tags
) AS tags ON tags.user_id = users.id
GROUP BY username
ORDER BY COUNT(*) DESC;
````

To get to the answer of above query we are joining tables. But if we had to join tables too frequently it becomes inefficient to join tables again and again.

View is a like a fake table that wraps multiple tables together. We execute following query once ahead of time to avail views.

````sql
CREATE VIEW tags AS (
	SELECT id, created_at, user_id, post_id, 'photo_tag' AS type FROM photo_tags
  UNION ALL
  SELECT id, created_at, user_id, post_id, 'captions_tag' AS type FROM captions_tags
);
````

Now we use the above created view :

````sql
SELECT * FROM tags; -- above view is named as tags
SELECT * FROM tags WHERE type = 'caption_tag';
````

#### Updating and Deleting Views

````sql
CREATE OR REPLACE VIEW recent_views AS (
	SELECT *
  FROM posts
  ORDER BY created_at DESC
  LIMIT 15
);
````

````sql
DROP VIEW recent_posts;
````

#### Materialized Views

More formally *Views are queries that gets **executed every time** you refer to it* and Materialised Views are queries that gets executed at very specific times, but results are saved and can be referenced without rerunning the query.

Reason why we use Materialised Views is because it saves time when Views are expensive since results are saved.

Ques : For each week, show the number of likes that posts and comments recieved. Use the post and comment created_at, not when the like was received.

````sql
SELECT
	date_trunc('week',COALESCE(posts.created_at, comments.created_at)) AS week,
	COUNT(posts.id) AS num_posts,
	COUNT(comments.id) AS num_comments
FROM likes
LEFT JOIN posts ON posts.id = likes.post_id
LEFT JOIN comments ON comments.id = likes.comment_id
GROUP BY week
ORDER BY week;
````

Running above query takes a lots of time to execute, and if we run it again and again it will be slow to do more operation on views created. Materialized views helps caching the results of the query.

````sql
CREATE MATERIALIZED VIEW weekly_likes AS (
  SELECT
    date_trunc('week',COALESCE(posts.created_at, comments.created_at)) AS week,
    COUNT(posts.id) AS num_posts,
    COUNT(comments.id) AS num_comments
  FROM likes
  LEFT JOIN posts ON posts.id = likes.post_id
  LEFT JOIN comments ON comments.id = likes.comment_id
  GROUP BY week
  ORDER BY week;
 ) WITH DATA;
````

### Handling Concurrency and Reversibility with Transaction

#### Transactions

![image-20220425115826717](index.assets/image-20220425115826717.png)

If server crashes happen after the first step has completed then 50$ is lost in the system. So transaction ensure that either the entire process completes sucessfully or nothing changes.

To start transaction block start queries with `BEGIN` keyword.

Now what transaction does typically is create a virtual workspace kind of system where while executing queries if there is a error or mistake system will go in abort state and we will need to execute `ROLLBACK`, you can execute ROLLBACK yourself even though there is no error to revert current transaction block. After making intended queries execute `COMMIT` to make the changes permanent.

NOTE : while you are in transaction blocks and whatever changes you are making will not be reflected in the database until you commit changes. So if there is another client connected to database he will not see any updates.

````sql
-- Beginning of transaction block
BEGIN;
UPDATE accounts
SET balance = balance-50
WHERE name = 'Alyson';
-- if there is an error system will go in abort state
-- system will not respond to queries until ROLLBACK is passed
-- ROLLBACK will end the current transaction block
COMMIT; -- makes changes permanent
````

#### Managing Database Design with Schema Migrations

Schema Migration is all about changes structure of database.

Let’s say you are working an environment where making changes to the database breaks the applications running on that database i.e. lets say API. In that case if you want to share some updates to API as well as Database through a commit such that it won’t break the application. We use migration files that can be used by the person reviewing your requests for merge. They can easily change their database locally and updates to API you made and then revert back changes if they don’t like the commit or else accept the PR.

Migration Files : have two components UP (contains upgrades to structures of DB) and DOWN (undo whatever UP does).

**Issues solved by Migration Files**

- Changes to DB Structures and changes to clients need to be made at precisely the same time
- When working with other engineers, we need a really easy way to tie the structure of our database to our code.

Schema Migration Libraries are available almost in every language. Always write your own Migrations rather than using automatic migration provided with language.

```bash
mkdir -p pg-migrate
cd pg-migrate
npm init -y
npm install node-pg-migrate pg
```

```bash
npm run migrate create table comments
```

````js
/* eslint-disable camelcase */
exports.shorthands = undefined;
exports.up = pgm => {
    pgm.sql(`
        CREATE TABLE "comments" (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            content VARCHAR(255) NOT NULL
        );
    `);
};
exports.down = pgm => {
    pgm.sql(`
        DROP TABLE "comments";
    `);
};
````

**SETUP Database_URL**, NOTE : it varies if used in different Operating System, also remember to make database beforehand.

Then run following command :

````bash
DATABASE_URL=postgres://smk@localhost:5432/socialnetwork npm run migrate up
````

````bash
DATABASE_URL=postgres://smk@localhost:5432/socialnetwork npm run migrate down
````

More example of renaming a column

````bash
npm run migrate create rename contents to body
````

````js
/* eslint-disable camelcase */

exports.shorthands = undefined;

exports.up = pgm => {
    pgm.sql(`
        ALTER TABLE "comments"
        RENAME COLUMN "contents" TO "body";
    `);
};

exports.down = pgm => {
    pgm.sql(`
        ALTER TABLE "comments"
        RENAME COLUMN "body" TO "contents";
    `);
};
````

### Schema vs Data Migrations

Task : Remove x,y or lat/lng columns and create a new column with name loc and data type point.

We will split the process in mainly 3 steps : 

- Creating a new column called as loc with type point
- Copy lat/lng to the loc
- Drop the lat/lng column

Probably we should use transactions to make sure that above process happens completely.

Now lets assume there is API server POSTing data in real time :) . You transaction blocks won’t take them in consideration and we will have error or nulls.

Ideal process will be :

1. Add column loc
2. Deploy new Version of API that will write values to both lat/lng and loc
3. Copy lat/lng to loc
4. Update code to only write to loc column
5. Drop columns lat/lng

**Transaction Locks**

If one transaction has locked a row then another transaction can’t access it to update. But if transaction number is one is quite large then other transaction/updates will need to wait for it to finish. These transaction/updates will not terminate or error out they will just wait forever until either the first transaction is rolled back or committed.

#### Accessing PostgreSQL from API’s

````bash
mkdir social-repo
cd social-repo
npm init -y
npm install dedent express jest node-pg-migrate nodemon pg pg-format supertest
````

Replace “test” from scripts in package.json to :

````json
  "scripts": {
    "migrate": "node-pg-migrate",
    "start": "nodemon index.js"
  },
````

````bash
npm run migrate create add users table
````

````javascript
/* eslint-disable camelcase */
exports.shorthands = undefined;
exports.up = pgm => {
    pgm.sql(`
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            bio VARCHAR(400),
            username VARCHAR(100) UNIQUE NOT NULL
        );
    `);
};
exports.down = pgm => {
    pgm.sql('DROP TABLE users;');
};
````

NOTE : Create a database `socialnetwork`

To run migration : `DATABASE_URL=postgres://smk@localhost:5432/socialnetwork npm run migrate up`

We will create a Node API

![image-20220425185931927](index.assets/image-20220425185931927.png)

Create `src/app.js`

````javascript
const express = require('express');
const usersRouter = require('./routes/users.js');

module.exports = () => {
    const app = express();
    app.use(express.json());
  	app.use(usersRouter);
    return app;
};
````

Create a file `src/routes/users.js`

````javascript
const express = require('express');

const router = express.Router();

router.get('/users', (req, res) => {});

router.get('/users/:id', (req, res) => {});

router.post('/users', (req, res) => {});

router.put('/users/:id', (req, res) => {});

router.delete('/users/:id', (req, res) => {});

module.exports = router;
````

PG module just creates a connection to Postgresql backend, PG is very famous Node package and underlying power of many packages.

PG maintains a pool instead of creating clients. A pool internally maintains several different clients that can be reused. You only need client when running transactions.

Create a new `src/pool.js`

````javascript
const pg = require('pg');

class Pool {
    _pool = null;

    connect(callback) {
        this._pool = new pg.Pool(callback);
        return this._pool.query('SELECT 1 + 1;');
    }
    close() {
        this._pool.end();
    }
    // big security issue here
    query(sql) {
        return this._pool.query(sql);
    }
}

module.exports = new Pool;
````

Create a file `index.js`

````javascript
const app = require('./src/app.js');
const pool = require('./src/pool.js');

pool.connect({
    host: 'localhost',
    user: 'smk',
    port: 5432,
    database: 'socialnetwork',
    password: ''
})
  .then(() => {
  app.listen(3000, () => {
    console.log('Server is running on port 3000');
  });
})
  .catch(err => {
  console.log(err);
});
````

Complete Code Available at [Link](https://github.com/mightyjoe781/social-pg/tree/v1)

#### Security Issues around SQL

**SQL Injection**

We never, ever directly concatenate user provided input into a sql query. There are a variety of safe ways to get user-provided values into a string.

There are 2 solution : 

- Add code to ‘sanitize’ user-provided values to our app.
- Rely on Postgres to sanitize values for us.

Postgres create a `prepared` statement and executes the prepared statement. Use `$1` variable for assigning values.



---

## File: databases/sql/index.md

## SQL

SQL (Structured Query Language) is a domain-specific language used in programming and designed for managing data held in a relational database management system (RDBMS), or for stream processing in a relational data stream management system (RDSMS). It is particularly useful in handling structured data, i.e. data incorporating relations among entities and variables. 

Database Design

- What kind of *thing* are we storing ? (Tables)
- What *properties* does this thing have ? (Columns)
- What *type* of data does each of the properties contain ? (Records)

Table : Collection of records contained within database.

Column : Each column records one property about row.

Records : Each row represents one record.

Keyword : Tell the database that we want to do something. Always written in capital letters.

Indentifiers : Tell the database what thing we want to act on. Always written in lowercase letters.

#### Creating a Table

````postgresql
CREATE TABLE cities(
  -- column_name data_type
  name VARCHAR(50),
  country VARCHAR(50),
  population INTEGER,
  area INTEGER
);
````

VARCHAR : is just variable length character.

#### Inserting Data in Table

````postgresql
INSERT INTO cities (name, country, population, area)
VALUES ('Tokyo', 'Japan', 38505000, 8223);
````

Note all the values must map up to the values we enter. If we are entering all columns we could skip column naming.

#### Insert Multiple Data in Table

````postgresql
INSERT INTO cities (name, country, population, area)
VALUES ('Delhi', 'India', 28125000, 2240),
('Shanghai', 'China', 22125000, 4015),
('Sao Paulo', 'Brazil', 20935000, 3043);
````

#### Retrieving Data

**All Columns**

````postgresql
SELECT * FROM cities;
````

**Specific Columns**

````postgresql
SELECT area, name, population, name FROM cities;
````

Columns can be entered in any order, any number of times while selecting.

We can also transform or process data before recieving it i.e. Alias and Calculations.

````postgresql
SELECT name, population / area AS population_density
FROM cities;
````

#### String Operators and Functions

- `||` Join two string
- CONCAT() : joins two strings
- LOWER() : gives a lower case string
- UPPER() : gives a UPPER case string
- LENGHT(): gives number of characters in string

````sql
SELECT name || country AS location FROM cities; 	  -- delhi India
SELECT name || ', ' || country AS loc FROM cities; 	-- delhi, India
````

````sql
SELECT CONCAT(name,', ',country) AS loc FROM cities;
````

````sql
SELECT
	CONCAT(UPPER(name),', ',UPPER(country)) AS loc
FROM 
	cities;
````

#### Filtering Records

WHERE Keyword : filters records based on some conditions.

````sql
SELECT name, area FROM cities WHERE area > 4000;
````

Conditional Operators `= , >, <, >=, <= , != , <>, IN, NOT IN, BETWEEN`.

<> : is same as != , IN : value present in list ?, BETWEEN : value present between two other values.

````sql
SELECT name, area FROM cities WHERE area BETWEEN 2000 AND 4000;
````

````sql
SELECT name, area FROM cities WHERE
	name IN ('Delhi','Shangai');
````

We can have as many as compound checks connected using `OR` , `AND`.

We can also put **calculations** in WHERE clause.

#### Updating Records

````sql
UPDATE cities SET population = 39505000 WHERE name = 'Tokyo';
````

#### Deleting Records

````sql
DELETE FROM cities WHERE name = 'Tokyo';
````

#### Database Design

Design a Database for Photo-Sharing App. 

To approach the problem, analyze your app and ask yourself what type of resources exist in your app. Create a table for each of these features. Features that seem to indicate *relationship* or *ownership* between two resources needs to be reflected in our table design.

There are 4 types of tables : users, photos, comments, likes.

#### Relationship within Databases

- One-to-Many i.e. user-to-photos
- Many-to-One i.e. photos-to-user

Both relations given above are almost same it depends on Perspective :)

- One-to-One i.e. company-to-ceo, boats-to-captains.
- Many-to-Many i.e. students-to-course, tasks-to-engineers, movies-to-actors

#### Primary and Foreign Keys

**Primary Key** : Uniquely identifies a records in a table.

**Foreign Key** : identifies a record (usually in another table) that this row is associated with.

Usually `many` side of relationship gets the foreign key column. So comments table is connected to users and photos.

Properties of Primary Key : 

- each row in every table has one primary key.
- no other row in the same table can have the same value.
- 99% of the time its named as `id`
- either a integer or UUID.
- primary key never changes.

Properties of Foreign Key :

- rows will only have this if they belong to another record.
- many rows in the same table can have same foreign key.
- name varies, usually called as `xyz_id`
- exactly equal to primary key of the reference table
- will change if relation ship changes

#### Auto-Generated ID’s

````sql
CREATE TABLE users (
  -- serial keyword is used for auto generated ID
	id SERIAL PRIMARY KEY,
  username VARCHAR(50)
);

INSERT INTO users (username)
VALUES ('monahan93'),
	('prfrerres'),
	('freeBSD');
````

#### Creating Foreign Keys

````sql
CREATE TABLE photos (
	id SERIAL PRIMARY KEY,
	url VARCHAR(200),
  user_id INTEGER REFERENCES users(id)
);
````

````sql
SELECT url, username FROM photos JOIN users ON users.id = photos.user_id;
````

#### Foreign Key and Constraints Around Insertion

If we want to add a record to photos table we will certainly expect a user to exist. Reference needs to exist or we will get foreign key constraint error.

Now if you still want to insert a photo that is not associated with user. Pass the value as `NULL` for the no association with user.

````sql
INSERT INTO photos(url, user_id) 
VALUES ('seaside.png',NULL);
````

#### Foreign Key and Constraints Around Deletion

If we delete the user we will have dangling references for photos to users. We will need to set them to null.

- ON DELETE RESTRICT (default) : spits out error message
- ON DELETE NO ACTION : error
- ON DELETE CASCADE : deletes the photos too
- ON DELETE SET NULL : sets user_id field to NULL in photos table
- ON DELETE SET DEFAULT : sets to some default value, if one provided.

````sql
CREATE TABLE photos (
	id SERIAL PRIMARY KEY,
	url VARCHAR(200),
  user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);
````

#### Relating Records with Joins

Use this sample data [Link](http://p.ip.fi/NxI7)

**Joins** : Produces values by merging together rows from different related tables. Use a join *most* times that you are asked to find data that involves multiple resources.

**Aggregation** : Looks at many rows and calculates a single value. Words like ‘most’, ‘average’, ‘least’ are signs that you need to use an aggregation.

Ques : For each comment, show the content of the comment and user who wrote it.

````sql
SELECT contents, username FROM comments
JOIN users ON users.id = comments.user_id;
````

Ques : For each comment, list the contents of the comment and the URL of the photo the comment was added to.

````sql
SELECT contents, url FROM comments
JOIN photos ON photos.id = comments.photo_id;
````

An another syntax, notice the table order :P

````postgresql
SELECT comments.id AS comment_id, p.id
FROM photos AS p
JOIN comments ON p.id = comments.photo_id;
````

**NOTE** : Table order between ‘FROM’ and ‘JOIN’ frequently makes a difference.

We must provide context if column name collide. Tables can be renamed using the `AS` Keyword.

Ques : Show each photo and associated user. Given some photos might not have users and they will be marked as NULL.

Notice if we use query given above, it won’t work because there is no user which is NULL so join condition doesn’t let us join that photo. We will use Left Join

#### Types of Join

Consider two tables $A$ and $B$

- Inner Join (default JOIN) : $A \and B$

````sql
SELECT url, username FROM photos
JOIN users ON users.id = photos.user_id;
````

- Left Join : $A - B$ : Everything of A table is kept

````sql
SELECT url, username FROM photos
LEFT JOIN users ON users.id = photos.user_id;
````

- Right Join : $B - A$ : Everything of B table is kept

````sql
SELECT url, username FROM photos
RIGHT JOIN users ON users.id = photos.user_id;
````

- Outer Join : $ A \or B$ : Merge as many rows as possible.

````sql
SELECT url, username FROM photos
OUTER JOIN users ON users.id = photos.user_id;
````

Now we know that these are different join, it must be clear ORDER of tables in JOIN matters!

**WHERE** Keyword.

Ques : Who is commenting on their photo ?

````sql
SELECT url, contents FROM comments
JOIN photos ON photos.id = comments.photo_id
WHERE comments.user_id = photos.user_id;
````

**Three Way Join** : We never printed the user in above query :)

````sql
SELECT url, contents FROM comments
JOIN photos ON photos.id = comments.photo_id
JOIN users ON users.id = comments.user_id AND users.id = photos.user_id;
````

#### Aggregation of Records

Grouping : reduces many rows down to fewer rows. Done by using the `GROUP BY` Keyword. Visualizing the result is key to use.

````sql
SELECT user_id FROM comments
GROUP BY user_id;
````

Notice the selected column, we can only selected grouped column.

Aggregates : reduces many values down to one. Done by using `aggregate fucntions`.

Examples : COUNT, SUM, AVG, MIN, MAX

````sql
SELECT MAX(id) FROM comments;
````

Combining Group by and Aggregates 

````sql
SELECT user_id, COUNT(id) AS num_comments_created
FROM comments
GROUP BY user_id;
````

**NOTE** : Important : Issues with COUNT is that it doesn’t count NULL values. So it is recommended to use `*`

````sql
SELECT user_id, COUNT(*) AS num_comments_created
FROM comments
GROUP BY user_id;
````

Ques : Find the number of Comments for each photo.

````sql
SELECT photo_id, COUNT(*)
FROM comments
GROUP BY photo_id;
````

**Having Keyword**

Ques : find the number of components for each photo where the photo_id is < 3 and Photo has more than 2 comments.

Note : mostly we use aggregate function inside Having

````sql
SELECT photo_id, COUNT(*)
FROM comments
WHERE photo_id < 3
GROUP BY photo_id
HAVING COUNT(*) > 2;
````

Ques : find the user_ids where the user has commented on the photo with photo_id < 50 and the user added more than 20 comments on those photos.

````sql
SELECT user_id, COUNT(*)
FROM comments
WHERE photo_id < 50
GROUP BY user_id
HAVING COUNT(*) > 2;
````

#### Note : This Order of Keywords is fixed.

- **FROM** : specifies starting set of rows to work with.
- **JOIN** : merges data from another table.
- **WHERE** : Filters the set of rows.
- **GROUP BY** : Groups rows by unique set of values.
- **HAVING** : Filters the set of groups

#### Sorting

````sql
SELECT *
FROM products
-- default order is ASC;
ORDER BY price;
-- ORDER BY price DESC;
````

Mutiple ordering instructions

````sql
SELECT *
FROM products
ORDER BY price, weight DESC;
````

#### Offset and LIMIT

Offset : Skips the first n rows of the result set.

Limit : only gives the first n rows of result set.

````sql
SELECT * FROM users OFFSET 40;
````

````sql
SELECT * FROM users LIMIT 10;
````

Ques : Find first 5 most expensive products

````sql
SELECT *
FROM products
ORDER BY price DESC
LIMIT 5;
````

generally we use offset after limit keyword, but order doesn’t matter :P

#### Unions and Intersections Sets

Ques : Find the 4 products with the highest price **and** the 4 products with the highest price/weight ratio.

````sql
(	
  SELECT *
	FROM products
	ORDER BY price DESC
	LIMIT 4
)
-- by default UNION removes all duplicated items
-- can change default behaviour using UNION ALL
UNION
(
  SELECT *
	FROM products
	ORDER BY price/weight DESC;
	LIMIT 4
);
````

NOTE : parenthesis are optional but they are useful for precendence errors. Also selected columns must be same and named same.

Keywords : `UNION, UNION ALL, INTERSECT, INTERSECT ALL, EXCEPT, EXCEPT ALL `

UNION : joins result of both queries and removes duplicates.

INTERSECT : find the same rows in both query.

EXCEPT : Finds the rows which are in first query but not in the second query.

#### Assembling queries with SubQueries

List the name and price of all products that are more expensive than all products in Toys department. We can see its 2 queries.

````sql
SELECT name, price
FROM products
WHERE price > (
  SELECT MAX(price) FROM products WHERE Department = 'Toys'
);
````

Subqueries can be used as A source of a value, A source of rows, Source of a column but we must be careful of the structure of data that comes back from Subquery.

````sql
SELECT p1.name, (SELECT COUNT(name) FROM PRODUCTS) -- type : value
FROM (SELECT * FROM products) AS p1 -- alias is a must -- type : source of rows
JOIN (SELECT * FROM products) AS p2 ON p1.id = p2.id
WHERE p1.id IN (SELECT id FROM products);			-- type : source of column
````

note : There are two more keywords that are used with where are `ALL/SOME`.

##### Co-related Query

Ques : Show the name, department and price of the most expensive product in each department.

````sql
SELECT name, department, price
FROM products AS p1
WHERE price p1.price = (
	SELECT MAX(price)
  FROM products AS p2
  -- notice how we relate to value from p1 :P co-related :P
  WHERE p2.department = p1.department
);
````

Without using a join or a group by, print the number of orders for each product

````sql
SELECT name, (
	SELECT COUNT(*)
  FROM orders AS o1
  WHERE o1.product_id = p1.id
)
FROM products AS p1
````

##### SELECT without FROM :)

````sql
SELECT (
	SELECT MAX(price) FROM products
);
````

#### DISTINCT Keyword

````sql
SELECT DISTINCT department
FROM products;
````

#### Utility Operators, Keywords, and Functions

Greatest

````sql
SELECT GREATEST (200, 10, 12);
-- better example -- kinda max operation :)
SELECT name, weight, GREATEST(30, 2*weight)
FROM products;
````

Least

````sql
SELECT LEAST (200, 10, 12);
````

CASE

````sql
SELECT name, price,
	CASE
		WHEN price > 600 THEN 'high'
		WHEN price > 300 THEN 'medium'
		ELSE 'cheap'
	END
FROM products,
````



---


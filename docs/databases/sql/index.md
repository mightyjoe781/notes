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


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


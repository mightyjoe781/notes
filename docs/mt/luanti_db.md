# Managing Postgres Backend

## Minetest Storage

```txt
                List of relations
 Schema |          Name          | Type  | Owner
--------+------------------------+-------+-------
 public | auth                   | table | smk
 public | blocks                 | table | smk
 public | player                 | table | smk
 public | player_inventories     | table | smk
 public | player_inventory_items | table | smk
 public | player_metadata        | table | smk
 public | user_privileges        | table | smk
(7 rows)
```

Usually `sqlite` is best for `modstorage` in Luanti. Rest all could be stored on PostgreSQL.
https://niklp.net/posts/minetest-postgresql-benchmark/
## Running Migrations

`world.mt` state before migration

```mt
enable_damage = true
creative_mode = false
auth_backend = sqlite3
player_backend = sqlite3
backend = sqlite3
gameid = minetest
world_name = prismo
mod_storage_backend = sqlite3
```

Add postgresql details for each tables

```mt
enable_damage = true
creative_mode = false
auth_backend = sqlite3
player_backend = sqlite3
backend = sqlite3
gameid = minetest
world_name = prismo
mod_storage_backend = sqlite3
pgsql_connection = host=postgres_db port=5432 user=smk password=mypassword dbname=prismo
pgsql_auth_connection = host=postgres_db port=5432 user=smk password=mypassword dbname=prismo
pgsql_player_connection = host=postgres_db port=5432 user=smk password=mypassword dbname=prismo
```

Execute following commands

```bash
~/mt/bin/luantiserver --migrate postgresql --world ~/worlds/prismo
~/mt/bin/luantiserver --migrate-player postgresql --world ~/worlds/prismo
~/mt/bin/luantiserver --migrate-auth postgresql --world ~/worlds/prismo
```


Source : https://forum.luanti.org/viewtopic.php?t=16689

## Accessing the Database

Essentially internally Postgres versions each row do get rid of ghost writes using Versioning. Eventually all these dangling version needs to be cleaned up every now and then (usually postgres cleans it eventually).

```bash

psql -h hostname -p port -U username -d database_name
# prompt for password >

# list all tables
> \dt
> SELECT pg_size_pretty(pg_total_relation_size('public.blocks')) AS size;

# vaccum a table
VACUUM [VERBOSE] schema_name.table_name;

# vaccum entire db
VACUUM;
```

## Backups !

```bash
pg_dump -U username -h hostname -F c -b -v -f /path/to/backup/file.backup dbname
```

`-U` : username
`-h` : host
`-F c` : custom format
`-b` : include large objects
`-v` : verbose
`-f`: output file
`dbname` : database name

Example taking prismo backup

```sh
pg_dump -U prismo -h 127.0.0.1 -b -v -f ~/bkp/20251018_adv.backup adventure
```

## Trimming Database

Since Luanti Maps are generated using a Perlin noise, we can trim database to make our database lean.

https://github.com/minetest-go/mapcleaner
https://github.com/random-geek/MapEditr

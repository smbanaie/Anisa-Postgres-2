# How to Set Up a Foreign Data Wrapper in PostgreSQL

## Query a table in one database from another



**A foreign data wrapper is an extension available in PostgreSQL that allows you to access a table or schema in one database from another.** Foreign data wrappers can serve all sorts of purposes:

- Completing a data flow cycle
- Your data may be segregated across databases, but still related in ways that makes being able to combine or aggregate it desirable
- Allows you to control the permissions on the foreign tables

Let’s go!

For this example, we’ll use the databases `localdb` and `foreigndb`. I want to access a table `account_metrics` in `foreigndb` from `localdb`:

```
postgres=# \lList of databasesName    |  Owner   | Encoding | Collate | Ctype |   Access privileges-----------+----------+----------+---------+-------+-----------------------localdb | postgres | UTF8     | C       | C     |foreigndb | postgres | UTF8     | C       | C     |(2 rows)
```

And a look at the `account_metrics` table:

```
foreigndb=# select * from account_metrics;id | time_spent | pages_viewed----+------------+--------------1 |         60 |            52 |        100 |            23 |         15 |            5(3 rows)
```

# **Step 1: Set up a Foreign User**

For security reasons, you’ll likely want to create a read-only user to act as the go-between. This foreign user is the user that we’ll use for user mapping, which will be discussed later in this article.

Let’s create a user `fdwUser` . Then, in the foreign database (`foreigndb`) we’ll grant this user read-only access to the table in question, and usage on the schema where our table lives (in this case `public` )

```
foreigndb=# CREATE USER fdwUser WITH PASSWORD 'secret';CREATE ROLEforeigndb=# GRANT USAGE ON SCHEMA PUBLIC TO fdwUser;GRANTforeigndb=# GRANT SELECT ON account_metrics TO fdwUser;GRANT
```

# Step 1.5: Update your `pg_hba.conf` if necessary

When our foreign data wrapper is set up, we’ll need the foreign server to prompt the user for a password. This is configured in `pg_hba.conf`

First, find where your `pg_hba.conf` is located. The most common installations for `postgreSQL` are `homebrew` and EnterpriseDB. However, the easiest way to find your data directory (where `pg_hba.conf` is located) is to query it directly in a `psql` instance:

```
foreigndb=# SHOW hba_file;hba_file-----------------------------------------/Library/PostgreSQL/11/data/pg_hba.conf(1 row)foreigndb=# SHOW data_directory;data_directory-----------------------------/Library/PostgreSQL/11/data(1 row)
```

Depending on your OS, you may need to log in as root to access `/Library/PostgreSQL/11/data` by logging in as `sudo su -` . Brew installations won’t require you to log in as the superuser.

Next, open `pg_hba.conf` in your text editor of choice. Under `IPv4 local connections` add a line for the foreign database using the read-only user. A record can have one of 7 formats, [see the documentation](https://www.postgresql.org/docs/9.1/auth-pg-hba-conf.html) for more information:

```
# IPv4 local connections:host    foreigndb       fdwuser         127.0.0.1/32            md5
```

Save the file and exit. If you logged in as root, logout using `ctrl + d`. Now you need to signal the server to reload the configuration file. Depending on how you’ve set up your databases, you’ll likely need to do this as the `postgres` user by using `sudo -u postgres`:

```
user$ sudo -u postgres pg_ctl reload -D /Library/PostgreSQL/11/data/server signaled
```

# Step 2: Create the Extension

Now connect to `localdb` and create the foreign data wrapper extension by running `CREATE EXTENSION postgres_fdw;` or `CREATE EXTENSION IF NOT EXISTS postgres_fdw;`

```
localdb=# CREATE EXTENSION IF NOT EXISTS postgres_fdw;CREATE EXTENSION
```

Check that worked by querying the database’s extensions:

```
localdb=# select * from pg_extension;extname    | extowner | extnamespace | extrelocatable | extversion | extconfig | extcondition--------------+----------+--------------+----------------+------------+-----------+--------------plpgsql      |       10 |           11 | f              | 1.0        |           |postgres_fdw |       10 |         2200 | t              | 1.0        |           |(2 rows)
```

# **Step 3: Create the Foreign Server**

Now we’re going to create the foreign server that we’ll import the foreign schema into. You can name this whatever you want. In this example I’ll name this one`foreigndb_fdw` . We’ll create the server with `OPTIONS` for our host, port, and the name of the foreign database as follows:

```
localdb=# CREATE SERVER foreigndb_fdw FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '127.0.0.1', port '5432', dbname 'foreigndb');CREATE SERVER
```

Let’s check and make sure that worked:

If you’re using `psql` you can use `\des` in the working database to list your foreign servers. You can also query it from `pg_foreign_server` :

```
localdb=# \desList of foreign serversName      |  Owner   | Foreign-data wrapper---------------+----------+----------------------foreigndb_fdw | postgres | postgres_fdw(1 row)localdb=# select * from pg_foreign_server;srvname    | srvowner | srvfdw | srvtype | srvversion | srvacl |                 srvoptions---------------+----------+--------+---------+------------+--------+---------------------------------------------foreigndb_fdw |       10 |  41198 |         |            |        | {host=127.0.0.1,port=5432,dbname=foreigndb}(1 row)
```

# Step 4: Create User Mapping

Now we’re going to create the user mapping. Let’s say that all of the objects and tables in `localdb` are owned by `localuser` . We’re going to create the user mapping for the foreign schema for this user as well. I don’t recommend setting up user mapping for the `postgres` superuser.

```
localdb=# CREATE USER MAPPING FOR localuser SERVER foreigndb_fdw OPTIONS (user 'fdwuser', password 'secret');CREATE USER MAPPING
```

Now, let’s check and make sure that worked by querying `pg_user_mapping` (restricted for users that are not the superuser) or `pg_user_mappings` which is not restricted:

```
localdb=# select * from pg_user_mapping;umuser | umserver |           umoptions--------+----------+--------------------------------41201 |    41199 | {user=fdwuser,password=secret}(1 row)localdb=# select * from pg_user_mappings;umid  | srvid |    srvname    | umuser |  usename  |           umoptions-------+-------+---------------+--------+-----------+--------------------------------41202 | 41199 | foreigndb_fdw |  41201 | localuser | {user=fdwuser,password=secret}(1 row)
```

**An important note about the fdwuser and its password**

As we set up `pg_hba.conf` earlier to be `md5` for this connection, we will need to supply a password. That password is required to be passed in to the usermapping. That password, as you can see above, is stored in plaintext in `pg_user_mapping` and `pg_user_mappings`. This can make things a little tricky if you have multiple environments, so you’ll need to give the `fdwUser` the same password in each environment. Otherwise, you will need to explicitly drop and recreate the FDW if you want the password to be different across environments. This is one reason why this user should **not** have write permission for tables, to help prevent injection attack. Make sure the password you’re using has high entropy and make sure you’re using unique passwords for all of your database users. If needed, set up a `.pgpass` file so you don’t need to remember them all.

# Step 5: Grant the Local User Access to the Foreign Data Wrapper

As we aren’t creating user mapping for the `postgres` superuser, we’ll need to grant our local user `localuser` access to the foreign data wrapper. Logged in as the `postgres` user in `localdb` do the following:

```
localdb=# GRANT USAGE ON FOREIGN SERVER foreigndb_fdw TO localuser;GRANT
```

Now we should be able to import the foreign schema as `localuser` .

# **Step 6: Import the Foreign Schema or Tables**

Now it’s finally time to import the foreign schema. In this case, we’ll import the public schema and limit it to the table that we’d like. I’m going to import this into the public schema of the local database, but you may want to create a different schema specifically for foreign tables. If you do so, you will need to use **schema-qualified language** when querying the foreign table.

Postgres also allows for you to create foreign tables that are mirrors of tables in the foreign database, or import only some columns from a foreign table. For more information, [see the documentation](https://www.postgresql.org/docs/9.5/sql-createforeigntable.html).

Log in as `localuser` and import the `foreigndb`’s `public` schema:

```
user$ psql -U localuser -d localdb
Password for user localuser:
psql (11.1)
Type "help" for help.localdb=> IMPORT FOREIGN SCHEMA public LIMIT TO (account_metrics) FROM SERVER foreigndb_fdw INTO public;IMPORT FOREIGN SCHEMA
```

# And that’s it!

The `localuser` now has read-only access to the `account_metrics` table located in `foreigndb` :

```
localdb=> select * from account_metrics;id | time_spent | pages_viewed----+------------+--------------1 |         60 |            52 |        100 |            23 |         15 |            5(3 rows)
```

What about other access? Test that you’re read-only by trying to insert a row into the foreign table:

```
localdb=> INSERT INTO account_metrics(time_spent,pages_viewed) VALUES (10,1);ERROR:  permission denied for table account_metrics
CONTEXT:  remote SQL command: INSERT INTO public.account_metrics(id, time_spent, pages_viewed) VALUES ($1, $2, $3)
```

As well, you can confirm that you can only access this table as the `localuser` and not the `postgres` user:

```
user$ psql -U postgres -d localdb
psql (11.1)
Type "help" for help.localdb=# select * from account_metrics;ERROR:  user mapping not found for "postgres"
```

Query away!

# Deleting the Foreign Data Wrapper

The easiest way I’ve found to completely delete a foreign data wrapper (and drop the FDW user) is by dropping the extension using `CASCADE`, revoking the permissions for the read-only user, and dropping any owned objects that depend on the read-only user. Don’t be alarmed, doing this won’t drop the original table from `foreigndb` :

```
user$ psql -U postgres -d localdb
psql (11.1)
Type "help" for help.localdb=# DROP EXTENSION IF EXISTS postgres_fdw CASCADE;NOTICE:  drop cascades to 3 other objects
DETAIL:  drop cascades to server foreigndb_fdw
drop cascades to user mapping for localuser on server foreigndb_fdw
drop cascades to foreign table account_metrics
DROP EXTENSIONlocaldb=# REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM fdwuser;REVOKElocaldb=# DROP OWNED BY fdwuser;DROP OWNEDlocaldb=# \c foreigndbYou are now connected to database "foreigndb" as user "postgres".foreigndb=# REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM fdwuser;REVOKEforeigndb=# DROP OWNED BY fdwuser;DROP OWNEDforeigndb=# DROP ROLE fdwuser;DROP ROLE
```

And that’s all there is to it! You’ve now completed your foreign data wrapper, and can freely query your imported foreign schema remotely.

Enjoy your newfound powers!
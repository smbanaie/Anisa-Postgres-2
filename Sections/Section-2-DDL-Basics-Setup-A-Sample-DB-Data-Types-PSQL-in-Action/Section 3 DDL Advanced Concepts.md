# A Step-by-Step Guide To PostgreSQL Temporary Table

**Summary**: in this tutorial, you will learn about the PostgreSQL temporary table and how to manage it effectively.

## Creating a PostgreSQL temporary table

A temporary table, as its name implied, is a short-lived table that exists for the duration of a database session. PostgreSQL automatically [drops](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-drop-table/) the temporary tables at the end of a session or a [transaction](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-transaction/).

To create a temporary table, you use the `CREATE TEMPORARY TABLE` statement:

```
CREATE TEMPORARY TABLE temp_table_name(
   column_list
);
```

In this syntax:

- First, specify the name of the temporary table after the `CREATE TEMPORARY TABLE` keywords.
- Second, specify the column list, which is the same as the one in the `CREATE TABLE` statement.

The `TEMP` and `TEMPORARY` keywords are equivalent so you can use them interchangeably:

```
CREATE TEMP TABLE temp_table(
   ...
);
```

A temporary table is visible only to the session that creates it. In other words, it is invisible to other sessions.

Let’s take a look at an example.

First, log in to the PostgreSQL database server using the `psql` program and [create a new database](https://www.postgresqltutorial.com/postgresql-create-database/) named `test`:

```
postgres=# CREATE DATABASE test;
CREATE DATABASE
postgres-# \c test;
You are now connected to database "test" as user "postgres"
```

Next, create a temporary table named `mytemp` as follows:

```
test=# CREATE TEMP TABLE mytemp(c INT);
CREATE TABLE
test=# SELECT * FROM mytemp;
 c
---
(0 rows)

```

Then, launch another session that connects to the `test` database and query data from the `mytemp` table:

```
test=# SELECT * FROM mytemp;
ERROR:  relation "mytemp" does not exist
LINE 1: SELECT * FROM mytemp;

```

As can see clearly from the output, the second session could not see the `mytemp` table. Only the first session can access it.

After that, quit all the sessions:

```
test=# \q
```

Finally, log in to the database server again and query data from the `mytemp` table:

```
test=# SELECT * FROM mytemp;
ERROR:  relation "mytemp" does not exist
LINE 1: SELECT * FROM mytemp;
                      ^

```

The `mytemp` table does not exist because it has been dropped automatically when the session ended, therefore, PostgreSQL issued an error.

## PostgreSQL temporary table name

A temporary table can have the same name as a permanent table, even though it is not recommended.

When you create a temporary table that shares the same name as a permanent table, you cannot access the permanent table until the temporary table is removed. Consider the following example:

First, [create a table](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-table/) named `customers`:

```
CREATE TABLE customers(
   id SERIAL PRIMARY KEY, 
   name VARCHAR NOT NULL
)
```

Second, create a temporary table with the same name: `customers`

```
CREATE TEMP TABLE customers(
    customer_id INT
);

```

Now, query data from the  `customers` table:

```
SELECT * FROM customers;
 customer_id
-------------
(0 rows)

```

This time PostgreSQL accessed the temporary table `customers` instead of the permanent one.

Note that PostgreSQL creates temporary tables in a special schema, therefore, you cannot specify the schema in the `CREATE TEMP TABLE` statement.

If you [list the tables](https://www.postgresqltutorial.com/postgresql-show-tables/) in the `test` database, you will only see the temporary table `customers`, not the permanent one:

```
                 List of relations
  Schema   |       Name       |   Type   |  Owner
-----------+------------------+----------+----------
 pg_temp_3 | customers        | table    | postgres
 public    | customers_id_seq | sequence | postgres
(2 rows)

```

The output shows the schema of the `customers` temporary table is `pg_temp_3`.

In this case, to access the permanent table, you need to use a fully qualified name i.e., prefixed with the schema. For example:

```
SELECT * FROM public.customers;
```

## Removing a PostgreSQL temporary table

To drop a temporary table, you use the [`DROP TABLE`](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-drop-table/) statement. The following statement uses the DROP TABLE statement to drop a temporary table:

```
DROP TABLE temp_table_name
```

Unlike the `CREATE TABLE` statement, the `DROP TABLE` statement does not have the `TEMP` or `TEMPORARY` keyword created specifically for temporary tables.

For example, the following statement drops the temporary table `customers` that we have created in the above example:

```
DROP TABLE customers
```

If you list the tables in the `test` database again, the permanent table `customers` will appear as follows:

```
test=# \d
                List of relations
 Schema |       Name       |   Type   |  Owner
--------+------------------+----------+----------
 public | customers        | table    | postgres
 public | customers_id_seq | sequence | postgres
(2 rows)

```

In this tutorial, you have learned about the temporary table and how to create and drop it using `CREATE TEMP TABLE` and `DROP TABLE` statements



# PostgreSQL SELECT INTO

**Summary**: in this tutorial, you will learn how to use the PostgreSQL `SELECT INTO` statement to create a new table from the result set of a query.

If you are looking for the way to select data into variables, check it out the [PL/pgSQL `SELECT INTO` statement](https://www.postgresqltutorial.com/plpgsql-select-into/).

## Introduction to PostgreSQL SELECT INTO statement

The PostgreSQL `SELECT INTO` statement [creates a new table ](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-table/)and [inserts data](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-insert/) returned from a query into the table.

The new table will have columns with the names the same as columns of the result set of the query. Unlike a regular [`SELECT`](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select/) statement, the `SELECT INTO` statement does not return a result to the client.

The following illustrates the syntax of the PostgreSQL `SELECT INTO` statement:

```
SELECT
    select_list
INTO [ TEMPORARY | TEMP | UNLOGGED ] [ TABLE ] new_table_name
FROM
    table_name
WHERE
    search_condition;

```

To create a new table with the structure and data derived from a result set, you specify the new table name after the `INTO` keyword.

The `TEMP` or `TEMPORARY` keyword is optional; it allows you to create a [temporary table](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-temporary-table/) instead.

The `UNLOGGED` keyword if available will make the new table as an unlogged table.

The `WHERE` clause allows you to specify the rows from the original tables that should be inserted into the new table. Besides the `WHERE` clause, you can use other clauses in the `SELECT` statement for the `SELECT INTO` statement such as `INNER JOIN`, `LEFT JOIN`, `GROUP BY`, and `HAVING`.

Note that you cannot use the `SELECT INTO` statement in PL/pgSQL because it interprets the `INTO` clause differently. In this case, you can use the `CREATE TABLE AS` statement which provides more functionality than the `SELECT INTO` statement.

## PostgreSQL SELECT INTO examples

We will use the `film` table from the [sample database](https://www.postgresqltutorial.com/postgresql-sample-database/) for the demonstration.

![PostgreSQL SELECT INTO sample table](images/film_table.png)

The following statement creates a new table called `film_r` that contains films with the rating `R` and rental duration 5 days from the `film` table.

```
SELECT
    film_id,
    title,
    rental_rate
INTO TABLE film_r
FROM
    film
WHERE
    rating = 'R'
AND rental_duration = 5
ORDER BY
    title;

```

To verify the table creation, you can query data from the `film_r` table:

```
SELECT * FROM film_r;
```

![img](images/PostgreSQL-Select-Into-Example.png)

The following statement creates a temporary table named `short_film` that contains the films whose lengths are under 60 minutes.

```
SELECT
    film_id,
    title,
    length 
INTO TEMP TABLE short_film
FROM
    film
WHERE
    length < 60
ORDER BY
    title;
```

The following shows the data from the `short_film` table:

```
SELECT * FROM short_film
```

![img](images/PostgreSQL-Select-Into-Temp-table-example.png)

In this tutorial, you have learned how to use the PostgreSQL `SELECT INTO` statement to create a new table from the result set of a query.



# PostgreSQL CREATE TABLE AS

**Summary**: in this tutorial, you will learn how to use the PostgreSQL `CREATE TABLE AS` statement to create a new table from the result set of a query.

## Introduction to the PostgreSQL CREATE TABLE statement

The `CREATE TABLE AS` statement [creates a new table](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-table/) and fills it with the data returned by a query. The following shows the syntax of the `CREATE TABLE AS` statement:

```
CREATE TABLE new_table_name

```

In this syntax:

1. First, specify the new table name after the `CREATE TABLE` clause.
2. Second, provide a query whose result set is added to the new table after the `AS` keyword.

The `TEMPORARY` or `TEMP` keyword allows you to to create a [temporary table](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-temporary-table/):

```
CREATE TEMP TABLE new_table_name 
AS query; 
```

The `UNLOGGED` keyword allows the new table to be created as an unlogged table:

```
CREATE UNLOGGED TABLE new_table_name
AS query;
```

The columns of the new table will have the names and data types associated with the output columns of the `SELECT` clause.

If you want the table columns to have different names, you can specify the new table columns after the new table name:

```
CREATE TABLE new_table_name ( column_name_list)
AS query;
```

In case you want to avoid an error by creating a new table that already exists, you can use the `IF NOT EXISTS` option as follows:

```
CREATE TABLE IF NOT EXISTS new_table_name
AS query
```

## PostgreSQL CREATE TABLE AS statement examples

We will use the `film` and `film_category` table from the [sample database ](https://www.postgresqltutorial.com/postgresql-sample-database/)for the demonstration.

![film_and_film_category_tables](images/film_and_film_category_tables.png)

The following statement creates a table that contains action films that belong to category one.

```
CREATE TABLE action_film AS
SELECT
    film_id,
    title,
    release_year,
    length,
    rating
FROM
    film
INNER JOIN film_category USING (film_id)
WHERE
    category_id = 1;

```

To verify the table creation, you can query data from the `action_film` table:

```
SELECT * FROM action_film
ORDER BY title;

```

![PostgreSQL CREATE TABLE AS data verification](images/PostgreSQL-CREATE-TABLE-AS-data-verification.png)

To check the structure of the `action_film`, you can use the following command in the psql tool:

```
\d action_film
```

It returns the following output:

![PostgreSQL CREATE TABLE AS example](images/PostgreSQL-CREATE-TABLE-AS-example.png)

As clearly shown in the output, the names and data types of the `action_film` table are derived from the columns of the `SELECT` clause.

If the `SELECT` clause contains expressions, it is a good practice to override the columns, for example:

```
CREATE TABLE IF NOT EXISTS film_rating (rating, film_count) 
AS 
SELECT
    rating,
    COUNT (film_id)
FROM
    film
GROUP BY
    rating;

```

This example statement created a new table `film_rating` and filled it with the summary data from the `film` table. It explicitly specified the column names for the new table instead of using the column names from the `SELECT` clause.

To check the structure of the `film_rating` table, you use the following command in psql tool:

```
\d film_rating
```

The following is the output:

![PostgreSQL CREATE TABLE AS with explicit column names](images/PostgreSQL-CREATE-TABLE-AS-with-explicit-column-names.png)

Note that the `CREATE TABLE AS` statement is similar to the `SELECT INTO` statement, but the `CREATE TABLE AS` statement is preferred because it is not confused with other uses of the `SELECT INTO` syntax in [PL/pgSQL](https://www.postgresqltutorial.com/postgresql-stored-procedures/). In addition, the `CREATE TABLE AS` statement provides a superset of functionality offered by the `SELECT INTO` statement.



#### Copy a Table

```sql
CREATE TABLE new_table AS TABLE existing_table WITH NO DATA;
```





# PostgreSQL TRUNCATE TABLE

**Summary**: in this tutorial, you will learn how to use PostgreSQL `TRUNCATE TABLE` statement to quickly delete all data from large tables.

## Introduction to PostgreSQL TRUNCATE TABLE statement

To remove all data from a table, you use the `DELETE` statement. However, when you use the `DELETE` statement to delete all data from a table that has a lot of data, it is not efficient. In this case, you need to use the `TRUNCATE TABLE` statement:

```
TRUNCATE TABLE table_name;
```

The `TRUNCATE TABLE` statement deletes all data from a table without scanning it. This is the reason why it is faster than the `DELETE` statement.

In addition, the `TRUNCATE TABLE` statement reclaims the storage right away so you do not have to perform a subsequent `VACUMM` operation, which is useful in the case of large tables.

## Remove all data from one table

The simplest form of the `TRUNCATE TABLE` statement is as follows:

```
TRUNCATE TABLE table_name;
```

The following example uses the `TRUNCATE TABLE` statement to delete all data from the `invoices` table:

```
TRUNCATE TABLE invoices;
```

Besides removing data, you may want to reset the values in the [identity column](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-identity-column/) by using the `RESTART IDENTITY` option like this:

```
TRUNCATE TABLE table_name 
RESTART IDENTITY;
```

For example, the following statement removes all rows from the `invoices` table and resets the [sequence](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-sequences/) associated with the `invoice_no` column:

```
TRUNCATE TABLE invoices 
RESTART IDENTITY;
```

By default, the `TRUNCATE TABLE` statement uses the `CONTINUE IDENTITY` option. This option basically does not restart the value in sequence associated with the column in the table.

## Remove all data from multiple tables

To remove all data from multiple tables at once, you separate each table by a comma (,) as follows:

```
TRUNCATE TABLE 
    table_name1, 
    table_name2,
    ...;
```

For example, the following statement removes all data from `invoices` and `customers` tables:

```
TRUNCATE TABLE invoices, customers;
```

## Remove all data from a table that has foreign key references

In practice, the table you want to truncate often has the [foreign key](https://www.postgresqltutorial.com/postgresql-foreign-key/) references from other tables that are not listed in the `TRUNCATE TABLE` statement.

By default, the `TRUNCATE TABLE` statement does not remove any data from the table that has foreign key references.

To remove data from a table and other tables that have foreign key reference the table, you use `CASCADE` option in the `TRUNCATE TABLE` statement as follows :

```
TRUNCATE TABLE table_name 
CASCADE;
```

The following example deletes data from the `invoices` table and other tables that reference the `invoices` table via foreign key constraints:

```
TRUNCATE TABLE invoices CASCADE;
```

The `CASCADE `option should be used with further consideration or you may potentially delete data from tables that you did not want.

By default, the `TRUNCATE TABLE` statement uses the `RESTRICT` option which prevents you from truncating the table that has foreign key constraint references.

## PostgreSQL TRUNCATE TABLE and ON DELETE trigger

Even though the `TRUNCATE TABLE` statement removes all data from a table, it does not fire any `ON DELETE` [triggers](https://www.postgresqltutorial.com/postgresql-triggers/) associated with the table.

To fire the trigger when the `TRUNCATE TABLE` command applied to a table, you must define `BEFORE TRUNCATE` and/or `AFTER TRUNCATE` triggers for that table.

## PostgreSQL TRUNCATE TABLE and transaction

The `TRUNCATE TABLE` is transaction-safe. It means that if you place it within a transaction, you can roll it back safely.

## Summary

- Use the `TRUNCATE TABLE` statement to delete all data from a large table.
- Use the `CASCADE` option to truncate a table and other tables that reference the table via foreign key constraint.
- The `TRUNCATE TABLE` does not fire `ON DELETE` trigger. Instead, it fires the `BEFORE TRUNCATE` and `AFTER TRUNCATE` triggers.
- The `TRUNCATE TABLE` statement is transaction-safe.
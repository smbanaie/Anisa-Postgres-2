# [Understand SQL Query execution more closely: PostgreSQL Operator and Cast](https://virender-cse.medium.com/understand-sql-query-execution-more-closely-postgresql-operator-and-cast-5c505d33f518)



In RDBMS, a query execution goes through a number of steps like syntax and semantic checks, generate a parse tree with an optimized plan, execute the nodes and return the results but ever wondered, there are more interesting pieces to a simple look like query execution? Take an example of following query ( column `name` is of type`text`):

> **SELECT employee_id FROM employee WHERE name = ‘Dungen_Master’;**

Let’s dig into `WHERE name='Dungen_Master’` part and understand how it works.

So here `=` is an operator defined in `pg_catalog` schema and it executes a function with two arguments (oprleft and oprright) of type `text`.

```
 SELECT oprname, oprnamespace::regnamespace, oprowner, oprleft::regtype, 
 oprright::regtype, oprcode from pg_operator 
 WHERE oprname='=' and oprleft::regtype='text'::regtype;

 oprname | oprnamespace | oprowner | oprleft | oprright |  oprcode
---------+--------------+----------+---------+----------+------------
 =       | pg_catalog   |       10 | text    | text     | texteq
```

We can create [new operators](https://medium.com/r?url=https%3A%2F%2Fwww.postgresql.org%2Fdocs%2Fcurrent%2Fsql-createoperator.html) to execute a non default function as per our needs.

## Use case of Operators:

Recently, I came across a migration project from SQL Server to PostgreSQL where queries were using Case Insensitivity and Accent Insensitivity in Sql Server and this functionality comes out of the box with collation defined at the column level in SQL Server. Customer don’t want to change a lot of their queries when porting the code to PostgreSQL.

PostgreSQL provides `citext` extension for case insensitivity and `unaccent` extension for accent insensitivity. While `citext` works transparently (no query changes required) but `unaccent` needs to add a function in the query. Let’s see with an example:

```
/* Test Setup */

create extension unaccent;
create extension citext;
drop table test;
create table test (id int, name citext);

/* Populate few values */

insert into test values(1,'Test'); 
insert into test values(1,'Hôtel'); 
insert into test values(1,'Hotel');
insert into test values(1,'hotel');

postgres=> select * from test;
 id | name
----+-------
  1 | Test
  1 | Hôtel
  1 | Hotel
  1 | hotel

/* Case Insensitive Query: Returning 'hotel' as well due to use of citext */

postgres=> select * from test where name='Hotel';
 id | name
----+-------
  1 | Hotel
  1 | hotel

/* Case insensitive & Accent insensitive Query: Missing 'hotel' */

postgres=> select * from test where unaccent(name)='Hotel';  
 id | name
----+-------
  1 | Hôtel
  1 | Hotel

/* Function definition of unaccent is returning text type, not citext */

postgres=> \df+ unaccent
                                                                              List of functions
 Schema |   Name   | Result data type | Argument data types | Type | Volatility | Parallel |  Owner   | Security | Access privileges | Language |  Source code  | Description
--------+----------+------------------+---------------------+------+------------+----------+----------+----------+-------------------+----------+---------------+-------------
 public | unaccent | text             | text                | func | stable     | safe     | postgres | invoker  |                   | c        | unaccent_dict |

/* Implicit cast the text to citext and now Query returns expected results */

postgres=> select * from test where unaccent(name)::citext='Hotel';
 id | name
----+-------
  1 | Hôtel
  1 | Hotel
  1 | hotel
```

Now let’s see how a custom operator helps to avoid this code change of additional function.

We will not be using `citext` extension anymore as will implement the functionality in the operator function so lets convert the data type to `text`.

> **ALTER TABLE test ALTER COLUMN name SET DATA TYPE text;**

Let’s create a new operator and change the *search_path* of the calling user. We are changing the *search_path* so the new function defined in the `public` schema appears before the default function defined in the `pg_catalog` schema.

```
CREATE OR REPLACE FUNCTION public.unacc_equal(text, text)
RETURNS BOOLEAN LANGUAGE sql immutable as $$
  select unaccent(lower($1)) operator(pg_catalog.=) unaccent(lower($2))
$$;

CREATE OPERATOR public.= (
LEFTARG = TEXT,
RIGHTARG = TEXT,
PROCEDURE = public.unacc_equal);

postgres=> show search_path;
   search_path
-----------------
 "$user", public

postgres=> set search_path to '$user', public, pg_catalog;
SET
```

Now Query is using the new operator which has both lower and unaccent functions applied on the inputs:

```
postgres=> select * from test where name='Hotel';
 id | name
----+-------
  1 | Hôtel
  1 | Hotel
  1 | hotel
```

We can create a functional Index to speed up the query execution.

```
create index idx on test(unaccent(lower(name)));

postgres=> explain select * from test where name='Hotel';
                                 QUERY PLAN
----------------------------------------------------------------------------
 Index Scan using idx on test  (cost=0.13..8.15 rows=1 width=36)
   Index Cond: (unaccent(lower(name)) OPERATOR(pg_catalog.=) 'hotel'::text)
```

Similarly we can override `like` operator for search queries.

```
create extension if not exists pg_trgm;

create index idx1 on test using gin(unaccent(lower(name)) gin_trgm_ops);
   
CREATE OR REPLACE FUNCTION public.unacc_like(text, text)
RETURNS BOOLEAN LANGUAGE sql immutable as $$
  select unaccent(lower($1)) operator(pg_catalog.~~) unaccent(lower($2))
$$;

CREATE OPERATOR public.~~ (
LEFTARG = TEXT,
RIGHTARG = TEXT,
PROCEDURE = public.unacc_like);

postgres=> select * from test where name like 'Hote%';
 id | name
----+-------
  1 | Hôtel
  1 | Hotel
  1 | hotel

postgres=> explain select * from test where name like 'Hote%';
                                    QUERY PLAN
-----------------------------------------------------------------------------------
 Bitmap Heap Scan on test  (cost=20.00..24.02 rows=1 width=36)
   Recheck Cond: (unaccent(lower(name)) OPERATOR(pg_catalog.~~) 'hote%'::text)
   ->  Bitmap Index Scan on idx1  (cost=0.00..20.00 rows=1 width=0)
         Index Cond: (unaccent(lower(name)) OPERATOR(pg_catalog.~~) 'hote%'::text)
```

So we can see with the new operators, we don’t need to change our queries. BTW, I have not done any performance comparison between default and non default operators.

## Cast:

A cast specifies how to perform a conversion between two data types. Now let’s try with another query which compares text to integer (earlier we were comparing text to text).

```
select * from employee where name=1;

ERROR:  operator does not exist: text = integer
LINE 1: select * from employee where name=1;
                                         ^
HINT:  No operator matches the given name and argument types. You might need to add explicit type casts.
```

Query failed because there is no default `=` operator comparing text to integer and also there is no cast doing conversion from integer to text. We can get this query working either by creating a new operator or adding an explicit type cast from integer to text.

```
select * from employee where name=1::text;
```

One limitation of defining an operator is that you need to define operators for all your use cases, say equality (=), inequality (!=) or like queries. So let’s create a custom cast and see that query now works without adding any explicit cast.

```
CREATE CAST (integer AS text) WITH INOUT AS IMPLICIT;

postgres=> \dC+ text
                                      List of casts
    Source type    |    Target type    |      Function      |   Implicit?   
-------------------+-------------------+--------------------+---------------
 integer           | text              | (with inout)       | yes           

select * from employee where name=1;
 name
------
(0 rows)
```

## Summary:

You can define new operators and cast based on your use case and that helps to avoid code changes. There can be more advanced use cases. For example, create an extension to define a new data type (something like `citext`) which has its own operators and cast rules. I recommend testing carefully specially on custom cast as they can cause unexpected behaviour some time. One such failure case is mentioned in the [official document](https://www.postgresql.org/docs/current/sql-createcast.html).
## About PostgreSQL

PostgreSQL has a high value in the world of database systems due to its capability to handle extensive amounts of data with high concurrency, ensuring data integrity, and offering numerous advanced features. As an open-source tool, it plays an essential role in the software industry, providing flexible and cost-effective solutions for various database-related tasks.

PostgreSQL is an object-relational database management system ([ORDBMS](https://www.techopedia.com/definition/8715/object-relational-database-management-system-ordbms)) that uses and extends the SQL language, combined with multiple features that safely store and scale complex data workloads. It is known for its robustness, advanced features, strong standards compliance, and versatility in managing diverse workloads.

Section 2

## Installation and Configuration

Understanding how to install and configure PostgreSQL is crucial for database administrators and developers, as it ensures optimal performance, security, and reliability of the database system. Proper installation and configuration lay the foundation for scalable applications, safeguard data integrity, and facilitate seamless integration with various software tools and platforms.

### Versioning and History 

The first implementation of [POSTGRES](https://www.postgresql.org/docs/current/history.html) began back in 1986 and was put into production in 1988. After the user community and demands doubled in size in the early 90s, the POSTGRES Project ended and Postgres95, an open-source SQL language interpreter, was launched. Since then, Postgres has continued to receive widespread adoption, especially with the introduction of the public cloud. With each release, there are significant enhancements and improvements providing more functionality and scalability for customer data. There are various versions of the open-source relational database, and by 1996, PostgreSQL 6.0 was born from the origin product.

In keeping with its yearly update cycle, PostgreSQL 16 ver. 2 was Beta released in June 2023. This newest version is expected to continue PostgreSQL's commitment to being a powerful, open-source, object-relational database system that emphasizes extensibility and standards compliance.

As in previous updates, PostgreSQL consistently made improvements to performance, functionality, and stability. Consequently, version 15 focused on areas such as enhancing partitioning and sharding capabilities, increasing performance for complex queries and improving the database's handling of JSON data. Version 16, on the other hand, has brought additional features for replication between primary/standby servers, better multi-core and parallel query execution, and more advanced maintenance utilities including advanced vacuum capabilities and development support. 

### Template Databases 

The [template database](https://www.postgresql.org/docs/current/manage-ag-templatedbs.html) concept is a valuable and functional feature in PostgreSQL. PostgreSQL is an advanced, open-source relational database system that provides an impressive range of features including the template database feature, which offers a convenient way to control the initial database setup whenever a new database is created.

A template database is essentially a model or a blueprint for creating new databases. Whenever a new database is created in PostgreSQL, it's a clone of a template database. The newly created database contains all the tables, functions, operators, and data present at the time of copying. PostgreSQL has two default template databases: template0 and template1.

1. `**template1**`: This is the default template database for PostgreSQL. Whenever a command is executed to create a new database without specifying any template, PostgreSQL uses `template1`. If you modify this database, for example, by installing extensions or changing parameters, all new databases created will inherit those changes, unless you specify otherwise.
2. `**template0**`: This is a backup template. This database contains the standard objects that a fresh install of PostgreSQL would contain. You can use it if you've somehow damaged `template1`. You can't connect to `template0` while any other connections exist, which means you can't modify it accidentally or intentionally. This is useful if you want to create a new database that's a clean slate and doesn't include any of the modifications present in `template1`.

Here's how to create a new database from a template:

```sql
CREATE DATABASE newdb WITH TEMPLATE originaldb OWNER dbuser;
```

You can also create your own template databases. For example, if you have a configuration for many databases, you can create a template database with that configuration and then use it as the template for creating new databases.

To create a database as a template, you can do the following:

1. Create a database
2. Connect to the new database and set up the database how you want your template to look
3. Disconnect from the database and then run the following command to set the database as a template:

```sql
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'my_template_db';
```

You can now use your new database as a template:

```sql
CREATE DATABASE new_db WITH TEMPLATE my_template_db OWNER dbuser;
```



The template database feature in PostgreSQL is a powerful tool for managing and streamlining the creation of new databases. It allows you to customize the default settings for new databases and ensure that they are set up in a consistent manner.

### Configuring a Database

At this point, you’ve installed PostgreSQL and created a database and the Postgres database user. There are steps recommended for more advanced [configurations of PostgreSQL](https://www.postgresql.org/docs/16/manage-ag-config.html) to secure and ensure the system is ready for use, some of which will be reviewed here.

In the first step, we will create a role for the database user to control specific grants for the application:



```sql
CREATE ROLE app_role LOGIN PASSWORD 'rolepassword';
```



The next step is to create the initial schema/user and assign the role:

```sql
CREATE USER myuser;
GRANT app_role TO myuser;
```



Set a password for the user — you can set a password for the newly created role using the `ALTER ROLE` SQL command. Replace mypassword with your desired password from the example:

```sql
ALTER USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
```



PostgreSQL supports fine-grained access control through roles and privileges. You can grant privileges to the new role for the database using the `GRANT SQL` command:

```sql
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

Granting these privileges, log into the database as the new user from the [psql](https://www.postgresql.org/docs/16/app-psql.html) utility:

```sql
psql -d mydb -U myuser
```



This guide is just a starting point; PostgreSQL is highly configurable and can be tailored for a variety of use cases. You can adjust configurations such as memory allocation, concurrent connections, and database file locations among other parameters in the PostgreSQL configuration file ([postgresql.conf)](https://www.postgresql.org/docs/16/config-setting.html) to suit your specific needs.

### Tablespaces

[Tablespaces](https://www.postgresql.org/docs/16/manage-ag-tablespaces.html) in PostgreSQL are locations on the hard disk where PostgreSQL stores data files containing database objects such as tables and indexes. This concept allows administrators to control the [disk layout](https://www.postgresql.org/docs/16/storage-file-layout.html) of a PostgreSQL instance at a level of granularity beyond what is possible by simply choosing the location of the main data directory. By default, PostgreSQL provides two predefined tablespaces named `pg_default` and `pg_global`. `pg_default` is where your database is stored by default, while `pg_global` is used for shared system catalogs that are visible across all databases

Tablespaces are particularly useful in large databases where you need to distribute the storage of data across different storage devices, each potentially having different performance characteristics. For example, you may decide to store frequently accessed tables in a tablespace located on a fast SSD drive, while infrequently accessed tables might be stored in a tablespace located on slower, but more cost-effective, hard disk drives. Alternatively, tablespaces can be used to store a database on a larger, but slower, storage medium if the database has outgrown its current storage. Note that the management and use of tablespaces require some degree of planning and ongoing management to ensure that they meet the needs of your specific use case.

## Database Objects

Database objects in PostgreSQL, such as tables, indexes, sequences, and views, are foundational to the organization, retrieval, and manipulation of data. They enable structured data storage, efficient data access, and the implementation of relational integrity, ensuring that data remains consistent, accurate, and available for various applications and users.

### Schemas

Schemas in PostgreSQL offer a way to group objects, including tables, views, indexes, data types, functions, and operators, into distinct namespaces. This means that objects with the same name can exist in different schemas within the same database without conflicting. This ability to encapsulate objects into schemas provides a kind of namespace management, giving you a more organized and manageable database.

A[ schema](https://www.postgresql.org/docs/16/ddl-schemas.html) in PostgreSQL is essentially a named collection of database objects. You can think of it as a container that holds related tables and other relational objects together. This feature is useful in multi-tenant database scenarios where each tenant might have a separate schema. Another notable advantage of using schemas is the security aspect. By assigning privileges at the schema level, a database administrator can efficiently manage the accessibility of data in a more fine-grained manner. So, schemas not only contribute to better organization and separation of database objects but also to enhanced data security.

### Tables 

In PostgreSQL, tables are fundamental storage entities where data is stored in structured and organized ways. A table in PostgreSQL consists of rows and columns, with each row representing a unique record and each column representing a specific field of data. These tables are defined by a schema, which outlines the data types for each column, any constraints or rules for the data, and other metadata. As an ORDBMS, PostgreSQL allows for complex queries across multiple tables, making it powerful for handling structured data in large-scale applications.

[Creating tables](https://www.postgresql.org/docs/16/sql-createtable.html) in PostgreSQL is a fundamental and straightforward task. This process starts with the `CREATE TABLE` statement, which specifies the table's name, columns, and the data types of those columns.  For example, to create a table named users with columns id, name, and email, the statement would be: 

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL
);
```



In this case, `id` is an auto-incrementing integer (`SERIAL`), name' and email are variable-length strings (`VARCHAR`), `'id'` is the primary key (ensuring uniqueness and not null), and `email` is defined to be unique and not null. 

### Constraints 

In PostgreSQL, [constraints](https://www.postgresql.org/docs/16/ddl-constraints.html) are rules that you can apply to the type of data in a table to maintain the integrity, accuracy, and reliability of that data. Constraints are implemented to enforce the correctness of your data and are a part of the database schema. 

There are several types of constraints in PostgreSQL:

| CONSTRAINT                                                   | DEFINITION                                                   |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [Primary Key](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/ddl-constraints.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6MDY0NTowNmQzOTUzNDI3ZDlmZjI1YWJiZmFmYTAwOWZjZTNkN2FkMWNjMzc5MzczYTIxYzJmNGNjYmY5ZDk2MWE4NzdmOnA6VA#DDL-CONSTRAINTS-PRIMARY-KEYS) | Ensure that each row in a table has a unique and non-null value, which helps in identifying records within the table |
| [Foreign Key](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/ddl-constraints.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6MDY0NTowNmQzOTUzNDI3ZDlmZjI1YWJiZmFmYTAwOWZjZTNkN2FkMWNjMzc5MzczYTIxYzJmNGNjYmY5ZDk2MWE4NzdmOnA6VA#DDL-CONSTRAINTS-FK) | Maintain the referential integrity between two tables; they create a relationship where the value in a column (or set of columns) in one table matches the value in a column (or set of columns) in another table |
| [Not Null](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/ddl-constraints.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6MDY0NTowNmQzOTUzNDI3ZDlmZjI1YWJiZmFmYTAwOWZjZTNkN2FkMWNjMzc5MzczYTIxYzJmNGNjYmY5ZDk2MWE4NzdmOnA6VA#DDL-CONSTRAINTS-NOT-NULL) | As the name suggests, these constraints ensure that a column cannot have a null value |
| [Unique](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/ddl-constraints.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6MDY0NTowNmQzOTUzNDI3ZDlmZjI1YWJiZmFmYTAwOWZjZTNkN2FkMWNjMzc5MzczYTIxYzJmNGNjYmY5ZDk2MWE4NzdmOnA6VA#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS) | Ensure that all values in a column are distinct              |
| [Check](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/ddl-constraints.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6MDY0NTowNmQzOTUzNDI3ZDlmZjI1YWJiZmFmYTAwOWZjZTNkN2FkMWNjMzc5MzczYTIxYzJmNGNjYmY5ZDk2MWE4NzdmOnA6VA#DDL-CONSTRAINTS-CHECK-CONSTRAINTS) | Allow you to specify a condition on the possible values that can be inserted into a column. |

All these constraints are designed to prevent inadvertent or malicious corruption of data within PostgreSQL databases and provide a robust set of tools for managing the consistency and reliability of your data. However, constraints can also limit the flexibility of the database to some extent and might impose some performance overhead, so they should be implemented judiciously.

### Default Values

[Default values](https://www.postgresql.org/docs/16/ddl-default.html) in PostgreSQL are predefined values that a column will have when no value is explicitly provided during the data insertion process. They serve as a failsafe, ensuring that every row has data for certain columns, even if the user does not specify what that data should be. You can set default values for a column when creating or altering a table. They can be static values, like a specific number or string, or dynamic values produced by a function, like the current date and time.

### Partitioning 

[Partitioning](https://www.postgresql.org/docs/16/ddl-partitioning.html) is a database design technique used to improve performance, management, and availability of large-scale database applications. It works by segregating data into smaller, more manageable parts, or "partitions", that can be accessed, managed, and indexed independently of the other partitions. Essentially, partitioning allows a table, index, or database to be subdivided into smaller pieces, where each piece of such a database object is known as a partition. Each partition can be stored in a separate file or on a separate disk and can also be distributed across multiple nodes in a distributed database system.

In PostgreSQL, the SQL used to implement partitioning mainly involves using the `CREATE TABLE` command with the `PARTITION BY` clause, to define the partition key and type of partitioning (e.g., `RANGE`, `LIST`, or `HASH`). For example, you might use the following command to create a partitioned table based on a range of values:

```sql
CREATE TABLE orders (
    order_id int not null,
    date date not null,
    customer_id int not null,
    amount numeric(10,2)
) PARTITION BY RANGE (date);
```



After the partitioned table is created, individual partitions can be created using similar syntax but with the `PARTITION OF `clause. For instance:

```sql
CREATE TABLE orders_2023 
PARTITION OF orders 
FOR VALUES FROM ('2023-01-01') TO ('2023-12-31');
```



This will create a partition `orders_2023` that will contain all orders where the date is in the year 2023. You can create as many partitions as needed, depending on the requirements of your application.

The key benefit of this partitioning scheme is that PostgreSQL can ignore scanning irrelevant partitions when a query is executed. This is known as "partition pruning", which can significantly improve the performance of queries and data loading.

## Procedural Languages

PostgreSQL allows users to write stored procedures in a variety of different languages. These are known as procedural languages and are a key component of PostgreSQL's extensibility. Some of the procedural languages supported by PostgreSQL include PL/pgSQL, PL/Python, PL/Perl, and PL/Tcl. Let's dive into these languages a bit more:

| PROCEDURAL LANGUAGE                                          | PURPOSE                                                      | SYNTAX                                                       |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [PL/pgSQL](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/plpgsql-overview.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6OTNiYTowOGI1ZjY5OWYzZWFjODBlNzMxNDNiMGQ1OWM2ODhjNTNhNjViZDNhYTZiYzNkNjFhNjRhYjg5YTdjMzMxMmUwOnA6VA) | This is the most used procedural language for PostgreSQL. It is a block-structured language that allows you to write complex business logic to be executed by the database server. | Like Oracle's procedural language, PL/SQL, PL/pgSQL supports control structures like loops and conditionals. |
| [PL/Python](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/plpython.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6YjQ4MDo2NDNjYzhhYmFiOGNlMjNiYzQ3YzM3MGUzNTIzZTcxOTdmNWQ3M2I3YzAxZTM0OWI1NDYzMTVmYjhjNDJmYWNlOnA6VA) | Using PL/Python, you can leverage Python's extensive standard library and ecosystem within your database functions. | This allows you to write PostgreSQL functions in the Python programming language. Python is a high-level, interpreted programming language known for its readability and support for multiple programming paradigms, such as procedural, object-oriented, and functional programming. |
| [PL/Perl](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/plperl.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6YzJlMjpjNTE4NjUyNGY3MjNjYWNjOGRjYzExZjNkODAxNDY0ZTEyM2E2YWRiMjdjNTg1N2ZmNDlmNTZiMDZlMjBlMGU4OnA6VA) | PL/Perl can be particularly useful if you need to do complex text transformations or pattern matching inside your database. | This procedural language allows you to write database functions in Perl. Perl is a high-level, general-purpose, interpreted scripting language known for its powerful text processing capabilities. |
| [PL/Tcl](https://url.avanan.click/v2/___https://www.postgresql.org/docs/16/pltcl.html___.YXAzOnBlcmNvbmE6YTpnOjE1Yzk5ZDBhODM5YmE0ZGFiZGQ5ZWE5YTg5M2E0Nzc5OjY6Y2ZlNjpiY2NhMzRkYmI2ZmMxMmZmZjdjMWQyODBkZTZlMDZjYmI4YWJkMTc2NzlkMmQ3MzdlOGExZGFlYTIxZGUzNTc0OnA6VA) | Often used for prototyping, scripted applications, GUIs, and testing, PL/Tcl can be an effective choice if you are already using Tcl in your application or if you require its particular strengths for certain tasks within your database functions. | This allows you to write PostgreSQL functions in the Tcl programming language. Tcl (Tool Command Language) is a high-level, interpreted scripting language that is easy to learn and use. |



The choice of procedural language can impact factors like database performance, security, and the complexity of stored procedures. The necessary language extensions must be installed and enabled in the PostgreSQL server before beginning to write stored procedures in procedural languages.

### Procedures 

Stored procedures in SQL are a powerful feature that allows the encapsulation of repetitive or complex logic. They provide an efficient method of handling the same set of operations with different inputs. These are precompiled SQL statements that are stored in the database and can be executed as needed. Stored procedures offer the benefits of improved performance, code reusability, security, and integrity.

PostgreSQL allows the creation of stored procedures using the [CREATE PROCEDURE](https://www.postgresql.org/docs/16/sql-createprocedure.html) command. In PostgreSQL, the procedure is a type of database object that contains a set of SQL commands to be executed in a sequence. Unlike functions, procedures in PostgreSQL can perform transactions and don't return a value.

Here's a simple example of creating a stored procedure in PostgreSQL:

```sql
CREATE OR REPLACE PROCEDURE insert_into_table(table_name text, col1_value text, col2_value int)
LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format('INSERT INTO %I (col1, col2) VALUES (%L, %L)', table_name, col1_value, col2_value);
    COMMIT;
EXCEPTION
    WHEN others THEN
    RAISE NOTICE 'Insert operation failed.';
END; $$
```



In this example, `CREATE OR REPLACE PROCEDURE` command is used to create a new stored procedure named` insert_into_table`. The procedure takes three parameters: `table_name`, `col1_value`, and `col2_value`. It then executes an `INSERT` command, using the `EXECUTE` format function to dynamically generate the SQL statement. If the insertion fails for any reason, a notice is raised. The `COMMIT` statement is used to make sure that the transaction is permanently saved.

This procedure can be called using the `CALL` statement like: `CALL insert_into_table('my_table', 'text_value', 123);`.

#### Functions 

Functions in SQL, are a group of SQL statements that return a value. They provide a way to encapsulate complex operations into a single, callable routine. This not only helps in simplifying complex queries but also promotes reusability and modularization. They are highly beneficial when you need to perform the same operations on multiple parts of your application or on multiple applications, reducing the amount of code and, thus, the potential for errors.

In PostgreSQL, you can create functions using the [CREATE FUNCTION](https://www.postgresql.org/docs/16/sql-createfunction.html) command. The function can be defined to take a list of parameters, which are then available to the code within the function. Here's a simple example:

```sql
CREATE FUNCTION get_total_sales(sales_date date)
RETURNS numeric AS $$
DECLARE 
    total_sales numeric;
BEGIN
    SELECT SUM(sales_amount) INTO total_sales
    FROM sales
    WHERE sale_date = sales_date;

    RETURN total_sales;
END; $$
LANGUAGE plpgsql;
```





In this example, a function named get_total_sales is created, which takes one parameter sales_date of type date. The DECLARE block is used to define local variables, and in this example, this is total_sales of type numeric. The BEGIN ... END block encapsulates the actual SQL logic of the function. The LANGUAGE keyword is used to specify the language in which the function is written — in this case, plpgsql. The function calculates the total sales for a given date and returns it. The function can then be called anywhere in your SQL code where an expression of its return type is allowed. 

For example:

```sql
SELECT get_total_sales('2023-07-01');
```



#### Other Objects 

In PostgreSQL, [views](https://www.postgresql.org/docs/16/rules-views.html) and [triggers](https://www.postgresql.org/docs/16/trigger-definition.html) are powerful tools that aid in data manipulation and enforcement of business rules. A view is a virtual table based on the result-set of an SQL statement, acting as a stored query which allows users to work with the subsets of data or computed values. Views can encapsulate complex queries, providing an abstract layer over tables and making data access more efficient and secure. On the other hand, triggers are database callbacks that automatically execute or fire when a specified database event (insert, update, or delete) occurs. Triggers allow automated enforcement of business rules, complex validation checks, and maintenance of referential integrity. Together, views and triggers support robust, dynamic, and secure data handling within PostgreSQL.

#### Data Definition (DDL) 

A robust list of essential PostgreSQL functions is included in the newest version of the PostgreSQL product, including built-in functions like date/time functions, string functions, aggregate functions, control structures, and more.  

Beyond those packages built into the product, Data Definition Language (DDL) is a subset of SQL that is primarily used for defining and managing database schemas and objects. This includes [commands](https://www.postgresql.org/docs/16/reference.html) like `CREATE`, `ALTER`, `DROP`, and `TRUNCATE`, which allow for the creation, modification, deletion, or emptying of database objects such as tables, indices, sequences, or views. In addition to these basic operations, PostgreSQL's DDL offers a wide range of features, including advanced options for defining constraints, triggers, rules, and more. It's important to note that most DDL commands in PostgreSQL are [transactional](https://www.postgresql.org/docs/16/tutorial-transactions.html), meaning they can be rolled back if necessary, providing a measure of safety and flexibility when performing database alterations.

#### Query Language (DML) 

Data Manipulation Language (DML) in PostgreSQL refers to a subset of SQL commands that allows users to manipulate and interact with the data in database tables.  The commands are actions, such as `SELECT`, `INSERT`, `UPDATE` and `DELETE`.  These operations include mathematical and string operations, along with crucial queries and commands for database administration.

The most common DML statement, the [SELECT](https://www.postgresql.org/docs/16/sql-select.html) statement, is used to fetch data from the database, presenting it in a structured format based on the query requirements. The [INSERT](https://www.postgresql.org/docs/16/sql-insert.html) command allows users to add new rows of data to a table.[ UPDATE](https://www.postgresql.org/docs/16/sql-update.html) enables the modification of existing data within the table. Lastly, [DELETE](https://www.postgresql.org/docs/16/sql-delete.html) allows users to remove specific rows of data from a table. PostgreSQL, a powerful, open-source, object-relational database system, supports these DML commands and provides additional features like transaction control commands to manage the operations on the data residing within.

Examples of DML statements in PostgreSQL can assist in understanding how data is inserted, updated, deleted, and queried in a database, using the example of an employees table:

1. **Insert**:

```sql
INSERT INTO employees (first_name, last_name, email, hire_date)
VALUES ('John', 'Doe', 'john.doe@example.com', '2023-07-31');
```



The above `INSERT` statement is used to insert a new row into the employees table.

2. **Update**:

```sql
UPDATE employees
SET email = 'jdoe@example.com'
WHERE first_name = 'John' AND last_name = 'Doe';
```



This `UPDATE` statement modifies the email address of a certain employee named John Doe in the employees table.

3. **Delete**:

```sql
DELETE FROM employees
WHERE first_name = 'John' AND last_name = 'Doe';
```



The `DELETE` statement demonstrated above removes the row of a certain employee named John Doe from the employees table.

4. **Select**:

```sql
SELECT first_name, last_name, email
FROM employees
WHERE hire_date > '2023-01-01';
```



This `SELECT` statement retrieves the first name, last name, and email of all employees who were hired after January 1, 2023, from the employees table.

Please replace the table name employees and the column names `first_name`, `last_name`, `email`, and `hire_date` with your actual table and column names. Also, you can replace the values in the `WHERE` clause to suit your data.

Always remember that modifying data with DML statements should be done carefully, as it might be impossible to undo the changes.

Section 5

## Common Tasks

Common database administration tasks, such as creating users, setting up user, role and object security is essential to 

### User Creation 

In PostgreSQL, users are referred to as roles. The basic syntax for creating a new user is:

```sql
CREATE USER username WITH PASSWORD 'password';
```



For example:

```sql
CREATE USER john WITH PASSWORD 'johnspassword';
```



### Roles and Access 

There are many privileges you can grant a role, including `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, `REFERENCES`, `TRIGGER`, `CREATE`, `CONNECT`, `TEMPORARY`, `EXECUTE`, and `USAGE`. Here's the general syntax:

SQL

```
GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [,...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
        | ALL TABLES IN SCHEMA schema_name [, ...] }
    TO { username | GROUP group_name | PUBLIC } [, ...] [ WITH GRANT OPTION ];
```



To grant all privileges on a table to a user, you would do:

```sql
GRANT ALL PRIVILEGES ON TABLE tablename TO username;
```



### Client Authentication 

Client authentication is managed in the [pg_hba.conf](https://www.postgresql.org/docs/16/auth-pg-hba-conf.html) file. You might see entries as shown in the following example:

```bash
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             127.0.0.1/32            md5
```



By default, this [configuration file](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html) can be found in the data directory of the database cluster and controls the type of access that will be used for authentication.  The file has a required format and manual edits incorrectly performed could render the file incapable of authenticating to the database.

As database authentication is a topic of serious concern in today’s relational database world, details on authentication methods are located in the [PostgreSQL documentation](https://www.postgresql.org/docs/current/auth-methods.html), which will step through each authentication mode at a deeper level.

### Object Security 

PostgreSQL allows permissions to be set on various database objects. For example, you can allow a user to only select from a table and not update, insert, or delete:

```sql
GRANT SELECT ON TABLE tablename TO username;
```

You can also use `REVOKE` to take away permissions:



```sql
REVOKE UPDATE ON TABLE tablename FROM username;
```



It is essential to remember to replace `username`, `password`, `tablename`, `schema_name`, `group_name` and `mydb`, `myuser` with your actual username, password, table name, schema name, group name, database name and user name.

Section 6

## Administration Tasks

There are regular [administration tasks](https://www.postgresql.org/docs/16/maintenance.html) that must be performed as standard maintenance. This next section will go into some of the highest-level procedures that should be done to ensure PostgreSQL runs optimally.

### Vacuuming 

PostgreSQL uses a method called [Multiversion Concurrency Control](https://www.postgresql.org/docs/16/mvcc-intro.html) (MVCC) to handle concurrent transactions, which creates a new version of a row each time it's updated, leading to "dead" rows over time. [Vacuuming](https://www.postgresql.org/docs/16/routine-vacuuming.html) removes these dead row versions. It can be done manually or automatically.

To manually vacuum a database, you can use the `VACUUM` command:

```sql
VACUUM (VERBOSE, ANALYZE) table_name;
```



`VERBOSE` provides progress reports and `ANALYZE` updates statistics.  There is an advanced [ANALYZE](https://www.postgresql.org/docs/16/sql-analyze.html) command to collect statistics that resides outside the `VACUUM` command, as well.

PostgreSQL also has an auto-vacuum process that runs in the background and performs vacuuming as needed. 

### Reindexing 

Over time, indexes can become fragmented and slow down query performance. [Reindexing](https://www.postgresql.org/docs/16/sql-reindex.html) rebuilds indexes to improve performance. 

To reindex a specific table:

```sql
REINDEX TABLE table_name;
```



To reindex an entire database:

```sql
REINDEX DATABASE database_name;
```



### Log File Maintenance 

PostgreSQL log files store database activities and can be useful for troubleshooting issues, but they can take up significant disk space over time.

The `log_rotation_age` and `log_rotation_size` parameters control how often [log files](https://www.postgresql.org/docs/16/runtime-config-logging.html) are rotated. You can set them in the postgresql.conf file. To maintain the size of your log files, you can set the `log_truncate_on_rotation` parameter to on in the postgresql.conf file. This will cause old log data to be deleted when the log file is rotated.

### Database Resiliency 

Backup and recovery are critical aspects of any database management system, including PostgreSQL. A comprehensive backup strategy is crucial for protecting the data stored within your PostgreSQL databases, allowing you to recover quickly and efficiently in case of any failures or errors that could lead to data loss. PostgreSQL provides various methods for creating backups, ranging from simple file-system-level backups to more sophisticated logical backups. The three main methods of backup are [SQL dump](https://www.postgresql.org/docs/16/backup-dump.html), [file system level backup](https://www.postgresql.org/docs/16/backup-file.html), and [continuous archiving](https://www.postgresql.org/docs/16/continuous-archiving.html).

Recovery in PostgreSQL refers to the process of restoring and recovering your database from a backup when data loss occurs. PostgreSQL offers Point-In-Time Recovery (PITR), which allows you to restore your database to any point in time. This can be extremely valuable in case of accidental data deletion or corruption. PITR uses a [write-ahead log](https://www.postgresql.org/docs/16/wal.html) (WAL), which records all changes made to the data. By replaying these logs up to a certain point, you can restore the database to a previous state. PostgreSQL also supports replication, which helps in data recovery and provides additional benefits like load balancing and failover capabilities. The flexibility and robustness of PostgreSQL's backup and recovery mechanisms are part of what makes it a popular choice for managing complex and critical databases.

#### Backup 

Backups can be performed via a backup of a PostgreSQL database using the [pg_dump](https://www.postgresql.org/docs/16/backup.html) command.

Via the command line:

```sql
pg_dump -U username -W -F t database_name > backup_file.tar
```



In this example, `-U` specifies the username, `-W` prompts for the password, `-F` specifies the format of the output file (in this case, tar), and `database_name` is the name of your database.

#### Restore 

You can restore a PostgreSQL database from a backup using the [pg_restore](https://www.postgresql.org/docs/16/backup-dump.html#BACKUP-DUMP-RESTORE) command.

From the command line:

```sql
pg_restore -U username -d database_name -1 backup_file.tar
```



Here, `-U` specifies the username, `-d` specifies the database to restore into, `-1` tells PostgreSQL to restore the dump as a single transaction, and `backup_file.tar` is the name of your backup file.  Always remember to perform these operations with care and test everything in a non-production environment before executing in production. In the newest release, version 16.2, the [recovery.conf](https://www.postgresql.org/docs/16/recovery-config.html) file is now obsolete, as it was merged into the `postgresql.conf` configuration file.

Section 7

## Conclusion

To conclude, this PostgreSQL Refcard aims to provide a comprehensive, easy-to-understand, and quick-reference material on the fundamental aspects of PostgreSQL. The guide intends to enhance the efficiency of database interaction for both beginners and experienced users.
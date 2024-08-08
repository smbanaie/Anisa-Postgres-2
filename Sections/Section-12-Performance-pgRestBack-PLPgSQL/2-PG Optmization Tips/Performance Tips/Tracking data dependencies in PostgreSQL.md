# [Tracking data dependencies in PostgreSQL](https://medium.com/@shaileshkumarmishra/tracking-data-dependencies-in-postgresql-41a2da91350c)









![img](https://miro.medium.com/v2/resize:fit:875/1*ZhhNQLTk_xxrvkVhIFWwZA.png)

Tracking data dependencies in PostgreSQL tables is an essential aspect of managing and analyzing data relationships within a database. This blog post provides an overview of how to track data dependencies in PostgreSQL tables and highlight some PostgreSQL extensions that can aid in this process.

Data dependencies refer to the relationships and dependencies between different tables, columns, and constraints within a database. These dependencies are crucial for maintaining data integrity, optimizing queries, and understanding the overall structure of the database.

PostgreSQL provides several built-in features and system catalogs that allow you to track data dependencies. Here are some methods you can use:

# 1. System Catalogs:

PostgreSQL stores metadata about the database objects in system catalogs, such as `pg_class`, `pg_attribute`, `pg_constraint`, and others. These catalogs contain valuable information about tables, columns, constraints, and their relationships. By querying these catalogs, you can gather details about data dependencies.

The SQL query provided is designed to find all foreign key constraints in a PostgreSQL database that reference a specific table (`mytable` in this case). However, it will not show other types of object dependencies like views, functions, or indexes.

Let’s go through an example to illustrate how this might work. Suppose we have the following hypothetical database setup:

\- A table named `mytable` in the `public` schema.

\- Another table named `othertable` in the `public` schema.

\- A foreign key constraint named `mytable_fk` in `othertable` that references `mytable`.

Given this setup, the result of the query might look something like this:

```
SELECT
conname AS constraint_name,
conrelid::regclass AS table_name,
connamespace::regnamespace AS schema_name,
pg_get_constraintdef(c.oid) AS constraint_definition
FROM
pg_constraint c
WHERE
confrelid = 'mytable'::regclass;
constraint_name | table_name | schema_name | constraint_definition
 - - - - - - - - -+ - - - - - - -+ - - - - - - -+ - - - - - - - - - - - - - - - - - - - - - - - - - - -
mytable_fk | othertable | public | FOREIGN KEY (column_name) REFERENCES mytable(id)
(1 row)
```

# Explanation of the Output:

1. **constraint_name**: `mytable_fk` — This is the name of the foreign key constraint.
2. **table_name**: `othertable` — This is the name of the table that contains the foreign key constraint.
3. **schema_name:** `public` — This is the name of the schema in which `othertable` is located.
4. **constraint_definition:** `FOREIGN KEY (column_name) REFERENCES mytable(id)` — This shows the full definition of the foreign key constraint. It indicates that a column (presumably named `column_name`) in `othertable` is a foreign key that references the `id` column in `mytable`.

The primary goal of these foreign key constraints is to maintain referential integrity in the database. This means ensuring that relationships between tables are consistent. If a record in the referenced table (`mytable`) is deleted or its primary key changed, PostgreSQL will enforce actions (e.g., CASCADE, SET NULL, etc.) as defined by the foreign key constraints on the referencing tables.

Please note that these queries utilize the system catalog tables `pg_constraint` and `pg_depend` to fetch the required information about data dependencies. Adjust the queries according to your specific needs, such as filtering by schema or including additional columns.

# Other Types of Dependencies:

This query specifically targets foreign key constraints that reference `mytable`. To trace other types of object dependencies, you would need to query other system catalogs or use functions such as `pg_depend`. Here are some examples of other dependencies:

1. **Views**: If there is a view that depends on `mytable`, you would need to look into the `pg_depend` and `pg_rewrite` system catalogs to trace this dependency.
2. **Functions/Procedures**: If there are any functions or procedures that depend on `mytable`, you might need to inspect the function definitions or use `pg_depend`.
3. **Indexes**: While indexes are directly tied to their tables and might not be considered dependencies in the same way as foreign keys or views, you can list them using `pg_index` and related system catalogs.
4. **Triggers**: Triggers that depend on `mytable` can be found using `pg_trigger`.
5. **Sequences**: If `mytable` has any serial columns, it will depend on a sequence. This can be found through `pg_depend`.

To get a comprehensive list of all dependencies, you might need to craft a more complex query or use a tool designed for this purpose. Additionally, PSQL’s `\d` meta-command in `psql` can also provide information on dependencies, though it might not be as detailed or specific as querying the system catalogs directly.

Remember to execute these queries within a PostgreSQL database connection to retrieve the desired data dependencies information.

# 2. Information Schema:

PostgreSQL also provides an information schema, which is a standard schema that contains structured views providing information about the database’s objects. You can query the information schema views to retrieve data dependency information. For example, you can use the `information_schema.columns` view to find columns used in different tables or `information_schema.constraint_column_usage` to identify constraints and their associated columns.

Here’s a sample SQL code snippet that demonstrates how to track PostgreSQL data dependencies using the information schema:

**Query to track data dependencies for a specific table**

```
SELECT
tc.constraint_name,
tc.table_name,
tc.table_schema,
ccu.column_name,
ccu.referenced_table_name,
ccu.referenced_column_name
FROM
information_schema.table_constraints AS tc
JOIN
information_schema.constraint_column_usage AS ccu
ON
tc.constraint_name = ccu.constraint_name
WHERE
tc.table_name = 'mytable';
```

**Query to track dependent objects for a specific table**

```
SELECT
conname AS constraint_name,
conrelid::regclass AS table_name,
connamespace::regnamespace AS schema_name,
confrelid::regclass AS dependent_object_name,
confkey AS dependent_column_ids
FROM
pg_constraint
WHERE
confrelid = 'mytable'::regclass;
```

**Query to track dependencies of a specific object**

```
SELECT
objid::regclass AS object_name,
refobjid::regclass AS dependent_object_name,
refobjsubid AS dependent_column_id,
deptype
FROM
pg_depend
WHERE
classid = 'example_object_classid'::regclass
AND objid = 'example_object_oid'::regclass;
```

First query retrieves the constraints associated with the specified table, including the constraint name, table name, schema name, the column name, referenced table name, and referenced column name.

The second query tracks dependent objects for a specific table. This query returns the constraint name, table name, schema name, dependent object name, and dependent column IDs.

Lastly, the third query allows you to track dependencies of a specific object. Replace `’example_object_classid’` with the class ID of the object and `’example_object_oid’` with the object’s OID (Object ID) for which you want to track dependencies. This query retrieves the object name, dependent object name, dependent column ID, and the dependency type.

Please note that these queries utilize the information schema views `table_constraints` and `constraint_column_usage` to fetch the required information about data dependencies. Adjust the queries according to your specific needs, such as filtering by schema or including additional columns.

Remember to execute these queries within a PostgreSQL database connection to retrieve the desired data dependencies information.

# Some more Takeaway

In PostgreSQL, object dependencies are managed within the system catalogs, primarily using the `pg_depend` table. Let’s go through some SQL queries to extract these dependencies and the associated considerations.

**1. Dependencies Between Tables (Foreign Key Relations):**

```
SELECT
conname AS constraint_name,
conrelid::regclass AS table_with_foreign_key,
aconfrelid::regclass AS referenced_table
FROM
pg_constraint
WHERE
contype = 'f';
```

**2. Dependencies of a Table on Other Objects (Views, Functions, etc.):**

```
SELECT
classid::regclass,
objid,
objsubid,
refobjid::regclass AS referenced_table
FROM
pg_depend
WHERE
refobjid = 'myschema.mytable'::regclass
AND deptype = 'n';
```

Here, `myschema.mytable` is the table for which you want to find dependencies.

**3. Dependencies on a Table Across Schemas:**

Cross-schema dependencies are naturally captured since the system catalogs use OIDs (Object Identifiers) to track objects. OID is unique across the database, so it would inherently account for cross-schema dependencies.

```
SELECT
classid::regclass,
objid,
objsubid,
refobjid::regclass AS referenced_table
FROM
pg_depend
WHERE
refobjid = 'myschema.mytable'::regclass;
```

This would give you dependencies across all schemas.

**4. Dependencies Across Databases:**

PostgreSQL system catalogs are specific to each database, so you cannot directly query across databases. If you suspect there are dependencies that span multiple databases, you would need to run your queries in each database context separately.

However, it’s uncommon to have true dependencies across databases. In PostgreSQL, databases are more isolated from each other compared to some other RDBMS systems. Let’s go through an example to illustrate the context where dependencies might span across multiple databases in PostgreSQL and how you might approach querying to identify these dependencies.

**Example Scenario:**

**1. Database 1: `db1`**

\- Table: `users`

\- View: `active_users` (depends on `users` table)

**2. Database 2: `db2`**

\- Table: `orders`

\- Stored Procedure: `get_user_orders` (this is supposed to fetch data from `db1.users`)

**Objective:**

Identify dependencies within each database and any apparent cross-database dependencies.

## Steps and Queries:

**1. Within Database 1 (`db1`):**

Connect to `db1` and run the following queries:

**Identify dependencies for the `users` table:**

```
SELECT dependent_obj.objid::regclass AS dependent_object
FROM pg_depend AS depend
JOIN pg_class AS dependent_obj ON depend.objid = dependent_obj.oid
WHERE depend.refobjid = 'users'::regclass;
```

**Identify objects that the `active_users` view depends on:**

```
SELECT referenced_obj.objid::regclass AS referenced_object
FROM pg_depend AS depend
JOIN pg_class AS referenced_obj ON depend.refobjid = referenced_obj.oid
WHERE depend.objid = 'active_users'::regclass;
```

This should show that `active_users` depends on the `users` table.

**2. Within Database 2 (`db2`):**

Connect to `db2` and run the following queries:

**Check dependencies for `get_user_orders`:**

```
SELECT * FROM pg_proc WHERE proname = 'get_user_orders';
```

\- Manually inspect the definition of `get_user_orders` to see if it references any objects in `db1`. PostgreSQL won’t track these dependencies in its system catalogs, so you have to do this part manually.

**Considerations:**

Cross-database dependencies are not tracked in PostgreSQL’s system catalogs. If you have a stored procedure in `db2` that queries a table in `db1`, you won’t find a record of this dependency in the system catalogs. You would need to manually inspect the procedure’s code or have external documentation tracking these dependencies.

\- If your PostgreSQL instance is part of a larger ecosystem with external applications, scripts, or services interacting with it, dependencies might exist there as well. You’d need to inspect the code of these external components to understand the full picture of dependencies.

\- It’s generally a good practice to avoid cross-database dependencies when possible, as they can make your system more complex and harder to maintain. If you find that you have many such dependencies, it might be worth considering a database design that consolidates related objects within the same database or schema, or using a tool that can track dependencies across databases.

**Cautions & Considerations:**

**1. Understand Your Queries:** Before you run any queries, especially if you’re thinking about modifying the system catalogs directly (which you generally shouldn’t), make sure you understand the implications.

**2. Schema-qualified Names:** Always use schema-qualified names (`schema_name.table_name`) when querying for a specific table or object. This avoids ambiguities and ensures you’re looking at the correct object.

**3. Dependencies Impact on DDL Operations:** If you’re investigating dependencies with the intent to drop or modify objects, be aware that PostgreSQL might prevent certain operations if there are dependencies. For instance, dropping a table that’s referenced by a view or another table through a foreign key will lead to an error unless you use the `CASCADE` option. However, be extremely careful with the `CASCADE` option, as it can drop dependent objects.

**4. Backups:** Always backup your database before making major changes, especially if those changes are based on a dependency analysis. This ensures that you can recover if something goes wrong.

**5. Cross-Database Dependencies:** If you have logic or applications that imply dependencies across databases (like one database’s function calling another database’s table), then these are not “true” dependencies in the PostgreSQL sense and won’t be captured in the system catalogs. You’ll need a higher-level tool or documentation to track these.
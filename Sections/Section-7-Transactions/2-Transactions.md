#### Transactions Workshop using Northwind DB 



**1. Setting up PostgreSQL (5 minutes):**

   - Instruct participants to create a database and load the Northwind dataset.

```sql
-- Create a new database
CREATE DATABASE northwind;

-- Connect to the new database
\c northwind;

-- Execute SQL script to create tables and insert data (use the downloaded Northwind SQL file)
\i path/to/northwind.sql;
```

**2. Basic Querying :**

   - Run a simple SELECT query to showcase the initial state of the data.

```sql
-- Select some data from the Customers table
SELECT * FROM customers LIMIT 5;
```

**3. Transaction Basics (5 minutes):**

   - Introduce the `BEGIN`, `COMMIT`, and `ROLLBACK` statements.
   - Explain that a transaction is a series of SQL statements executed as a single unit of work.

```sql
-- Start a transaction
BEGIN;

-- Perform some data modifications
UPDATE customers SET contact_name = 'John Doe' WHERE customer_id = 'ALFKI';

select * from customers WHERE customer_id = 'ALFKI';
-- Demonstrate how to rollback the changes
ROLLBACK;

select * from customers WHERE customer_id = 'ALFKI';
```

**4. Savepoints**

   - Explain how savepoints allow you to roll back to a specific point within a transaction.

```sql
-- Start a transaction
BEGIN;

-- Perform some data modifications
UPDATE customers SET contact_name = 'Jane Doe' WHERE customer_id = 'ANATR';

-- Create a savepoint
SAVEPOINT my_savepoint;

-- Perform additional changes
DELETE FROM order_details WHERE customer_id = 'ANATR';

-- Demonstrate rolling back to the savepoint
ROLLBACK TO my_savepoint;


```

- check the session manager in `DBeaver`
- change the delete query to :`DELETE FROM orders_details WHERE customer_id = 'ANATR';`  and run it again
- add the commit to finalize the tx.

**5. Error Handling in Transactions :**

   - in the PL/pgSQL section this topic will be covered.
   - RELEASE SAVEPOINT

```sql
BEGIN;
SAVEPOINT my_savepoint;

-- Perform some data modifications
UPDATE products SET unit_price = unit_price / 0 WHERE category_id = 2;

-- If no error occurred, release the savepoint and commit
RELEASE SAVEPOINT my_savepoint;
COMMIT;
```



### The Final Solution

```sql
DO $$
DECLARE
    has_error BOOLEAN := FALSE;
BEGIN
    BEGIN
        UPDATE products SET unit_price = unit_price / 0 WHERE category_id = 2;
    EXCEPTION
        WHEN OTHERS THEN
            has_error := TRUE;
            RAISE NOTICE 'An error occurred: %', SQLERRM;
    END;

    IF has_error THEN
        RAISE NOTICE 'Rolling back transaction';
        ROLLBACK;
    ELSE
        RAISE NOTICE 'Committing transaction';
        COMMIT;
    END IF;
END $$;
```




#### DML : A Deeper Dive

1. Copy Structure

   ```sql
   -- Step 1: Create a base table with constraints
   
   -- Create a table
   CREATE TABLE original_table (
       id serial PRIMARY KEY,
       name varchar(50) NOT NULL,
       age int CHECK (age >= 18),
       city varchar(50),
       CONSTRAINT unique_name_city UNIQUE (name, city)
   );
   
   -- Insert some rows
   INSERT INTO original_table (name, age, city) VALUES
       ('John', 25, 'New York'),
       ('Jane', 30, 'San Francisco'),
       ('Bob', 22, 'Los Angeles');
   
   -- Step 2: Use SELECT INTO to 
   
   -- Create a new table using SELECT INTO
   SELECT * INTO new_table_select_into
   FROM original_table;
   
   -- Step 3: Use CREATE TABLE AS 
   
   -- Create a new table using CREATE TABLE AS
   CREATE TABLE new_table_create_as AS
   SELECT * FROM original_table;
   
   CREATE TABLE new_table_create_as_table AS TABLE original_table WITH NO DATA;
   
   -- Create a new table using Like
   CREATE TABLE new_table_like (LIKE original_table INCLUDING ALL);
   
   -- Step 4: Check the structure of the new tables
   
   -- Show the structure of the original table
   \d original_table
   
   -- Show the structure of the table created with SELECT INTO
   \d new_table_select_into
   
   -- Show the structure of the table created with CREATE TABLE AS
   \d new_table_create_as
   \d new_table_create_as_table
   
   -- Show the structure of the table created with CREATE TABLE LIKE
   \d new_table_like
   
   
   ```

   

2. The Last ID or All Inserted IDs?

   ```sql
   CREATE Temp TABLE users (
       id SERIAL PRIMARY KEY,
       first_name VARCHAR(50) NOT NULL,
       last_name VARCHAR(50) NOT NULL,
       other_values TEXT
   );
   
   INSERT INTO users (first_name, last_name, other_values)
   VALUES 
     ('John', 'Doe', 'other_values1'),
     ('Jane', 'Smith', 'other_values2'),
     ('Alice', 'Johnson', 'other_values3')
   RETURNING id;
   
   ```

   

3. **Multiple Fields? Multiple Conflicts? Multiple With Same Target?**

   ```sql
   CREATE TABLE your_table (
       id SERIAL PRIMARY KEY,
       username VARCHAR(50) NOT NULL,
       email VARCHAR(100) NOT NULL,
       product_code VARCHAR(20) NOT NULL,
       other_column1 TEXT,
       other_column2 TEXT,
       other_values TEXT
   );
   
   
   -- Test data with conflicts
   INSERT INTO your_table (username, email, product_code, other_values)
   VALUES 
       ('john_doe', 'john@example.com', 'ABC123', 'other_values'),
       ('jane_smith', 'john@example.com', 'XYZ456', 'other_values'),
       ('john_doe', 'jane@example.com', 'ABC123', 'other_values')
   ON CONFLICT (username, email) DO UPDATE SET other_column1 = 'new_value1'
   ON CONFLICT (product_code) DO UPDATE SET other_column2 = 'new_value2';
   
   ```

4. Is It Valid ?

   ```sql
   -- Assuming a check constraint on min_salary
   CREATE TEMP TABLE employees (
       employee_id SERIAL PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       salary INT CHECK (salary >= 7500000),
       other_columns TEXT
   );
   
   -- Test data with potential conflicts
   INSERT INTO employees (name, salary, other_columns)
   VALUES 
       ('John Doe', 7000000, 'other_values')
   ON CONFLICT (salary) DO UPDATE SET salary = CASE 
       WHEN EXCLUDED.salary < 7500000 THEN 7500000
       ELSE EXCLUDED.salary
   END
   RETURNING *;
   
   ```

   

   

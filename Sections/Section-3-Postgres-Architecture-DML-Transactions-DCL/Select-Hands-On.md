#### First Steps

some basic select usage

1. **Select a literal **

   ```sql
   select 2;
   
   select "Ali" ; 
   or
   select 'ALI' ; 
   
   select 'Ali' as "ALI" ;
   
   select 'ALi' as name, 28 as age;
   
   ```

   

2. **Concatenate Strings:**

   ```sql
   SELECT 'Hello' || ' ' || 'World';
   
   ?: 
   SELECT 'Hello' || ' ' || 'World' as "Message";
   
   or 
   
   SELECT 'Hello' || ' ' || 'World' as 'Message';
   
   ?: Another Way ?
   
   
   ?: Is it Correct?
   SELECT 'Hello' + ' ' + 'World' as "Message";
   
   ```
   This query concatenates the strings 'Hello', a space, and 'World', resulting in the output 'Hello World'.

3. **Mathematical Expression:**
   ```sql
   SELECT 5 * 3;
   
   ?: output?
   SELECT '90' *3;
   ```
   This query performs a simple multiplication operation and returns the result, which is 15.

4. **Current Date:**

   ```sql
   SELECT current_date;
   ```
   Returns the current date.

5. **Current Time:**
   ```sql
   SELECT current_time;
   
   
   ?: Which one is correct ?
   
   SELECT current_timestamp - current_time;
   SELECT current_timestamp - current_date;
   
   ```
   Returns the current time.

6. **String Length:**
   ```sql
   SELECT length('Database');
   ```
   Computes the length of the string 'Database' and returns the result.

7. **Random Number:**
   ```sql
   SELECT random();
   ```
   Generates a random value between 0 and 1.

8. **Power Function:**
   ```sql
   SELECT power(2, 3);
   ```
   Computes 2 raised to the power of 3, resulting in 8.

9. **Square Root:**
   ```sql
   SELECT sqrt(25);
   ```
   Calculates the square root of 25, resulting in 5.

10. **Absolute Value:**
   ```sql
   SELECT abs(-10);
   ```
   Returns the absolute value of -10, which is 10.

11. **Trigonometric Function:**
   ```sql
   SELECT sin(pi() / 2);
   
   ?: Valid?
   SELECT 'PI :' || pi()  ;
   ```
   Calculates the sine of π/2, which is 1.

12. **UUID Generation:**
   ```sql
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   
   SELECT uuid_generate_v4();
   ```
   Generates a version 4 UUID.

13. **String Concatenation:**
   ```sql
   SELECT 'Hello' || ' ' || 'World';
   ```
   Concatenates strings.

14. **Mathematical Functions:**
   ```sql
   SELECT sqrt(25), power(2, 3), abs(-10);
   ```
   Calculates square root, power, and absolute value.

15. **Trigonometric Functions:**
   ```sql
   SELECT sin(pi() / 2), cos(pi()), tan(pi() / 4);
   ```
   Computes sine, cosine, and tangent.

16. **Rounding Numbers:**
   ```sql
   SELECT round(3.14159, 2), ceil(4.5), floor(4.5);
   ```
   Rounds to a specified number of decimal places, rounds up, and rounds down.

17. **Date Formatting:**
   ```sql
   SELECT to_char(current_timestamp, 'YYYY-MM-DD HH24:MI:SS');
   ```
   Formats the current timestamp as a string.

18. **Decode Binary to Text:**
   ```sql
   SELECT decode('48656C6C6F', 'hex');
   ```
   Decodes a hexadecimal string to text.

19. **SHA-256 Hashing:**
   ```sql
   SELECT digest('Hello, World!', 'sha256');
   ```
   Computes the SHA-256 hash of a string.

20.**Interval Arithmetic:**
        ```SELECT interval '1 day' * 3;```
    
  Performs interval arithmetic.



#### One Step Forward

Here are 10 more advanced examples of using the `SELECT` statement without the `FROM` clause in PostgreSQL:

1. **Date Manipulation:**
   
    ```sql
    SELECT current_date + interval '1 week';
    ```
    Adds one week to the current date.
    
12. **Substring Extraction:**
    ```sql
    SELECT substring('Hello World' from 1 for 5);
    
    ?: Valid?
    SELECT substring('Hello World' from 1 for 50);
    ```
    Extracts a substring of length 5 from the beginning of the string 'Hello World'.
    
13. **Case Statement:**
    ```sql
    SELECT 
    	  CASE 
    		WHEN 1 = 1 THEN 'True' 
    	    ELSE 'False' 
    	  END;
    
    ?: Valid ?
    SELECT 'ALI ' || CASE WHEN 1 = 1 THEN 'True' ELSE 'False' END as "Test";
    
    ```
    Uses a `CASE` statement to conditionally return a value.
    
14. **Array Operations:**
    ```sql
    SELECT array[1, 2, 3] || array[4, 5, 6];
    
    ? : which one is valid ?
    
    SELECT 4 in array[4, 5, 6];
    
    SELECT 4 = ANY (array[4, 5, 6]);
    
    SELECT 4 != ALL (array[4, 5, 6]);
    
    ```
    Concatenates two arrays, resulting in a new array.
    
15. **JSON Manipulation:**
    
    ```sql
    SELECT jsonb_set('{"name": "John", "age": 25}'::jsonb, '{age}', '30');
    ```
    Modifies a JSONB object by setting the 'age' field to '30'.
    
16. **Generate Series:**
    
    ```sql
    SELECT generate_series(10, 15) as seq;
    
    ?: valid ?
    
     SELECT generate_series(1, 15, 2) as seq;
    
    -----------
    
    SELECT ARRAY(SELECT generate_series(10, 15, 2))
    
    SELECT array_length(ARRAY(SELECT generate_series(10, 15, 2)), 1);
    1 is the dimension  
    
    
    
    SELECT ARRAY(
        SELECT ARRAY(
            SELECT generate_series(1, 3) -- Inner array values
        )
        FROM generate_series(1, 2) -- Outer array values
    ) AS two_dimensional_array;
    ```
    
17. **Common Table Expressions (CTE):**
    ```sql
    WITH cte AS (SELECT 1 as num)
    SELECT num * 2 FROM cte;
    ```
    Defines a Common Table Expression (CTE) to reuse within the query.

18. **Recursive Query:**
    ```sql
    WITH RECURSIVE factorial(n, result) AS (
      SELECT 1, 1
      UNION
      SELECT n + 1, (n + 1) * result FROM factorial WHERE n < 10
    )
    SELECT result FROM factorial;
    ```
    Calculates the factorial of numbers using a recursive query.

    
    

#### Casting

Here are some intermediate examples that involve the use of casting operators in PostgreSQL:

1. **Integer to Text Conversion:**
    ```sql
    SELECT 123::text;
    ```
    Converts the integer value 123 to text.

2. **Date to Text Conversion:**
    ```sql
    SELECT current_date::text;
    
    
    ?: Extract The year part with substring : 
    ....
    ```
    Converts the current date to text.
    
3. **Text to Integer Conversion:**
    ```sql
    SELECT '456'::integer;
    SELECT '456'::int;
    
    ?: which one is valid ? 
    SELECT '456'::int2;
    SELECT '456'::smallint;
    SELECT '456'::int4;
    SELECT '456'::int8;
    SELECT '456'::int16;
    SELECT '456'::bigint;
    
    ```
    Converts the text '456' to an integer.
    
4. **Float to Integer Conversion:**
    ```sql
    SELECT 123.45::integer;
    ```
    Converts the float value 123.45 to an integer, truncating the decimal part.

5. **Date to Timestamp:**
    ```sql
    SELECT current_date::timestamp;
    
    ?: Time?
    ...
    
    ```
    Converts the current date to a timestamp.
    
6. **Timestamp to Date:**
    ```sql
    SELECT current_timestamp::date;
    ```
    Extracts the date part from the current timestamp.

7. **Boolean to Integer Conversion:**
    ```sql
    SELECT true::integer, false::integer;
    ```
    Converts boolean values true and false to integers (1 and 0, respectively).

8. **Integer to Boolean Conversion:**
    ```sql
    SELECT 0::boolean, 1::boolean;
    ```
    Converts integer values 0 and 1 to booleans (false and true, respectively).

9. **Text to Date Conversion:**
    ```sql
    SELECT '2023-12-18'::date;
    ```
    Converts the text '2023-12-18' to a date.

10. **Timestamp to Text Conversion:**
    ```sql
    SELECT current_timestamp::text;
    ```
    Converts the current timestamp to text.

Casting operators (`::`) are used in these examples to explicitly convert one data type to another. These conversions are useful when you need to control the data type of the result or when working with functions or expressions that expect specific data types.



### Working With dates

The `EXTRACT` function in PostgreSQL is used to extract a specific part (such as year, month, day) from a date or timestamp. Here are some examples of using the `EXTRACT` function to extract date parts:

1. **Extract Year:**
    ```sql
    SELECT EXTRACT(YEAR FROM current_date);
    ```
    Returns the year from the current date.

2. **Extract Month:**
    ```sql
    SELECT EXTRACT(MONTH FROM current_timestamp);
    ```
    Returns the month from the current timestamp.

3. **Extract Day:**
    ```sql
    SELECT EXTRACT(DAY FROM '2023-12-18'::date);
    ```
    Returns the day from the specified date.

4. **Extract Hour:**
    ```sql
    SELECT EXTRACT(HOUR FROM current_timestamp);
    ```
    Returns the hour from the current timestamp.

5. **Extract Minute:**
    ```sql
    SELECT EXTRACT(MINUTE FROM '2023-12-18 15:30:00'::timestamp);
    ```
    Returns the minute from the specified timestamp.

6. **Extract Second:**
    ```sql
    SELECT EXTRACT(SECOND FROM current_timestamp);
    ```
    Returns the second from the current timestamp.

7. **Extract Timezone:**
    ```sql
    SELECT EXTRACT(TIMEZONE_HOUR FROM current_timestamp) AS tz_hour,
           EXTRACT(TIMEZONE_MINUTE FROM current_timestamp) AS tz_minute;
    ```
    Returns the timezone offset in hours and minutes from the current timestamp.

8. **Extract Quarter:**
    ```sql
    SELECT EXTRACT(QUARTER FROM '2023-12-18'::date);
    ```
    Returns the quarter from the specified date.

9. **Extract Weekday:**
    ```sql
    SELECT EXTRACT(ISODOW FROM current_date);
    ```
    Returns the day of the week as an ISO weekday (1 for Monday, 7 for Sunday) from the current date.

10. **Extract ISO Year:**
    ```sql
    SELECT EXTRACT(ISOYEAR FROM current_timestamp);
    ```
    Returns the ISO year from the current timestamp.
    
11. **Date Part**

	```sql
	SELECT date_part('month', current_timestamp);
	
	SELECT date_part('minute', '2023-12-18 15:30:00'::timestamp);
	
	SELECT date_part('timezone_hour', current_timestamp) AS tz_hour,
	       date_part('timezone_minute', current_timestamp) AS tz_minute;
	
	```
	
	- **`date_part`:** It is not part of the ANSI SQL standard.
	- **`EXTRACT`:** It is part of the ANSI SQL standard, making it more portable across different database systems.

While `date_part` and `EXTRACT` cover the basics of extracting date and time components, there are a few more considerations and functionalities related to working with dates and times in PostgreSQL:

1. **Time Zone Handling:**
   ```sql
   SELECT EXTRACT(HOUR FROM current_timestamp AT TIME ZONE 'ASIA/TEHRAN');
   SELECT date_part('hour', current_timestamp AT TIME ZONE 'UTC');
   ```
   
3. **Microseconds and Milliseconds:**
   
   - For extracting fractions of a second, you can use the `microseconds` and `milliseconds` units.
     ```sql
     SELECT EXTRACT(MICROSECONDS FROM timestamp_column);
     SELECT date_part('milliseconds', timestamp_column);
     ```
   
4. **Age Function:**
   - The `AGE` function calculates the interval between two dates or timestamps.
     ```sql
     SELECT AGE('2023-10-01'::date, '2022-01-01'::date);
     
     SELECT 
       (EXTRACT(YEAR FROM '2023-10-01'::date) - EXTRACT(YEAR FROM '2022-01-01'::date)) * interval '1 year' +
       (EXTRACT(MONTH FROM '2023-10-01'::date) - EXTRACT(MONTH FROM '2022-01-01'::date)) * interval '1 month' +
       (EXTRACT(DAY FROM '2023-10-01'::date) - EXTRACT(DAY FROM '2022-01-01'::date)) * interval '1 day' AS date_interval;
     
     ```
   
6. **Parsing Dates:**
   - If you have a formatted string and need to convert it to a timestamp, you can use the `TO_TIMESTAMP` function.
     ```sql
     SELECT TO_TIMESTAMP('2023-01-01', 'YYYY-MM-DD');
     ```

#### Case When 

The `CASE WHEN` statement in PostgreSQL is often used for conditional logic within queries. Here are some examples demonstrating the use of `CASE WHEN` without the `FROM` clause:

1. **Simple Case Statement:**
   ```sql
   SELECT
     CASE 
       WHEN 1 = 1 THEN 'True'
       ELSE 'False'
     END;
   ```
   Returns 'True' if the condition is met, otherwise 'False'.

2. **Numeric Comparison:**
   ```sql
   SELECT
     CASE 
       WHEN 10 > 5 THEN 'Greater'
       WHEN 10 = 5 THEN 'Equal'
       ELSE 'Less'
     END;
   ```
   Returns 'Greater' if the first condition is true, 'Equal' if the second condition is true, and 'Less' otherwise.

3. **String Comparison:**
   ```sql
   SELECT
     CASE 
       WHEN 'apple' = 'orange' THEN 'Fruit Match'
       WHEN 'apple' = 'apple' THEN 'Apple Match'
       ELSE 'No Match'
     END;
   ```
   Returns 'Fruit Match' if the first condition is true, 'Apple Match' if the second condition is true, and 'No Match' otherwise.

4. **Nested Case Statement:**
   ```sql
   SELECT
     CASE 
       WHEN 1 = 1 THEN
         CASE 
           WHEN 2 = 2 THEN 'Nested True'
           ELSE 'Nested False'
         END
       ELSE 'Outer False'
     END;
   ```
   Demonstrates nesting of `CASE WHEN` statements.

5. **Date-based Case:**
   ```sql
   SELECT
     CASE 
       WHEN EXTRACT(MONTH FROM current_date) = 12 THEN 'December'
       WHEN EXTRACT(MONTH FROM current_date) = 1 THEN 'January'
       ELSE 'Other Month'
     END;
   ```
   Returns the month name based on the current date.

6. **Boolean Conditions:**
   ```sql
   SELECT
     CASE 
       WHEN true THEN 'It is true'
       WHEN false THEN 'It is false'
       ELSE 'Neither true nor false'
     END;
   ```
   Demonstrates using boolean conditions in `CASE WHEN`.

7. **NULL Handling:**
   ```sql
   SELECT
     CASE 
       WHEN NULL IS NULL THEN 'NULL is NULL'
       ELSE 'NULL is not NULL'
     END;
   ```
   Handles NULL conditions.

8. **Using Aggregate Functions:**
   ```sql
   SELECT
     CASE 
       WHEN COUNT(*) > 5 THEN 'Many Rows'
       WHEN COUNT(*) = 1 THEN 'One Row'
       ELSE 'Other'
     END;
   ```
   Uses an aggregate function in the condition.

9. **Checking for NULL Values in a Column:**
   ```sql
   SELECT
     CASE 
       WHEN column_name IS NULL THEN 'NULL Value'
       ELSE 'Not NULL Value'
     END;
   ```
   Checks if a specific column contains NULL values.

10. **Numeric Range Check:**
    ```sql
    SELECT
      CASE 
        WHEN column_name BETWEEN 1 AND 10 THEN 'Between 1 and 10'
        WHEN column_name BETWEEN 11 AND 20 THEN 'Between 11 and 20'
        ELSE 'Other'
      END;
    ```
    Checks if a numeric column falls within certain ranges.

#### Working With Null

 When working with `SELECT` statements without a `FROM` clause, you can use various SQL expressions to handle NULL values. Here are some examples:

1. **Use `COALESCE` to Replace NULL:**
   ```sql
   SELECT COALESCE(NULL, 'Replacement Value');
   ```
   Returns 'Replacement Value' if the first expression is NULL; otherwise, returns the first expression.

2. **Use `NULLIF` to Return NULL if Values Match:**
   
   ```sql
   SELECT NULLIF('Hello', 'Hello');
   ```
   Returns NULL if the two expressions are equal; otherwise, returns the first expression.
   
3. **Use `CASE WHEN` to Handle NULL:**
   
   ```sql
   SELECT
     CASE 
       WHEN NULL IS NULL THEN 'NULL Value'
       ELSE 'Not NULL Value'
     END;
   ```
   Checks if a specific expression is NULL and provides a result based on the condition.
   
4. **Numeric Calculation with NULL Handling:**
   
   ```sql
   SELECT 10 / COALESCE(column_name, 1);
   ```
   Performs a numeric calculation with NULL handling to avoid division by zero.
   
6. **Use `IS NULL` and `IS NOT NULL` Conditions:**
   ```sql
   SELECT
     CASE 
       WHEN column_name IS NULL THEN 'NULL'
       WHEN column_name IS NOT NULL THEN 'Not NULL'
     END;
   ```
   Checks if a column value is NULL or not NULL using the `IS NULL` and `IS NOT NULL` conditions.

7. **Use `NVL` (Oracle Compatibility):**
   ```sql
   SELECT NVL(column_name, 'Replacement Value');
   ```
   Returns 'Replacement Value' if the column value is NULL (Oracle compatibility).

8. **Check for NULL and Return Default Value:**
   ```sql
   SELECT
     CASE 
       WHEN column_name IS NULL THEN 'Default Value'
       ELSE column_name
     END;
   ```
   Checks if a column is NULL and returns a default value if true.

9. **Concatenate with NULL Handling Using `||`:**
   ```sql
   SELECT 'Prefix ' || column_name || ' Suffix';
   ```
   Concatenates strings with a prefix and suffix, where NULL values are treated as empty strings.

10. **Use `IFNULL` (MySQL Compatibility):**
    ```sql
    SELECT IFNULL(column_name, 'Default Value');
    ```
    Returns 'Default Value' if the column value is NULL (MySQL compatibility).



#### Useful String Functions

Certainly! PostgreSQL provides a variety of string manipulation functions that you can use in the `SELECT` statement without the `FROM` clause. Here are some useful string manipulation functions:

1. **Concatenate Strings:**
   ```sql
   SELECT 'Hello' || ' ' || 'World';
   ```
   Concatenates strings.

2. **Substring Extraction:**
   ```sql
   SELECT substring('PostgreSQL' FROM 1 FOR 4);
   ```
   Extracts a substring from a string.

3. **String Length:**
   ```sql
   SELECT length('Hello, World!');
   ```
   Returns the length of the string.

4. **Uppercase and Lowercase Conversion:**
   ```sql
   SELECT upper('hello'), lower('WORLD');
   ```
   Converts a string to uppercase or lowercase.

5. **Trim Spaces:**
   ```sql
   SELECT trim('   spaces   ');
   ```
   Removes leading and trailing spaces.

6. **Pad String:**
   ```sql
   SELECT lpad('5', 3, '0'), rpad('7', 4, 'X');
   ```
   Pads a string on the left or right with a specified character.

7. **Replace Substring:**
   ```sql
   SELECT replace('Hello, World!', 'World', 'Universe');
   ```
   Replaces occurrences of a substring with another substring.

8. **Position of Substring:**
   ```sql
   SELECT position('lo' IN 'Hello');
   ```
   Returns the position of a substring in a string.

9. **Reverse String:**
   ```sql
   SELECT reverse('Hello');
   ```
   Reverses the characters in a string.

10. **Left and Right Part of String:**
    ```sql
    SELECT left('Hello, World!', 5), right('Hello, World!', 6);
    ```
    Returns the leftmost or rightmost part of a string.

11. **Split String into Array:**
    ```sql
    SELECT string_to_array('apple,orange,banana', ',');
    ```
    Splits a string into an array using a delimiter.

12. **Join Array into String:**
    
    ```sql
    SELECT array_to_string(ARRAY['apple', 'orange', 'banana'], ',');
    ```
    Joins elements of an array into a string using a delimiter.
    
13. **Extract Word from String:**
    ```sql
    SELECT regexp_split_to_table('Hello, World!', '\s+') AS word;
    ```
    Splits a string into words using regular expression.

14. **String Position in Array:**
    ```sql
    SELECT position('orange' IN ARRAY['apple', 'orange', 'banana']);
    ```
    Returns the position of a string in an array.

15. **Translate Characters:**
    ```sql
    SELECT translate('Hello', 'elo', '123');
    ```
    Translates characters in a string based on a mapping.

These string manipulation functions provide a powerful set of tools for working with text data in PostgreSQL. Choose the functions that suit your specific requirements.

### Arrays in Postgres

1. Creating a table with an array column:

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    scores INTEGER[]
);
```

2. Inserting data with arrays:

```sql
INSERT INTO students (name, scores) VALUES
('Alice', ARRAY[85, 92, 78]),
('Bob', ARRAY[76, 88, 90]),
('Charlie', ARRAY[91, 94, 89]);
```

3. Querying array data:

a. Retrieve all data:
```sql
SELECT * FROM students;
```

Output:
```
 id |  name   |  scores  
----+---------+----------
  1 | Alice   | {85,92,78}
  2 | Bob     | {76,88,90}
  3 | Charlie | {91,94,89}
```

b. Access a specific array element (1-based indexing):
```sql
SELECT name, scores[2] AS second_score FROM students;
```

Output:
```
  name   | second_score
---------+--------------
 Alice   |           92
 Bob     |           88
 Charlie |           94
```

4. Array functions:

a. array_length: Get the length of an array
```sql
SELECT name, array_length(scores, 1) AS num_scores FROM students;
```

b. unnest: Expand an array to a set of rows
```sql
SELECT name, unnest(scores) AS individual_score FROM students;
```

5. Array operators:

a. Contains (`@>`):
```sql
    SELECT * FROM students WHERE scores @> ARRAY[90];
```

b. Overlaps (`&&`):
```sql
SELECT * FROM students WHERE scores && ARRAY[85, 86, 87];
```

6. Modifying arrays:

a. Append an element:
```sql
UPDATE students SET scores = array_append(scores, 95) WHERE name = 'Alice';
```

b. Remove an element:
```sql
UPDATE students SET scores = array_remove(scores, 78) WHERE name = 'Alice';
```

c. Replace an element:
```sql
UPDATE students SET scores[1] = 80 WHERE name = 'Bob';
```

7. Aggregating arrays:

a. array_agg: Aggregate values into an array
```sql
SELECT array_agg(name) AS student_names FROM students;
```

b. Combining arrays:
```sql
SELECT name, scores || ARRAY[100] AS extended_scores FROM students;
```

8. Array constructors:

a. Using ARRAY constructor:
```sql
INSERT INTO students (name, scores) VALUES ('David', ARRAY[88, 85, 90]);
```

b. Using array literal:
```sql
INSERT INTO students (name, scores) VALUES ('Eve', '{93, 89, 95}');
```

9. Searching within arrays:

a. ANY: Check if any array element satisfies a condition
```sql
SELECT * FROM students WHERE 90 = ANY(scores);
```

b. ALL: Check if all array elements satisfy a condition
```sql
SELECT * FROM students WHERE 80 < ALL(scores);
```

10. Array slicing:

```sql
SELECT name, scores[1:2] AS first_two_scores FROM students;
```

11. Multidimensional arrays:

```sql
CREATE TABLE matrix_example (
    id SERIAL PRIMARY KEY,
    matrix INTEGER[][]
);

INSERT INTO matrix_example (matrix) VALUES
(ARRAY[[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

SELECT matrix[2][2] FROM matrix_example;  -- Returns 5
```

12. Array set operations:

```sql
SELECT ARRAY[1,2,3] || ARRAY[4,5,6] AS concatenated,
       ARRAY[1,2,3,4] & ARRAY[2,3,4,5] AS intersection,
       ARRAY[1,2,3,4] | ARRAY[3,4,5,6] AS union;
 ?      
       
       
```

13. Generating arrays:

```sql
SELECT generate_series(1, 5) AS generated_array;
```

14. JSON to array conversion:

```sql
SELECT json_array_elements('[1, 2, 3]'::json) AS json_to_array;
```




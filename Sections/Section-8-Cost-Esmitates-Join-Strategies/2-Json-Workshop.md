#### JSON Workshop

1. Creating a table with a JSONB column

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    data JSONB
);
```

2. Inserting data into the JSONB column

```sql
INSERT INTO users (data) VALUES 
('{"name": "John Doe", "age": 30, "city": "New York"}'),
('{"name": "Jane Smith", "age": 25, "city": "London", "hobbies": ["reading", "hiking"]}');
```

3. Querying JSONB data

a. Retrieving all data:
```sql
SELECT * FROM users;
```
Output:
```
 id |                                  data                                  
----+------------------------------------------------------------------------
  1 | {"age": 30, "city": "New York", "name": "John Doe"}
  2 | {"age": 25, "city": "London", "name": "Jane Smith", "hobbies": ["reading", "hiking"]}
```

b. Accessing a specific field:
```sql
SELECT data->>'name' AS name FROM users;
```
Output:
```
    name    
------------
 John Doe
 Jane Smith
```

4. Filtering based on JSONB values

```sql
SELECT * FROM users WHERE data->>'city' = 'London';
```
Output:
```
 id |                                  data                                  
----+------------------------------------------------------------------------
  2 | {"age": 25, "city": "London", "name": "Jane Smith", "hobbies": ["reading", "hiking"]}
```

5. Updating JSONB data

a. Adding a new field:
```sql
UPDATE users SET data = data || '{"email": "john@example.com"}'::jsonb WHERE id = 1;
```

b. Modifying an existing field:
```sql
UPDATE users SET data = jsonb_set(data, '{age}', '31') WHERE id = 1;
```

6. Working with arrays in JSONB

a. Checking if an array contains a value:
```sql
SELECT * FROM users WHERE data->'hobbies' ? 'reading';
```
Output:
```
 id |                                  data                                  
----+------------------------------------------------------------------------
  2 | {"age": 25, "city": "London", "name": "Jane Smith", "hobbies": ["reading", "hiking"]}
```

b. Adding an element to an array:
```sql
UPDATE users SET data = jsonb_set(data, '{hobbies}', data->'hobbies' || '"swimming"'::jsonb) WHERE id = 2;
```

7. Advanced querying and indexing

a. Creating a GIN index for faster JSON querying:
```sql
CREATE INDEX idx_users_data ON users USING GIN (data);
```

b. Using the `@>` operator for containment queries:
```sql
SELECT * FROM users WHERE data @> '{"city": "London", "age": 25}';
```

c. Querying nested structures:
```sql
INSERT INTO users (data) VALUES ('{"name": "Alice", "address": {"street": "123 Main St", "city": "Chicago"}}');

SELECT * FROM users WHERE data->'address'->>'city' = 'Chicago';
```

8. Aggregating JSONB data

a. Counting occurrences of a specific value:
```sql
SELECT data->>'city' AS city, COUNT(*) FROM users GROUP BY data->>'city';
```

b. Finding the average age:
```sql
SELECT AVG((data->>'age')::int) AS average_age FROM users;
```

9. Using JSONB functions

a. jsonb_each: Expand the outermost JSON object into key-value pairs
```sql
SELECT jsonb_each(data) FROM users WHERE id = 1;
```

b. jsonb_object_keys: Get a set of keys in the JSON object
```sql
SELECT jsonb_object_keys(data) FROM users WHERE id = 1;
```

10. Using JSONB operators

a. The `-` operator to remove a key:
```sql
UPDATE users SET data = data - 'email' WHERE id = 1;
```

b. The `#-` operator to remove a path:
```sql
UPDATE users SET data = data #- '{address,street}' WHERE id = 3;
```

This tutorial covers a range of operations with JSONB in PostgreSQL, from basic to advanced. 

### Removing an Array Element

Removing an array element from a JSONB array in PostgreSQL can be done in a few different ways. I'll show you some methods, starting with the simplest and moving to more flexible options:

1. Using the `-` operator (for removing a specific value):

```sql
UPDATE users 
SET data = data || jsonb_build_object('hobbies', data->'hobbies' - 'hiking')
WHERE id = 2;
```

This method works well when you know the exact value you want to remove.

2. Using `jsonb_array_elements` and `jsonb_build_array` (for more complex filtering):

```sql
UPDATE users 
SET data = data || jsonb_build_object(
    'hobbies', 
    (SELECT jsonb_agg(elem) 
     FROM jsonb_array_elements(data->'hobbies') elem 
     WHERE elem::text != '"hiking"')
)
WHERE id = 2;
```

This method allows you to use more complex conditions for removing elements.

3. Using a custom function (for reusability):

First, create a function:

```sql
CREATE OR REPLACE FUNCTION jsonb_array_remove(arr jsonb, elem text)
RETURNS jsonb AS $$
SELECT jsonb_agg(x) FROM jsonb_array_elements(arr) x WHERE x::text != elem::text;
$$ LANGUAGE SQL IMMUTABLE;
```

Then use it in your update:

```sql
UPDATE users
SET data = jsonb_set(data, '{hobbies}', jsonb_array_remove(data->'hobbies', '"hiking"'))
WHERE id = 2;
```

4. Removing by index (if you know the position):

```sql
UPDATE users
SET data = jsonb_set(
    data,
    '{hobbies}',
    (data->'hobbies') #- '{1}'  -- Removes the second element (index 1)
)
WHERE id = 2;
```

5. For removing multiple elements at once:

```sql
UPDATE users
SET data = data || jsonb_build_object(
    'hobbies', 
    (SELECT jsonb_agg(elem) 
     FROM jsonb_array_elements(data->'hobbies') elem 
     WHERE elem::text NOT IN ('"hiking"', '"swimming"'))
)
WHERE id = 2;
```

After applying any of these methods, you can verify the result:

```sql
SELECT data->'hobbies' FROM users WHERE id = 2;
```

Each of these methods has its use cases:
- Method 1 is simplest for removing a single, known value.
- Method 2 is more flexible and allows for complex filtering.
- Method 3 is great if you'll be doing this operation frequently.
- Method 4 is useful when you know the position of the element to remove.
- Method 5 is best for removing multiple elements in one operation.


### UUID Auto Increments

1. Enable the UUID extension (if not already enabled):
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

2. Create a table with a UUID primary key:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

3. Insert data without specifying the UUID:
```sql
INSERT INTO users (username, email) 
VALUES ('john_doe', 'john@example.com');

INSERT INTO users (username, email) 
VALUES ('jane_smith', 'jane@example.com');

INSERT INTO users (username, email, created_at) 
VALUES ('bob_johnson', 'bob@example.com', '2024-08-01 10:00:00+00');
```

4. Query the table to see the auto-generated UUIDs:
```sql
SELECT * FROM users;
```

5. Update a record using the UUID:
```sql
UPDATE users 
SET email = 'john.doe@newdomain.com' 
WHERE id = '123e4567-e89b-12d3-a456-426614174000';  -- Replace with an actual UUID from your table
```

6. Delete a record using the UUID:
```sql
DELETE FROM users 
WHERE id = '123e4567-e89b-12d3-a456-426614174000';  -- Replace with an actual UUID from your table
```

7. Query for a specific user by UUID:
```sql
SELECT * FROM users 
WHERE id = '123e4567-e89b-12d3-a456-426614174000';  -- Replace with an actual UUID from your table
```

8. Join with another table using UUID:
```sql
CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    order_date DATE DEFAULT CURRENT_DATE
);

INSERT INTO orders (user_id) 
SELECT id FROM users WHERE username = 'john_doe';

SELECT u.username, o.order_id, o.order_date
FROM users u
JOIN orders o ON u.id = o.user_id;
```

This tutorial covers creating a table with a UUID primary key, inserting data, querying, updating, deleting, and even joining with another table using UUID fields.

Would you like me to explain any part of this tutorial in more detail?
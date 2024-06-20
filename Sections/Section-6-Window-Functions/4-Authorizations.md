### Authorization in Postgres



### 1. Create a Role
```sql
CREATE ROLE marketing_role;
```

### 2. Create a User and Assign a Password
```sql
CREATE USER marketing_user WITH PASSWORD 'securepassword';
```

### 3. Update User Password
```sql
ALTER USER marketing_user WITH PASSWORD 'newpassword';
```

### 4. Grant Select Permission on a Table
```sql
GRANT SELECT ON TABLE customers TO marketing_user;
```

### 5. Grant Update Permission on a Table
```sql
GRANT UPDATE ON TABLE products TO marketing_user;
```

### 6. Grant Usage on Schema
```sql
GRANT USAGE ON SCHEMA public TO marketing_role;
```

### 7. Grant All Privileges on a Table to a Role
```sql
GRANT ALL PRIVILEGES ON TABLE orders TO marketing_role;
```

### 8. Revoke Select Permission on a Table
```sql
REVOKE SELECT ON TABLE employees FROM marketing_user;
```

### 9. Revoke Update Permission on a Table
```sql
REVOKE UPDATE ON TABLE categories FROM marketing_user;
```

### 10. Revoke All Privileges on a Table from a Role
```sql
REVOKE ALL PRIVILEGES ON TABLE suppliers FROM marketing_role;
```

These examples cover creating roles, users, updating passwords, granting specific permissions on tables and schemas, and revoking those permissions. Adjust the role and user names, passwords, and table names as needed for your specific use case.
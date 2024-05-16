### Introduction to PSQL and Connecting to PostgreSQL:

#### Connect to PostgreSQL:

```bash
psql -h your_host -p your_port -U your_user -d your_database
```

Replace `your_host`, `your_port`, `your_user`, and `your_database` with your actual PostgreSQL server details.

### Main Commands in PSQL:

Here are some essential PSQL commands:

| Command            | Description                                                 |
| ------------------ | ----------------------------------------------------------- |
| `\q`               | Quit psql.                                                  |
| `\l` - `\l+`       | List all databases.                                         |
| `\c your_database` | Connect to a different database.                            |
| `\dt`              | List all tables in the current database.                    |
| `\d your_table`    | Show table details (columns, types, constraints).           |
| `\i your_file.sql` | Execute SQL commands from a file.                           |
| `\e`               | Open the default text editor to compose a multi-line query. |

**Hint**: ICU stands for "International Components for Unicode. (`\l` result)

#### Template1 Workaround

```bash
\c template1

### List Schemas -  lists user-created schemas
\dn 

\dn+

\e 
SELECT distinct schemaname
FROM pg_tables;


### Describe a table
\d pg_tables

\d+ pg_tables

\d information_schema.tables

### List All View
\dv

\dv *.*

#### Describe Views
\d+ pg_stats


### List Indices
\di 

\di+ *.*

\d+ pg_class_oid_index

#### List Tables of the Current Schema
\dt 

\dt *.*

\c postgres

 \dt pg_catalog.*
 
```



#### Four Default Schema in Postgres

Here's a table comparing the `pg_catalog`, `pg_toast`, `information_schema`, and `postgres` schemas in PostgreSQL:

| Schema               | Purpose and Content                                          |
| -------------------- | ------------------------------------------------------------ |
| `pg_catalog`         | - Contains the system catalog tables and views that store metadata about the database, such as tables, columns, indexes, and data types. |
|                      | - Holds crucial information for PostgreSQL's internal operations. |
|                      | - Managed by PostgreSQL and generally not intended for direct user modifications. |
| `pg_toast`           | - Stores large objects or oversized data that does not fit into a regular table row. |
|                      | - Used for storage of out-of-line data, such as large text or binary objects. |
|                      | - `pg_toast` tables are associated with regular tables and store "toasted" data. |
| `information_schema` | - Provides a standardized way to access metadata about the database. |
|                      | - Offers views that represent various aspects of the database, such as tables, columns, constraints, and privileges. |
|                      | - Designed to be compliant with the SQL standard and provides a more user-friendly interface for retrieving metadata. |
|                      | - Generally used for querying metadata in a portable and standard way across different database systems. |
| `postgres`           | - The default schema used for user-created objects when no explicit schema is specified. |
|                      | - Tables and other objects created without specifying a schema are placed in the `public` schema by default, which is equivalent to the `postgres` schema in many cases. |
|                      | - Users often create their tables, functions, and other objects within the `public` schema. |

It's important to note that while `pg_catalog` and `pg_toast` are integral to the internal functioning of PostgreSQL and may contain system-specific information, `information_schema` provides a standardized and portable way to access metadata across different database systems. The `postgres` schema is more user-centric and is often the default location for user-created objects.

### System Catalog Schema

In PostgreSQL, the system catalog tables are typically located in the `pg_catalog` schema. This schema is a system schema that contains system-related information, including metadata about tables, columns, indexes, and other database objects .

some tables/views in the `pg_catalog` schema:

| Table/View Name        | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| `pg_tables`            | Lists all tables in all schemas in the current database.     |
| `pg_indexes`           | Provides information about indexes on tables.                |
| `pg_class`             | Contains information about tables and other relations.       |
| `pg_namespace`         | Stores schema-related information.                           |
| `pg_constraint`        | Holds information about table constraints.                   |
| `pg_attribute`         | Contains information about table columns.                    |
| `pg_type`              | Stores data types used in the database.                      |
| `pg_database`          | Lists all databases on the PostgreSQL server.                |
| `pg_roles`             | Contains information about database roles (users).           |
| `pg_user`              | A view on top of `pg_roles` providing additional information about database users. |
| `pg_settings`          | Shows the current settings of configuration parameters.      |
| `pg_stat_user_tables`  | Provides statistics on user tables.                          |
| `pg_stat_user_indexes` | Provides statistics on user indexes.                         |
| `pg_stat_bgwriter`     | Displays statistics about the background writer process.     |

Please note that this is not an exhaustive list, and PostgreSQL has many more system catalog tables. Additionally, the availability of some tables may depend on the version of PostgreSQL you are using. You can explore these tables to gain insights into the structure and metadata of your PostgreSQL database.

### Workshop: Creating Schema and Inserting Data:

1. **Create Database/ Schema / ENUM and Sequence:**

    ```sql
    DROP DATABASE IF EXISTS jobs;
    create database jobs;
    
    \c jobs;
    
    CREATE TYPE user_role AS ENUM ('job_seeker', 'employer');
    
    \dT
    
    \dT *.* 
    
    \dT+ bigint
    
    SELECT enumlabel
    FROM pg_enum
    WHERE enumtypid = 'user_role'::regtype;
    
    
    CREATE SEQUENCE custom_id_seq;
    
    \ds+
    
    \ds *.*
    
    SELECT nextval('custom_id_seq');
    
    
    ```

2. **Create Users Table:**

    ```sql
    CREATE TABLE users (
        user_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        user_type user_role NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    
    \dt+
    
    \d+ users
    
    SELECT oid, relname FROM pg_class WHERE relname = 'users';
    ```

3. **Insert Data into Users Table:**

    ```sql
    INSERT INTO users (username, password_hash, email, user_type) VALUES
        ('john_doe', 'hashed_password', 'john@example.com', 'job_seeker'),
        ('company_xyz', 'hashed_password', 'info@companyxyz.com', 'employer');
        
        
    ```

4. **Check Data in Users Table:**

    ```sql
    SELECT * FROM users;
    ```

5. **Create Job Seekers Table:**

    ```sql
    CREATE TABLE job_seekers (
        seeker_id INT PRIMARY KEY REFERENCES users(user_id),
        resume JSON NOT NULL,
       --	additional_info JSONB,
        FOREIGN KEY (seeker_id) REFERENCES users(user_id)
    );
    ```

6. **Insert Data into Job Seekers Table:**

    ```sql
    INSERT INTO job_seekers (seeker_id, resume ) VALUES
        (1, '{"education": "B.Sc in Computer Science", "experience": "3 years"}');
        
        Note : check that the user_id exist in the user table . 
    ```

7. **Check Data in Job Seekers Table:**

    ```sql
    SELECT * FROM job_seekers;
    ```

    ##### Create Employers Table:

    ```sql
    CREATE TABLE employers (
        employer_id INT PRIMARY KEY REFERENCES users(user_id),
        company_name VARCHAR(100),
        company_info JSONB,
        FOREIGN KEY (employer_id) REFERENCES users(user_id)
    );
    ```

    ##### Insert Data into Employers Table:

    ```sql
    INSERT INTO employers (employer_id, company_name, company_info) VALUES
        (2, 'Company XYZ', '{"industry": "Technology", "employees": 100}');
    ```

    ##### Check Data in Employers Table:

    ```sql
    SELECT * FROM employers;
    ```

    ##### Create Job Listings Table:

    ```sql
    CREATE TABLE job_listings (
        job_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
        employer_id INT REFERENCES employers(employer_id),
        title VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        location VARCHAR(100),
        posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) CHECK (status IN ('open', 'closed')) DEFAULT 'open'
    );
    ```

    ##### Insert Data into Job Listings Table:

    ```sql
    INSERT INTO job_listings (employer_id, title, description, location, status) VALUES
        (2, 'Software Engineer', 'Join our dynamic team!', 'New York', 'open'),
        (2, 'Product Manager', 'Lead innovative projects', 'San Francisco', 'open');
    ```

    ##### Check Data in Job Listings Table:

    ```sql
    SELECT * FROM job_listings;
    ```

    Now, you should have data in the Employers and Job Listings tables. Feel free to run these commands in your PSQL session. If you encounter any issues or have further questions, let me know!

8. **Create Applications Table:**

    ```sql
    CREATE TABLE applications (
        application_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
        job_id INT REFERENCES job_listings(job_id),
        seeker_id INT REFERENCES job_seekers(seeker_id),
        application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) CHECK (status IN ('pending', 'accepted', 'rejected')) DEFAULT 'pending'
    );
    ```

9. **Insert Data into Applications Table:**

    ```sql
    INSERT INTO applications (job_id, seeker_id, status) VALUES
        (1, 1, 'accepted'),
        (1, 2, 'pending');
    ```

10. **Check Data in Applications Table:**

    ```sql
    SELECT * FROM applications;
    ```

11. **Create Index on Job Listings Table:**

     ```sql
     CREATE INDEX idx_job_listings ON job_listings(title, location);
     ```




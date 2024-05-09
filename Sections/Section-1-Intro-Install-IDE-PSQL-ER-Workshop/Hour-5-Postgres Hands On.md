Creating a PostgreSQL schema, database, and the required tables with sample records for the given SQL practice exercises involves several steps. Here's a guide on how you can set this up:

### Step 1: Install PostgreSQL

Make sure PostgreSQL is installed on your system. You can download it from the [official PostgreSQL website](https://www.postgresql.org/download/).

### Step 2: Create a New Database

1. **Open PostgreSQL**: Open your PostgreSQL command line client. 
2. **Create Database**: Run the following command to create a new database:
   ```sql
   CREATE DATABASE sql_practice;
   ```

### Step 3: Connect to the Database

Connect to the database you just created:
```sql
\c sql_practice
```

### Step 4: Create Tables

#### 1. Create `distribution_companies` Table

```sql
CREATE TABLE distribution_companies (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL
);
```

#### 2. Create `movies` Table

```sql
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    movie_title VARCHAR(255) NOT NULL,
    imdb_rating DECIMAL(2,1),
    year_released INT,
    budget DECIMAL(10,2),
    box_office DECIMAL(10,2),
    distribution_company_id INT,
    language VARCHAR(255),
    FOREIGN KEY (distribution_company_id) REFERENCES distribution_companies (id)
);
```

### Step 5: Insert Sample Data

#### Insert into `distribution_companies`:

```sql
INSERT INTO distribution_companies (company_name) VALUES
('Columbia Pictures'),
('Paramount Pictures'),
('Warner Bros. Pictures'),
('United Artists'),
('Universal Pictures'),
('New Line Cinema'),
('Miramax Films'),
('Produzioni Europee Associate'),
('Buena Vista'),
('StudioCanal');
```

#### Insert into `movies`:

```sql
INSERT INTO movies (movie_title, imdb_rating, year_released, budget, box_office, distribution_company_id, language) VALUES
('The Shawshank Redemption', 9.2, 1994, 25.00, 73.30, 1, 'English'),
('The Godfather', 9.2, 1972, 7.20, 291.00, 2, 'English'),
('The Dark Knight', 9.0, 2008, 185.00, 1006.00, 3, 'English'),
('The Godfather Part II', 9.0, 1974, 13.00, 93.00, 2, 'English, Sicilian'),
('12 Angry Men', 9.0, 1957, 0.34, 2.00, 4, 'English'),
('Schindler\'s List', 8.9, 1993, 22.00, 322.20, 5, 'English, German, Yiddish'),
('The Lord of the Rings: The Return of the King', 8.9, 2003, 94.00, 1146.00, 6, 'English'),
('Pulp Fiction', 8.8, 1994, 8.50, 213.90, 7, 'English'),
('The Lord of the Rings: The Fellowship of the Ring', 8.8, 2001, 93.00, 898.20, 6, 'English'),
('The Good, the Bad and the Ugly', 8.8, 1966, 1.20, 38.90, 8, 'English, Italian, Spanish');
```

### Step 6: Run Sample Queries

Now you can run the queries : https://learnsql.com/blog/sql-practice-exercises/


Adjusting the schema to include JSON data types and separating the job seeker and employer tables is a good approach for more specialized data handling and clearer separation of concerns. Here's the revised schema:

### Job-Seeking Online App

```sql
-- Define custom ENUM for user_type
CREATE TYPE user_role AS ENUM ('job_seeker', 'employer');

-- Create a sequence for generating custom IDs
CREATE SEQUENCE custom_id_seq;

-- Users Table (Common for both job seekers and employers)
CREATE TABLE users (
    user_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- Use a more secure data type for passwords
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type user_role NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job Seekers Table
CREATE TABLE job_seekers (
    seeker_id INT PRIMARY KEY REFERENCES users(user_id),
    resume JSON NOT NULL,
    additional_info HSTORE,  -- Storing additional information in HStore
    FOREIGN KEY (seeker_id) REFERENCES users(user_id)
);

-- Employers Table
CREATE TABLE employers (
    employer_id INT PRIMARY KEY REFERENCES users(user_id),
    company_name VARCHAR(100),
    company_info HSTORE,  -- Storing company information in HStore
    FOREIGN KEY (employer_id) REFERENCES users(user_id)
);

-- Job Listings Table
CREATE TABLE job_listings (
    job_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
    employer_id INT REFERENCES employers(employer_id),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(100),
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('open', 'closed')) DEFAULT 'open'
);

-- Applications Table
CREATE TABLE applications (
    application_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
    job_id INT REFERENCES job_listings(job_id),
    seeker_id INT REFERENCES job_seekers(seeker_id),
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('pending', 'accepted', 'rejected')) DEFAULT 'pending'
);

-- Creating an index for faster searches on job listings
CREATE INDEX idx_job_listings ON job_listings(title, location);

```

### Schema Explanation

- **Users Table**: This remains common for both job seekers and employers. The `user_type` field distinguishes between them.

- **Job Seekers Table**: Stores job seeker-specific information. The `resume` and `additional_info` fields are of type JSON, allowing flexible data structures for resumes and additional details.

- **Employers Table**: Holds employer-specific information. The `company_info` field is a JSON type, suitable for various company-related data.

- **Job Listings and Applications Tables**: Linked to `employers` and `job_seekers` tables respectively through foreign keys.

### Notes:

- **JSON Data Type**: This allows for storing structured data in a format that's both human-readable and machine-parseable. It's flexible but should be used judiciously, as querying and indexing JSON data can be more complex than standard relational columns.
  
- **Data Integrity and Relations**: The use of foreign keys ensures referential integrity. For example, each job listing must be associated with a valid employer, and each application must be tied to a specific job listing and job seeker.

- **Normalization**: This schema design aims to reduce redundancy and improve data integrity by separating concerns into distinct tables.

This updated schema provides a more robust structure for the job-seeking application, accommodating complex and varied data while maintaining clear relationships between different entities.

#### Insert Sample Data

```sql

INSERT INTO users (username, password, email, user_type) VALUES
('johnDoe', 'john123', 'john@example.com', 'job_seeker'),
('janeDoe', 'jane123', 'jane@example.com', 'employer'),
('mikeSmith', 'mike123', 'mike@example.com', 'job_seeker'),
('sarahJones', 'sarah123', 'sarah@example.com', 'employer');

INSERT INTO job_seekers (seeker_id, resume, additional_info) VALUES
(1, '{"skills": ["Java", "Python"], "experience": 5}', '{"preferred_location": "New York"}'),
(3, '{"skills": ["HTML", "CSS", "JavaScript"], "experience": 3}', '{"preferred_location": "San Francisco"}');

INSERT INTO employers (employer_id, company_name, company_info) VALUES
(2, 'TechCorp', '{"industry": "Technology", "size": "100-500"}'),
(4, 'HealthPlus', '{"industry": "Healthcare", "size": "500-1000"}');

INSERT INTO job_listings (employer_id, title, description, location) VALUES
(2, 'Software Engineer', 'Develop and maintain web applications.', 'New York'),
(4, 'Data Analyst', 'Analyze healthcare data and provide insights.', 'Chicago');

INSERT INTO applications (job_id, seeker_id) VALUES
(1, 1),
(2, 3);

```



## Some SQL Simple Queries

### Easy

1. **List all users**:
   ```sql
   SELECT * FROM users;
   ```

2. **Count the number of job seekers**:
   
   ```sql
   SELECT COUNT(*) FROM job_seekers;
   ```
   
3. **Find all job listings posted by a specific employer (employer_id = 1)**:
   ```sql
   SELECT * FROM job_listings WHERE employer_id = 1;
   ```

4. **Retrieve the email addresses of all employers**:
   ```sql
   SELECT u.email FROM users u JOIN employers e ON u.user_id = e.employer_id;
   ```

5. **Display the usernames and creation dates of all users created after January 1, 2023**:
   ```sql
   SELECT username, created_at FROM users WHERE created_at > '2023-01-01';
   ```

### Intermediate

6. **List job seekers along with their resumes**:
   ```sql
   SELECT u.username, j.resume FROM job_seekers j JOIN users u ON j.seeker_id = u.user_id;
   ```

7. **Show all job listings with the status 'open'**:
   ```sql
   SELECT * FROM job_listings WHERE status = 'open';
   ```

8. **Find the number of applications for each job listing**:
   ```sql
   SELECT job_id, COUNT(*) FROM applications GROUP BY job_id;
   ```

9. **Display company names of all employers**:
   ```sql
   SELECT company_name FROM employers;
   ```

10. **List all users who are job seekers but haven’t applied for any job**:
    ```sql
    SELECT u.username FROM users u
    LEFT JOIN job_seekers j ON u.user_id = j.seeker_id
    LEFT JOIN applications a ON j.seeker_id = a.seeker_id
    WHERE u.user_type = 'job_seeker' AND a.application_id IS NULL;
    ```

### Medium

11. **Show job listings along with the number of applications received for each, including those with zero applications**:
    ```sql
    SELECT jl.job_id, COUNT(a.application_id) AS application_count
    FROM job_listings jl
    LEFT JOIN applications a ON jl.job_id = a.job_id
    GROUP BY jl.job_id;
    ```

12. **Find job seekers who have applied for more than one job**:
    ```sql
    SELECT j.seeker_id, COUNT(*) FROM applications a
    JOIN job_seekers j ON a.seeker_id = j.seeker_id
    GROUP BY j.seeker_id
    HAVING COUNT(*) > 1;
    ```

13. **List all job listings in 'open' status that have not received any applications**:
    ```sql
    SELECT jl.* FROM job_listings jl
    LEFT JOIN applications a ON jl.job_id = a.job_id
    WHERE jl.status = 'open' AND a.application_id IS NULL;
    ```

14. **Retrieve the latest three job listings**:
    ```sql
    SELECT * FROM job_listings ORDER BY posted_date DESC LIMIT 3;
    ```

15. **List job seekers and the titles of jobs they’ve applied for**:
    ```sql
    SELECT u.username, jl.title FROM applications a
    JOIN job_seekers j ON a.seeker_id = j.seeker_id
    JOIN users u ON j.seeker_id = u.user_id
    JOIN job_listings jl ON a.job_id = jl.job_id;
    ```

16. **Count the number of job listings for each employer**:
    ```sql
    SELECT employer_id, COUNT(*) FROM job_listings GROUP BY employer_id;
    ```

17. **List all employers who haven’t posted any job listings**:
    ```sql
    SELECT e.employer_id FROM employers e
    LEFT JOIN job_listings jl ON e.employer_id = jl.employer_id
    WHERE jl.job_id IS NULL;
    ```

18. **Show job seekers’ usernames and the number of jobs each has applied for**:
    ```sql
    SELECT u.username, COUNT(a.application_id) AS num_applications FROM job_seekers j
    JOIN users u ON j.seeker_id = u.user_id
    LEFT JOIN applications a ON j.seeker_id = a.seeker_id
    GROUP BY u.username;
    ```

19. **Find the job listing with the highest number of applications**:
    ```sql
    SELECT job_id, COUNT(*) AS num_applications FROM applications
    GROUP BY job_id ORDER BY num_applications DESC LIMIT 1;
    ```

20. **List job seekers who have applied for a job in 'Engineering' **

    

    

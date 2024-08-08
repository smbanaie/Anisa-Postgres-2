**Introduction to PL/pgSQL**

PL/pgSQL is the procedural programming language for PostgreSQL, which allows you to write custom functions, procedures, and triggers. It provides a structured way to interact with the database, perform complex data manipulations, and implement business logic.

**Step 1: Simple Queries**

Let's start with some simple queries to familiarize ourselves with the data:

```sql
-- Count the total number of users
CREATE OR REPLACE FUNCTION get_user_count()
RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT COUNT(*) FROM users);
END;
$$ LANGUAGE plpgsql;

-- Select the email and user type for the first 10 users
CREATE OR REPLACE FUNCTION get_user_samples()
RETURNS TABLE (email VARCHAR, user_type user_role) AS $$
BEGIN
    RETURN QUERY SELECT u.email, u.user_type 
    FROM users u
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_user_limit(limit_count INTEGER)
RETURNS TABLE (email VARCHAR, user_type user_role) AS $$
BEGIN
    RETURN QUERY SELECT u.email, u.user_type
        FROM users u
    LIMIT limit_count;
    
END;
$$ LANGUAGE plpgsql;


-- Get the number of job listings per location
CREATE OR REPLACE FUNCTION get_job_listings_per_location()
RETURNS TABLE (location VARCHAR, num_jobs INTEGER) AS $$
BEGIN
    RETURN QUERY SELECT j.location, CAST(COUNT(*) AS INTEGER) AS num_jobs
    FROM job_listings j
    GROUP BY j.location;
END;
$$ LANGUAGE plpgsql;
```

These functions demonstrate how to create simple PL/pgSQL functions that return a single value, a result set, and a table. They showcase the basic syntax and structure of PL/pgSQL code.

**Step 2: Queries with Filters**

Now, let's write some functions that include filters and conditions:

```sql
-- Get job listings for a specific location
CREATE OR REPLACE FUNCTION get_job_listings_by_location(loc VARCHAR)
RETURNS TABLE (title VARCHAR, description TEXT) AS $$
BEGIN
    RETURN QUERY SELECT title, description FROM job_listings WHERE location = loc;
END;
$$ LANGUAGE plpgsql;

-- Get pending job applications for job seekers
CREATE OR REPLACE FUNCTION get_pending_job_applications()
RETURNS TABLE (username VARCHAR, job_title VARCHAR, application_date TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT u.username, j.title, a.application_date
    FROM users u
    JOIN job_seekers js ON u.user_id = js.seeker_id
    JOIN applications a ON js.seeker_id = a.seeker_id
    JOIN job_listings j ON a.job_id = j.job_id
    WHERE u.user_type = 'job_seeker' AND a.status = 'pending';
END;
$$ LANGUAGE plpgsql;
```

These functions demonstrate how to pass parameters to PL/pgSQL functions and how to use conditional logic and joins to filter the data.

**Step 3: Queries with Window Functions**

Next, let's explore the use of window functions in PL/pgSQL:

```sql
-- Get job listings with row numbers per employer
CREATE OR REPLACE FUNCTION get_job_listings_with_row_numbers()
RETURNS TABLE (title VARCHAR, description TEXT, row_num INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT l.title, l.description, CAST(ROW_NUMBER() OVER (PARTITION BY l.employer_id ORDER BY l.posted_date DESC) AS INTEGER) AS row_num
    FROM job_listings l;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_job_listings_with_row_numbers();


select  get_job_listings_with_row_numbers()

-- Get job applications with rank per job seeker
CREATE OR REPLACE FUNCTION get_job_applications_with_rank()
RETURNS TABLE (username VARCHAR, job_title VARCHAR, application_date TIMESTAMP, application_rank INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT u.username, j.title, a.application_date, CAST(RANK() OVER (PARTITION BY a.seeker_id ORDER BY a.application_date DESC) AS INTEGER) AS application_rank
    FROM users u
    JOIN job_seekers js ON u.user_id = js.seeker_id
    JOIN applications a ON js.seeker_id = a.seeker_id
    JOIN job_listings j ON a.job_id = j.job_id
    WHERE u.user_type = 'job_seeker';
END;
$$ LANGUAGE plpgsql;
```

These functions demonstrate the use of window functions like `ROW_NUMBER()` and `RANK()` to provide additional context and ordering for the results.


Adjusting the schema to include JSON data types and separating the job seeker and employer tables is a good approach for more specialized data handling and clearer separation of concerns. Here's the revised schema:

### Job-Seeking Online App

```sql
-- Users Table (Common for both job seekers and employers)
CREATE TABLE users (
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type VARCHAR(20) CHECK (user_type IN ('job_seeker', 'employer')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job Seekers Table
CREATE TABLE job_seekers (
    seeker_id INT REFERENCES users(user_id),
    resume JSON NOT NULL,  -- Storing resume in JSON format
    additional_info JSON,  -- Additional information in JSON format
    PRIMARY KEY (seeker_id)
);

-- Employers Table
CREATE TABLE employers (
    employer_id INT REFERENCES users(user_id),
    company_name VARCHAR(100),
    company_info JSON,  -- Company information in JSON format
    PRIMARY KEY (employer_id)
);

-- Job Listings Table
CREATE TABLE job_listings (
    job_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employer_id INT REFERENCES employers(employer_id),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(100),
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('open', 'closed')) DEFAULT 'open'
);

-- Applications Table
CREATE TABLE applications (
    application_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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
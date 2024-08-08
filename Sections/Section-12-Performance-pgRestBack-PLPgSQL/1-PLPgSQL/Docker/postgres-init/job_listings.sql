CREATE TYPE user_role AS ENUM ('job_seeker', 'employer');

CREATE SEQUENCE custom_id_seq;

CREATE TABLE users (
    user_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type user_role NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE job_seekers (
    seeker_id INT PRIMARY KEY REFERENCES users(user_id),
    resume JSON NOT NULL,
   --	additional_info JSONB,
    FOREIGN KEY (seeker_id) REFERENCES users(user_id)
);



CREATE TABLE employers (
    employer_id INT PRIMARY KEY REFERENCES users(user_id),
    company_name VARCHAR(100),
    company_info JSONB,
    FOREIGN KEY (employer_id) REFERENCES users(user_id)
);


CREATE TABLE job_listings (
    job_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
    employer_id INT REFERENCES employers(employer_id),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(100),
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('open', 'closed')) DEFAULT 'open'
);

CREATE TABLE applications (
    application_id INT DEFAULT nextval('custom_id_seq') PRIMARY KEY,
    job_id INT REFERENCES job_listings(job_id),
    seeker_id INT REFERENCES job_seekers(seeker_id),
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('pending', 'accepted', 'rejected')) DEFAULT 'pending'
);

-- Insert users
INSERT INTO users (username, password_hash, email, user_type) VALUES
    ('john_doe_1', 'hashed_password', 'john1@example.com', 'job_seeker'),
    ('john_doe_2', 'hashed_password', 'john2@example.com', 'job_seeker'),
    ('john_doe_3', 'hashed_password', 'john3@example.com', 'job_seeker'),
    ('company_xyz_1', 'hashed_password', 'info1@companyxyz.com', 'employer'),
    ('company_xyz_2', 'hashed_password', 'info2@companyxyz.com', 'employer'),
    ('company_xyz_3', 'hashed_password', 'info3@companyxyz.com', 'employer'),
    ('jane_smith_1', 'hashed_password', 'jane1@example.com', 'job_seeker'),
    ('jane_smith_2', 'hashed_password', 'jane2@example.com', 'job_seeker'),
    ('jane_smith_3', 'hashed_password', 'jane3@example.com', 'job_seeker'),
    ('acme_inc_1', 'hashed_password', 'info1@acmeinc.com', 'employer'),
    ('acme_inc_2', 'hashed_password', 'info2@acmeinc.com', 'employer'),
    ('acme_inc_3', 'hashed_password', 'info3@acmeinc.com', 'employer'),
    ('bob_johnson_1', 'hashed_password', 'bob1@example.com', 'job_seeker'),
    ('bob_johnson_2', 'hashed_password', 'bob2@example.com', 'job_seeker'),
    ('bob_johnson_3', 'hashed_password', 'bob3@example.com', 'job_seeker');

-- Insert job_seekers
INSERT INTO job_seekers (seeker_id, resume) VALUES
    (2, '{"education": "B.Sc in Computer Science", "experience": "3 years"}'),
    (3, '{"education": "B.Sc in Computer Science", "experience": "3 years"}'),
    (4, '{"education": "M.A in Economics", "experience": "5 years"}'),
    (5, '{"education": "M.A in Economics", "experience": "5 years"}'),
    (6, '{"education": "M.A in Economics", "experience": "5 years"}'),
    (8, '{"education": "B.A in English Literature", "experience": "2 years"}'),
    (9, '{"education": "B.A in English Literature", "experience": "2 years"}'),
    (10, '{"education": "B.A in English Literature", "experience": "2 years"}');

-- Insert employers
INSERT INTO employers (employer_id, company_name, company_info) VALUES
    (4, 'Acme Inc', '{"industry": "Manufacturing", "employees": 500}'),
    (5, 'Acme Inc', '{"industry": "Manufacturing", "employees": 500}'),
    (6, 'Acme Inc', '{"industry": "Manufacturing", "employees": 500}'),
    (11, 'Company XYZ', '{"industry": "Technology", "employees": 100}'),
    (12, 'Company XYZ', '{"industry": "Technology", "employees": 100}'),
    (13, 'Company XYZ', '{"industry": "Technology", "employees": 100}');

-- Insert job_listings
INSERT INTO job_listings (employer_id, title, description, location, status) VALUES
    (4, 'Manufacturing Technician', 'Hands-on experience required', 'Chicago', 'open'),
    (4, 'Financial Analyst', 'Analyze financial data and trends', 'Los Angeles', 'open'),
    (5, 'Manufacturing Technician', 'Hands-on experience required', 'Chicago', 'open'),
    (5, 'Financial Analyst', 'Analyze financial data and trends', 'Los Angeles', 'open'),
    (6, 'Manufacturing Technician', 'Hands-on experience required', 'Chicago', 'open'),
    (6, 'Financial Analyst', 'Analyze financial data and trends', 'Los Angeles', 'open'),
    (11, 'Software Engineer', 'Join our dynamic team!', 'New York', 'open'),
    (11, 'Product Manager', 'Lead innovative projects', 'San Francisco', 'open'),
    (12, 'Software Engineer', 'Join our dynamic team!', 'New York', 'open'),
    (12, 'Product Manager', 'Lead innovative projects', 'San Francisco', 'open'),
    (13, 'Software Engineer', 'Join our dynamic team!', 'New York', 'open'),
    (13, 'Product Manager', 'Lead innovative projects', 'San Francisco', 'open');


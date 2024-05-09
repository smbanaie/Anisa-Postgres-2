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

20. **List job seekers who have applied for a job in 'Engineering'  **

    
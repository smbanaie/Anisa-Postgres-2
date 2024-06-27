#### MV Performance check

- create `jobs` db and populate it.

- create this View and MV:

  ```sql
  -- Create a regular  view for job application counts per job seeker
  CREATE VIEW job_seeker_application_count_view AS
  SELECT
      j.seeker_id,
      u.username,
      COUNT(a.application_id) AS application_count
  FROM
      job_seekers j
  JOIN
      users u ON j.seeker_id = u.user_id
  LEFT JOIN
      applications a ON j.seeker_id = a.seeker_id
  GROUP BY
      j.seeker_id, u.username;
  
  -- Create an index on the regular view for faster queries !!!! Error
  CREATE INDEX idx_job_seeker_application_count_view ON job_seeker_application_count_view(seeker_id);
  
  -- Create a materialized view for job application counts per job seeker
  CREATE MATERIALIZED VIEW job_seeker_application_count AS
  SELECT
      j.seeker_id,
      u.username,
      COUNT(a.application_id) AS application_count
  FROM
      job_seekers j
  JOIN
      users u ON j.seeker_id = u.user_id
  LEFT JOIN
      applications a ON j.seeker_id = a.seeker_id
  GROUP BY
      j.seeker_id, u.username;
  
  -- Create an index on the materialized view for faster queries
  CREATE INDEX idx_job_seeker_application_count ON job_seeker_application_count(seeker_id);
  
  -- Refresh the materialized view to update the data
  REFRESH MATERIALIZED VIEW job_seeker_application_count;
  
  -- Query the materialized view for aggregate reports
  SELECT * FROM job_seeker_application_count;
  SELECT * FROM job_seeker_application_count_view;
  
  ```

  

- Enable timing in psql 

  ```bash
  \timing
  
  ```

  - run the above select queries :

    ```sql
    SELECT * FROM eeker_application_count_view;
    SELECT * FROM job_seeker_application_count;
    ```

- disable timing : `\timing`

- Check it Using the Explain/Analyze :

```sql

-- Query the regular view
EXPLAIN ANALYZE SELECT * FROM job_seeker_application_count_view;

-- Query the materialized view
EXPLAIN ANALYZE SELECT * FROM job_seeker_application_count;

-- Query the original SQL query
EXPLAIN ANALYZE
SELECT
    j.seeker_id,
    u.username,
    COUNT(a.application_id) AS application_count
FROM
    job_seekers j
JOIN
    users u ON j.seeker_id = u.user_id
LEFT JOIN
    applications a ON j.seeker_id = a.seeker_id
GROUP BY
    j.seeker_id, u.username;
```






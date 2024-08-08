import psycopg
import threading
import time
import random

# Database connection parameters
conn_params = "port=5434 dbname=jobs user=postgres password=postgres123"

# Function to execute queries
def execute_queries(queries):
    with psycopg.connect(conn_params) as conn:
        with conn.cursor() as cur:
            while True:
                for query in queries:
                    try:
                        cur.execute(query)
                        print(f"Executed query: {query}")
                        if 'SELECT' in query:
                            print(cur.fetchall())
                    except Exception as e:
                        print(f"Error executing query: {query}")
                        print(e)
                    time.sleep(random.uniform(0.5, 2.0))  # Simulate processing time

# Generate an array of 20 queries

queries = [
    # Simple queries
    "SELECT COUNT(*) FROM users;",
    "SELECT email, user_type FROM users LIMIT 10;",
    "SELECT location, COUNT(*) AS num_jobs FROM job_listings GROUP BY location;",

    # Queries with filters
    "SELECT title, description FROM job_listings WHERE location = 'New York';",
    "SELECT u.username, j.title, a.application_date "
    "FROM users u "
    "JOIN job_seekers js ON u.user_id = js.seeker_id "
    "JOIN applications a ON js.seeker_id = a.seeker_id "
    "JOIN job_listings j ON a.job_id = j.job_id "
    "WHERE u.user_type = 'job_seeker' AND a.status = 'pending';",

    # Queries with window functions
    "SELECT title, description, ROW_NUMBER() OVER (PARTITION BY employer_id ORDER BY posted_date DESC) AS row_num "
    "FROM job_listings;",
    "SELECT u.username, j.title, a.application_date, "
    "       RANK() OVER (PARTITION BY a.seeker_id ORDER BY a.application_date DESC) AS application_rank "
    "FROM users u "
    "JOIN job_seekers js ON u.user_id = js.seeker_id "
    "JOIN applications a ON js.seeker_id = a.seeker_id "
    "JOIN job_listings j ON a.job_id = j.job_id "
    "WHERE u.user_type = 'job_seeker';",

    # Queries with heavy joins
    "SELECT e.company_name, COUNT(l.job_id) AS num_listings, "
    "       DENSE_RANK() OVER (ORDER BY COUNT(l.job_id) DESC) AS company_rank "
    "FROM employers e "
    "LEFT JOIN job_listings l ON e.employer_id = l.employer_id "
    "GROUP BY e.company_name "
    "ORDER BY num_listings DESC "
    "LIMIT 10;",
    "SELECT j.title, COUNT(a.application_id) AS num_applications, "
    "       ROUND(AVG(CAST(EXTRACT(EPOCH FROM (NOW() - a.application_date)) / 86400 AS NUMERIC)), 2) AS avg_days_to_apply "
    "FROM job_listings j "
    "LEFT JOIN applications a ON j.job_id = a.job_id "
    "GROUP BY j.title "
    "ORDER BY num_applications DESC "
    "LIMIT 10;",

    # Additional queries
    "SELECT user_type, COUNT(*) AS count "
    "FROM users "
    "GROUP BY user_type;",
    "SELECT l.title, l.description, e.company_name "
    "FROM job_listings l "
    "JOIN employers e ON l.employer_id = e.employer_id "
    "WHERE l.status = 'open' "
    "ORDER BY l.posted_date DESC "
    "LIMIT 5;",
]

# Randomly shuffle the queries
random.shuffle(queries)

# Run the queries in 5 threads
threads = []
for _ in range(5):
    thread = threading.Thread(target=execute_queries, args=(queries,))
    thread.start()
    threads.append(thread)

# Run the code in an infinite loop
while True:
    # Wait for the threads to complete
    for thread in threads:
        thread.join()
    
    # Randomly shuffle the queries and start new threads
    random.shuffle(queries)
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=execute_queries, args=(queries,))
        thread.start()
        threads.append(thread)
import random
import json
from faker import Faker
import psycopg

# Initialize Faker
fake = Faker()

# Database connection parameters
conn_params = "dbname=postgres user=postgres password=postgres123"

# Function to insert fake data into the database
def populate_db():
    with psycopg.connect(conn_params) as conn:
        with conn.cursor() as cur:
            
            # Insert users
            for i in range(100):
                username = f"{fake.user_name()}_{i}"
                password = fake.password()
                email = fake.email()
                user_type = random.choice(['job_seeker', 'employer'])
                cur.execute(
                    "INSERT INTO users (username, password, email, user_type) VALUES (%s, %s, %s, %s)",
                    (username, password, email, user_type)
                )


            # Insert job_seekers and employers based on user_type
            cur.execute("SELECT user_id, user_type FROM users")
            users = cur.fetchall()
            for user_id, user_type in users:
                if user_type == 'job_seeker':
                    resume = json.dumps({'resume': fake.text()})
                    cur.execute(
                        "INSERT INTO job_seekers (seeker_id, resume) VALUES (%s, %s)",
                        (user_id, resume)
                    )
                else:
                    company_name = fake.company()
                    company_info = json.dumps({'description': fake.catch_phrase()})
                    cur.execute(
                        "INSERT INTO employers (employer_id, company_name, company_info) VALUES (%s, %s, %s)",
                        (user_id, company_name, company_info)
                    )

            # Insert job_listings
            cur.execute("SELECT employer_id FROM employers")
            employers = cur.fetchall()
            for _ in range(50):
                employer_id = random.choice(employers)[0]
                title = fake.job()
                description = fake.text()
                location = fake.city()
                cur.execute(
                    "INSERT INTO job_listings (employer_id, title, description, location) VALUES (%s, %s, %s, %s)",
                    (employer_id, title, description, location)
                )

            # Insert applications
            cur.execute("SELECT job_id FROM job_listings")
            job_ids = cur.fetchall()
            cur.execute("SELECT seeker_id FROM job_seekers")
            seeker_ids = cur.fetchall()
            for _ in range(200):
                job_id = random.choice(job_ids)[0]
                seeker_id = random.choice(seeker_ids)[0]
                cur.execute(
                    "INSERT INTO applications (job_id, seeker_id) VALUES (%s, %s)",
                    (job_id, seeker_id)
                )

            # Commit changes
            conn.commit()

# Run the function
if __name__ == "__main__":
    populate_db()

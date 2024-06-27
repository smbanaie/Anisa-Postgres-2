import random
import json
from faker import Faker
import psycopg

# Initialize Faker
fake = Faker()

# Database connection parameters
conn_params = "dbname=jobs user=postgres password=postgres123"

# Function to check if an email already exists
def email_exists(email, cur):
    cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
    return cur.fetchone()[0] > 0

# Function to check if a username already exists
def username_exists(username, cur):
    cur.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
    return cur.fetchone()[0] > 0

# Function to insert fake data into the database
def populate_db():
    with psycopg.connect(conn_params) as conn:
        with conn.cursor() as cur:

            # Insert users
            print("Inserting users...")
            for i in range(10000):
                username = fake.user_name()
                email = fake.email()

                # Check if the username and email already exist, generate new ones if needed
                while username_exists(username, cur) or email_exists(email, cur):
                    username = fake.user_name()
                    email = fake.email()

                password = fake.password()
                user_type = random.choice(['job_seeker', 'employer'])
                cur.execute(
                    "INSERT INTO users (username, password, email, user_type) VALUES (%s, %s, %s, %s)",
                    (username, password, email, user_type)
                )
                
                # Print progress
                if i % 1000 == 0:
                    print(f"{i} users inserted")

            # Insert job_seekers and employers based on user_type
            print("Inserting job_seekers and employers...")
            cur.execute("SELECT user_id, user_type FROM users")
            users = cur.fetchall()
            for i, (user_id, user_type) in enumerate(users):
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
                
                # Print progress
                if i % 1000 == 0:
                    print(f"{i} job_seekers and employers inserted")

            # Insert job_listings
            print("Inserting job_listings...")
            cur.execute("SELECT employer_id FROM employers")
            employers = cur.fetchall()
            for i in range(50000):
                employer_id = random.choice(employers)[0]
                title = fake.job()
                description = fake.text()
                location = fake.city()
                cur.execute(
                    "INSERT INTO job_listings (employer_id, title, description, location) VALUES (%s, %s, %s, %s)",
                    (employer_id, title, description, location)
                )

                # Print progress
                if i % 1000 == 0:
                    print(f"{i} job_listings inserted")

            # Insert applications
            print("Inserting applications...")
            cur.execute("SELECT job_id FROM job_listings")
            job_ids = cur.fetchall()
            cur.execute("SELECT seeker_id FROM job_seekers")
            seeker_ids = cur.fetchall()
            for i in range(20000):
                job_id = random.choice(job_ids)[0]
                seeker_id = random.choice(seeker_ids)[0]
                cur.execute(
                    "INSERT INTO applications (job_id, seeker_id) VALUES (%s, %s)",
                    (job_id, seeker_id)
                )

                # Print progress
                if i % 1000 == 0:
                    print(f"{i} applications inserted")

            # Commit changes
            conn.commit()

            print("Data population completed.")

# Run the function
if __name__ == "__main__":
    populate_db()

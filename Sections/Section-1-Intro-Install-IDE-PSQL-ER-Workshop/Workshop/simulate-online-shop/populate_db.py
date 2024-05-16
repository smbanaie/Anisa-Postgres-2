import psycopg
import random
import time
from faker import Faker
import threading
from datetime import datetime, timedelta


# Replace these values with your database connection details
db_connection_params = {
    'host': 'localhost',
    'dbname': 'sales',
    'user': 'postgres',
    'password': 'postgres123',
    'port': 5434
}

fake = Faker()

# Function to initialize the database with sample data
def initdb():
    try:
        conn = psycopg.connect(**db_connection_params)
        cursor = conn.cursor()

        # Insert products into the 'products' table
        for _ in range(20):
            product_name = fake.word()
            price = round(random.uniform(5.0, 100.0), 2)
            url = fake.url()
            cursor.execute(
                "INSERT INTO products (product_name, price, url) VALUES (%s, %s, %s)",
                (product_name, price, url)
            )

        # Insert customers into the 'customers' table
        for _ in range(50):
            customer_name = fake.name()
            email = fake.email()
            cursor.execute(
                "INSERT INTO customers (customer_name, email) VALUES (%s, %s)",
                (customer_name, email)
            )

        # Commit the changes
        conn.commit()
        print("Sample data inserted successfully.")

    except psycopg.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()

# Function to get a random product ID from the database
def get_random_product_id(cursor):
    cursor.execute("SELECT product_id FROM products ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    return result[0] if result else None

# Function to get a random customer ID from the database
def get_random_customer_id(cursor):
    cursor.execute("SELECT customer_id FROM customers ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    return result[0] if result else None

def get_random_timestamp():
    now = datetime.now()
    end_of_year = datetime(now.year, 12, 31, 23, 59, 59)
    random_time = now + timedelta(seconds=random.randint(0, int((end_of_year - now).total_seconds())))
    return random_time

# Function to simulate the online shop
def simulate_online_shop():
    try:
        conn = psycopg.connect(**db_connection_params)
        cursor = conn.cursor()

        while True:
            # Simulate random actions (insert/update/delete)
            action = random.choices(['insert', 'update', 'delete', 'view'], weights=[0.10, 0.05, 0.05, 0.8])[0]

            if action == 'insert':
                # Simulate a new order or a new customer with an order
                create_new_customer = random.choices([True, False], weights=[0.1, 0.9])[0]
                
                if create_new_customer:
                    # Create a new customer
                    customer_name = fake.name()
                    email = fake.email()
                    cursor.execute(
                        "INSERT INTO customers (customer_name, email) VALUES (%s, %s) RETURNING customer_id",
                        (customer_name, email)
                    )
                    customer_id = cursor.fetchone()[0]
                else:
                    # Use an existing customer
                    customer_id = get_random_customer_id(cursor)

                create_new_order = random.choices([True, False], weights=[0.2, 0.8])[0]

                if create_new_order:
                    # Create a new order
                    cursor.execute(
                        "INSERT INTO orders (customer_id) VALUES (%s) RETURNING order_id",
                        (customer_id,)
                    )
                    order_id = cursor.fetchone()[0]

                    # Add order details
                    for _ in range(random.randint(1, 5)):
                        product_id = get_random_product_id(cursor)
                        quantity = random.randint(1, 10)
                        cursor.execute(
                            "INSERT INTO order_details (order_id, product_id, quantity, total_price) "
                            "VALUES (%s, %s, %s, %s)",
                            (order_id, product_id, quantity, quantity * random.uniform(5.0, 50.0))
                        )

                    print(f"Inserted order: Customer {customer_id}, Order {order_id}")

            elif action == 'update':
                # Simulate updating order details (e.g., change quantity or total_price)
                product_id = get_random_product_id(cursor)
                cursor.execute(
                    "UPDATE order_details SET quantity = %s, total_price = %s "
                    "WHERE order_detail_id = (SELECT order_detail_id FROM order_details ORDER BY RANDOM() LIMIT 1)",
                    (random.randint(1, 10), random.uniform(5.0, 50.0))
                )

                print(f"Updated order details: Product {product_id}")

            elif action == 'delete':
                # Simulate deleting order details
                cursor.execute(
                    "DELETE FROM order_details WHERE order_detail_id = (SELECT order_detail_id FROM order_details ORDER BY RANDOM() LIMIT 1)"
                )

                print("Deleted order details")

            elif action == 'view':
                # Simulate a product view
                customer_id = get_random_customer_id(cursor) if random.random() < 0.5 else None
                original_product_id = get_random_product_id(cursor) if random.random() < 0.3 else None
                viewed_product_id = get_random_product_id(cursor)
                view_timestamp = get_random_timestamp()
                cursor.execute(
                    "INSERT INTO product_views (customer_id, original_product_id, viewed_product_id, view_timestamp) VALUES (%s, %s, %s, %s)",
                    (customer_id, original_product_id, viewed_product_id, view_timestamp)
                )

                print(f"Inserted product view: Customer {customer_id}, Original Product {original_product_id}, Viewed Product {viewed_product_id}")

            # Commit the changes
            conn.commit()

            # Pause for 1 second before the next iteration
            time.sleep(0.0001)

    except psycopg.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()

# Function to run multiple threads
def run_threads():
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=simulate_online_shop)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Run the initdb function to populate the database with sample data
initdb()

# Uncomment the line below if you want to run the simulation
run_threads()

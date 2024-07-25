import psycopg2
import random
import time
from faker import Faker

# Replace these values with your database connection details
db_connection_params = {
    'host': 'localhost',
    'database': 'shopping',
    'user': 'postgres',
    'password': 'postgres123',
    'port': 5434
}

fake = Faker()

# Function to initialize the database with sample data
def initdb():
    try:
        conn = psycopg2.connect(**db_connection_params)
        cursor = conn.cursor()

        # Insert products into the 'products' table
        for _ in range(20):
            product_name = fake.word()
            price = round(random.uniform(5.0, 100.0), 2)
            cursor.execute(
                "INSERT INTO products (product_name, price) VALUES (%s, %s)",
                (product_name, price)
            )

        # Insert customers into the 'customers' table
        for _ in range(50):
            customer_name = fake.name()
            email = fake.email()
            cursor.execute(
                "INSERT INTO customers (customer_name, email) VALUES (%s, %s)",
                (customer_name, email)
            )

        # Insert orders into the 'orders' table
        for customer_id in range(1, 51):
            cursor.execute(
                "INSERT INTO orders (customer_id) VALUES (%s) RETURNING order_id",
                (customer_id,)
            )
            order_id = cursor.fetchone()[0]

            # Insert order details for each order
            for _ in range(random.randint(1, 5)):
                product_id = get_random_product_id(cursor)
                quantity = random.randint(1, 10)

                cursor.execute(
                    "INSERT INTO order_details (order_id, product_id, quantity, total_price) "
                    "VALUES (%s, %s, %s, %s)",
                    (order_id, product_id, quantity, quantity * random.uniform(5.0, 50.0))
                )

        # Commit the changes
        conn.commit()
        print("Sample data inserted successfully.")

    except psycopg2.Error as e:
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

# Function to simulate the online shop
# ... (Previous code)

# Function to simulate the online shop
def simulate_online_shop():
    try:
        conn = psycopg2.connect(**db_connection_params)
        cursor = conn.cursor()

        while True:
            # Simulate random actions (insert/update/delete)
            action = random.choices(['insert', 'update', 'delete'], weights=[0.6, 0.2, 0.2])[0]


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

            # Commit the changes
            conn.commit()

            # Pause for 1 second before the next iteration
            time.sleep(0.001)

    except psycopg2.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()


# Run the initdb function to populate the database with sample data
initdb()

# Uncomment the line below if you want to run the simulation
simulate_online_shop()

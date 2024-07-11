import json
import psycopg2

# Replace these values with your database connection details
db_connection_params = {
    'host': 'localhost',
    'database': 'cbd_store',
    'user': 'postgres',
    'password': 'postgres123',
    'port' : 5434
}

# Read data from 'products_cleaned.txt'
with open('products.txt', 'r') as file:
    data = json.load(file)

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(**db_connection_params)
    cursor = conn.cursor()

    # Iterate through products and insert into the 'products' table
    for hit in data['hits']:
        product_id = hit['_source']['product_id']
        product_name = hit['_source']['product']
        seo_desc = hit['_source']['seo_desc']
        category = hit['_source']['category']

        # Inserting data into the 'products' table
        cursor.execute(
            "INSERT INTO products (product_id, product_name, seo_desc, category) VALUES (%s, %s, %s, %s)",
            (product_id, product_name, seo_desc, category)
        )

    # Commit the changes
    conn.commit()
    print("Data inserted successfully.")

except psycopg2.Error as e:
    print(f"Error: {e}")

finally:
    # Close the database connection
    if conn:
        conn.close()

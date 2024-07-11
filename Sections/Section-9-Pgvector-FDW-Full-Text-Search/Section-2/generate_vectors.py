import json
import psycopg2
from gpt4all import GPT4All, Embed4All


# Replace these values with your database connection details
db_connection_params = {
    'host': 'localhost',
    'database': 'cbd_store',
    'user': 'postgres',
    'password': 'postgres123',
    'port' : 5434
}

try:
    conn = psycopg2.connect(**db_connection_params)
    cursor = conn.cursor()

    # Fetch all products
    cursor.execute("SELECT product_id, seo_desc FROM products")
    products = cursor.fetchall()

    # Initialize Embed4All
    embedder = Embed4All()

    # Update the table with vector embeddings
    for product_id, seo_desc in products:
        pgvector_desc = embedder.embed(seo_desc)

        # Update the pgvector_desc column in the products table
        cursor.execute("UPDATE products SET pgvector_desc = %s WHERE product_id = %s", (pgvector_desc, product_id))

    # Commit the changes
    conn.commit()
    print("Vector embeddings updated successfully.")

except psycopg2.Error as e:
    print(f"Error: {e}")

finally:
    # Close the database connection
    if conn:
        conn.close()

import psycopg2
from gpt4all import GPT4All, Embed4All

db_connection_params = {
    'host': 'localhost',
    'database': 'cbd_store',
    'user': 'postgres',
    'password': 'postgres123',
    'port': 5434
}

try:
    conn = psycopg2.connect(**db_connection_params)
    cursor = conn.cursor()

    # Ensure the vector extension is installed
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Create the products table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR PRIMARY KEY,
            product_name TEXT,
            seo_desc TEXT,
            category TEXT,
            pgvector_desc vector(384)
        );
    """)

    # Insert some sample data
    sample_products = [
        ("1", "CBD Oil", "High-quality CBD oil for relaxation", "Oils"),
        ("2", "CBD Gummies", "Tasty CBD gummies for sleep aid", "Edibles"),
        ("3", "CBD Cream", "Soothing CBD cream for pain relief", "Topicals")
    ]
    cursor.executemany("""
        INSERT INTO products (product_id, product_name, seo_desc, category)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING;
    """, sample_products)

    # Create embeddings and update the table
    embedder = Embed4All()
    for product in sample_products:
        pgvector_desc = embedder.embed(product[2])  # Embed the seo_desc
        cursor.execute("""
            UPDATE products 
            SET pgvector_desc = %s 
            WHERE product_id = %s
        """, (pgvector_desc, product[0]))

    # Perform a similarity search
    query = "sleep disorders"
    query_vector = embedder.embed(query)
    cursor.execute("""
        SELECT product_id, product_name, seo_desc, pgvector_desc <-> %s AS distance
        FROM products
        ORDER BY distance
        LIMIT 2
    """, (query_vector,))
    similar_products = cursor.fetchall()

    print(f"Products most similar to '{query}':")
    for product in similar_products:
        print(f"Product ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Distance: {product[3]}")

    conn.commit()

except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
        
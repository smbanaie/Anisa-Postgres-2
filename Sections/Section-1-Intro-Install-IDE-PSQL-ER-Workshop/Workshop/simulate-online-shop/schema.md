### Db Schema

```sql

-- Create a sequence for view_id with a cache capacity of 50
CREATE SEQUENCE view_id_seq
    CACHE 50;


-- Table for Products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    url VARCHAR(255) NOT NULL
);

-- Table for Customers
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Table for Orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Order Details
CREATE TABLE order_details (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) NOT NULL,
    product_id INT REFERENCES products(product_id) NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL
);

  
   
-- Modify the url_views table to use the sequence for view_id
CREATE TABLE product_views (
    view_id INTEGER NOT NULL DEFAULT nextval('view_id_seq'),
    view_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_id INT REFERENCES customers(customer_id) NULL,
    original_product_id INT REFERENCES products(product_id) NULL,
    viewed_product_id INT REFERENCES products(product_id) NOT NULL,
    PRIMARY KEY (view_id)
) ;
```



### Create & Populate the DB

```sql
create database shopping; 
-- Table for Products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
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

```

- run `populate_db.py`

#### Monitor Database using pgAdmin dashboard

- refer to the official [docs](https://www.pgadmin.org/docs/pgadmin4/latest/tabbed_browser.html).

- visualize the Explain command :

  ```sql
  SELECT 
      p.product_id,
      p.product_name,
      SUM(od.quantity) AS total_quantity
  FROM 
      orders o
  JOIN 
      order_details od ON o.order_id = od.order_id
  JOIN 
      products p ON od.product_id = p.product_id
  GROUP BY 
      p.product_id, p.product_name
  HAVING 
      SUM(od.quantity) >= 100;
  
  ```

  - click on the `E` button.

-  Disable the hash join and join rearrangement and do it again :

  ```sql
  -- Disable hash join and set the join_collapse_limit to 1 to disable join rearrangement
  SET enable_hashjoin = off;
  SET join_collapse_limit = 1;
  ```

  

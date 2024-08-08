#### LATERAL Join ?

```sql
-- Create the products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    options JSONB
);

-- Insert some sample data
INSERT INTO products (name, options)
VALUES
    ('Product A', '[{"name": "Color", "values": ["Red", "Blue"]}, {"name": "Size", "values": ["Small", "Medium", "Large"]}]'),
    ('Product B', '[{"name": "Material", "values": ["Leather", "Nylon"]}, {"name": "Weight", "values": ["Light", "Heavy"]}]'),
    ('Product C', '[{"name": "Flavor", "values": ["Vanilla", "Chocolate", "Strawberry"]}]');
    

SELECT
    p.id,
    p.name AS product_name,
    o.option->>'name' AS option_name,
    jsonb_array_elements(o.option->'values') AS option_value
FROM
    products p
CROSS JOIN LATERAL jsonb_array_elements(p.options) AS o(option);

```



### What is Lateral Join?

 Let’s delve into the details of **LATERAL joins** in PostgreSQL.

1. **Understanding LATERAL Joins:**

   - LATERAL joins are a powerful feature in PostgreSQL (and other relational databases like Oracle, DB2, and MS SQL) that allow you to reference columns from preceding parts of your query within subqueries.
   - The key idea is that LATERAL joins enable dynamic interaction between the primary query and subqueries, allowing you to perform more complex operations.

2. **Basic Concept:**

   - Imagine a SQL SELECT statement as a loop that processes each entry in a table. For example:

     ```sql
     SELECT whatever FROM tab;
     ```

     AI-generated code. Review and use carefully. [More info on FAQ](https://www.bing.com/new#faq).

   - In pseudo-code, this would look like:

     ```python
     for x in tab:
         # do whatever
     ```

     AI-generated code. Review and use carefully. [More info on FAQ](https://www.bing.com/new#faq).

   - But what if we need a “nested” loop? This is where LATERAL comes in handy.

3. **Example Scenario: Finding Top Products for Wishlists:**

   - Suppose we have two tables:

     - `t_product`: Contains product information (product ID, price, name).
     - `t_wishlist`: Contains wishlist data (wishlist ID, username, desired price).

   - Our goal is to find the top three products for each wishlist based on the desired price.

   - Here’s some sample data:

     ```sql
     CREATE TABLE t_product AS
     SELECT id AS product_id, id * 10 * random() AS price, 'product ' || id AS product
     FROM generate_series(1, 1000) AS id;
     
     CREATE TABLE t_wishlist (
         wishlist_id int,
         username text,
         desired_price numeric
     );
     
     INSERT INTO t_wishlist
     VALUES (1, 'hans', 450), (2, 'joe', 60), (3, 'jane', 1500);
     ```

     AI-generated code. Review and use carefully. [More info on FAQ](https://www.bing.com/new#faq).

4. **Using LATERAL Joins:**

   - To achieve our goal, we can use LATERAL joins to find the top three products for each wishlist.

   - The following query demonstrates this:

     ```sql
     SELECT w.wishlist_id, w.username, p.product_id, p.product, p.price
     FROM t_wishlist w
     CROSS JOIN LATERAL (
         SELECT product_id, product, price
         FROM t_product
         WHERE price <= w.desired_price
         ORDER BY price DESC
         LIMIT 3
     ) AS p;
     ```

     AI-generated code. Review and use carefully. [More info on FAQ](https://www.bing.com/new#faq).

   - In this query:

     - We use LATERAL to reference the `w.desired_price` column from the outer query within the subquery.
     - The subquery selects the top three products (based on price) for each wishlist.
     - The result includes wishlist ID, username, product ID, product name, and price.

5. **Summary:**

   - LATERAL joins allow subqueries to reference columns from preceding parts of the query.
   - They are useful for scenarios where you need to perform nested operations or dynamic calculations.
   - Remember that LATERAL joins can significantly enhance your query capabilities!



> LATERAL ->  Convert to a Pseudo Table having some Internal Relationships!
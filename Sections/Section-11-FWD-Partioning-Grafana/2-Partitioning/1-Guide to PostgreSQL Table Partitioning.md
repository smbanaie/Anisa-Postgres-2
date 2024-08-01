# [Guide to PostgreSQL Table Partitioning](https://medium.com/@rasiksuhail/guide-to-postgresql-table-partitioning-c0814b0fbd9b)

![img](https://miro.medium.com/v2/resize:fit:875/0*1RxKZgAtkD0PEk5X)

Photo by [Caspar Camille Rubin](https://unsplash.com/@casparrubin?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=medium&utm_medium=referral)

PostgreSQL is a powerful open-source relational database management system that offers various advanced features for managing large and complex datasets. One such feature is table partitioning, which allows you to divide a large table into smaller, more manageable pieces called partitions.

> This guide will explore the concept of table partitioning in PostgreSQL and discuss how it can be leveraged to improve query performance and manage data efficiently.

# What is Table Partitioning?

Table partitioning is a database design technique used to divide a large table into smaller, more manageable chunks called partitions. Each partition is essentially a separate table that stores a subset of the original data. This technique can significantly improve query performance and data management for large datasets.

Partitioning can be done based on one or more columns, such as a date column or a range of values. For example, you can partition a table based on the date of the records, where each partition represents data for a specific date range. When querying the data, PostgreSQL can quickly eliminate partitions that are not relevant to the query, resulting in faster query execution.

# Benefits of Table Partitioning

1. **Improved Query Performance**: Partitioning allows the database to quickly narrow down the data to a specific partition, reducing the amount of data that needs to be scanned during queries. This results in faster query execution times, especially for large datasets.
2. **Easier Data Management**: With table partitioning, you can easily manage large datasets by splitting them into smaller, more manageable partitions. This can simplify tasks such as data archiving, data purging, and backup and restore operations.
3. **Enhanced Data Loading and Indexing**: When loading data into a partitioned table, the process can be parallelized, leading to faster data ingestion. Additionally, indexes on partitioned tables can be more efficient, as they only need to cover a smaller subset of data.
4. **Cost-Effective Storage**: Partitioning allows you to store older or less frequently accessed data on cheaper storage media, while keeping frequently accessed data on faster storage devices.

# Partitioning Methods in PostgreSQL

PostgreSQL offers various partitioning methods, including:

- Range Partitioning
- List Partitioning
- Hash Partitioning

> Lets look at each partitioning methods

# Range Partitioning

Range partitioning is a type of table partitioning where data is divided into partitions based on a specified range of values in a column. This is particularly useful when dealing with time-series data or any data that has a natural order. Each partition represents a distinct range of values, and data falling within that range is stored in that partition. Range partitioning allows for efficient retrieval of data within specific ranges, leading to improved query performance.

Let’s consider an example of a sales table with the following structure:

```
CREATE TABLE sales (
    sale_id SERIAL,
    sale_date DATE,
    product_id INT,
    quantity INT,
    amount NUMERIC,
    PRIMARY KEY (sale_id, sale_date)
) partition by range (sale_date);

```

> The `sale_date` column is used as the partition key, so it needs to be included in the PRIMARY KEY constraint. To fix this, you should include `sale_date` in the PRIMARY KEY definition

To create a range-partitioned table for this sales data based on the sale_date column, we need to follow these steps:

**Create Partitions**

We’ll create individual tables to represent each partition, each covering a specific range of dates. For demonstration purposes, we’ll create three partitions: “sales_january,” “sales_february,” and “sales_march.”

```
CREATE TABLE sales_january PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE sales_february PARTITION OF sales
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

CREATE TABLE sales_march PARTITION OF sales
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');
```

**Set Up Constraints**

We need to define constraints on each partition to ensure that data is correctly routed to the appropriate partition. In this example, we will use CHECK constraints on the sale_date column for each partition:

```
ALTER TABLE sales_january ADD CONSTRAINT sales_january_check
    CHECK (sale_date >= '2024-01-01' AND sale_date < '2024-02-01');

ALTER TABLE sales_february ADD CONSTRAINT sales_february_check
    CHECK (sale_date >= '2024-02-01' AND sale_date < '2024-03-01');

ALTER TABLE sales_march ADD CONSTRAINT sales_march_check
    CHECK (sale_date >= '2024-03-01' AND sale_date < '2024-04-01');
```

**Insert Data into Partitions**

Now, we can insert data into the sales table, and PostgreSQL will automatically route the data to the appropriate partition based on the sale_date:

```
INSERT INTO sales (sale_date, product_id, quantity, amount)
VALUES ('2024-01-15', 101, 5, 100.00);

INSERT INTO sales (sale_date, product_id, quantity, amount)
VALUES ('2024-02-20', 102, 10, 200.00);

INSERT INTO sales (sale_date, product_id, quantity, amount)
VALUES ('2024-03-10', 103, 8, 150.00);
```

**Querying Data from Partitions**

When querying data, PostgreSQL will automatically access only the relevant partitions based on the WHERE clause.

```
-- Retrieve sales data for January
SELECT * FROM sales WHERE sale_date >= '2024-01-01' AND sale_date < '2024-02-01';

-- Retrieve sales data for February
SELECT * FROM sales WHERE sale_date >= '2024-02-01' AND sale_date < '2024-03-01';

-- Retrieve sales data for March
SELECT * FROM sales WHERE sale_date >= '2024-03-01' AND sale_date < '2024-04-01';
```

These queries will only access the appropriate partitions, resulting in improved query performance.

```sql
explain SELECT * FROM sales WHERE sale_date >= '2024-01-01' AND sale_date < '2024-02-01';

explain SELECT * FROM sales WHERE sale_date >= '2024-01-01' AND sale_date < '2024-03-01';

```



# List Partitioning in PostgreSQL

List partitioning is another type of table partitioning in PostgreSQL, where data is divided into partitions based on specific values in a column. Unlike range partitioning, which uses a range of values, list partitioning allows you to define specific values for each partition. This partitioning technique is useful when data can be categorized into distinct, non-overlapping sets.

Let’s consider an example of a products table with the following structure:

```
CREATE TABLE products (
    product_id SERIAL,
    category TEXT,
    product_name TEXT,
    price NUMERIC,
    PRIMARY KEY (product_id, category)
) partition by list(category);

```

To create a list-partitioned table for this products data based on the category column, we need to follow these steps:

**Create Partitions**

We’ll create individual tables to represent each partition, with each partition covering a specific category of products. For demonstration purposes, we’ll create three partitions: “electronics,” “clothing,” and “furniture.”

```
CREATE TABLE electronics PARTITION OF products
    FOR VALUES IN ('Electronics');

CREATE TABLE clothing PARTITION OF products
    FOR VALUES IN ('Clothing');

CREATE TABLE furniture PARTITION OF products
    FOR VALUES IN ('Furniture');
```

**Set Up Constraints**

Since list partitioning is based on specific values, we don’t need CHECK constraints. However, we need to set up the partitions correctly by adding rows to the appropriate tables.

**Insert Data into Partitions**

Now, we can insert data into the products table, and PostgreSQL will automatically route the data to the appropriate partition based on the category.

```
INSERT INTO products (category, product_name, price)
VALUES ('Electronics', 'Smartphone', 500.00);

INSERT INTO products (category, product_name, price)
VALUES ('Clothing', 'T-Shirt', 25.00);

INSERT INTO products (category, product_name, price)
VALUES ('Furniture', 'Sofa', 800.00);
```

**Querying Data from Partitions**

When querying data, PostgreSQL will automatically access only the relevant partition based on the WHERE clause.

```
-- Retrieve electronics products
SELECT * FROM products WHERE category = 'Electronics';

-- Retrieve clothing products
SELECT * FROM products WHERE category = 'Clothing';

-- Retrieve furniture products
SELECT * FROM products WHERE category = 'Furniture';
```

List partitioning in PostgreSQL is a valuable technique for managing and querying data based on specific values in a column. By dividing data into partitions based on categories or other distinct sets, list partitioning allows for faster data retrieval and improved data management

```sql
explain SELECT * FROM products WHERE category = 'Electronics';
```



# Hash Partitioning in PostgreSQL

Hash partitioning is a type of table partitioning in PostgreSQL, where data is divided into partitions based on the hash value of a specified column. Unlike range or list partitioning, which uses specific values or ranges, hash partitioning uses a hash function to distribute data uniformly across partitions. This partitioning technique is useful when you want to evenly distribute data across partitions to achieve load balancing.

Let’s consider an example of an orders table with the following structure:

```
CREATE TABLE orders (
    order_id SERIAL,
    order_date DATE,
    customer_id INT,
    total_amount numeric,
    PRIMARY KEY (order_id, customer_id)
) partition by hash(customer_id);
```

To create a hash-partitioned table for this orders data based on the customer_id column, we need to follow these steps:

**Create Partitions**

We’ll create individual tables to represent each partition, with each partition covering a specific range of hash values. For demonstration purposes, let’s create three partitions.

```
CREATE TABLE orders_1 PARTITION OF orders
    FOR VALUES WITH (MODULUS 3, REMAINDER 0);

CREATE TABLE orders_2 PARTITION OF orders
    FOR VALUES WITH (MODULUS 3, REMAINDER 1);

CREATE TABLE orders_3 PARTITION OF orders
    FOR VALUES WITH (MODULUS 3, REMAINDER 2);
```

In this example, we use the `HASH()` function to specify that the data should be partitioned based on the hash value of the `customer_id` column. We use `MODULUS` and `REMAINDER` to specify the number of partitions (3 in this case) and the remainder value for each partition.

**Insert Data into Partitions**

Now, we can insert data into the orders table, and PostgreSQL will automatically route the data to the appropriate partition based on the hash value of the `customer_id`:

```
INSERT INTO orders (order_date, customer_id, total_amount)
VALUES ('2024-01-15', 101, 500.00);

INSERT INTO orders (order_date, customer_id, total_amount)
VALUES ('2024-02-20', 102, 600.00);

INSERT INTO orders (order_date, customer_id, total_amount)
VALUES ('2024-03-10', 103, 700.00);
```

**Querying Data from Partitions**

When querying data, PostgreSQL will automatically access the appropriate partition based on the hash value of the `customer_id`.

```
-- Retrieve orders for customer_id 101
SELECT * FROM orders WHERE customer_id = 101;

-- Retrieve orders for customer_id 102
SELECT * FROM orders WHERE customer_id = 102;

-- Retrieve orders for customer_id 103
SELECT * FROM orders WHERE customer_id = 103;
```

Hash partitioning in PostgreSQL is a useful technique for distributing data evenly across partitions based on the hash value of a specified column. By leveraging hash functions to uniformly distribute data, hash partitioning achieves load balancing and improves query performance.

> Partition makes querying faster.

PostgreSQL table partitioning is a powerful feature that can significantly enhance the performance and management of large datasets. By dividing data into smaller partitions, you can optimize query performance, simplify data management, and achieve more efficient data loading and indexing. When designing a partitioning strategy, consider your data and query patterns to choose the most appropriate partitioning method. With the right implementation, table partitioning can be a game-changer for handling massive amounts of data in PostgreSQL.



### Other Samples 

**List Partitioning by Customer Country:**

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name TEXT,
    country TEXT
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE,
    customer_id INT,
    total_amount NUMERIC
) PARTITION BY LIST (country);

CREATE TABLE orders_usa PARTITION OF orders
    FOR VALUES IN ('USA');

CREATE TABLE orders_uk PARTITION OF orders
    FOR VALUES IN ('UK');
```

Here, the `orders` table is partitioned based on the `country` column. Separate partitions are created for orders from the USA and the UK.

**Integer Range Partitioning:**

```sql
CREATE TABLE logs (
    log_id SERIAL PRIMARY KEY,
    log_date DATE,
    user_id INT,
    action TEXT
) PARTITION BY RANGE (user_id);

CREATE TABLE logs_low PARTITION OF logs
    FOR VALUES FROM (1) TO (1000);

CREATE TABLE logs_medium PARTITION OF logs
    FOR VALUES FROM (1001) TO (5000);

CREATE TABLE logs_high PARTITION OF logs
    FOR VALUES FROM (5001) TO (10000);
```

Here, the `logs` table is partitioned based on the `user_id`, and partitions are created for different ranges of user IDs.



### Attach/Detach Partitions 

#### Detach

```sql
ALTER TABLE orders DETACH PARTITION orders_3;
```

- `select * from orders`
- `select * from orders_3`

#### Attach Again

```sql
ALTER TABLE orders ATTACH PARTITION orders_3 FOR VALUES WITH (MODULUS 3, REMAINDER 2);
```



**Start Partitioning !**






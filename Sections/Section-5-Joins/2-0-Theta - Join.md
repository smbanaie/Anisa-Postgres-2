### Group by Rollup

 The `GROUP BY ROLLUP` clause is used to generate subtotals and grand totals for the groups specified in the `GROUP BY` clause. Here's a sample query using `GROUP BY ROLLUP` with hypothetical tables representing sales data:

```sql
CREATE TABLE products (
    product_id INT,
    category VARCHAR(50),
    product_name VARCHAR(50)
);

CREATE TABLE sales (
    sale_id INT,
    product_id INT,
    sale_date DATE,
    quantity INT
);

INSERT INTO products VALUES
(1, 'Electronics', 'Laptop'),
(2, 'Electronics', 'Smartphone'),
(3, 'Clothing', 'T-Shirt'),
(4, 'Clothing', 'Jeans');

INSERT INTO sales VALUES
(101, 1, '2023-07-05', 5),
(102, 2, '2023-07-05', 8),
(103, 3, '2023-07-06', 10),
(104, 4, '2023-07-06', 7),
(105, 1, '2023-07-10', 3),
(106, 2, '2023-07-10', 6);

-- Sample query using GROUP BY ROLLUP
SELECT
    products.category,
    products.product_name,
    SUM(sales.quantity) AS total_quantity
FROM
    sales
JOIN
    products ON sales.product_id = products.product_id
GROUP BY ROLLUP (products.category, products.product_name);
```

This query calculates the total quantity of products sold, providing subtotals for each category and a grand total for all products. The result might look like this:

```sql
+--------------+----------------+-------------------+
| category     | product_name   | total_quantity    |
+--------------+----------------+-------------------+
| Clothing     | Jeans          | 7                 |
| Clothing     | T-Shirt        | 10                |
| Clothing     | null           | 17                |
| Electronics  | Laptop         | 8                 |
| Electronics  | Smartphone     | 14                |
| Electronics  | null           | 22                |
| null         | null           | 39                |
+--------------+----------------+-------------------+
```

In this example, the result includes subtotals for each category and a grand total for all products. The `null` values in the `category` and `product_name` columns represent the grand total.

### Handling Nulls

You can use the `COALESCE` function to replace the `null` values with more descriptive labels. Here's an updated version of the query:

```sql
-- Sample query using GROUP BY ROLLUP with COALESCE
SELECT
    COALESCE(products.category, 'Total') AS category,
    COALESCE(products.product_name, 'Total') AS product_name,
    SUM(sales.quantity) AS total_quantity
FROM
    sales
JOIN
    products ON sales.product_id = products.product_id
GROUP BY ROLLUP (products.category, products.product_name);
```

Now, the result will have more descriptive labels in place of `null`:

```sql
+--------------+----------------+-------------------+
| category     | product_name   | total_quantity    |
+--------------+----------------+-------------------+
| Clothing     | Jeans          | 7                 |
| Clothing     | T-Shirt        | 10                |
| Clothing     | Total          | 17                |
| Electronics  | Laptop         | 8                 |
| Electronics  | Smartphone     | 14                |
| Electronics  | Total          | 22                |
| Total        | Total          | 39                |
+--------------+----------------+-------------------+
```

Now, instead of `null`, the labels 'Total' are used for both category and product_name in the appropriate places.

### Theta Join

Sample "advertising_campaigns" table:

```sql
CREATE TABLE advertising_campaigns (
    campaign_id INT,
    campaign_name VARCHAR(50),
    start_date DATE,
    end_date DATE
);

INSERT INTO advertising_campaigns VALUES
(1, 'Summer Sale', '2023-07-01', '2023-07-15'),
(2, 'Holiday Promo', '2023-12-10', '2023-12-25');
```

Sample "orders" table:

```sql
CREATE TABLE orders (
    order_id INT,
    date DATE
);

INSERT INTO orders VALUES
(101, '2023-07-05'),
(102, '2023-07-12'),
(103, '2023-12-15'),
(104, '2023-12-20'),
(105, '2024-01-02');
```

Now, let's run the query:

```sql
SELECT
    COALESCE(campaign_name, 'No Campaign') AS campaign_or_no_campaign,
    SUM(order_count) AS total_orders
FROM
    (SELECT
        CASE
            WHEN orders.date BETWEEN advertising_campaigns.start_date AND advertising_campaigns.end_date THEN 'Campaign'
            ELSE 'No Campaign'
        END AS campaign_name,
        COUNT(orders.order_id) AS order_count
    FROM
        orders
    LEFT JOIN
        advertising_campaigns ON orders.date BETWEEN advertising_campaigns.start_date AND advertising_campaigns.end_date
    WHERE
        orders.date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
    GROUP BY
        campaign_name) AS joined_data
GROUP BY
    campaign_or_no_campaign;
```

Resultant table:

```
+-------------------------+--------------+
| campaign_or_no_campaign | total_orders |
+-------------------------+--------------+
| Campaign                | 2            |
| No Campaign             | 1            |
+-------------------------+--------------+
```

In this example, the "Summer Sale" campaign had two orders, the "Holiday Promo" had one order, and there was one order with no associated campaign within the last month.



### Campaign Names

```sql
SELECT
    campaign_name,
    SUM(order_count) AS total_orders
FROM
    (SELECT
        COALESCE(advertising_campaigns.campaign_name, 'No Campaign') AS campaign_name,
        COUNT(orders.order_id) AS order_count
    FROM
        orders
    LEFT JOIN
        advertising_campaigns ON orders.date BETWEEN advertising_campaigns.start_date AND advertising_campaigns.end_date
    WHERE
        orders.date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
    GROUP BY
        campaign_name) AS joined_data
GROUP BY
    campaign_name;
```

Now, the result will include the campaign names:

```bash
+--------------+--------------+
| campaign_name| total_orders |
+--------------+--------------+
| Summer Sale  | 2            |
| Holiday Promo| 1            |
| No Campaign  | 1            |
+--------------+--------------+
```

This way, you can see the campaign names along with the total number of orders for each campaign and non-campaign days within the last month.



### Average Daily Orders

To compare the average daily orders for each campaign (including the "No Campaign"), you can modify the query as follows:

```sql
SELECT
    campaign_name,
    total_orders,
    duration_in_days,
    total_orders / duration_in_days AS avg_daily_orders
FROM
    (SELECT
        COALESCE(advertising_campaigns.campaign_name, 'No Campaign') AS campaign_name,
        COUNT(orders.order_id) AS total_orders,
        MAX(advertising_campaigns.end_date - advertising_campaigns.start_date + 1) AS duration_in_days
    FROM
        orders
    LEFT JOIN
        advertising_campaigns ON orders.date BETWEEN advertising_campaigns.start_date AND advertising_campaigns.end_date
    WHERE
        orders.date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
    GROUP BY
        campaign_name) AS joined_data;

```




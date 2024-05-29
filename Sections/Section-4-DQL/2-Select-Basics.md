## DQL with Northwind database

---

1. **Retrieve all columns from the "Customers" table:**
   
   ```sql
   SELECT * FROM customers;
   ```
   
   **Question :**  I need to bring the city at first . how can I shift the region to the end?
   
2. **Show only the "customer_id" and "company_name" columns from the "Customers" table:**

   ```sql
   SELECT customer_id, company_name FROM customers;
   ```

3. **List all products from the "Products" table with a price greater than $20:**
   ```sql
   SELECT * FROM products WHERE unit_price > 20;
   ```

4. **Display orders from the "Orders" table placed by the customer with ID 'ALFKI':**
   ```sql
   SELECT * FROM orders WHERE customer_id = 'ALFKI';
   ```

5. **Retrieve employees from the "Employees" table hired after the year 1995:**
   ```sql
   SELECT * FROM employees WHERE hire_date > '1995-01-01';
   ```

6. **Show all categories from the "Categories" table ordered alphabetically by category name:**
   ```sql
   SELECT * FROM categories ORDER BY category_name;
   ```

7. **List products with a quantity in stock less than 10 from the "Products" table:**
   ```sql
   SELECT * FROM products WHERE units_in_stock < 10;
   ```

8. **Display customers from the "Customers" table located in the USA or Canada:**
   ```sql
   SELECT * FROM customers WHERE country IN ('USA', 'Canada');
   ```

9. **Show orders from the "Orders" table where the order date is after '1996-01-01' and shipped to Germany:**

   ```sql
   SELECT * FROM orders WHERE order_date > '1996-01-01' AND ship_country = 'Germany';
   ```

10. **Retrieve employees from the "Employees" table born between 1960 and 1970:**
    ```sql
    SELECT * FROM employees WHERE birth_date BETWEEN '1960-01-01' AND '1970-12-31';
    ```



### Using `IN` Operator:


1. **List orders from the "Orders" table placed by specific customers:**
   
   ```sql
   SELECT * FROM orders WHERE customer_id IN ('ALFKI', 'BLONP', 'CHOPS');
   ```
   
2. **Display customers from the "Customers" table located in either France, Germany, or Spain:**
   
   ```sql
   SELECT * FROM customers WHERE country IN ('France', 'Germany', 'Spain');
   ```
3. **Retrieve products from the "Products" table in specific categories:** ('Beverages', 'Confections')
   
   ```sql
   ?
   ```

### Handling `NULL` Values:

4. **Retrieve Suppliers with unknown fax number:**
   
   ```sql
   SELECT * FROM suppliers
   WHERE ?
   ```
   
5. **List employees from the "Employees" table with no assigned territories :**
   
   ```sql
   SELECT * FROM employees WHERE employee_id NOT IN (SELECT employee_id FROM employee_territories);
   ```
   
6. **Display customers from the "Customers" table with no specified region (NULL in "Region"):**
   
   ```sql
   SELECT * FROM customers WHERE region IS NULL;
   ```

These examples provide practical scenarios for using the `IN` operator to filter results based on a list of values and handling `NULL` values in different columns.



### Using `IS NULL`:

1. **Retrieve products from the "Products" table where the "discontinued" is 1 (indicating discontinuation):**
   ```sql
   SELECT * FROM products WHERE discontinued = 1;
   ```

2. **List employees from the "Employees" table with no supervisor assigned (NULL in "reports_to"):**
   ```sql
   SELECT * FROM employees WHERE reports_to IS NULL;
   ```

3. **Display orders from the "Orders" table with no shipped date recorded (NULL in "shipped_date"):**
   ```sql
   SELECT * FROM orders WHERE shipped_date IS NULL;
   ```

### Using `IS NOT NULL`:

4. **Retrieve products from the "Products" table where the "unit_price" is specified (not NULL):**
   ```sql
   SELECT * FROM products WHERE unit_price IS NOT NULL;
   ```

5. **List employees from the "Employees" table who are linked to territories (existing in "employee_territories" table):**
   ```sql
   SELECT * FROM employees WHERE employee_id IN (SELECT employee_id FROM employee_territories);
   ```

6. **Show customers from the "Customers" table with specified postal codes (not NULL in "postal_code"):**
   ```sql
   SELECT * FROM customers WHERE postal_code IS NOT NULL;
   ```

---

#### Order By

The `ORDER BY` clause in SQL is used to sort the result set of a query. You can use it in combination with the optional `ASC` (ascending) or `DESC` (descending) keywords to control the sorting order. Here's how you can use `ORDER BY` and sort by multiple fields:

### Sorting by a Single Field:

1. **Sort products from the "products" table by their unit price in ascending order:**
   ```sql
   SELECT * FROM products ORDER BY unit_price ASC;
   ```

2. **Sort employees from the "employees" table by their hire date in descending order:**
   ```sql
   SELECT * FROM employees ORDER BY hire_date DESC;
   ```

### Sorting by Multiple Fields:

3. **Sort orders from the "orders" table by customer ID in ascending order and then by order date in descending order:**
   
   ```sql
   SELECT * FROM orders 
   ORDER BY ?
   ```
   
4. **Sort customers from the "customers" table by country in ascending order and then by company name in ascending order:**
   
   ```sql
   SELECT * FROM customers 
   ORDER BY ?
   
   ```

### Combining ASC and DESC:

5. **Sort products from the "products" table by category ID in ascending order and then by unit price in descending order:**
   ```sql
   SELECT * FROM products ORDER BY 
   ?;
   ```
   
6. **Sort employees from the "employees" table by region in descending order and then by birth date in ascending order:**
   ```sql
   SELECT * FROM employees ORDER BY ?;
   ```

These examples demonstrate how to use `ORDER BY` to sort query results. The default order is ascending, but you can explicitly specify `ASC` for clarity. If you want descending order, use the `DESC` keyword. When sorting by multiple fields, the order specified for each field applies sequentially. 

### Handling NULL Values in `ORDER BY`:

Here are examples to illustrate how NULL values behave with `ORDER BY`:

1. **Sort customers from the "customers" table by the "region" in ascending order where NULL values appear last **
   
   ```sql
   SELECT * FROM customers
   ORDER BY region asc ;
   ```
   
2. **Sort employees from the "employees" table by the "reports_to" in descending order, where NULL values appear first:**
   
   ```sql
   SELECT * FROM employees ORDER BY reports_to desc;
   ```
   
3. **Sort orders from the "orders" table by "ship_postal_code" in ascending order, where NULL values appear first:**
   
   ```sql
   SELECT * FROM orders ORDER BY ship_postal_code desc;
   ```

### Changing NULL Value Behavior in Sorting:

```sql
-- Sort products by "unit_price" in ascending order, where NULL values appear last
SELECT * FROM products ORDER BY unit_price ASC NULLS LAST;
```

```sql
-- Sort employees by "reports_to" in descending order, where NULL values appear first
SELECT * FROM employees ORDER BY reports_to NULLS FIRST;
```

These clauses help you explicitly control the placement of NULL values in the sorting order. 

### Pagination with `LIMIT`, `OFFSET`, and `FETCH`:

#### Using `LIMIT`:

1. **Retrieve the first 5 products from the "products" table:**
   ```sql
   SELECT * FROM products LIMIT 5;
   ```

2. **Get the top 10 orders from the "orders" table, ordered by order date:**
   ```sql
   SELECT * FROM orders ORDER BY order_date LIMIT 10;
   ```

#### Using `OFFSET`:

3. **Retrieve the next 5 products from the "products" table (skipping the first 5):**
   ```sql
   SELECT * FROM products OFFSET 5 LIMIT 5;
   ```

4. **Get orders 11 to 20 from the "orders" table, ordered by order date:**
   ```sql
   SELECT * FROM orders 
   ORDER BY order_date 
   ?
   ```

#### Using `FETCH` with `OFFSET`:

5. **Fetch the next 5 products starting from the 6th product in the "products" table:**
   ```sql
   SELECT * FROM products 
   OFFSET 5 FETCH NEXT 5 ROWS ONLY;
   ```
   
6. **Fetch orders 6 to 15 from the "orders" table, ordered by order date:**
   ```sql
   SELECT * 
   FROM orders 
   ORDER BY order_date 
   OFFSET 5 FETCH NEXT 10 ROWS ONLY;
   ```

These examples demonstrate how to use `LIMIT`, `OFFSET`, and `FETCH` for result pagination. Keep in mind that the availability of these clauses might vary between different database systems, and the syntax may differ slightly.

---

#### Aggregate functions

Aggregate functions in SQL perform a calculation on a set of values and return a single value. These functions are often used with the `GROUP BY` clause to perform operations on groups of rows. Here are some common aggregate functions and how to use them:

### 1. **COUNT:**
   - Counts the number of rows in a group.

```sql
   -- Count the number of products in each category
   SELECT category_id, COUNT(*) AS "ProductCount" FROM products GROUP BY category_id;
```

**Question** : Which city has the most customers? which country ? 

### 2. **SUM:**

   - Calculates the sum of values in a numeric column.

   ```sql
   -- Calculate the total units in stock for each category
   SELECT category_id, SUM(units_in_stock) AS "TotalUnitsInStock" FROM products GROUP BY category_id;
   ```

### 3. **AVG:**
   - Calculates the average value of a numeric column.

   ```sql
   -- Calculate the average unit price for each category
   SELECT category_id, AVG(unit_price) AS "AverageUnitPrice" FROM products GROUP BY category_id;
   ```

### 4. **MIN and MAX:**
   - Find the minimum and maximum values in a column.

   ```sql
   -- Find the minimum and maximum unit price for each category
   SELECT category_id, MIN(unit_price) AS "MinUnitPrice", MAX(unit_price) AS "MaxUnitPrice" FROM products GROUP BY category_id;
   ```

**Question** : we need the Category Name .

### 5. **GROUP_CONCAT (STRING_AGG in PostgreSQL):**

   - Concatenates values from multiple rows into a single string.

   ```sql
   -- Concatenate product names for each category
   SELECT category_id, STRING_AGG(product_name, ', ') AS "ProductNames"
   FROM products 
   GROUP BY category_id;
   ```

**Question :**  which category has the most products? 

### 6. **HAVING:**

   - Filters groups based on a condition.

   ```sql
   -- Find categories with an average unit price greater than 50
   SELECT category_id, AVG(unit_price) AS "AverageUnitPrice" 
   FROM products 
   GROUP BY category_id 
   HAVING AVG(unit_price) > 50;
   ```

These examples demonstrate the use of common aggregate functions in SQL. Remember to use `GROUP BY` when applying aggregate functions to group rows based on a specific column or columns. The `HAVING` clause is used to filter the groups based on aggregate conditions. The actual available functions and syntax might vary slightly depending on the database system you are using.



---

### Advanced SQL Query Examples

#### 1. **Count and Categorize Products by Category:**
   - Count the number of products in each category and categorize them as "Low," "Medium," or "High" based on the count.

   ```sql
   SELECT
       category_id,
       COUNT(*) AS ProductCount,
       CASE
           WHEN COUNT(*) < 10 THEN 'Low'
           WHEN COUNT(*) >= 10 AND COUNT(*) < 50 THEN 'Medium'
           ELSE 'High'
       END AS CategorySize
   FROM products
   GROUP BY category_id;
   ```

#### 2. **Average Unit Price Range by Category:**
   - Find the average unit price for each category and categorize them as "Affordable," (<20) "Moderate," (20 < price <50) or "Expensive."

   ```sql
   ?
   ```

#### 3. **Product Availability Status:**
   - Determine the availability status of products based on the sum of units in stock.
     - 0 -> 'Out of Stock'
     - 0-50 ->  'Low Stock'
     - else : 'In Stock'


   ```sql
   ?
   ```

#### 4. **Weighted Average Unit Price by Category:**
   - Calculate the weighted average unit price for each category based on the quantity in stock.

   ```sql
   SELECT
       category_id,
       SUM(unit_price * units_in_stock) / NULLIF(SUM(units_in_stock), 0) AS WeightedAverageUnitPrice
   FROM products
   GROUP BY category_id;
   ```

#### 5. **Conditional Count of High Price Products:**
   - Count products in each category, considering only those with a unit price greater than $20.

   ```sql
   SELECT
       category_id,
       COUNT(CASE WHEN unit_price > 20 THEN 1 END) AS HighPriceProductCount
   FROM products
   GROUP BY category_id;
   ```

#### 6. **Dynamic Category Size Based on Total Units in Stock:**
   - Categorize the categories dynamically based on the total units in stock.

   ```sql
   SELECT
       category_id,
       SUM(units_in_stock) AS TotalUnitsInStock,
       CASE
           WHEN SUM(units_in_stock) < 100 THEN 'Small'
           WHEN SUM(units_in_stock) >= 100 AND SUM(units_in_stock) < 500 THEN 'Medium'
           ELSE 'Large'
       END AS CategorySize
   FROM products
   GROUP BY category_id;
   ```

#### 7. **Average Unit Price for Stocked Products:**
   - Calculate the average unit price for each category, considering only products with more than 10 units in stock.

   ```sql
   select 
      count(
   	case when ship_country = 'USA' then 1 end
   	) as "USA",
   	 count(
   	case when ship_country = 'Canada' then 1 end
   	) as "Canada",
   	 count(
   	case when ship_country = 'France' then 1 end
   	) as "France",
   	 count(
   	case when ship_country = 'Germany' then 1 end
   	) as "Germany"
   from orders o
   ;
   ```

8. I need to count the orders of (France,USA, Canada, Germany), the out put has this structure :

| USA  | Canada | France | Germany |
| ---- | ------ | ------ | ------- |
| 122  | 30     | 77     | 122     |

? 

How Can I add Year to this table ? 

| Year | USA  | Canada | France | Germany |
| ---- | ---- | ------ | ------ | ------- |
| 1996 | 23   | 4      | 15     | 24      |
| 1997 | ...  |        |        |         |



### Advanced SQL Exercises

---

**Monthly Order Analysis Using TO_CHAR Function:**
```sql
SELECT
    TO_CHAR(order_date, 'Month') AS "MonthName",
    COUNT(*) AS "OrderCount"
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 1997
GROUP BY TO_CHAR(order_date, 'Month')
ORDER BY MIN(order_date);
```

In this query:
- `TO_CHAR(order_date, 'Month')` converts the "order_date" to the full month name.
- The query calculates the count of orders for each month in 1997.

---

**Using Conditional Aggregations in SQL:**

### 1. **SUM with Conditional Filtering:**
   ```sql
   -- Sum the "Freight" column for orders with "Freight" greater than 100
   SELECT SUM(CASE WHEN freight > 100 THEN freight ELSE 0 END) AS "SumHighFreight"
   FROM orders;
   ```

### 2. **COUNT with Conditional Filtering:**
   ```sql
   -- Count the number of products with "UnitsInStock" less than 20
   SELECT COUNT(CASE WHEN units_in_stock < 20 THEN 1 END) AS "LowStockProductCount"
   FROM products;
   ```

### 3. **AVG with Conditional Filtering:**
   ```sql
   -- Calculate the average "UnitPrice" for discontinued products
   SELECT AVG(CASE WHEN discontinued = 1 THEN unit_price END) AS "AvgDiscontinuedPrice"
   FROM products;
   ```

### 4. **MAX with Conditional Filtering:**
   ```sql
   -- Find the maximum "Freight" for orders shipped to 'USA'
   SELECT MAX(CASE WHEN ship_country = 'USA' THEN freight END) AS "MaxFreightToUSA"
   FROM orders;
   ```

### 5. **MIN with Conditional Filtering:**
   ```sql
   -- Find the minimum "ReorderLevel" for products with "CategoryID" equal to 1
   SELECT MIN(CASE WHEN category_id = 1 THEN reorder_level END) AS "MinReorderLevelForCategory1"
   FROM products;
   ```

---

**Question** : how to change the category_id=1 -> 20 while the other remain the same as before.



### PostgreSQL Specific Aggregate Functions

### 1. **FILTER Clause:**
   ```sql
   -- Sum the "Freight" for orders with "ShipCountry" equal to 'Germany'
   SELECT SUM(freight) FILTER (WHERE ship_country = 'Germany') AS "SumFreightToGermany"
   FROM orders;
   ```

### 2. **DISTINCT Aggregate Functions:**
   ```sql
   -- Count the distinct "CustomerID" values in the "Orders" table
   SELECT COUNT(DISTINCT customer_id) AS "DistinctCustomerCount"
   FROM orders;
   ```

### 3. **ARRAY_AGG:**
   ```sql
   -- Aggregate "ProductName" values into an array for each "CategoryID"
   SELECT category_id, ARRAY_AGG(product_name) AS "ProductNames"
   FROM products
   GROUP BY category_id;
   ```

### 4. **STRING_AGG (PostgreSQL 14+):**
   ```sql
   -- Concatenate "ProductName" values into a comma-separated string for each "CategoryID"
   SELECT category_id, STRING_AGG(product_name, ', ') AS "ProductNames"
   FROM products
   GROUP BY category_id;
   ```

### 5. **PERCENTILE_CONT and PERCENTILE_DISC:**
   ```sql
   -- Calculate the median ("50%") of "UnitPrice" for each "CategoryID"
   SELECT category_id, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY unit_price) AS "MedianUnitPrice"
   FROM products
   GROUP BY category_id;
   ```

### 6. **JSON_AGG:**
   ```sql
   -- Aggregate "ProductName" values into a JSON array for each "CategoryID"
   SELECT category_id, JSON_AGG(product_name) AS "ProductNames"
   FROM products
   GROUP BY category_id;
   ```

These exercises are now aligned with your database schema and showcase advanced SQL techniques and PostgreSQL-specific functions.



### Group By / Having

### 1. **GROUP BY Clause:**
   - The `GROUP BY` clause is used to group rows that have the same values in specified columns.

   ```sql
   -- Count the number of orders for each customer
   SELECT customer_id, COUNT(*) AS OrderCount
   FROM orders
   GROUP BY customer_id;
   ```

   In this example, rows from the `orders` table are grouped by the `customer_id` column, and the count of orders for each customer is calculated.

### 2. **HAVING Clause:**
   - The `HAVING` clause is used to filter the results of a `GROUP BY` based on aggregate conditions.

   ```sql
   -- List customers who have placed more than 5 orders
   SELECT customer_id, COUNT(*) AS OrderCount
   FROM orders
   GROUP BY customer_id
   HAVING COUNT(*) > 5;
   ```

   In this example, the `HAVING` clause filters out customers who have placed fewer than 6 orders.

### 3. **Combining GROUP BY and HAVING:**
   - You can use both clauses together to group rows and filter groups based on aggregate conditions.

   ```sql
   -- List products with an average unit price greater than $50
   SELECT category_id, AVG(unit_price) AS AverageUnitPrice
   FROM products
   GROUP BY category_id
   HAVING AVG(unit_price) > 50;
   ```

   Here, products are grouped by the `category_id`, and only categories with an average unit price greater than $50 are included in the results.

### 4. **Multiple Grouping Columns:**
   - You can group by multiple columns to create more granular groups.

   ```sql
   -- Count the number of orders for each customer in each year
   SELECT customer_id, EXTRACT(YEAR FROM order_date) AS OrderYear, COUNT(*) AS OrderCount
   FROM orders
   GROUP BY customer_id, EXTRACT(YEAR FROM order_date);
   ```

   This query counts the number of orders for each customer in each year by using both `customer_id` and the extracted `OrderYear` as grouping columns.

### Advanced Examples with GROUP BY and HAVING:

### 1. **Revenue Analysis by Customer:**
   - Find customers who have placed orders with a total revenue greater than $10,000.

   ```sql
   SELECT customer_id, SUM(unit_price * quantity * (1 - discount)) AS TotalRevenue
   FROM orders
   JOIN order_details ON orders.order_id = order_details.order_id
   GROUP BY customer_id
   HAVING SUM(unit_price * quantity * (1 - discount)) > 10000;
   ```

### 2. **Product Sales Distribution:**
   - Identify products with total sales exceeding 100 units and having an average unit price higher than $50.

   ```sql
   SELECT product_id, COUNT(*) AS TotalSales, AVG(unit_price) AS AverageUnitPrice
   FROM order_details
   GROUP BY product_id
   HAVING COUNT(*) > 100 AND AVG(unit_price) > 50;
   ```

### 3. **Customer Order Frequency:**
   - Find customers who have placed more than 5 orders in a single day.

   ```sql
   ?
   ```

### 4. **Category Comparison:**
   - Compare categories based on the average unit price and exclude categories with fewer than 3 products.

   ```sql
   SELECT category_id, AVG(unit_price) AS AverageUnitPrice, COUNT(*) AS ProductCount
   FROM products
   GROUP BY category_id
   HAVING COUNT(*) >= 3;
   ```

### 5. **Employee Performance Analysis:**
   - Identify employees who have processed more than 50 orders.

   ```sql
   SELECT employee_id, COUNT(*) AS TotalOrders
   FROM orders
   GROUP BY employee_id
   HAVING COUNT(*) > 50;
   ```

These examples illustrate the use of `GROUP BY` to create groups and `HAVING` to filter those groups based on aggregate conditions. Remember that the `HAVING` clause is used after `GROUP BY` and is specifically for filtering groups, whereas the `WHERE` clause is used for filtering individual rows.

Let's explore a scenario involving the use of `GROUP BY`, `HAVING`, `NULL`, and `CASE WHEN` in combination. Consider a situation where you want to analyze orders based on the payment status and filter out those with a specific condition, such as orders with a NULL payment status. Here's an example:

### **Order Payment Status Analysis:**
Assuming you have an "orders" table with columns like "OrderID," "CustomerID," "OrderDate," "OrderAmount," and "PaymentStatus," where "PaymentStatus" can be either 'Paid', 'Pending', or NULL.

```sql
-- Count the number of orders for each payment status and include only those with NULL status
SELECT
    COALESCE("PaymentStatus", 'Not Specified') AS "PaymentStatus",
    COUNT(*) AS "OrderCount"
FROM orders
GROUP BY COALESCE("PaymentStatus", 'Not Specified')
HAVING COALESCE("PaymentStatus", 'Not Specified') = 'Not Specified' OR COUNT(*) > 5;
```

Explanation:
- The `COALESCE("PaymentStatus", 'Not Specified')` function is used to handle NULL values in the "PaymentStatus" column and replace them with 'Not Specified'.
- The `GROUP BY` clause groups the results based on the modified "PaymentStatus."
- The `HAVING` clause filters out groups where the count is not greater than 5 or where the payment status is 'Not Specified'.

This example demonstrates combining `GROUP BY` with `HAVING` to analyze order payment status, handling NULL values using `COALESCE`, and using `CASE WHEN` implicitly through `COALESCE`. Adjust the conditions and column names based on your actual data model and requirements.




#### View in Postgres 



### 1. Create a View
- **Objective**: Create a view that shows information about customers and their orders.
- **SQL**:
  ```sql
  CREATE VIEW customer_order_view AS
  SELECT
      c.CustomerID,
      c.CompanyName,
      o.OrderID,
      o.OrderDate,
      o.ShippedDate
  FROM
      Customers c
  JOIN Orders o ON c.CustomerID = o.CustomerID;
  ```

### 2. Create a Materialized View
- **Objective**: Create a materialized view that stores the total sales amount for each product.
- **SQL**:
  ```sql
  CREATE MATERIALIZED VIEW product_sales_mv AS
  SELECT
      p.ProductID,
      p.ProductName,
      SUM(od.Quantity * od.UnitPrice) AS total_sales
  FROM
      Products p
  JOIN OrderDetails od ON p.ProductID = od.ProductID
  GROUP BY
      p.ProductID, p.ProductName;
  ```

### 3. Refresh a Materialized View
- **Objective**: Refresh the materialized view to update the total sales amount.
- **SQL**:
  ```sql
  REFRESH MATERIALIZED VIEW product_sales_mv;
  ```

### 4. Create a View with Aggregation
- **Objective**: Create a view that shows the total sales amount for each customer.
- **SQL**:
  ```sql
  CREATE VIEW customer_total_sales_view AS
  SELECT
      c.CustomerID,
      c.CompanyName,
      SUM(od.Quantity * od.UnitPrice) AS total_sales
  FROM
      Customers c
  JOIN Orders o ON c.CustomerID = o.CustomerID
  JOIN OrderDetails od ON o.OrderID = od.OrderID
  GROUP BY
      c.CustomerID, c.CompanyName;
  ```

### 5. Concurrently Refresh a Materialized View
- **Objective**: Refresh the materialized view concurrently to allow concurrent reads during the refresh.
- **SQL**:
  ```sql
  REFRESH MATERIALIZED VIEW CONCURRENTLY product_sales_mv;
  ```

These examples demonstrate the creation of views and materialized views in PostgreSQL using the Northwind dataset. Additionally, it includes refreshing materialized views, both traditionally and concurrently, to keep the data up-to-date.
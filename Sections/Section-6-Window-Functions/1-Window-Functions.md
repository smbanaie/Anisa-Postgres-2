#### NOrthwind Dataset

### Basic SQL Window Function Exercises

#### Exercise 1: Numbering Rows in a Table
- **Objective**: Assign a unique row number to each order in the Orders table.
- **Skills**: ROW_NUMBER().
- **Query**:
  ```sql
  ?
  
  ```

#### Exercise 2: Ranking Products by Price
- **Objective**: Rank products by unit price in ascending order.
- **Skills**: RANK().
- **Query**:
  ```sql
  ?
  ```

#### Exercise 3: Dense Ranking of Employees by Hire Date
- **Objective**: Assign a dense rank to employees based on their hire date.
- **Skills**: DENSE_RANK().
- **Query**:
  ```sql
  ?
  ```

#### Exercise 4: Cumulative Total of Orders
- **Objective**: Calculate the cumulative total of orders over time.
- **Skills**: SUM().
- **Query**:
  ```sql
  ?
  ```

#### Exercise 5: Finding Previous Order Date for Each Order
- **Objective**: Find the previous order date for each order.
- **Skills**: LAG().
- **Query**:
  ```sql
  ?
  ```

#### Exercise 6: Calculating the Lead Time to the Next Order
- **Objective**: Calculate the number of days until the next order for each order.
- **Skills**: LEAD(), DATEDIFF().
- **Query**:
  ```sql
  ?
  ```

#### Exercise 7: Assigning a Running Total of Order Quantities
- **Objective**: Create a running total of order quantities.
- **Skills**: SUM().
- **Query**:
  ```sql
  ?
  ```

#### Exercise 8: Percentile Rank of Order Amounts
- **Objective**: Find the percentile rank of order amounts.
- **Skills**: PERCENT_RANK().
- **Query**:
  ```sql
  ?
  ```

#### Exercise 9: Average Price of All Products
- **Objective**: Calculate the average price of all products for comparison with each product.
- **Skills**: AVG().
- **Query**:
  ```sql
  ?
  ```

#### Exercise 10: Identifying the First Purchase Date in Orders
- **Objective**: Identify the first purchase date in the entire orders dataset.
- **Skills**: FIRST_VALUE().
- **Query**:
  ```sql
  ?
  ```

These exercises provide a practical understanding of basic window functions and their application in real-world scenarios, highlighting the differences and advantages over traditional `GROUP BY` approaches.





Certainly! Let's expand on Part 2 of the workshop, which focuses on Aggregate Window Functions in SQL. This section will provide a deeper understanding of these functions using the Northwind database. We'll include sample SQL codes and more exercises for practical learning.

### Deep Dive into Aggregate Window Functions (20 Minutes)

**Objective**: Understand and apply aggregate window functions like `SUM()`, `AVG()`, `COUNT()`, etc., in different scenarios using the Northwind database.



**1. Calculate Total Sales Per Order**  
Objective: Find the total price of items for each order without using `GROUP BY`.

```sql
?
```

**2. Average Product Price Per Category**  
Objective: Determine the average price of products within each category.

```sql
?
```

#### Exercises (10 Minutes)

**Exercise 1: Total Number of Products Sold Per Category**  
Participants write a query to count the total number of products sold per category.

```sql
?
```

**Exercise 2: Cumulative Sales Per Customer**  
Participants create a query to calculate the cumulative total of sales for each customer over time.

```sql
?
```

**Exercise 3: Average Order Size Per Employee**  
Write a query to find out the average order size handled by each employee.

```sql
?
```

Designing advanced SQL window function exercises using the Northwind database can be a great way to challenge and enhance your SQL skills. These exercises will incorporate joins, CASE WHEN statements, and other advanced SQL topics alongside window functions. Let's get into the details:

### Advanced SQL Window Function Exercises

#### Exercise 1: Year-over-Year Sales Growth by Category
- **Objective**: Calculate the year-over-year growth in sales for each product category.
- **Skills**: JOIN, DATE functions, CASE WHEN, LAG(), PARTITION BY.
- **Sample Query Structure**:
  ```sql
  SELECT a.CategoryID, a.Year, 
         SUM(a.TotalSales) OVER (PARTITION BY a.CategoryID ORDER BY a.Year) AS AnnualSales,
         LAG(SUM(a.TotalSales), 1) OVER (PARTITION BY a.CategoryID ORDER BY a.Year) AS PreviousYearSales,
         ((AnnualSales - PreviousYearSales) / PreviousYearSales) * 100 AS YoY_Growth
  FROM (SELECT DATEPART(year, OrderDate) AS Year, CategoryID, SUM(UnitPrice * Quantity) AS TotalSales
        FROM Orders
        JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
        JOIN Products ON OrderDetails.ProductID = Products.ProductID
        GROUP BY DATEPART(year, OrderDate), CategoryID) a;
  ```

#### Exercise 2: Rank Employees by Quarterly Sales
- **Objective**: Rank employees based on their total sales in each quarter.
- **Skills**: JOIN, DATE functions, SUM(), ROW_NUMBER().
- **Sample Query Structure**:
  ```sql
  SELECT EmployeeID, Quarter, TotalSales,
         ROW_NUMBER() OVER (PARTITION BY Quarter ORDER BY TotalSales DESC) AS SalesRank
  FROM (SELECT EmployeeID, DATEPART(quarter, OrderDate) AS Quarter,
               SUM(UnitPrice * Quantity) AS TotalSales
        FROM Orders
        JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
        GROUP BY EmployeeID, DATEPART(quarter, OrderDate)) a;
  ```

#### Exercise 3: Moving Average of Monthly Sales
- **Objective**: Calculate a 3-month moving average of sales for each product.
- **Skills**: JOIN, DATE functions, AVG(), OVER with frame specification.
- **Sample Query Structure**:
  ```sql
  SELECT ProductID, OrderMonth,
         AVG(TotalSales) OVER (PARTITION BY ProductID ORDER BY OrderMonth
                               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MovingAvgSales
  FROM (SELECT ProductID, FORMAT(OrderDate, 'yyyy-MM') AS OrderMonth,
               SUM(UnitPrice * Quantity) AS TotalSales
        FROM Orders
        JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
        GROUP BY ProductID, FORMAT(OrderDate, 'yyyy-MM')) a;
  ```

#### Exercise 4: Cumulative Quantity of Products Sold Over Time
- **Objective**: For each product, calculate the cumulative quantity sold over time.
- **Skills**: JOIN, SUM() with ORDER BY in OVER().
- **Sample Query Structure**:
  ```sql
  SELECT ProductID, OrderDate, Quantity,
         SUM(Quantity) OVER (PARTITION BY ProductID ORDER BY OrderDate) AS CumulativeQuantity
  FROM OrderDetails
  JOIN Orders ON OrderDetails.OrderID = Orders.OrderID;
  ```

#### Exercise 5: Percentage of Total Sales Per Customer
- **Objective**: Calculate the percentage of total sales for each customer.
- **Skills**: JOIN, SUM(), CASE WHEN, CTE (Common Table Expressions).
- **Sample Query Structure**:
  ```sql
  WITH TotalSales AS (
    SELECT CustomerID, SUM(UnitPrice * Quantity) AS CustomerTotal
    FROM Orders
    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
    GROUP BY CustomerID
  ),
  GrandTotal AS (
    SELECT SUM(CustomerTotal) AS Total FROM TotalSales
  )
  SELECT TotalSales.CustomerID, CustomerTotal,
         (CustomerTotal / GrandTotal.Total) * 100 AS SalesPercentage
  FROM TotalSales, GrandTotal;
  ```

#### Exercise 6: First and Last Purchase Date for Each Customer
- **Objective**: Identify the first and last purchase date for each customer.
- **Skills**: JOIN, FIRST_VALUE(), LAST_VALUE(), DISTINCT.
- **Sample Query Structure**:
  ```sql
  SELECT DISTINCT CustomerID,
         FIRST_VALUE(OrderDate) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS FirstPurchase,
         LAST_VALUE(OrderDate) OVER (PARTITION BY CustomerID ORDER BY OrderDate 
                                      ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS LastPurchase
  FROM Orders;
  ```

#### Exercise 7: Employee Ranking by Number of Orders Handled
- **Objective**: Rank employees based on the number of orders they have handled.
- **Skills**: COUNT(), DENSE
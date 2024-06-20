### Hands-On

### 1. Inner Join - Retrieve Customer Information with Orders
```sql
SELECT customers.customerid, customers.companyname, orders.orderid
FROM customers
INNER JOIN orders ON customers.customerid = orders.customerid;
```

### 2. Left Join - Retrieve Customers and Their Orders (Include Customers Without Orders)
```sql
SELECT customers.customerid, customers.companyname, orders.orderid
FROM customers
LEFT JOIN orders ON customers.customerid = orders.customerid;
```

### 3. Right Join - Retrieve Orders and Corresponding Customer Information (Include Orders Without Customers)
```sql
SELECT customers.customerid, customers.companyname, orders.orderid
FROM customers
RIGHT JOIN orders ON customers.customerid = orders.customerid;
```

### 4. Full Outer Join - Retrieve Customers and Orders (Include All Customers and Orders)
```sql
SELECT customers.customerid, customers.companyname, orders.orderid
FROM customers
FULL OUTER JOIN orders ON customers.customerid = orders.customerid;
```

### 5. Cross Join - Retrieve Cartesian Product of Customers and Employees
```sql
SELECT customers.customerid, customers.companyname, employees.employeeid, employees.firstname
FROM customers
CROSS JOIN employees;
```

### 6. Self Join - Retrieve Employees and Their Managers
```sql
SELECT e.employeeid, e.firstname, m.firstname AS manager
FROM employees e
LEFT JOIN employees m ON e.reportsto = m.employeeid;
```

### 7. Natural Join - Retrieve Orders with Matching Customers
```sql
SELECT *
FROM orders
NATURAL JOIN customers;
```

### 8. Theta Join - Retrieve Products with Prices Higher Than Average
```sql
SELECT products.productid, products.productname, products.unitprice
FROM products, (SELECT AVG(unitprice) AS avg_price FROM products) AS avg_table
WHERE products.unitprice > avg_table.avg_price;
```


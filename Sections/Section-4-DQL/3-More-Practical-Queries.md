### Some More DQL Samples

These queries include some more complex operations like `GROUP BY` and `CASE WHEN`.

11. **Average Price by Category**
    ```sql
    SELECT category_id, AVG(unit_price) AS average_price FROM products GROUP BY category_id;
    ```

12. **Count Customers by Country**
    ```sql
    SELECT country, COUNT(*) AS customer_count FROM customers GROUP BY country;
    ```

13. **Employee Title Count**
    ```sql
    SELECT title, COUNT(*) AS title_count FROM employees GROUP BY title;
    ```

14. **Product Stock Status**
    ```sql
    SELECT product_id, product_name,
           CASE 
               WHEN units_in_stock > units_on_order THEN 'In Stock'
               ELSE 'Out of Stock' 
           END AS stock_status
    FROM products;
    ```

15. **Customer Order Counts**
    ```sql
    SELECT customer_id, COUNT(*) AS order_count FROM orders GROUP BY customer_id;
    ```

16. **Total Freight by Country**
    ```sql
    SELECT ship_country, SUM(freight) AS total_freight FROM orders GROUP BY ship_country;
    ```

17. **Employees by Year of Birth**
    ```sql
    SELECT EXTRACT(YEAR FROM birth_date) AS birth_year, COUNT(*) AS employee_count FROM employees GROUP BY birth_year;
    ```

18. **Average Freight by Year, Month**
    
    ```sql
    ?
    ```
    
19. **Product Category Distribution**
    ```sql
    SELECT category_id, COUNT(*) AS product_count FROM products GROUP BY category_id;
    ```

20. **Suppliers by Region**
    ```sql
    SELECT region, COUNT(*) AS supplier_count FROM suppliers GROUP BY region;
    ```

### Advanced Queries
These queries are more complex and involve multiple advanced SQL features.

21. **Top 5 Expensive Products**
    ```sql
    SELECT product_id, product_name, unit_price 
    FROM products 
    ?
    ```

22. **Employee Tenure**

    ```sql
    ?
    ```

23. **Total Orders by Year**
    ```sql
    SELECT EXTRACT(YEAR FROM order_date) AS order_year, COUNT(*) AS total_orders 
    FROM orders 
    GROUP BY order_year;
    ```

24. **Employee Sales Performance**
    ```sql
    SELECT e.employee_id, e.first_name, e.last_name, 
           COUNT(o.order_id) AS total_sales 
    FROM employees e 
    JOIN orders o ON e.employee_id = o.employee_id 
    GROUP BY e.employee_id;
    
    ? Rewrite the Query with subqueries
    ```

25. **Customer Lifetime Value**
    ```sql
    SELECT customer_id, SUM(freight) AS total_spent 
    FROM orders 
    GROUP BY customer_id;
    ```

26. **Average Product Price by Category**
    ```sql
    SELECT c.category_name, AVG(p.unit_price) AS avg_price 
    FROM products p 
    JOIN categories c ON p.category_id = c.category_id 
    GROUP BY c.category_name;
    
    ? Rewrite the Query with subqueries
    ```

27. **Employee Age Group**

    < 30 :  'Under 30'

    <30 age < 50 : '30 to 50'

    \> 50 :  'Over 50'

    ```sql
    ?
    ```

28. **Customer Order Frequency**

    COUNT(*) > 5 -> 'Frequent' else Infrequent

    ```sql
    ?
    ```

29. **Top 10 Selling Products** 

    ```sql
    ? 
    ```

30. **Region-wise Employee Distribution**
    ```sql
    SELECT region, COUNT(*) AS employee_count 
    FROM employees 
    GROUP BY region;
    ```



31. **Products with Highest Discount**
    ```sql
    SELECT product_id, MAX(discount) AS max_discount 
    FROM order_details 
    GROUP BY product_id;
    ```

32. **Suppliers with Most Products**
    ```sql
    SELECT supplier_id, COUNT(*) AS product_count 
    FROM products 
    GROUP BY supplier_id 
    ORDER BY product_count DESC;
    ```

33. **Average Employee Age**
    ```sql
    SELECT AVG(AGE(birth_date)) AS average_age 
    FROM employees;
    ```

34. **Total Revenue by Product**
    ```sql
    SELECT product_id, SUM(unit_price * quantity * (1 - discount)) AS total_revenue 
    FROM order_details 
    GROUP BY product_id;
    ```

35. **Customers with Most Orders**
    ```sql
    SELECT customer_id, COUNT(*) AS order_count 
    FROM orders 
    GROUP BY customer_id 
    HAVING COUNT(*) > 5;
    ```

36. **Average Quantity Per Order**
    ```sql
    SELECT order_id, AVG(quantity) AS avg_quantity 
    FROM order_details 
    GROUP BY order_id;
    ```

37. **Product Availability**
    ```sql
    SELECT product_id, product_name, 
           CASE 
               WHEN units_in_stock - units_on_order > 0 THEN 'Available'
               ELSE 'Unavailable' 
           END AS availability 
    FROM products;
    ```

38. **Customer Region Analysis**
    ```sql
    SELECT region, COUNT(*) AS customer_count, AVG(LENGTH(company_name)) AS avg_name_length 
    FROM customers 
    GROUP BY region;
    ```

39. **Employees by Birth Month**
    ```sql
    SELECT EXTRACT(MONTH FROM birth_date) AS birth_month, COUNT(*) AS employee_count 
    FROM employees 
    GROUP BY birth_month;
    ```

40. **Product Price Range**
    ```sql
    SELECT category_id, 
           MIN(unit_price) AS min_price, 
           MAX(unit_price) AS max_price 
    FROM products 
    GROUP BY category_id;
    ```

41. **Order Volume by Month**
    ```sql
    SELECT EXTRACT(MONTH FROM order_date) AS order_month, SUM(quantity) AS total_volume 
    FROM orders 
    JOIN order_details ON orders.order_id = order_details.order_id 
    GROUP BY order_month;
    ```

42. **Discontinued Product Count**
    ```sql
    SELECT COUNT(*) AS discontinued_count 
    FROM products 
    WHERE discontinued = 1;
    ```

43. **Employees with Longest Tenure**
    ```sql
    SELECT first_name, last_name, 
           MAX(AGE(hire_date)) AS tenure 
    FROM employees 
    GROUP BY employee_id;
    ```

44. **Total Orders by Customer Type**
    ```sql
    SELECT cd.customer_type_id, COUNT(o.order_id) AS total_orders 
    FROM customer_demographics cd 
    JOIN customers c ON cd.customer_type_id = c.customer_id 
    JOIN orders o ON c.customer_id = o.customer_id 
    GROUP BY cd.customer_type_id;
    ```

45. **Supplier Contact Length Analysis**
    ```sql
    SELECT supplier_id, 
           AVG(LENGTH(contact_name) + LENGTH(contact_title)) AS avg_contact_length 
    FROM suppliers 
    GROUP BY supplier_id;
    ```

46. **Employees without Photo**
    ```sql
    SELECT employee_id, first_name, last_name 
    FROM employees 
    WHERE photo IS NULL;
    ```

47. **Customer Address Length**
    ```sql
    SELECT customer_id, 
           LENGTH(address) + LENGTH(city) + LENGTH(region) + LENGTH(postal_code) + LENGTH(country) AS address_length 
    FROM customers;
    ```

48. **Product Stock Value**
    ```sql
    SELECT product_id, product_name, units_in_stock * unit_price AS stock_value 
    FROM products;
    ```

49. **Customers Without Orders**
    ```sql
    SELECT c.customer_id, c.company_name 
    FROM customers c 
    LEFT JOIN orders o ON c.customer_id = o.customer_id 
    WHERE o.order_id IS NULL;
    ```

50. **Employee Age at Hiring**
    ```sql
    SELECT employee_id, first_name, last_name, AGE(hire_date, birth_date) AS age_at_hiring 
    FROM employees;
    ```

These queries cover a range of SQL features and functions, from basic data retrieval to more complex operations involving aggregate functions, conditional logic, and joining tables. They should provide a comprehensive practice experience for different levels of SQL proficiency.
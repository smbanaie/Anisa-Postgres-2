### Pagila Intro

Pagila is a sample database that represents a DVD rental store, and it's commonly used for learning and practicing SQL queries. Here are 20 queries ranging from simple to advanced, incorporating subqueries, CTEs, CASE WHEN, HAVING, GROUP BY, and the EXTRACT function. Note that I'm avoiding JOIN and window functions as requested:

### 1. Simple SELECT:

Retrieve the first 5 records from the "actor" table.

```sql
SELECT * FROM actor LIMIT 5;
```

### 2. Filter with WHERE:

Retrieve films released in the year 2006 from the "film" table.

```sql
SELECT * FROM film WHERE release_year = 2006;
```

### 3. Order by:

Retrieve the titles and release years of films, ordered by release year in descending order. Display only the top 10.

```sql
SELECT title, release_year FROM film ORDER BY release_year DESC LIMIT 10;
```

### 4. Aggregate with GROUP BY:

Count the number of films in each rating category from the "film" table.

```sql
?
```

### 5. Aggregate with HAVING:

Count the number of films in each category and display only those categories with more than 10 films.

```sql
?
```

### 6. Subquery in WHERE:

Retrieve customers who have made payments greater than $5, using the "customer" and "payment" tables.

```sql
?
```

### 7. Subquery in SELECT:

Show the first names of customers along with the count of rentals they have made, using the "customer" and "rental" tables.

```sql
?
```

### 8. CTE (Common Table Expression):

Create a CTE to select films with a rental rate greater than $4 and display the results.

```sql
?
```

### 9. CASE WHEN in SELECT:

Display film titles, rental rates, and categorize the rental rates as 'High,' 'Moderate,' or 'Low' using CASE WHEN.

```sql
?
```

### 10. Subquery with ANY:

Assume you want to find customers who have rented any film with a rental rate greater than 4. You can use the `ANY` operator for this:

```sql
?
```



### 11. Subquery in SELECT with MAX:

Display film titles, rental rates, and the maximum rental rate across all films.

```sql
?
```

### 12. CTE with Aggregate:

Use a CTE to find customers with more than 5 total rentals and display the results.

```sql
?
```

### 13. Nested CASE WHEN:

Display film titles and categorize rental rates as 'Expensive,' 'Moderate,' or 'Inexpensive' using nested CASE WHEN.

```sql
?
```

### 14. Subquery with ORDER BY and LIMIT:

Retrieve the customer IDs and payment amounts for payments greater than the average payment, ordered by amount in descending order, and limit to the top 10.

```sql
?
```

### 15. Group by and HAVING with COUNT:

Count the number of films in each category and display only those categories with more than 5 films.

```sql

```

### 16. Subquery with NOT IN:

Select films that are not present in the "inventory" table.

```sql
?
```

### 17. CTE with Multiple Levels:

Use a two-level CTE to select films with rental rates greater than 3 and then further filter those with rates greater than 4. the second one must use the first one and the final query, select data from the second one.

```sql
?
```

### 18. Subquery with Aggregate Function in WHERE:

Find customers with more than the average number of rentals and display the customer ID along with the total number of rentals.

```sql
?
```


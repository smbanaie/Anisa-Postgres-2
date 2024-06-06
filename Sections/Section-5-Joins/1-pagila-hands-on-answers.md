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
SELECT rating, COUNT(*) FROM film GROUP BY rating;
```

### 5. Aggregate with HAVING:

Count the number of films in each category and display only those categories with more than 10 films.

```sql
SELECT category_id, COUNT(*) FROM film GROUP BY category_id HAVING COUNT(*) > 10;
```

### 6. Subquery in WHERE:

Retrieve customers who have made payments greater than $5, using the "customer" and "payment" tables.

```sql
SELECT * FROM customer WHERE customer_id IN (SELECT customer_id FROM payment WHERE amount > 5);
```

### 7. Subquery in SELECT:

Show the first names of customers along with the count of rentals they have made, using the "customer" and "rental" tables.

```sql
SELECT first_name, (SELECT COUNT(*) FROM rental WHERE rental.customer_id = customer.customer_id) AS rental_count
FROM customer;
```

### 8. CTE (Common Table Expression):

Create a CTE to select films with a rental rate greater than $4 and display the results.

```sql
WITH high_revenue_films AS (
    SELECT film_id, title
    FROM film
    WHERE rental_rate > 4
)
SELECT * FROM high_revenue_films;
```

### 9. CASE WHEN in SELECT:

Display film titles, rental rates, and categorize the rental rates as 'High,' 'Moderate,' or 'Low' using CASE WHEN.

```sql
SELECT title, 
       rental_rate,
       CASE WHEN rental_rate > 4 THEN 'High' 
            WHEN rental_rate > 2 THEN 'Moderate' 
            ELSE 'Low' 
       END AS rental_category
FROM film;
```

### 10. Subquery with ANY:

Assume you want to find customers who have rented any film with a rental rate greater than 4. You can use the `ANY` operator for this:

```sql
SELECT customer_id, first_name, last_name
FROM customer
WHERE customer_id = ANY (
    SELECT DISTINCT customer_id
    FROM rental
    WHERE rental_id IN (
        SELECT rental_id
        FROM inventory
        WHERE film_id IN (
            SELECT film_id
            FROM film
            WHERE rental_rate > 4
        )
    )
);
```



### 11. Subquery in SELECT with MAX:

Display film titles, rental rates, and the maximum rental rate across all films.

```sql
SELECT title, 
       rental_rate,
       (SELECT MAX(rental_rate) FROM film) AS max_rental_rate
FROM film;
```

### 12. CTE with Aggregate:

Use a CTE to find customers with more than 5 total rentals and display the results.

```sql
WITH rental_counts AS (
    SELECT customer_id, COUNT(*) AS total_rentals
    FROM rental
    GROUP BY customer_id
)
SELECT customer_id, total_rentals
FROM rental_counts
WHERE total_rentals > 5;
```

### 13. Nested CASE WHEN:

Display film titles and categorize rental rates as 'Expensive,' 'Moderate,' or 'Inexpensive' using nested CASE WHEN.

```sql
SELECT title,
       CASE 
           WHEN rental_rate > 4 THEN 'Expensive'
           WHEN rental_rate > 2 THEN 'Moderate'
           ELSE 'Inexpensive'
       END AS rental_category
FROM film;
```

### 14. Subquery with ORDER BY and LIMIT:

Retrieve the customer IDs and payment amounts for payments greater than the average payment, ordered by amount in descending order, and limit to the top 10.

```sql
SELECT customer_id, amount
FROM payment
WHERE amount > (SELECT AVG(amount) FROM payment)
ORDER BY amount DESC
LIMIT 10;
```

### 15. Group by and HAVING with COUNT:

Count the number of films in each category and display only those categories with more than 5 films.

```sql
SELECT category_id, COUNT(*) AS film_count
FROM film, film_category
where film.film_id in( select film_id from film_category where film.film_id=film_category.film_id)
GROUP BY category_id
HAVING COUNT(*) > 5;
```

### 16. Subquery with NOT IN:

Select films that are not present in the "inventory" table.

```sql
SELECT title
FROM film
WHERE film_id NOT IN (SELECT film_id FROM inventory);
```

### 17. CTE with Multiple Levels:

Use a two-level CTE to select films with rental rates greater than 3 and then further filter those with rates greater than 4. the second one must use the first one and the final query, select data from the second one.

```sql
WITH top_films AS (
    SELECT film_id, title, rental_rate
    FROM film
    WHERE rental_rate > 3
)
, expensive_films AS (
    SELECT film_id, title
    FROM top_films
    WHERE rental_rate > 4
)
SELECT * FROM expensive_films;
```

### 18. Subquery with Aggregate Function in WHERE:

Find customers with more than the average number of rentals and display the customer ID along with the total number of rentals.

```sql
with customer_rental as 
(
SELECT customer_id, COUNT(*) AS total_rentals
FROM rental
GROUP BY customer_id
), customer_rental_avg as 
(
select 
	avg(total_rentals) as rental_avg
from
	customer_rental
)
select * 
from customer_rental
where 
total_rentals > (select rental_avg from  customer_rental_avg)


```


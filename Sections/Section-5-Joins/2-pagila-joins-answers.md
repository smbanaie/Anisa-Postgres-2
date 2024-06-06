### Easy Questions (1-10)

1. **List All Customers**
   - **Question:** Retrieve all details for every customer in the `customer` table.
   - **SQL Query:** 
     ```sql
     SELECT * FROM customer;
     ```

2. **Find Specific Customer Information**
   - **Question:** Display the first and last names of customers whose `customer_id` is less than 10.
   - **SQL Query:** 
     ```sql
     SELECT first_name, last_name FROM customer WHERE customer_id < 10;
     ```

3. **Count of Films in a Category**
   - **Question:** Find the total number of films in the 'Action' category.
   - **SQL Query:** 
     ```sql
     SELECT COUNT(*) FROM film 
     JOIN film_category ON film.film_id = film_category.film_id
     JOIN category ON film_category.category_id = category.category_id
     WHERE category.name = 'Action';
     ```

4. **List of Films with 'PG-13' Rating**
   - **Question:** Retrieve the titles of all films that have a 'PG-13' rating.
   - **SQL Query:** 
     ```sql
     SELECT title FROM film WHERE rating = 'PG-13';
     ```

5. **Inner Join Between Two Tables**
   - **Question:** Display the first and last names of actors and the titles of the films they have acted in.
   - **SQL Query:** 
     ```sql
     SELECT actor.first_name, actor.last_name, film.title
     FROM film_actor
     JOIN actor ON film_actor.actor_id = actor.actor_id
     JOIN film ON film_actor.film_id = film.film_id;
     ```

6. **Basic Left Join Usage**
   - **Question:** Find all customers and list their payment details, if any.
   - **SQL Query:** 
     ```sql
     SELECT customer.*, payment.amount
     FROM customer
     LEFT JOIN payment ON customer.customer_id = payment.customer_id;
     ```

7. **Simple Right Join**
   - **Question:** List all payments and include customer information even if the customer doesn't exist in the customer table.
   - **SQL Query:** 
     ```sql
     SELECT payment.*, customer.first_name, customer.last_name
     FROM payment
     RIGHT JOIN customer ON payment.customer_id = customer.customer_id;
     ```

8. **Display Actor Names with a Specific Film Title**
   - **Question:** Show the names of actors who acted in the film titled 'Academy Dinosaur'.
   - **SQL Query:** 
     ```sql
     SELECT actor.first_name, actor.last_name
     FROM film
     JOIN film_actor ON film.film_id = film_actor.film_id
     JOIN actor ON film_actor.actor_id = actor.actor_id
     WHERE film.title = 'Academy Dinosaur';
     ```

9. **List Inventory for a Specific Store**
   - **Question:** Retrieve all inventory items available at the store with `store_id` 1.
   - **SQL Query:** 
     ```sql
     SELECT * FROM inventory WHERE store_id = 1;
     ```

10. **Find Active Customers**
    - **Question:** Select all customers who are marked as active in the database.
    - **SQL Query:** 
      ```sql
      SELECT * FROM customer WHERE activebool = true;
      ```

### Medium Questions (11-20)

11. **Full Join on Customer and Payment**
    - **Question:** Perform a full join between the `customer` and `payment` tables and display the results, including customers who have not made any payments and payments that do not have a corresponding customer.
    - **SQL Query:** 
      ```sql
      SELECT customer.*, payment.*
      FROM customer
      FULL JOIN payment ON customer.customer_id = payment.customer_id;
      ```

12. **Natural Join Between Two Tables**
    - **Question:** Use a natural join to combine the `film` and `language` tables to display film titles along with the language they are in.
    - **SQL Query:** 
      ```sql
      SELECT film.title, language.name
      FROM film
      NATURAL JOIN language;
      ```

13. **Most Active Actors**
    
    - **Question:** Identify the Top 10 Most Active Actors in a Specific Film Category (Comedy). show their names and the title of films they acted in (use `string_agg`).  
    - **SQL Query:** 
      ```sql
      SELECT
          actor.actor_id,
          actor.first_name || ' ' || actor.last_name AS actor_name,
          string_agg(film.title, ', ') AS films_played
      FROM
          actor
      JOIN
          film_actor ON actor.actor_id = film_actor.actor_id
      JOIN
          film ON film_actor.film_id = film.film_id
      JOIN
          film_category ON film.film_id = film_category.film_id
      JOIN
          category ON film_category.category_id = category.category_id
      WHERE
          category.name = 'Comedy'
      GROUP BY
          actor.actor_id
      ORDER BY
          COUNT(film_actor.film_id) DESC
      LIMIT
          10;
      
      ```
    
14. **Self-join on Actor Table**
    - **Question:** Find pairs of actors who share the same last name using a self-join.
    - **SQL Query:** 
      ```sql
      SELECT a1.first_name AS actor1_first_name, a1.last_name AS actor1_last_name, 
             a2.first_name AS actor2_first_name, a2.last_name AS actor2_last_name
      FROM actor a1
      JOIN actor a2 ON a1.last_name = a2.last_name AND a1.actor_id != a2.actor_id;
      ```

15. **Multi-table Join**
    - **Question:** Combine `film`, `film_actor`, and `actor` tables to display film titles along with their actors' names.
    - **SQL Query:** 
      ```sql
      SELECT film.title, actor.first_name, actor.last_name
      FROM film
      JOIN film_actor ON film.film_id = film_actor.film_id
      JOIN actor ON film_actor.actor_id = actor.actor_id;
      ```

16. **Aggregation with Join**
    - **Question:** List each category and the average rental rate of films in that category.
    - **SQL Query:** 
      ```sql
      SELECT category.name, AVG(film.rental_rate) AS average_rental_rate
      FROM film
      JOIN film_category ON film.film_id = film_category.film_id
      JOIN category ON film_category.category_id = category.category_id
      GROUP BY category.name;
      ```

17. **Join with Subquery**
    - **Question:** Display the names of customers who have rented more than 5 films.
    - **SQL Query:** 
      ```sql
      SELECT customer.first_name, customer.last_name
      FROM customer
      JOIN (
          SELECT rental.customer_id, COUNT(rental.rental_id) AS rental_count
          FROM rental
          GROUP BY rental.customer_id
          HAVING COUNT(rental.rental_id) > 5
      ) AS subquery ON customer.customer_id = subquery.customer_id;
      ```

18. **Conditional Join**
    - **Question:** Show film titles and their actors only for films with a rental duration longer than 5 days.
    - **SQL Query:** 
      ```sql
      SELECT film.title, actor.first_name, actor.last_name
      FROM film
      JOIN film_actor ON film.film_id = film_actor.film_id
      JOIN actor ON film_actor.actor_id = actor.actor_id
       WHERE film.rental_duration > 5;
    

19. **Complex Join with ORDER BY and GROUP BY**
    
    - **Question:** List categories and the number of films in each category, ordered by the number of films descending.
    - **SQL Query:** 
      ```sql
      SELECT category.name, COUNT(film_category.film_id) AS film_count
      FROM category
      JOIN film_category ON category.category_id = film_category.category_id
      GROUP BY category.name
      ORDER BY film_count DESC;
      ```
    
20. **Join Involving a VIEW**
    - **Question:** Use the `film_list` view to display films and their actors, filtered to show only 'Drama' films.
    - **SQL Query:** 
      ```sql
      SELECT * FROM film_list WHERE category = 'Drama';
      ```

### Advanced Questions (21-30)

21. **Join with Multiple Conditions**
    - **Question:** Display customer names and their payments, joining on `customer_id`, but only for payments greater than $5.
    - **SQL Query:** 
      ```sql
      SELECT customer.first_name, customer.last_name, payment.amount
      FROM customer
      JOIN payment ON customer.customer_id = payment.customer_id
      WHERE payment.amount > 5;
      ```

22. **Join with Aggregate Functions and HAVING**
    - **Question:** List stores and their total sales, but only include stores with more than $15,000 in sales.
    - **SQL Query:** 
      ```sql
      SELECT store.store_id, SUM(payment.amount) AS total_sales
      FROM payment
      JOIN staff ON payment.staff_id = staff.staff_id
      JOIN store ON staff.store_id = store.store_id
      GROUP BY store.store_id
      HAVING SUM(payment.amount) > 15000;
      ```

23. **Nested Joins**
    - **Question:** Show film titles and their categories, along with the store ID where these films are available, using nested joins.
    - **SQL Query:** 
      ```sql
      SELECT film.title, category.name AS category, inventory.store_id
      FROM film
      JOIN film_category ON film.film_id = film_category.film_id
      JOIN category ON film_category.category_id = category.category_id
      JOIN inventory ON film.film_id = inventory.film_id;
      ```

24. **Recursive Query**
    - **Question:** Write a recursive query to display all categories and their sub-categories (if any). Assume a hypothetical self-referencing column in the `category` table for this scenario.
    - **SQL Query:** 
      ```sql
      WITH RECURSIVE subcategories AS (
          SELECT category_id, name, parent_category_id
          FROM category
          WHERE parent_category_id IS NULL
          UNION ALL
          SELECT c.category_id, c.name, c.parent_category_id
          FROM category c
          INNER JOIN subcategories sc ON sc.category_id = c.parent_category_id
      )
      SELECT * FROM subcategories;
      ```
      Note: This query assumes a column `parent_category_id` in the `category` table, which is not present in the actual Pagila schema.

25. **CTE with Join**
    
    - **Question:** Use a Common Table Expression (CTE) to list all films and the number of times they were rented.
    - **SQL Query:** 
      ```sql
      WITH film_rentals AS (
          SELECT film.film_id, COUNT(rental.rental_id) AS rental_count
          FROM film
          JOIN inventory ON film.film_id = inventory.film_id
          JOIN rental ON inventory.inventory_id = rental.inventory_id
          GROUP BY film.film_id
      )
      SELECT film.title, film_rentals.rental_count
      FROM film
      JOIN film_rentals ON film.film_id = film_rentals.film_id;
      ```
    
28. **Join Involving a Complex WHERE Clause**
    - **Question:** Display films that have never been rented.
    - **SQL Query:** 
      ```sql
      SELECT film.title
      FROM film
      LEFT JOIN inventory ON film.film_id = inventory.film_id
      LEFT JOIN rental ON inventory.inventory_id = rental.inventory_id
      WHERE rental.rental_id IS NULL;
      ```

29. **Join with UPDATE Statement**
    - **Question:** Write a query to update the `rental_rate` of films in the 'Comedy' category by 10%.
    - **SQL Query:** 
      ```sql
      UPDATE film
      SET rental_rate = rental_rate * 1.1
      FROM film_category
      JOIN category ON film_category.category_id = category.category_id
      WHERE film_category.film_id = film.film_id AND category.name = 'Comedy';
      ```

30. **Analytical Query Using Joins**
    - **Question:** Analyze the average rental duration for films by rating and category.
    - **SQL Query:** 
      ```sql
      SELECT film.rating, category.name AS category, AVG(film.rental_duration) AS avg_rental_duration
      FROM film
      JOIN film_category ON film.film_id = film_category.film_id
      JOIN category ON film_category.category_id = category.category_id
      GROUP BY film.rating, category.name;
      ```

These questions and queries cover a wide range of SQL concepts and should provide a comprehensive learning experience using the Pagila dataset.
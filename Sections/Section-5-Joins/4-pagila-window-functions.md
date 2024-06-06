#### Window Functions - A Quick Intro

 Window functions in SQL are powerful tools for performing complex data analytics, and they can be quite nuanced. Let's start with the basics and gradually progress to more advanced concepts using the Pagila database. I'll structure the learning in stages, starting with the simplest use of window functions and gradually introducing more complexity.

### Stage 1: Basic Window Functions using `OVER()`

1. **Simple Row Numbering**
   - **Objective:** Number the rows in a table.
   - **Query:**
     ```sql
     SELECT actor_id, first_name, last_name, ROW_NUMBER() OVER() AS row_num
     FROM actor;
     ```
   - **Explanation:** This query assigns a unique row number to each actor in the `actor` table.

2. **Cumulative Sum**
   - **Objective:** Calculate a running total of film lengths.
   - **Query:**
     ```sql
     SELECT film_id, title, length, SUM(length) OVER() AS running_total_length
     FROM film;
     ```
   - **Explanation:** This query calculates a cumulative sum of film lengths in the `film` table.

### Stage 2: Introduction to `PARTITION BY`

3. **Partitioned Row Number**
   - **Objective:** Assign row numbers within partitions of a category.
   - **Query:**
     ```sql
     SELECT category_id, film_id, ROW_NUMBER() OVER(PARTITION BY category_id) AS row_num
     FROM film_category;
     ```
   - **Explanation:** This query assigns row numbers to films within each category separately.

4. **Cumulative Sum Within Partitions**
   - **Objective:** Calculate a running total within each category.
   - **Query:**
     ```sql
     SELECT category_id, film_id, length, SUM(length) OVER(PARTITION BY category_id) AS running_total_length
     FROM film
     JOIN film_category USING(film_id);
     ```
   - **Explanation:** Calculates a cumulative sum of film lengths, but resets the sum for each category.

### Stage 3: Using `ORDER BY` with Window Functions

5. **Ordered Row Numbering**
   - **Objective:** Assign row numbers based on a specific order.
   - **Query:**
     ```sql
     SELECT film_id, title, rental_rate, ROW_NUMBER() OVER(ORDER BY rental_rate DESC) AS row_num
     FROM film;
     ```
   - **Explanation:** Numbers the films based on their rental rate in descending order.

6. **Running Average**
   - **Objective:** Calculate the running average of rental rates.
   - **Query:**
     ```sql
     SELECT film_id, title, rental_rate, AVG(rental_rate) OVER(ORDER BY rental_rate) AS running_avg_rental_rate
     FROM film;
     ```
   - **Explanation:** Computes the cumulative average of the rental rates, ordered by rental rate.

### Stage 4: Advanced Window Functions

7. **Partitioned Ranking**
   - **Objective:** Rank films within each rating category based on their length.
   - **Query:**
     ```sql
     SELECT film_id, title, rating, length, RANK() OVER(PARTITION BY rating ORDER BY length DESC) AS rank_in_rating
     FROM film;
     ```
   - **Explanation:** Ranks films by length within each rating category.

8. **Moving Average**
   - **Objective:** Calculate a 3-film moving average of lengths.
   - **Query:**
     ```sql
     SELECT film_id, title, length, AVG(length) OVER(ORDER BY length ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_length
     FROM film;
     ```
   - **Explanation:** Calculates a moving average that includes the current film, one preceding, and one following film, based on length.

9. **First Value in Partition**
   - **Objective:** Identify the first film's title in each category based on alphabetical order.
   - **Query:**
     ```sql
     SELECT category_id, film_id, title, FIRST_VALUE(title) OVER(PARTITION BY category_id ORDER BY title) AS first_film_in_category
     FROM film
     JOIN film_category USING(film_id);
     ```
   - **Explanation:** For each category, this query identifies the first film title when ordered alphabetically.

10. **N-Tile Distribution**
    - **Objective:** Divide films into 4 quartiles based on length.
    - **Query:**
      ```sql
      SELECT film_id, title, length, NTILE(4) OVER(ORDER BY length) AS quartile
      FROM film;
      ```
    - **Explanation:** Distributes the films into four equal parts (quartiles) based on their length.

### Stage 5: Combining Multiple Window Functions

11. **Complex Analysis**
    - **Objective:** Combine multiple window functions in a single query.
    - **Query:**
      ```sql
      SELECT
          film_id,
          title,
          length,
          AVG(length) OVER() AS avg_length,
          MAX(length) OVER(PARTITION BY rating) AS max_length_in_rating,
          RANK() OVER(ORDER BY length DESC) AS rank_by_length
      FROM film;
      ```
    - **Explanation:** This query provides a comprehensive analysis, including the average film length across all films, the maximum length within each rating, and a rank based on length.

These stages cover a range of window function capabilities, from basic to advanced, helping to understand their utility in SQL for data analysis. Remember, the key to mastering window functions is practice and experimentation with different datasets and scenarios.
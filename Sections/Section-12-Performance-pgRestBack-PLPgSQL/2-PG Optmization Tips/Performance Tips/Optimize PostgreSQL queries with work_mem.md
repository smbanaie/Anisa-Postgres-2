# [Optimize PostgreSQL queries with work_mem](https://medium.com/@shaileshkumarmishra/optimise-postgresql-queries-with-work-mem-f16c9de06bd4)

![img](https://miro.medium.com/v2/resize:fit:875/1*rbZzubPX6Zvd5CxZ-reXsA.png)

Welcome to this deep dive into PostgreSQL performance tuning, where we’ll unravel the mysteries of `work_mem` and explore how you can supercharge your database operations! Whether you’re a database administrator or a developer keen on optimising database interactions for your application, you’re in the right place. Let’s embark on this journey to squeeze every ounce of performance out of PostgreSQL! 💪

# 📜Introduction to work_mem

In PostgreSQL, memory plays a pivotal role in determining how quickly and efficiently queries are executed. One of the key parameters in this arena is `work_mem`. It specifies the amount of memory used for internal sort operations and hash tables before writing to temporary disk files. This is crucial for operations like ORDER BY, DISTINCT, and JOINs.

By default, `work_mem` is set to a conservative 4MB, which ensures that PostgreSQL can perform adequately on a wide array of systems. However, this default setting might not be optimal for your specific workload, especially if you’re dealing with large datasets.

# 🛠 Tuning work_mem: A Practical Example

Let’s walk through an example to better understand how tuning `work_mem` can lead to substantial performance improvements.

Suppose we have a table named `sales_data`:

```
CREATE TABLE sales_data (
id SERIAL PRIMARY KEY,
date DATE NOT NULL,
amount DECIMAL(10, 2) NOT NULL
);
```

To generate millions of rows of sample data for the `sales_data` table, you can use the `generate_series` function in PostgreSQL. Below is an example of how you can insert 1 million rows of sample data into the `sales_data` table.

Here’s an example SQL query to generate the data:

```
INSERT INTO sales_data (date, amount)
SELECT
generate_series(
'2020–01–01'::date,
'2022–12–31'::date,
'1 minute'::interval
) as date,
round(random() * 1000 + 50, 2) as amount
FROM generate_series(1, 20);
```

In this query:

1. We’re using `generate_series` to create a series of dates starting from January 1, 2020, to December 31, 2022, with a one-minute interval between each date. This will create about 1.5 million unique timestamps.
2. For each generated date, we’re creating 20 rows with random amounts between 50 and 1050, rounded to two decimal places. You can change these limits to fill as many many row you want to fill in.
3. The `INSERT INTO sales_data (date, amount)` part of the query is then used to insert the generated data into the `sales_data` table.

Please adjust the date range, interval, and the number of rows per timestamp according to your needs. If you need more than 1 million rows, you can adjust the parameters of the `generate_series` function or increase the number of rows generated per timestamp.

We’ve filled this table with millions of rows of sample data.

Now, let’s say we want to retrieve total sales amounts, sorted by date:

```
EXPLAIN ANALYZE SELECT date, SUM(amount) FROM sales_data GROUP BY date ORDER BY date;
.
.
.
Sort Method: external merge Disk: 31528kB
Execution Time: 1426.504 ms
```

With the default `work_mem` setting, you might notice that PostgreSQL is resorting to disk-based sort operations, which can be slow.

Now, let’s increase `work_mem` to 64MB and see how it affects the performance:

```
SET work_mem = '64MB';
EXPLAIN ANALYZE SELECT date, SUM(amount) FROM sales_data GROUP BY date ORDER BY date;
.
.
.
Sort Method: quicksort Memory: 52428kB
Execution Time: 438.372 ms
```

And voilà! The query performance is significantly better:

We’ve reduced the execution time by more than three times! 🎉

# 🤝 Other Parameters to Consider

While tuning `work_mem` can yield significant benefits, it’s not the only parameter you should pay attention to. Here are a couple of others that work hand-in-hand with `work_mem`:

# 1. `maintenance_work_mem`

This parameter controls the amount of memory used for maintenance operations like VACUUM, CREATE INDEX, and ALTER TABLE ADD FOREIGN KEY. Ensuring that `maintenance_work_mem` is adequately set can lead to faster index creation and more efficient disk space usage.

```
SET maintenance_work_mem = '128MB';
```

# 2. `shared_buffers`

This parameter determines how much memory is used for caching data blocks. A good starting point is to set `shared_buffers` to around 25% of the available RAM on your system.

```
SET shared_buffers = '1GB';
```

# 💪 Why Does This Matter?

Fine-tuning your PostgreSQL instance ensures that you are utilizing your system’s resources to their fullest potential, leading to faster query execution times and a smoother experience for end-users. It’s about creating a harmonious balance that matches your specific workload.

# 🚀 Conclusion

Mastering the art of performance tuning in PostgreSQL, especially when it comes to parameters like `work_mem`, can transform your database from a slow, disk-bound snail into a swift, memory-optimized hare. 🐢➡️🐇

Remember, the key is to experiment, monitor, and iterate. Every dataset, every query, and every system is unique. By paying close attention to your system’s behavior and understanding how these parameters interplay, you are well on your way to unlocking the true power of PostgreSQL.

Happy Querying! 📊🚀
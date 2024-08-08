# [Find slow queries in PostgreSQL](https://medium.com/@shaileshkumarmishra/find-slow-queries-in-postgresql-42dddafc8a0e)

Slow queries can have a significant impact on the performance of your PostgreSQL database. By identifying and optimizing slow queries, you can improve the overall performance of your database and provide a better experience for your users.

There are a number of ways to trace slow queries in PostgreSQL, including the following:

- **Using the slow query log**: The slow query log is a file that logs all queries that take longer than a certain amount of time to execute.
- **Using \*auto_explain\* extension**: PostgreSQL can help to surface the slow queries, Lets explore in subsequent sections.
- Using **pg_stat_statements**: pg_stat_statements is a built-in PostgreSQL extension that collects statistics about SQL statements. This information can be used to identify the queries that are consuming the most CPU or I/O, and the ones that are causing the most waits.

In this blog post, lets discuss how to use each of these methods to trace slow queries in PostgreSQL. Let’s will also provide some tips for optimizing slow queries.

## Why is it important to trace slow queries?

There are a number of reasons why it is important to trace slow queries:

- Slow queries can impact the performance of your database and make it difficult for users to access the data they need.
- Slow queries can consume a lot of resources, such as CPU and I/O. This can lead to increased costs and decreased performance.
- Slow queries can be a sign of a larger problem, such as a poorly designed query or a performance bottleneck.

By tracing slow queries in PostgreSQL, you can identify and optimize the queries that are causing the most problems. This can improve the overall performance of your database and provide a better experience for your users.

# **Using log_min_duration_statement parameter:**

To use the log_min_duration_statement parameter to trace slow queries in PostgreSQL. If you configure log_min_duration_statement in postgresql.conf as 3500, PostgreSQL will categorize queries lasting more than 3.5 seconds as slow queries and record them in the log file.

```
log_min_duration_statement = 3500
```

Once you have enabled slow query logging, you can view the logs by opening the log file in a text editor. The log file is typically located in the data/postgresql/pg_log or default slow query log file directory.

The slow query log will contain information such as the following:

- The query text
- The execution time
- The start time of the query
- The end time of the query
- The user who executed the query
- The application that executed the query

You can use this information to identify the queries that are causing the most problems in your database. For example, you can look for queries that are taking a long time to execute, or queries that are being executed frequently.

Once you have identified the slow queries, you can take steps to improve their performance. This may involve optimizing the query itself, or adding indexes to the database.

The following example shows how to use the log_min_duration_statement parameter to trace slow queries in PostgreSQL:

```
# Set the log_min_duration_statement parameter to 100 milliseconds.
log_min_duration_statement = 100
# Restart PostgreSQL for the changes to take effect.
pg_ctl restart
```

Once you have enabled slow query logging, check the configuration where log destination is configured with parameter [“log_directory”.](https://www.postgresql.org/docs/current/runtime-config-logging.html) you can view the slow query log by opening the `pg_log` file in a text editor. The log file will contain a list of all queries that took longer than 100 milliseconds to execute.

Monitor the Logs
As users continue to interact with the e-commerce platform, PostgreSQL logs queries taking longer than 2 seconds in the server log file (postgresql.log). Monitor this log file to identify the slow queries:

Sample entry in logfile:

```
2023–10–15 12:35:45 UTC [23537]: [1–1] user=db_user,db=ecommerce_db,app=pgAdmin,client=::1 LOG: duration: 3211.220 ms statement: SELECT * FROM products WHERE category_id = 123;
2023–10–15 12:36:10 UTC [23538]: [1–1] user=web_user,db=ecommerce_db,app=AppServer,client=192.168.1.100 LOG: duration: 2890.430 ms statement: UPDATE shopping_cart SET quantity = 2 WHERE user_id = 456 AND product_id = 789;
```

You can use the information in the slow query log to identify the queries that are causing the most problems in your database. For example, you can look for queries that are taking a long time to execute, or queries that are being executed frequently.

Once you have identified the slow queries, you can take steps to improve their performance. This may involve optimizing the query itself, or adding indexes to the database.

Here are some tips for using the log_min_duration_statement parameter:

- Set the *log_min_duration_statement* parameter to a value that is appropriate for your workload. If you set the value too low, you may generate a lot of noise in the logs. If you set the value too high, you may miss some slow queries.
- Monitor the size of the slow query log file. If the file becomes too large, you can either rotate the logs or increase the amount of disk space available to PostgreSQL.
- Use a tool to parse and analyze the slow query logs. This can help you to identify the queries that are causing the most problems and to take steps to improve their performance.

# **Using auto_explain extension:**

To use the auto_explain extension to trace slow queries in PostgreSQL, you need to:

1. Install the auto_explain extension. This can be done by running the following command on SQL prompt:

```
CREATE EXTENSION auto_explain;
```

2. Set the *auto_explain.log_min_duration* parameter to the number of milliseconds that a query must take to be considered slow. For example, to log all queries that take longer than 100 milliseconds, you would set the value to 100.

Optionally, you can also set the auto_explain.log_analyze parameter to true to log the execution plan of slow queries.

3. Depending upon DB engine version, restart PostgreSQL for the changes to take effect or use pg_reload_conf() to make setting effective.

Example configuration, see more details [here](https://www.postgresql.org/docs/16/auto-explain.html):

```
# Enable auto_explain module
shared_preload_libraries = 'auto_explain'

# Log slow queries with execution plans
auto_explain.log_min_duration = 1000  # Log queries taking longer than 1 second (adjust duration as needed)
auto_explain.log_analyze = on
auto_explain.log_buffers = on
auto_explain.log_format = text
```

Once you have enabled auto_explain, all queries that take longer than the auto_explain.log_min_duration threshold will be logged to the pg_log file. The log entry will contain the following information:

- The query text
- The execution time
- The execution plan

You can use this information to identify the queries that are causing the most problems in your database. For example, you can look for queries that have a high cost or queries that are taking a long time to execute.

Once you have identified the slow queries, you can take steps to improve their performance. This may involve optimizing the query itself, or adding indexes to the database.

Here are some tips for using the auto_explain extension:

- Set the auto_explain.log_min_duration parameter to a value that is appropriate for your workload. If you set the value too low, you may generate a lot of noise in the logs. If you set the value too high, you may miss some slow queries.
- Monitor the size of the pg_log file. If the file becomes too large, you can either rotate the logs or increase the amount of disk space available to PostgreSQL.
- Use a tool to parse and analyze the pg_log file. This can help you to identify the queries that are causing the most problems and to take steps to improve their performance.

**Advantages of using the auto_explain extension**

The auto_explain extension has a number of advantages over using the log_min_duration_statement parameter:

- It is easier to use. You only need to set a single parameter to enable auto_explain.
- It is more comprehensive. auto_explain logs the execution plan of slow queries, which can be helpful for identifying the root cause of performance problems.
- It is more flexible. You can configure auto_explain to log only certain types of queries, or to log queries from specific users or applications.

Overall, the auto_explain extension is a powerful and easy-to-use tool for tracing slow queries in PostgreSQL.

# Using Extension pg_stat_statements

To use the pg_stat_statements extension to trace slow queries in PostgreSQL, you need to:

1. Install the pg_stat_statements extension. This can be done by running the following command on SQL prompt:

```
CREATE EXTENSION pg_stat_statements;
```

Optionally, you can set the pg_stat_statements.track_utility_functions parameter to true to track statistics for utility functions, such as pg_sleep() and pg_stat_statements_reset().

2. Depending upon DB engine version, restart PostgreSQL for the changes to take effect or use pg_reload_conf() to make setting effective.

Once you have enabled pg_stat_statements, it will start collecting statistics about all SQL statements executed by the server. These statistics include the following:

- The number of times the statement has been executed
- The total execution time
- The average execution time
- The minimum execution time
- The maximum execution time

You can view the statistics for all SQL statements by running the following query:

```
SELECT *
FROM pg_stat_statements;
```

You can also view the statistics for a specific SQL statement by running the following query:

```
SELECT *
FROM pg_stat_statements
WHERE query = 'SELECT * FROM my_table';
```

You can use the statistics from pg_stat_statements to identify the queries that are causing the most problems in your database. For example, you can look for queries that have a high execution time or a high number of executions.

Once you have identified the slow queries, you can take steps to improve their performance. This may involve optimizing the query itself, or adding indexes to the database.

## Example

The following example shows how to use pg_stat_statements to identify the slow queries in a database:

```
SELECT
query,
total_exec_time::INTERVAL
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

This query will return the top 10 slowest queries in the database, ordered by execution time.

# Advantages of using the pg_stat_statements extension

The pg_stat_statements extension has a number of advantages over using the log_min_duration_statement parameter and the auto_explain extension:

- It is more comprehensive. pg_stat_statements collects statistics about all SQL statements, regardless of their execution time. This can be helpful for identifying slow queries that are not logged by the *log_min_duration_statement* parameter or the auto_explain extension.
- It is more flexible. You can use pg_stat_statements to generate reports on different types of SQL statements, such as the slowest queries, the most frequently executed queries, or the queries that are consuming the most resources.
- It is more scalable, *pg_stat_statements* is a built-in PostgreSQL extension, so it does not require any additional software or hardware. This makes it a good choice for high-volume databases.

Overall, the *pg_stat_statements* extension is a powerful and flexible tool for tracing slow queries in PostgreSQL.

I invite your comments and suggestion to improve this content.

Cheers!!
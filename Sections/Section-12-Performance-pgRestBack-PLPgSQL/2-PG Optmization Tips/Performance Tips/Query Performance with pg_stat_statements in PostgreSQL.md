# [Query Performance with pg_stat_statements in PostgreSQL](https://medium.com/@omernaci/query-performance-with-pg-stat-statements-in-postgresql-693e6dedc371)

![img](https://miro.medium.com/v2/resize:fit:875/0*C-X1d-RZwIyMcNH0)

Photo by Sunder Muthukumaran on Unsplash

In PostgreSQL, query performance is a critical aspect of database optimization. One powerful tool for monitoring and analyzing query performance is the , `pg_stat_statements` extension.

Enabling `pg_stat_statements`: you need to enable the extension in your PostgreSQL database. Here's how you can enable it:

```
-- Enable the pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

Once it is enabled, `pg_stat_statements` begins collecting statistics for all your queries executed on that database. You can view these statistics by using the pg_stat_statements view.

```
-- View query statistics
SELECT query, calls, total_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

## **Identifying Slow Queries**

By analyzing the total_time and rows columns in the `pg_stat_statements` view, you can spot queries that might need to be optimized. Here’s an example:

```
-- Identify slow-running queries
SELECT query, calls, total_time, rows
FROM pg_stat_statements
WHERE total_time > '1 second'
ORDER BY total_time DESC;
```

## **Monitoring Index Usage**

Suppose you had a database with many indexes and wanted to monitor how well they were being used. You can use the number of times the index scan is against sequential scan `pg_stat_statements`:

```
SELECT indexrelname, idx_scan, seq_scan
FROM pg_stat_all_indexes
ORDER BY (idx_scan + seq_scan) DESC
LIMIT 10;
```

#### [F.32. pg_stat_statements - track statistics of SQL planning and execution](https://www.postgresql.org/docs/current/pgstatstatements.html?source=post_page-----693e6dedc371--------------------------------)


www.postgresql.org
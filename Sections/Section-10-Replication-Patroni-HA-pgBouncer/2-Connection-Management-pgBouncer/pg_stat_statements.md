### `pg_stat_statements` and `pg_repack`

 This tutorial assumes that `pg_stat_statements` and `pg_repack` are already installed.

### Prerequisites

1. PostgreSQL server with `pg_stat_statements` and `pg_repack` installed.
2. `pgbench` for generating a sample dataset.

### Step 1: Setup `pgbench` Dataset

1. **Initialize the `pgbench` Database**:
   ```bash
   pgbench -i -s 10 pgbench
   ```
   This command initializes the `pgbench` database with a scale factor of 10. You can adjust the scale factor based on your needs.

### Step 2: Enable `pg_stat_statements`

1. **Edit PostgreSQL Configuration**:
   Open your `postgresql.conf` file and add or modify the following settings:
   ```plaintext
   shared_preload_libraries = 'pg_stat_statements'
   pg_stat_statements.track = all
   ```

2. **Restart PostgreSQL**:
   Restart the PostgreSQL service to apply the changes:
   ```bash
   sudo systemctl restart postgresql
   ```

3. **Create the Extension**:
   Connect to your database and create the `pg_stat_statements` extension:
   ```sql
   psql -d pgbench -c "CREATE EXTENSION pg_stat_statements;"
   ```

### Step 3: Using `pg_stat_statements`

1. **Generate Some Load**:
   Run the `pgbench` benchmark to generate some load on the database:
   ```bash
   pgbench -c 10 -j 2 -T 60 pgbench
   ```
   This command runs `pgbench` with 10 clients, 2 threads, for 60 seconds.

2. **Query `pg_stat_statements`**:
   Retrieve statistics from `pg_stat_statements`:
   ```sql
   psql -d pgbench -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
   ```

3. **Analyze the Output**:
   The output will show the most time-consuming queries, which you can use to identify performance bottlenecks.

### Step 4: Using `pg_repack`

`pg_repack` is a utility to reorganize tables and indexes without locks.

1. **Ensure `pg_repack` Extension is Installed**:
   Connect to your database and create the `pg_repack` extension:
   ```sql
   psql -d pgbench -c "CREATE EXTENSION pg_repack;"
   ```

2. **Repack a Table**:
   Reorganize a specific table, for example, the `pgbench_accounts` table:
   ```bash
   pg_repack -t pgbench_accounts -d pgbench
   ```

3. **Repack the Entire Database**:
   Reorganize all tables and indexes in the `pgbench` database:
   ```bash
   pg_repack -a -d pgbench
   ```

### Step 5: Advanced Usage of `pg_stat_statements` and `pg_repack`

#### Advanced `pg_stat_statements`

1. **Reset Statistics**:
   Reset the statistics collected by `pg_stat_statements`:
   ```sql
   psql -d pgbench -c "SELECT pg_stat_statements_reset();"
   ```

2. **Custom Queries**:
   Customize your queries to analyze specific patterns or user sessions:
   ```sql
   psql -d pgbench -c "SELECT userid, dbid, query, calls, total_time FROM pg_stat_statements WHERE query LIKE '%SELECT%' ORDER BY total_time DESC LIMIT 5;"
   ```

3. **Monitor Changes Over Time**:
   Regularly capture `pg_stat_statements` data to monitor query performance trends over time:
   ```sql
   psql -d pgbench -c "COPY (SELECT * FROM pg_stat_statements) TO '/path/to/log.csv' WITH CSV HEADER;"
   ```

#### Advanced `pg_repack`

1. **Repack a Specific Index**:
   Repack a specific index, for example, the primary key on the `pgbench_accounts` table:
   ```bash
   pg_repack -i pgbench_accounts_pkey -d pgbench
   ```

2. **Schedule Regular Maintenance**:
   Automate `pg_repack` using cron jobs to run during low-traffic periods:
   ```bash
   echo "0 2 * * * pg_repack -a -d pgbench" | crontab -
   ```

3. **Examine Table Bloat**:
   Use `pg_repack` to report table and index bloat without actually repacking:
   ```bash
   pg_repack -n -d pgbench
   ```

### Summary

Regular use of these tools can significantly improve the performance and efficiency of your PostgreSQL instances.

For further customization and advanced usage, you can explore the documentation of both extensions:
- [`pg_stat_statements` Documentation](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [`pg_repack` Documentation](https://reorg.github.io/pg_repack/)
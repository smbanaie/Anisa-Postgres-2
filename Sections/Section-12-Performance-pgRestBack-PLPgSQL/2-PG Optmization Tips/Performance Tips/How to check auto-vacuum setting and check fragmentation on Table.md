# [How to check auto-vacuum setting and check fragmentation on Table](https://medium.com/@anujkhandelwal0411/how-to-check-auto-vacuum-setting-and-check-fragmentation-on-table-a7873a5c8d65)

We recently encountered a significant fragmentation issue with a couple of tables in our production environment. Upon investigation, I discovered that auto-vacuum was disabled for these tables. However, enabling auto-vacuum did not resolve the space release issue. To validate this problem, I replicated the issue in a testing environment.

Let Identified What is auto-vacuum and how Is work.

In PostgreSQL, when rows are updated or deleted from a table, dead rows are created and left behind, vacuum daemon processes will clean those dead tuples ( rows) periodically based on parameter setting for vacuum process. Generally the following four reasons explain why vacuum is needed:

- To recover or reuse disk space occupied by updated or deleted rows.
- To update data statistics used by the PostgreSQL query planner.
- To update the visibility map, which speeds up index-only scans.
- To protect against loss of very old data due to *transaction ID wraparound* or *multixact ID wraparound*.

Below are the important settings to check, specifically related to the auto-vacuum parameter.

```
sales=# select name, setting,unit from pg_settings where name like '%autovacuum%';
                name                 |  setting  | unit
-------------------------------------+-----------+------
 autovacuum                          | on        |
 autovacuum_analyze_scale_factor     | 0.1       |
 autovacuum_analyze_threshold        | 50        |
 autovacuum_freeze_max_age           | 200000000 |
 autovacuum_max_workers              | 3         |
 autovacuum_multixact_freeze_max_age | 400000000 |
 autovacuum_naptime                  | 60        | s
 autovacuum_vacuum_cost_delay        | 2         | ms
 autovacuum_vacuum_cost_limit        | -1        |
 autovacuum_vacuum_scale_factor      | 0.2       |
 autovacuum_vacuum_threshold         | 50        |
 autovacuum_work_mem                 | -1        | kB
 log_autovacuum_min_duration         | -1        | ms
(13 rows)
```

The settings outlined above include two important parameters that provide information on when or under what conditions auto-vacuum is triggered.

```
              name              | setting | unit
--------------------------------+---------+------
 autovacuum_vacuum_scale_factor | 0.2     |
 autovacuum_analyze_threshold   | 50      |
```

`**autovacuum_vacuum_scale_factor**` **(**`**floating point**`**)** “ Specifies a fraction of the table size to add to `autovacuum_vacuum_threshold` when deciding whether to trigger a `VACUUM`. The default is 0.2 (20% of table size). This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters”.

`**autovacuum_analyze_threshold**` **(**`**integer**`**)** “Specifies the minimum number of inserted, updated or deleted tuples needed to trigger an `ANALYZE` in any one table. The default is 50 tuples. This parameter can only be set in the `postgresql.conf` file or on the server command line; but the setting can be overridden for individual tables by changing table storage parameters.”

Let’s create one temp table to test how this auto-vacumn trigger.

```
sales=# CREATE TABLE emp (
sales(#     emp_id SERIAL PRIMARY KEY,
sales(#     emp_name VARCHAR(50),
sales(#     emp_salary DECIMAL(10, 2)
sales(# );
CREATE TABLE
```

So, based on the aforementioned settings, if either the autovacuum_vacuum_scale_factor or autovacuum_analyze_threshold reaches its threshold, auto-vacuum is triggered. By default, these parameters are set to 50 and 0.1, respectively. It’s also possible to modify these parameters at the individual table level using the ALTER TABLE statement.

```
sales=# ALTER TABLE emp SET (autovacuum_enabled = true,autovacuum_vacuum_threshold=5);
ALTER TABLE
sales=# \d+ emp
                                                           Table "public.emp"
   Column   |         Type          | Collation | Nullable |               Default               | Storage  | Stats target | Description
------------+-----------------------+-----------+----------+-------------------------------------+----------+--------------+-------------
 emp_id     | integer               |           | not null | nextval('emp_emp_id_seq'::regclass) | plain    |              |
 emp_name   | character varying(50) |           |          |                                     | extended |              |
 emp_salary | numeric(10,2)         |           |          |                                     | main     |              |
Indexes:
    "emp_pkey" PRIMARY KEY, btree (emp_id)
Access method: heap
Options: autovacuum_enabled=true, autovacuum_vacuum_threshold=5
```

To View All table-specific auto-vacuum settings

```
WITH raw_data AS (
  SELECT
    pg_namespace.nspname,
    pg_class.relname,
    pg_class.oid AS relid,
    pg_class.reltuples,
    pg_stat_all_tables.n_dead_tup,
    pg_stat_all_tables.n_mod_since_analyze,
    (SELECT split_part(x, '=', 2) FROM unnest(pg_class.reloptions) q (x) WHERE x ~ '^autovacuum_analyze_scale_factor=' ) as c_analyze_factor,
    (SELECT split_part(x, '=', 2) FROM unnest(pg_class.reloptions) q (x) WHERE x ~ '^autovacuum_analyze_threshold=' ) as c_analyze_threshold,
    (SELECT split_part(x, '=', 2) FROM unnest(pg_class.reloptions) q (x) WHERE x ~ '^autovacuum_vacuum_scale_factor=' ) as c_vacuum_factor,
    (SELECT split_part(x, '=', 2) FROM unnest(pg_class.reloptions) q (x) WHERE x ~ '^autovacuum_vacuum_threshold=' ) as c_vacuum_threshold,
    to_char(pg_stat_all_tables.last_vacuum, 'YYYY-MM-DD HH24:MI:SS') as last_vacuum,
    to_char(pg_stat_all_tables.last_autovacuum, 'YYYY-MM-DD HH24:MI:SS') as last_autovacuum
  FROM
    pg_class
  JOIN pg_namespace ON pg_class.relnamespace = pg_namespace.oid
    LEFT OUTER JOIN pg_stat_all_tables ON pg_class.oid = pg_stat_all_tables.relid
  WHERE
    n_dead_tup IS NOT NULL
    AND nspname NOT IN ('information_schema', 'pg_catalog')
    AND nspname NOT LIKE 'pg_toast%'
    AND pg_class.relkind = 'r'
), data AS (
  SELECT
    *,
    COALESCE(raw_data.c_analyze_factor, current_setting('autovacuum_analyze_scale_factor'))::float8 AS analyze_factor,
    COALESCE(raw_data.c_analyze_threshold, current_setting('autovacuum_analyze_threshold'))::float8 AS analyze_threshold,
    COALESCE(raw_data.c_vacuum_factor, current_setting('autovacuum_vacuum_scale_factor'))::float8 AS vacuum_factor,
    COALESCE(raw_data.c_vacuum_threshold, current_setting('autovacuum_vacuum_threshold'))::float8 AS vacuum_threshold
  FROM raw_data
)
SELECT
  relid,
  nspname,
  relname,
  reltuples,
  n_dead_tup,
  ROUND(reltuples * vacuum_factor + vacuum_threshold) AS v_threshold,
  n_mod_since_analyze,
  ROUND(reltuples * analyze_factor + analyze_threshold) AS a_threshold,
  c_analyze_factor as caf,
  c_analyze_threshold as cat,
  c_vacuum_factor as cvf,
  c_vacuum_threshold as cvt,
  analyze_factor as af,
  analyze_threshold as at,
  vacuum_factor as vf,
  vacuum_threshold as vt,
  last_vacuum,
  last_autovacuum
FROM
  data
ORDER BY n_dead_tup DESC;
```

We have inserted 50 rows to observe whether auto-vacuum is triggered or not.

```
INSERT INTO emp (emp_name, emp_salary)
SELECT
    'Employee ' || CAST(generate_series AS VARCHAR),
    CAST(RANDOM() * 100000 AS DECIMAL(10, 2)) AS emp_salary
FROM generate_series(1,51);

sales=# select * from pg_stat_all_tables where relname='emp';
-[ RECORD 1 ]-------+---------------------------------
relid               | 16404
schemaname          | public
relname             | emp
seq_scan            | 1
seq_tup_read        | 0
idx_scan            | 0
idx_tup_fetch       | 0
n_tup_ins           | 51
n_tup_upd           | 0
n_tup_del           | 0
n_tup_hot_upd       | 0
n_live_tup          | 51
n_dead_tup          | 0
n_mod_since_analyze | 0
last_vacuum         |
last_autovacuum     |
last_analyze        |
last_autoanalyze    | 28-DEC-23 09:38:04.351835 +07:00
vacuum_count        | 0
autovacuum_count    | 0
analyze_count       | 0
autoanalyze_count   | 1
```

As anticipated, the auto-analyze kicked off immediately after inserting 50 records, hitting the threshold.

Now, let’s return to the main issue where we are experiencing fragmentation on the table, and the size of the table continues to increase. To replicate the problem, I have inserted 50 million records into the table and subsequently deleted 1 million records.

```
sales=# INSERT INTO emp (emp_name, emp_salary)
sales-# SELECT
sales-#     'Employee ' || CAST(generate_series AS VARCHAR),
sales-#     CAST(RANDOM() * 100000 AS DECIMAL(10, 2)) AS emp_salary
sales-# FROM generate_series(1, 50000000);
INSERT 0 50000000

sales=# DELETE FROM emp
sales=# WHERE emp_id IN (
sales=#     SELECT emp_id
sales=#     FROM emp
sales=#     ORDER BY RANDOM()
sales=#     LIMIT 1000000
sales=# );
DELETE 1000000
```

After deleting the records, we observed an increase in dead tuples on the table. Despite the auto-vacuum running, it did not release the occupied space.

```
edb=# select * from pg_stat_all_tables where relname='emp';
-[ RECORD 1 ]-------+---------------------------------
relid               | 16404
schemaname          | public
relname             | emp
seq_scan            | 3
seq_tup_read        | 100000102
idx_scan            | 2
idx_tup_fetch       | 2
n_tup_ins           | 50000051
n_tup_upd           | 0
n_tup_del           | 1000000
n_tup_hot_upd       | 0
n_live_tup          | 49000140
n_dead_tup          | 1000000
n_mod_since_analyze | 1000000
last_vacuum         |
last_autovacuum     |
last_analyze        |
last_autoanalyze    | 28-DEC-23 09:49:12.411106 +07:00
vacuum_count        | 0
autovacuum_count    | 0
analyze_count       | 0
autoanalyze_count   | 2
```

Apart from PostgreSQL having built-in features, there are also extensions available to analyze fragmentation on the table. You can check the extension details by querying ‘**pg_extension**’ and ‘**pg_available_extensions**’.

```
As super user, install extension pgstattuple as following if not yet.

CREATE EXTENSION pgstattuple;

edb=# SELECT * FROM pgstattuple('emp');
-[ RECORD 1 ]------+-----------
table_len          | 3011772416
tuple_count        | 49000051
tuple_len          | 2673328232
tuple_percent      | 88.76
dead_tuple_count   | 1000000
dead_tuple_len     | 54555370
dead_tuple_percent | 1.81
free_space         | 1477064
free_percent       | 0.05

edb=# select count(*) from emp;
-[ RECORD 1 ]---
count | 49000051
Column                Type         Description
table_len             bigint       Physical relation length in bytes
tuple_count           bigint       Number of live tuples
tuple_len             bigint       Total length of live tuples in bytes
tuple_percent         float8       Percentage of live tuples
dead_tuple_count      bigint       Number of dead tuples
dead_tuple_len        bigint       Total length of dead tuples in bytes
dead_tuple_percent    float8       Percentage of dead tuples
free_space bigint     Total        free space in bytes
free_percent          float8       Percentage of free space
```

Same thing we can check for index also for its fragemention.

pgstatindex
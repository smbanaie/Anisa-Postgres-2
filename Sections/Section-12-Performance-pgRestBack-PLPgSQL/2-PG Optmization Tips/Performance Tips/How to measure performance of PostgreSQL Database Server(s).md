# [How to measure performance of PostgreSQL Database Server(s)?](https://medium.com/@dmitry.romanoff/how-to-measure-performance-of-postgresql-database-server-s-b27e2e5130aa)



![img](https://miro.medium.com/v2/resize:fit:875/0*hy23bVQXjZjLGAzV)

Photo by [Kolleen Gladden](https://unsplash.com/fr/@rockthechaos?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=medium&utm_medium=referral)

In this blog I will demonstrate how to measure performance of PostgreSQL Database Server(s). I will guide you how to run a benchmark test.

The benchmark test is designed to evaluate and compare the performance of different configurations, topologies, systems and components. For this purpose I will use the pgbench utility.

You may ask, why use a separate utility to measure the performance of a PostgreSQL database? After all, we usually have a specific application or system that accesses the database and manipulates data. By running an existing application in different modes and simulating different load scenarios, we can check the performance of the database.

However, this method does not always work because the application itself may have architectural or system limitations. As a result, it can be very difficult and challenging to generate enough load and to objectively evaluate the performance of the database. When we’re talking about measuring performance of the database the most challenging thing is to generate enough load.

The pgbench is a benchmarking tool for PostgreSQL databases. It allows simulating a workload of multiple clients executing transactions on a PostgreSQL database. The pgbench utility measures the database’s performance under different scenarios.

Assume we have installed PostgreSQL database server:

```
dmi@dmi-VirtualBox:~$ psql -h 127.0.0.1 -p 5444 -U postgres -d postgres
Password for user postgres:
psql (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.
```

To run a benchmark test I will create a new database.

```
create database my_benchmark_test_db;
```

By running \list command I can validate the DB has created successfully:

```
postgres=# \l
                                                  List of databases
         Name         |  Owner   | Encoding | Collate | Ctype | ICU Locale | Locale Provider |   Access privileges
----------------------+----------+----------+---------+-------+------------+-----------------+-----------------------
 my_benchmark_test_db | postgres | UTF8     | en_IL   | en_IL |            | libc            |
 postgres             | postgres | UTF8     | en_IL   | en_IL |            | libc            |
 template0            | postgres | UTF8     | en_IL   | en_IL |            | libc            | =c/postgres          +
                      |          |          |         |       |            |                 | postgres=CTc/postgres
 template1            | postgres | UTF8     | en_IL   | en_IL |            | libc            | =c/postgres          +
                      |          |          |         |       |            |                 | postgres=CTc/postgres
(4 rows)
```

To set up pgbench to work with the newly created database my_benchmark_test_db run the command:

```
pgbench -i -s 50 my_benchmark_test_db -h <db_hostname> -p <db_port> -U <db_user>
```

For example:

```
dmi@dmi-VirtualBox:~$ pgbench -i -s 50 my_benchmark_test_db -h 127.0.0.1 -p 5444 -U postgres
Password:
dropping old tables...
NOTICE:  table "pgbench_accounts" does not exist, skipping
NOTICE:  table "pgbench_branches" does not exist, skipping
NOTICE:  table "pgbench_history" does not exist, skipping
NOTICE:  table "pgbench_tellers" does not exist, skipping
creating tables...
generating data (client-side)...
5000000 of 5000000 tuples (100%) done (elapsed 10.19 s, remaining 0.00 s)
vacuuming...
creating primary keys...
done in 30.29 s (drop tables 0.05 s, create tables 0.04 s, client-side generate 10.64 s, vacuum 4.75 s, primary keys 14.81 s).
dmi@dmi-VirtualBox:~$
```

The -i (initialize) option tells pgbench to initialize the database specified.

Connecting to the PostgreSQL database my_benchmark_test_db we can see the pgbench created four tables: pgbench_accounts, pgbench_branches, pgbench_history, pgbench_tellers

```
dmi@dmi-VirtualBox:~$ psql -h 127.0.0.1 -p 5444 -U postgres -d my_benchmark_test_db
Password for user postgres:
psql (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.
my_benchmark_test_db=# \d
              List of relations
 Schema |       Name       | Type  |  Owner
--------+------------------+-------+----------
 public | pgbench_accounts | table | postgres
 public | pgbench_branches | table | postgres
 public | pgbench_history  | table | postgres
 public | pgbench_tellers  | table | postgres
(4 rows)
my_benchmark_test_db=#
```

Let’s examine the number of rows in each table:

```
my_benchmark_test_db=# select count(1) from pgbench_accounts;
  count
---------
 5000000
(1 row)
my_benchmark_test_db=# select count(1) from pgbench_branches;
 count
-------
    50
(1 row)
my_benchmark_test_db=# select count(1) from pgbench_history;
 count
-------
     0
(1 row)
my_benchmark_test_db=# select count(1) from pgbench_tellers;
 count
-------
   500
(1 row)
my_benchmark_test_db=#
```

The database my_benchmark_test_db is now populated and ready to measure the performance of our PostgreSQL database server.

When we want to determine the performance of a system, we usually compare its metrics against a certain baseline. Let’s run the pgbench utility and set a baseline.

For this purpose, we run pgbench with the following parameters:

```
pgbench -c <the_number_of_clients_to_connect_with> -j <the_number_of_workers_processes> -t <the_number_of_transactions_to_execute> <sample_db_name>
```

For example:

```
pgbench -c 10 -j 2 -t 1000 my_benchmark_test_db -h 127.0.0.1 -p 5444 -U postgres
dmi@dmi-VirtualBox:~$ pgbench -c 10 -j 2 -t 1000 my_benchmark_test_db -h 127.0.0.1 -p 5444 -U postgres
Password:
pgbench (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
starting vacuum...end.
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 50
query mode: simple
number of clients: 10
number of threads: 2
maximum number of tries: 1
number of transactions per client: 1000
number of transactions actually processed: 10000/10000
number of failed transactions: 0 (0.000%)
latency average = 75.438 ms
initial connection time = 160.700 ms
tps = 132.559344 (without initial connection time)
dmi@dmi-VirtualBox:~$
```

The output has a lot of information.

The most interesting one is:

```
latency average = 75.438 ms
initial connection time = 160.700 ms
tps = 132.559344 (without initial connection time)
```

Now let’s increase the amount of memory the PostgreSQL DB Server can utilize for caching.
The idea is to store the contents of tables and indexes in memory.
For this purpose, we will change the PostgreSQL parameter shared_buffers.

Currently, it’s set to:

```
my_benchmark_test_db=# show shared_buffers;
 shared_buffers
----------------
 128MB
(1 row)
```

Let’s change it to 2GB:

```
sudo vi /etc/postgresql/15/main/postgresql.conf
...
#------------------------------------------------------------------------------
# RESOURCE USAGE (except WAL)
#------------------------------------------------------------------------------
# - Memory -
shared_buffers = 1GB                    # min 128kB
                                        # (change requires restart)
...
```

The change requires to restart the PostgreSQL service:

```
sudo systemctl restart postgresql
```

Examine the changed PostgreSQL parameter shared_buffers:

```
dmi@dmi-VirtualBox:~$ psql -h 127.0.0.1 -p 5444 -U postgres -d my_benchmark_test_db
Password for user postgres:
psql (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.
my_benchmark_test_db=# show shared_buffers;
 shared_buffers
----------------
 1GB
(1 row)
my_benchmark_test_db=#
```

Rerun the pgbench utility after the shared_buffers PostgreSQL parameter was increased:

```
pgbench -c 10 -j 2 -t 1000 my_benchmark_test_db -h 127.0.0.1 -p 5444 -U postgres
dmi@dmi-VirtualBox:~$ pgbench -c 10 -j 2 -t 1000 my_benchmark_test_db -h 127.0.0.1 -p 5444 -U postgres
Password:
pgbench (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
starting vacuum...end.
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 50
query mode: simple
number of clients: 10
number of threads: 2
maximum number of tries: 1
number of transactions per client: 1000
number of transactions actually processed: 10000/10000
number of failed transactions: 0 (0.000%)
latency average = 47.632 ms
initial connection time = 148.379 ms
tps = 209.944478 (without initial connection time)
dmi@dmi-VirtualBox:~$
```

latency average = 47.632 ms
initial connection time = 148.379 ms
tps = 209.944478 (without initial connection time)

In the baseline test, we reached a rate of 132 transactions per second. in this run, after increasing the shared_buffers parameter, we reached 209 transactions per second, an increase of ~58%.

The best practice recommends setting the shared_buffers value to 1/4 (one-fourth) of the system memory (free -m).

By measuring the performance of a database using pgbench utility, we can continue. For example, we can compare the performance of different versions of the PostgreSQL engines. This way, we can determine whether one version of PostgreSQL engine performs better or worse than another.

This methodology can become part of a performance test for your company.
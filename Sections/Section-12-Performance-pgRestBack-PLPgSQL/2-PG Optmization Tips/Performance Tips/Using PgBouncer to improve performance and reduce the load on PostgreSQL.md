# Using PgBouncer to improve performance and reduce the load on PostgreSQL

The article was initially published in [JFrog blog](https://jfrog.com/community/data-science/pgbouncer-improves-postgresql-performance/).

![img](https://miro.medium.com/v2/resize:fit:875/1*qItTtBdVkboGBLU_WBbK3Q.png)

How to improve the PostgreSQL Database Server architecture connections management

This blog post describes step-by-step how to improve the PostgreSQL Database Server architecture connections management, reduce the load on the PostgreSQL Server and improve the performance using the PgBouncer connection pooler. Here is a breakdown of the topics we will discover in this article

- How a PostgreSQL Database Server works
- Improving efficiency with PgBouncer poolers
- How to install and configure PgBouncer

First, let’s start with some basic concepts.

# How a PostgreSQL Database Server works

A **PostgreSQL Database Server** accepts, processes requests, and returns results. The requests are received from client applications. The application code interacts with the database. The database searches, saves, manipulates data, and responds to the client.

**PostgreSQL** creates a separate process for each client connection that serves that connection. For example:

if there are ten client connections, PostgreSQL creates ten processes and allocates memory per connection.

if there are one hundred client connections, then one hundred PostgreSQL Server processes serve those one hundred client connections.

This type of architecture is called the Client-Server model. It is slow, inefficient, and doesn’t scale. It is limited to the number of client connections that the Database server can serve due to its resource limits of CPU and Memory.

# Improving efficiency with PgBouncer poolers

To improve the above architecture, and reduce the overhead of database connections for each request, a special utility called Database connection poolers can be used. For the PostgreSQL Database Server, one of the commonly used connection poolers is PgBouncer.

![img](https://miro.medium.com/v2/resize:fit:875/0*VjNUJO2Zx86RIPzV.png)

Using PgBouncer to improve performance and reduce the load on PostgreSQL

**PgBouncer** is a middleware process responsible for managing a connection pool(s) to the Database(s). Clients connect to PgBouncer in the same way they would connect to the Database server. The Database server accepts the connections from PgBouncer as if they were regular clients.

By efficiently managing the connection pool(s), PgBouncer can handle a large number of incoming client connections and redirect them to a much smaller number of actual connections by using the pool(s). When the client application sends hundreds of requests to the database, PgBouncer serves as an intermediary. It distributes the requests among several dozen connections to the Database server and creates queues when necessary using settings like listen_backlog and query_wait_timeout.

This approach makes the management of Database connections more efficient, ensuring that all connection requests are handled effectively.

# Advantages of this approach

First, the application continues to work even if the number of requests dramatically increases. This is because each request does not create a separate process for the database. Instead, the requests are made to PgBouncer, which translates them into a small number of connections to the database by managing connection pool(s). Second, the application works faster, as time is saved by not creating a separate dedicated process in the database per each request.

# How to install and configure PgBouncer

If PostgresSQL exists:

```
dmi@dmi-VirtualBox:~$ psql -h 127.0.0.1 -p 5432 -U postgres -d postgres
Password for user postgres:
psql (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.

postgres=# select version();
version
-----------------------------------------------------------------------------------------------------------------------------------
PostgreSQL 15.1 (Ubuntu 15.1-1.pgdg22.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0, 64-bit
(1 row)
```

PgBouncer installation:

```
sudo apt-get install pgbouncer
```

PgBouncer configuration:

```
sudo vi /etc/pgbouncer/pgbouncer.ini
```

In the [databases] block, add the following entry:

```
* = host=localhost port=5432
```

In the “Pooler personality questions” section, define pool_mode=transaction.

```
...
;;;
;;; Pooler personality questions
;;;

;; When server connection is released back to pool:
;;   session      - after client disconnects (default)
;;   transaction  - after transaction finishes
;;   statement    - after statement finishes
pool_mode = transaction
...
```

In the “Connection limits” section, set the total number of clients that can connect to some high value: max_client_conn=5000.

```
...
;;;
;;; Connection limits
;;;

;; Total number of clients that can connect
max_client_conn = 5000
...
```

In the “Authentication settings” section, set auth_type = md5 to authenticate users by a password. The file with the database login and password will be located at /etc/pgbouncer/userlist.txt

```
...
;;;
;;; Authentication settings
;;;

;; any, trust, plain, md5, cert, hba, pam
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
...
```

In the “Users allowed into database ‘pgbouncer’” section, set the admin_users parameter. This is the database user who will have permission to make PgBouncer settings in the database.

```
...
;;;
;;; Users allowed into database 'pgbouncer'
;;;

;; comma-separated list of users who are allowed to change settings
;admin_users = user2, someadmin, otheradmin
admin_users = my_db_user
...
```

Now let’s open the file with users at /etc/pgbouncer/userlist.txt.
If you are using PostgreSQL versions up to 13 inclusively, then the default password_encryption method is md5.

Place the username in double quotes and the md5 password hash (in one line):

```
"my_db_user" "md5badc318d987f61146c6ad8e15d84a111"
```

To determine the md5 password hash, you can use the following method:

```
echo "md5"$(echo -n 'YourdbpasswordYourdbusername' | md5sum | awk ' { print $1 } ')
```

After that, let’s reload PgBouncer:

```
sudo service pgbouncer restart
```

Now you are able to connect to the database through PgBouncer using port 6432 (PgBouncer default port).

If you are using PostgreSQL versions starting from 14, then the default password_encryption method is scram-sha-256.

Place the username in double quotes and the scram-sha-256 password hash (in one line):

```
"my_db_user" "SCRAM-SHA-256$4096:lLN4+i05+kpeffD4s3rRiw==$Oq62iUGamAaF5cpB+agWV4u3xfc5cZCRtvMhmA+Zm3E=:hHkCesEi0p0wLWk1uUEeTtJTYLXHKDLdy2te3VAOe8s="
```

To determine the scram-sha-256 password hash, you can use the following method:

```
psql -h  -p  -Atq -U postgres -d postgres -c "SELECT concat('\"', usename, '\" \"', passwd, '\"') FROM pg_shadow"
```

To make our application use PgBouncer when connecting to the database, the only change that is needed is replacing the port number: use 6432 instead of 5432.

Let’s run a performance test to compare the performance of connecting to PostgreSQL with and without PgBouncer, using the pgbench utility.

The pgbench is a benchmarking tool for PostgreSQL databases. It allows the simulation of a workload of multiple clients executing transactions on a PostgreSQL database. The pgbench utility measures the database’s performance under different scenarios.

The maximum number of connections for my database is set to 100:

```
postgres=# show max_connections;
 max_connections
-----------------
 100
(1 row)
```

Connecting to the Postgres database server without using PgBouncer.
This command will start a test with 1000 concurrent clients for 60 seconds, connecting directly to the PostgreSQL database.

```
dmi@dmi-VirtualBox:~$  pgbench -c 1000 -T 60 my_benchmark_test_db -h 127.0.0.1 -p 5432 -U my_db_user
Password:
pgbench (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
starting vacuum...end.
pgbench: error: connection to server at "127.0.0.1", port 5432 failed: FATAL:  sorry, too many clients already
connection to server at "127.0.0.1", port 5432 failed: FATAL:  sorry, too many clients already
pgbench: error: could not create connection for client 44
```

Simulating the work of 1000 clients interacting with a database where only 100 clients can be connected at maximum results in an error.

```
FATAL:  sorry, too many clients already
```

When connecting to the database using PgBouncer, everything works without any issues.

```
pgbench -c 1000 -T 60 my_benchmark_test_db -h 127.0.0.1 -p 6432 -U my_db_user
Password:
pgbench (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
starting vacuum...end.
transaction type: 
scaling factor: 50
query mode: simple
number of clients: 1000
number of threads: 1
maximum number of tries: 1
duration: 60 s
number of transactions actually processed: 47370
number of failed transactions: 0 (0.000%)
latency average = 1106.280 ms
initial connection time = 8788.955 ms
tps = 903.930420 (without initial connection time)
dmi@dmi-VirtualBox:~$
```

Let’s compare a latency and a number of transactions per second (tps) that the database performs when the application connects to the database without using PgBouncer and when it uses PgBouncer.

The following test performs select-only transactions.

```
dmi@dmi-VirtualBox:~$ cat mysql.sql
select 1;
```

The reason is to exclude measuring update contention when lots of transactions are blocked waiting for other transactions.

The -C option in the pgbench indicates that for every single transaction, pgbench will close the open connection and create a new one. This is useful for measuring the connection overhead.

The application connects to the database without using PgBouncer:

```
dmi@dmi-VirtualBox:~$ pgbench -c 20 -t 100 -S my_benchmark_test_db -h 127.0.0.1 -p 5432 -U my_db_user -C -f mysql.sql
Password:
pgbench (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
starting vacuum...end.
transaction type: multiple scripts
scaling factor: 50
query mode: simple
number of clients: 20
number of threads: 1
maximum number of tries: 1
number of transactions per client: 100
number of transactions actually processed: 2000/2000
number of failed transactions: 0 (0.000%)
latency average = 340.479 ms
average connection time = 16.910 ms
tps = 58.740729 (including reconnection times)
SQL script 1: 
 - weight: 1 (targets 50.0% of total)
 - 979 transactions (49.0% of total, tps = 28.753587)
 - number of failed transactions: 0 (0.000%)
 - latency average = 158.504 ms
 - latency stddev = 133.666 ms
SQL script 2: mysql.sql
 - weight: 1 (targets 50.0% of total)
 - 1021 transactions (51.0% of total, tps = 29.987142)
 - number of failed transactions: 0 (0.000%)
 - latency average = 162.888 ms
 - latency stddev = 136.175 ms
```

The application connects to the database through PgBouncer:

```
dmi@dmi-VirtualBox:~$ pgbench -c 20 -t 100 -S my_benchmark_test_db -h 127.0.0.1 -p 6432 -U my_db_user -C -f mysql.sql
Password:
pgbench (15.1 (Ubuntu 15.1-1.pgdg22.04+1))
starting vacuum...end.
transaction type: multiple scripts
scaling factor: 50
query mode: simple
number of clients: 20
number of threads: 1
maximum number of tries: 1
number of transactions per client: 100
number of transactions actually processed: 2000/2000
number of failed transactions: 0 (0.000%)
latency average = 178.276 ms
average connection time = 8.867 ms
tps = 112.185757 (including reconnection times)
SQL script 1: 
 - weight: 1 (targets 50.0% of total)
 - 1022 transactions (51.1% of total, tps = 57.326922)
 - number of failed transactions: 0 (0.000%)
 - latency average = 85.993 ms
 - latency stddev = 50.377 ms
SQL script 2: mysql.sql
 - weight: 1 (targets 50.0% of total)
 - 978 transactions (48.9% of total, tps = 54.858835)
 - number of failed transactions: 0 (0.000%)
 - latency average = 84.039 ms
 - latency stddev = 51.036 ms
dmi@dmi-VirtualBox:~$
```

Both the latency average and the transactions per second (tps) indicate improvement when an application connects to the database through PgBouncer:

```bash
latency average: 340.479 ms -> 178.276 ms --- improvement 
tps: 58 -> 112  --- improvement
```
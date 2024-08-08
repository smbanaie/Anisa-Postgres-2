# [PostgreSQL with increased connection’s](https://medium.com/@pawanpg0963/postgresql-with-increased-connections-3a09f7cb6a9a)

![PAWAN SHARMA](https://miro.medium.com/v2/resize:fill:55:55/1*LX9aVVnKZZ25J-cxWkdXfg.jpeg)

**What is PostgreSQL DB Connections?**

PostgreSQL connection allow you to communicate with PostgreSQL DB server to perform and execute the SQL queries. Using the PostgreSQL Connections you can also manage the PostgreSQL databases.

There are various way to access the PostgreSQL database and the most common are psql (interactive terminal program) and pgadmin (a graphical frontend web based tool).

**How connection will Spawn?**

1. A client connection is sent to the postmaster. postmaster is a daemon process running on PostgreSQL DB server.
2. The postmaster spawns a user-backend process.
3. Authentication is performed using pg_hba.conf file.
4. The user-backend calls back to the client to continue operations.

![img](https://miro.medium.com/v2/resize:fit:620/1*7vdZ4iayBSf5R6d0if0EFA.png)

Process of connect request

Every connection require some memory to perform the certain tasks in DB.

**work_mem**

1. *Per-Backend sort / hash memory*
2. *Used during certain types of JOINs and for ORDER BY operations*
3. *Set globally, but can be modified per-session*

**Maintenance_work_mem**

1. *Used for certain types of maintenance operations ( vacuum, index creation, re-index )*
2. *Allocated per session that uses it ( i.e. multiple autovacuum workers)*

**What is the limit of PostgreSQL DB connection?**

The default value of max concurrent connection’s in PostgreSQL DB is 100, but we can tune/increased it if required using config parameter called [**max_connections**](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-MAX-CONNECTIONS)**.** In the defined value of max_connections there are few that are reserved for superuser called [**superuser_reserved_connections**](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-SUPERUSER-RESERVED-CONNECTIONS).

**How PostgreSQL DB will Perform if we keep increasing the max_connections value?**

1. *Each connection require more memory allocation since each connection require 5–10MB.*
2. *If with the high no. of connections any query ran with extensive Mem/CPU workload in database. It will create a lock for long time and it can cause the situations where database can be very slow or choked up and none of your database session will make any kind of progress. In such sometime its require restart of your database services.*
3. *The more connections you have, the risk will be bigger many connections suddenly becoming active and overloading the machine.*

![img](https://miro.medium.com/v2/resize:fit:849/1*QOaJnnMS8M-7vmeJ-6Z7OA.png)

[Pgbench ](https://postgresql.org/docs/current/pgbench.html)result when we are increasing the connection’s with out increasing the total memory.

![img](https://miro.medium.com/v2/resize:fit:815/1*BfuTp3NHfENVuqiQJrJVEw.png)

Pgbench result sets

**Test case 1:** *Duration: 10 min, Work_mem: 3932kB, Connection: 200*

```
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 684
query mode: simple
number of clients: 200
number of threads: 1
maximum number of tries: 1
duration: 600s
number of transactions per client: 1000
number of transactions actually processed: 680421
number of failed transactions: 0 (0.000%)
latency average = 176.016 ms
initial connection time = 1531.281 ms
tps = 1136.258398(without initial connection time)
```

**Test case 2:** *Duration: 10 min, Work_mem: 1966kB, Connection: 400*

```
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 684
query mode: simple
number of clients: 400
number of threads: 1
maximum number of tries: 1
duration: 600s
number of transactions actually processed: 6267661
number of failed transactions: 0 (0.000%)
latency average = 380.932 ms
initial connection time = 2743.666 ms
tps = 1050.056725 (without initial connection time)
```

**Test case 3:** *Duration: 10 min, Work_mem: 983kB, Connection: 800*

```
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 684
query mode: simple
number of clients: 800
number of threads: 1
maximum number of tries: 1
duration: 600s
number of transactions actually processed: 503018
number of failed transactions: 0 (0.000%)
latency average = 946.455 ms
initial connection time = 5986.173 ms
tps = 845.259690(without initial connection time)
```

**Test case 4**: *Duration: 10 min, Work_mem: 655kB, Connection: 1200*

```
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 684
query mode: simple
number of clients: 1200
number of threads: 1
maximum number of tries: 1
duration: 600s
number of transactions actually processed: 456771
number of failed transactions: 0 (0.000%)
latency average = 1594.282 ms
initial connection time = 8603.632 ms
tps = 752.690056(without initial connection time)
```

**Conclusion:**

Sometime increasing the connections at database level will not solve the problem of required more connections. We have plan, check the memory allocated to database server and how much we can extend to support the increased max_connections value else use connection pooling either database level (pg-pool or pg-bouncer) or application level (driver based connection pooling eg. JDBC we are using [***hikari\*** ](https://github.com/brettwooldridge/HikariCP)connection pool) with proper value of maxpool size , min idle, idletimeout and maxlifetime of connections.
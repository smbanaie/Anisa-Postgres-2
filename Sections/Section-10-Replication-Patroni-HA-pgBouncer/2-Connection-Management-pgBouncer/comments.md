### Introduction to PgBouncer, HAProxy, and PostgreSQL Configurations

#### PgBouncer:
PgBouncer is a lightweight connection pooler for PostgreSQL. It is designed to reduce the overhead of managing many client connections by pooling them, which improves performance and resource utilization. In this setup:
- **PgBouncer**: Connects to the `postgres-master` and listens on port 6432.
- **PgBouncer-Slave**: Connects to the `postgres-slave` and listens on port 6433.
- **Connection Pooling Mode**: Configured to operate in `transaction` mode, where a connection is assigned to a client for the duration of a transaction, then returned to the pool.

#### HAProxy:
HAProxy is a high-performance TCP/HTTP load balancer. It is used to distribute client connections across multiple servers to ensure high availability and reliability. In this setup, the HAProxy configuration is as follows:

```plaintext
global
    daemon
    maxconn 1000

defaults
    mode tcp
    timeout connect 10s
    timeout client 30m
    timeout server 30m

frontend psql-master
    mode tcp
    bind *:6000
    default_backend psql-master-back

frontend psql-slaves
    mode tcp
    bind *:6010
    default_backend psql-slaves-back

backend psql-master-back
    mode tcp
    option tcp-check
    server master pgbouncer:6432 check port 6432 inter 2s rise 2 fall 2 maxconn 100

backend psql-slaves-back
    mode tcp
    server slave1 pgbouncer-slave:6433 check port 6433 inter 2s rise 2 fall 2 maxconn 100

listen stats
    bind *:6404
    mode http
    stats enable
    stats uri /
    stats refresh 5s
```

- **Global Section**: Sets global HAProxy options, such as running as a daemon and setting the maximum number of connections to 1000.
- **Defaults Section**: Specifies default settings for all the following sections, including TCP mode and various timeouts.
- **Frontend Sections**: Defines the entry points for client connections:
  - `psql-master` listens on port 6000 and directs traffic to `psql-master-back`.
  - `psql-slaves` listens on port 6010 and directs traffic to `psql-slaves-back`.
- **Backend Sections**: Specifies the actual servers to which frontend sections direct traffic:
  - `psql-master-back` routes traffic to `pgbouncer` on port 6432.
  - `psql-slaves-back` routes traffic to `pgbouncer-slave` on port 6433.
- **Stats Section**: Enables a statistics page on port 6404, providing an HTTP interface for monitoring.

#### PostgreSQL Configurations:
The PostgreSQL configurations in this Docker Compose file are optimized for performance and replication.

- **General Configurations**:
  - **POSTGRESQL_SHARED_PRELOAD_LIBRARIES**: Loads extensions like `pg_stat_statements` and `pg_repack`.
  - **POSTGRESQL_SHARED_BUFFERS**: Set to 4GB, which is the amount of memory the server uses for shared memory buffers.
  - **POSTGRESQL_WORK_MEM**: Set to 16MB, used for internal sort operations and hash tables before writing to temporary disk files.
  - **POSTGRESQL_MAINTENANCE_WORK_MEM**: Set to 1GB, used for maintenance operations like VACUUM, CREATE INDEX, and ALTER TABLE ADD FOREIGN KEY.
  - **POSTGRESQL_EFFECTIVE_CACHE_SIZE**: Set to 6GB, an estimate of the memory available for disk caching by the operating system and within the database itself. The `POSTGRESQL_EFFECTIVE_CACHE_SIZE` parameter in PostgreSQL configuration is an estimate of how much memory is available for disk caching by the operating system and within the database itself. It is used by PostgreSQL's query planner to make more informed decisions about which execution plans to use, by providing an idea of how much cache is available for buffering I/O
  - **POSTGRESQL_MAX_CONNECTIONS**: Set to 200, the maximum number of concurrent connections to the database server.
  - **POSTGRESQL_WAL_BUFFERS**: Set to 16MB, the amount of memory allocated for write-ahead log (WAL) data.
  
- **Replication Settings**:
  - **POSTGRESQL_REPLICATION_MODE**: Defines the mode as `master` for `postgres-master` and `slave` for `postgres-slave`.
  - **POSTGRESQL_REPLICATION_USER**: The username for replication.
  - **POSTGRESQL_REPLICATION_PASSWORD**: The password for the replication user.
  - **POSTGRESQL_MASTER_HOST**: The hostname of the master server for the slave to connect to.
  - **POSTGRESQL_MASTER_PORT_NUMBER**: The port number of the master server.

- **Archiving Settings**:
  - **POSTGRESQL_ARCHIVE_MODE**: Enabled to allow WAL archiving.
  - **POSTGRESQL_ARCHIVE_COMMAND**: Defines the command to archive WAL files.

- **Additional Extensions**:
  - The commands ensure that `pg_stat_statements` and `pg_repack` extensions are created in the `CRAWL_DB`.

This configuration creates a robust PostgreSQL environment with connection pooling, load balancing, and optimized performance settings, ensuring high availability and efficient resource utilization.

Here's a table of important PostgreSQL performance parameters along with their recommended values and a brief explanation of each:

| Parameter                      | Recommended Value             | Description                                                  |
| ------------------------------ | ----------------------------- | ------------------------------------------------------------ |
| `shared_buffers`               | 25-40% of total RAM           | Amount of memory the database server uses for shared memory buffers. Helps in reducing disk I/O by keeping more data in memory. |
| `effective_cache_size`         | 50-75% of total RAM           | An estimate of how much memory is available for disk caching by the operating system and within PostgreSQL. Guides the query planner in making better decisions. |
| `work_mem`                     | 2-4% of total RAM per session | Memory used for internal sort operations and hash tables before writing to temporary disk files. Should be set higher for complex queries. |
| `maintenance_work_mem`         | 1-2GB                         | Memory used for maintenance operations like VACUUM, CREATE INDEX, and ALTER TABLE ADD FOREIGN KEY. Higher values can speed up these operations. |
| `wal_buffers`                  | 16-64MB                       | Amount of memory allocated for write-ahead log (WAL) data. Should be set higher for systems with heavy write loads. |
| `max_connections`              | 100-200                       | Maximum number of concurrent connections to the database server. Needs to balance with available resources and connection pooling solutions. |
| `checkpoint_completion_target` | 0.7-0.9                       | Fraction of the checkpoint interval that PostgreSQL should spend writing checkpoints. Higher values can smooth I/O spikes. |
| `default_statistics_target`    | 100-200                       | Controls the level of detail in the planner's statistics. Higher values can improve query planning but increase the time for ANALYZE operations. |
| `random_page_cost`             | 1.1-2.0 (SSD)                 | Cost estimation of a non-sequentially fetched disk page. Lower values for SSDs, higher for spinning disks. |
| `seq_page_cost`                | 1.0                           | Cost estimation of a sequentially fetched disk page. Typically set to 1.0. |
| `autovacuum_naptime`           | 60s                           | Time to sleep between autovacuum runs. Adjust based on the workload and database size. |
| `effective_io_concurrency`     | 2-4 (SSD)                     | Number of simultaneous requests that can be handled efficiently by the disk subsystem. Higher for SSDs and advanced storage systems. |

### Quick Explanations

- **shared_buffers**: This parameter defines how much memory PostgreSQL can use for caching data. Setting this too high can leave insufficient memory for other processes.
  
- **effective_cache_size**: Helps PostgreSQL's query planner estimate how much memory is available for caching. A higher value can lead to more efficient query plans.

- **work_mem**: Used for internal operations like sorting and hash tables. Setting this higher can speed up complex queries but may lead to excessive memory usage if too many sessions use it simultaneously.

- **maintenance_work_mem**: Used during maintenance tasks such as VACUUM, CREATE INDEX, and ALTER TABLE. Higher values can make these tasks faster.

- **wal_buffers**: This parameter sets the amount of memory for write-ahead logging. Higher values are beneficial for write-heavy workloads.

- **max_connections**: Sets the maximum number of concurrent connections. Too high a value can lead to excessive resource consumption, while too low can limit scalability.

- **checkpoint_completion_target**: Adjusts how aggressively PostgreSQL writes out data during checkpoints, smoothing out I/O spikes. The `checkpoint_completion_target` is a fraction of the checkpoint interval (`checkpoint_timeout`), which is the time PostgreSQL waits before starting a new checkpoint.

  ***For example, with a `checkpoint_completion_target` of 0.8 and a `checkpoint_timeout` of 5 minutes, PostgreSQL aims to complete the checkpoint within 80% of the 5 minutes (i.e., 4 minutes)***

- **default_statistics_target**: Determines the amount of data collected for query planning. Higher values can improve query planning at the cost of longer ANALYZE times.

- **random_page_cost**: Affects the planner's cost estimate for non-sequential page fetches. Lower for SSDs due to faster random access times.

- **seq_page_cost**: Affects the planner's cost estimate for sequential page fetches. Generally set to 1.0 as a baseline.

- **autovacuum_naptime**: Sets how often the autovacuum process runs. Frequent runs can keep tables clean but add overhead.

- **effective_io_concurrency**: Helps optimize parallel I/O operations. Higher values are better for systems with SSDs and advanced storage systems.
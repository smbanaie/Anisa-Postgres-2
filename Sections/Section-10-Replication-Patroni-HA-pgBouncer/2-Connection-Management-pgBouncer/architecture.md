### Architecture

```plaintext
                                    +-------------+
                                    |             |
                                    |   Client    |
                                    |             |
                                    +------+------+ 
                                           |
                                           |
                                    +------v------+
                                    |             |
                                    |   HAProxy   |
                                    |             |
                                    +------+------+
                                           |
                                           |
                    +----------------------+----------------------+
                    |                                             |
                    |                                             |
          +---------v--------+                         +----------v--------+
          |                  |                         |                   |
          |   PgBouncer      |                         |   PgBouncer-Slave |
          |                  |                         |                   |
          +--------+---------+                         +---------+---------+
                   |                                             |
                   |                                             |
        +----------v----------+                       +----------v----------+
        |                     |                       |                     |
        |   Postgres-Master   |                       |   Postgres-Slave    |
        |                     |                       |                     |
        +---------------------+                       +---------------------+
```

### Explanation:

1. **Client**: This represents the clients that will connect to your database through HAProxy.
2. **HAProxy**: This service balances the load between `pgbouncer` and `pgbouncer-slave`. It listens on ports 6000 and 6010.
3. **PgBouncer**: This service acts as a connection pooler for PostgreSQL master.
   - Connects to `postgres-master` on port 5432.
   - Exposes port 6432.
4. **PgBouncer-Slave**: This service acts as a connection pooler for PostgreSQL slave.
   - Connects to `postgres-slave` on port 5432.
   - Exposes port 6433.
5. **Postgres-Master**: The main PostgreSQL server with replication mode set to master.
   - Has multiple volumes for data, configuration, archive, backups, and scripts.
   - Has extensive environment configurations for PostgreSQL tuning and replication.
6. **Postgres-Slave**: The replicated PostgreSQL server with replication mode set to slave.
   - Has a volume for data.
   - Depends on `postgres-master`.

### Notes:
- The `depends_on` property ensures that the services start in a specific order.
- Each service is connected to a shared Docker network called `anisa_network`.
- Logging is configured for each service to limit the size and number of log files.
- `postgres-master` and `postgres-slave` use environment variables for sensitive data and configuration settings.

This setup ensures high availability and load balancing for PostgreSQL using `pgbouncer` and `haproxy`, with master-slave replication for redundancy.
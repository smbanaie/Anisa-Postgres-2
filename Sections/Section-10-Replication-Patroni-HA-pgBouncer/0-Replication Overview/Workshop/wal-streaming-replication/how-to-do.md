### 1. Preparing the Environment

#### Create a User:

```sql
CREATE USER replication_user REPLICATION LOGIN CONNECTION LIMIT 5 ENCRYPTED PASSWORD 'replica123';

```

#### Adjust `pg_hba.conf`:

Ensure that `pg_hba.conf` on both the primary and replica allows the replication user to connect. Add the following line:

```
host    replication_user    replication_user_ip/32    md5
```

### 2. Primary Server Configuration

#### Modify `postgresql.conf`:

Make the following changes in `postgresql.conf` on the primary server:

```conf
wal_level = replica
max_wal_senders = 10
wal_keep_size = 64
listen_addresses='*'
```

- `wal_level`: Set to `replica` to enable WAL streaming.
- `max_wal_senders`: Defines the maximum number of simultaneous connections from standby servers.
- `wal_keep_segments`: Defines the minimum number of WAL segments to keep for replication.

#### Sync Replication 

Postgres WAL replication is **asynchronous** by default however, it is possible to make streaming replication synchronous by setting the `synchronous_standby_names` 

```bash
synchronous_standby_names = 'replica_node'  or '*'
```

- `synchronous_standby_names`: Identifies the synchronous standby servers. 

  

Restart PostgreSQL after modifying the configuration.

#### Create a Basebackup 

```bash
pg_basebackup  -U replication_user -D /backup -P -Xs -c fast
```

- if not , the replica not be synced (` FATAL:  database system identifier differs between the primary and standby`)

### 3. Replica Server Configuration

- restore the backup
  - ***what about the new WAL file that are generating in real time?***
- create a `standby.signal` file 

#### Modify `postgresql.conf`:

Make the following changes in `postgresql.conf` on the replica server:

```conf
wal_level = replica
hot_standby = on
```

The parameters used are:

- **wal_level**: This is used to enable Postgres WAL replication/ streaming replication. The possible values here are replica, minimal, and logical.
- **wal_log_hints:** It is required for the pg_rewind capability, this helps when the standby server is out of sync with the master server.
- **max_wal_senders**: It is used to specify the maximum numbers of concurrent connections that can be established with the standby servers.
- **wal_keep_size**: Specifies the minimum size of past WAL files kept in the `pg_wal` directory, in case a standby server needs to fetch them for streaming replication. If a standby server connected to the sending server falls behind by more than `wal_keep_size` megabytes, the sending server might remove a WAL segment still needed by the standby, in which case the replication connection will be terminated. Downstream connections will also eventually fail as a result. (However, the standby server can recover by fetching the segment from archive, if WAL archiving is in use.)
- **hot_standby**: This parameter enables a read-only connection with the slave when it is set to ON.

Restart PostgreSQL after modifying the configuration.

### 4. Creating the Replication Slot

On the primary server, create a replication slot:

```sql
-- On the primary server
SELECT * FROM pg_create_physical_replication_slot('replica_slot');
```

### 5. Testing the Primary Server

Insert some sample data:

```sql
-- On the primary server
INSERT INTO job_seeker (id, name, skill) VALUES (2, 'Jane Doe', 'Python Developer');
```

### 6. Testing the Replica Server

#### Check the Replication Slot:

```sql
-- On the replica server
SELECT * FROM pg_replication_slots;

```

#### Start Replication:

On the replica server, create a `standby.signal` file in the data directory with the following content:

```conf
primary_conninfo = 'host=postgres_primary port=5432 user=replication_user password=replica123'
recovery_target_timeline = 'latest'
primary_slot_name = 'replica_slot'
```

Replace placeholders with the actual values.

### 7. Monitor Replication Status

Check the replication status on the primary server:

```sql
-- On the primary server
SELECT * FROM pg_stat_replication;
```

### 8. Verifying Synchronous Replication

On the primary server, insert data and ensure it's replicated synchronously:

```sql
-- On the primary server
INSERT INTO employer (id, name, industry) VALUES (2, 'SoftCorp', 'Software');
```

### Additional Notes:

- **`synchronous_standby_names`:**
  - Identifies the synchronous standby servers.
  - Set to the name of the standby server specified in the `primary_conninfo` on the replica.

  

This tutorial provides a basic setup for WAL Streaming Synchronous Replication in PostgreSQL. Adjust the configuration parameters based on your specific requirements and environment.



















### Create & Populate the DB

```sql
create database shopping; 
-- Table for Products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Table for Customers
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Table for Orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Order Details
CREATE TABLE order_details (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) NOT NULL,
    product_id INT REFERENCES products(product_id) NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL
);

```

- run `populate_db.py`

For this tutorial, let's assume you're using a sample shopping  database.

### 1. Preparing the Environment

#### Create a User:

```sql
CREATE ROLE replicator WITH REPLICATION LOGIN CONNECTION LIMIT 5;


CREATE USER replication_user WITH  REPLICATION ENCRYPTED PASSWORD 'replica123';
GRANT replicator TO replication_user;

```

#### Adjust `pg_hba.conf`:

- ***inspect container to get the replica actual address***

Ensure that `pg_hba.conf` on both the primary and replica allows the replication user to connect. Add the following line:

```
host    replication replication_user    172.18.0.4/32    md5
```

In the `pg_hba.conf` file, you can use various settings for authentication. The general syntax for an entry is as follows:

```plaintext
TYPE    DATABASE    USER    ADDRESS      METHOD
```

Here's what each field represents:

1. **`TYPE`:**

   - Specifies the connection type. Common values include:

     - `local`: Connections made using Unix domain sockets.

     - `host`: Connections made using TCP/IP.

     - `hostssl`: Connections made using SSL-encrypted TCP/IP.

     - `hostnossl`: Connections made using unencrypted TCP/IP.

       If you use just `host`, it allows both encrypted and non-encrypted connections, and it can be influenced by whether the client attempts to use SSL or not.

2. **`DATABASE`:**

   - Specifies the name of the PostgreSQL database to which the entry applies.
   - You can use `all` to match any database or specify a particular database name.

3. **`USER`:**

   - Specifies the PostgreSQL username to which the entry applies.
   - You can use `all` to match any username or specify a particular username.

4. **`ADDRESS`:**

   - Specifies the client's IP address or range of addresses.
   - You can use a specific IP address, a network in CIDR notation, or the keyword `all` to match any address.

5. **`METHOD`:**

   - Specifies the authentication method for the connection. Common methods include:
     - `trust`: No password is required; the connection is allowed.
     - `md5`: Requires MD5-encrypted passwords.
     - `password`: Requires plain-text passwords.
     - `reject`: Connection is rejected outright.
     - `cert`: Requires SSL certificate authentication.

### Example Entries:

- Allow local connections without password:

  ```plaintext
  local   all   all   trust
  ```

- Allow connections from a specific IP with MD5-encrypted password:

  ```plaintext
  host    all   all   192.168.1.2/32   md5
  ```

- Allow SSL-encrypted connections from any IP:

  ```plaintext
  hostssl   all   all   0.0.0.0/0   cert
  ```

### 2. Primary Server Configuration

#### Modify `postgresql.conf`:

Make the following changes in `postgresql.conf`:

```conf
listen_addresses = '*'
password_encryption = md5

wal_level = replica
max_replication_slots = 5
max_wal_senders = 5
```

- `wal_level`: Set to `replica` to enable wal streaming replication.

- `max_replication_slots`: Defines the maximum number of replication slots, adjust based on your needs.

  we will set the max_replication_slots to a minimum of the number of subscriptions that will connect, plus some reserve to account for table synchronization. This setting is not so easily changed on a running database because it will need a restart for changes to take effect, therefore it is often a good idea to set it a bit higher (the default of 10) to account for a growing system and future needs.

- `max_wal_senders`: Defines the maximum number of simultaneous connections from standby servers. The `max_wal_senders` setting should be equal to `max_replication_slots`, plus the number of physical replicas that will be connected simultaneously.

Restart PostgreSQL after modifying the configuration.

#### Create a Publication:

```sql
-- On the primary server select shopping db as the selected db (or \c in PSQL)
CREATE PUBLICATION shop_pub FOR TABLE products, customers, orders, order_details ;


SELECT * FROM pg_stat_replication;

# ALTER PUBLICATION shop_pub ADD TABLE aother_table;


```

### 3. Taking First Backup (Data/Schema)

### 4. Testing the Primary Server

Insert some sample data:

```sql
-- On the primary server
INSERT INTO job_seeker (id, name, skill) VALUES (1, 'John Doe', 'Java Developer');
```

Check the publication status:

```sql
-- On the primary server
SELECT * FROM pg_publication_tables;
```

### 5. Replica Server Configuration

#### Restoring Initial State:

If starting from a clean slate, you may consider taking a base backup:

```bash
pg_basebackup -h primary_host -U replication_user -D /path/to/replica/data -P -Xs -c fast
```

#### Modify `postgresql.conf`:

Make the same `wal_level`, `max_replication_slots`, and `max_wal_senders` modifications as on the primary server.

change the hba file same as before 

```bash
host    replication replication_user    172.18.0.2/32    md5  # primary

host    all             all             172.18.0.1/32            trust # Gateway/DBeaver

host    all             all             172.18.0.3/32            trust #PGAdmin
```



Restart PostgreSQL after modifying the configuration.

#### Create a Subscription:

```sql
-- On the replica server
CREATE SUBSCRIPTION shop_sub 
CONNECTION 'host=postgres_primary port=5432 dbname=shopping user=replication_user password=replica123' 
PUBLICATION shop_pub
WITH (slot_name = 'replica1', create_slot = true);
FOR ALL TABLES;
```

##### Error!

this entry specifically applies to replication connections. When the replica tries to establish a connection using the provided `CREATE SUBSCRIPTION` command, it is connecting as a regular user (`replication_user`), not as part of the replication process.

To resolve this issue, you can add a more general entry in `pg_hba.conf` to allow the specified user from the replica's IP address:

```bash
host    all             replication_user    172.18.0.4/32    md5

or

host    shopping             replication_user    172.18.0.4/32    md5
```

### Error!

SQL Error [42P01]: ERROR: relation "public.customers" does not exist

- restore the pg_basebackup output.
- or just create the database & tables and select it as the active one;



### 5. Testing the Replica Server

#### Check Subscription Status:

```sql
-- On the replica server
SELECT * FROM pg_stat_subscription;

-- On Primary
SELECT * FROM pg_replication_slots;

SELECT * FROM pg_stat_replication;

```

#### Insert More Data:

Insert data on the primary server and ensure it replicates to the replica.

#### Monitor Lag:

```sql
-- On the replica server
SELECT * FROM pg_replication_slots;
```

### 6. Using pgAdmin

1. **Check Publication Status in pgAdmin:**
   - Open pgAdmin and connect to the primary server.
   - Navigate to the primary server -> Databases -> your_database -> Publications.
   - You should see `my_publication` listed.

2. **Check Subscription Status in pgAdmin:**
   - Connect to the replica server in pgAdmin.
   - Navigate to the replica server -> Databases -> your_database -> Subscriptions.
   - You should see `my_subscription` listed.

### Additional Considerations:

- **wal_level:**
  - Set to `logical` to enable logical replication.
- **max_replication_slots:**
  - Represents the maximum number of replication slots available.
  - Ensure an adequate number for your setup.
- **max_wal_senders:**
  - Represents the maximum number of simultaneous connections from standby servers.
  - Adjust based on the number of replicas.

Remember to replace placeholders like `primary_host`, `your_password`, `mydatabase`, etc., with your actual values.

This tutorial provides a basic setup for logical replication in PostgreSQL. Adjust the configuration parameters based on your specific requirements and environment.

### Drop Subscription

```sql
DROP SUBSCRIPTION subscription_name;
```

```bash
created replication slot "shop_sub" on publisher
dropped replication slot "pg_16443_sync_16405_7340757556198154280" on publisher
dropped replication slot "pg_16443_sync_16414_7340757556198154280" on publisher
dropped replication slot "pg_16443_sync_16427_7340757556198154280" on publisher
dropped replication slot "pg_16443_sync_16398_7340757556198154280" on publisher
dropped replication slot "shop_sub" on publisher
```

#### - [Monitoring Lags](https://medium.com/@pawanpg0963/postgresql-remote-replica-lag-monitoring-a7eaec7faca0)


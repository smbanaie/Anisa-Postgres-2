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
CREATE ROLE replicator WITH REPLICATION LOGIN;
GRANT CONNECT ON DATABASE shopping TO replicator;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO replicator;
CREATE USER replication_user REPLICATION LOGIN CONNECTION LIMIT 5 ENCRYPTED PASSWORD 'replica123';

GRANT replicator TO replication_user;

```

#### Adjust `pg_hba.conf`:

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

wal_level = logical
max_replication_slots = 5
max_wal_senders = 5
```

- `wal_level`: Set to `logical` to enable logical replication.

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

#### Last Steps

- stop the replica ->
  -  **SELECT** * **FROM** **pg_stat_replication**;
  - **SELECT** * **FROM** **pg_replication_slots**;
  - **SELECT** **slot_name**, **confirmed_flush_lsn**, pg_current_wal_lsn(), (pg_current_wal_lsn() - **confirmed_flush_lsn**) **AS** *lsn_distance* **FROM** **pg_replication_slots**;
  - **What is replication lag?** we need to take a deeper look at the *_lsn columns. There are four, and it’s important to understand them:
    - sent_lsn
    - write_lsn
    - flush_lsn
    - replay_lsn
- stop the primary -> 
  - **SELECT** * **FROM** **pg_stat_subscription**;
- Add a new replica using the pg_dumpall

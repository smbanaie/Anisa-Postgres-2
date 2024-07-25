#### Enable Archiving in Master/Enable Restore Command in Replica/ Create Standby Server without the Primary Connection Info 

### 1. Setup the Master

- remove :
  - db data folders.
  - `archive` folder
  - `backup` folder

- run the `docker compose up postgres_primary`
- then change the following config : 

```bash
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'  # Unix

archive_command = 'copy "%p" "C:\\server\\archivedir\\%f"'  # Windows
```

disable `trust` mode in `hba` and add this Setting for `populate_db.py`  (use docker inspect tool & find out the gateway address - or just run the `populate.db` and check the error) to be work properly

```bash
host    all  all    172.18.0.1/32    md5
```

- Now stop & start primary again

  - check the `archive` folder : it must contains some wal files
  
    

- Create a Base Backup :

  ```bash
  docker exec -it postgres_primary bash
  su postgres
  pg_basebackup -D /backup/standalone-"$(date +%Y-%m-%dT%H-%M)" -c fast -P -R 
  ```

  

### 2. Setup the Replica

- restore the above backup & make sure that the `standby.signal`
- change this setting : 

```bash
restore_command = 'test ! -f %p && cp /archive/%f %p'
hot_standby = on
```

- start the replica : `docker compose up postgres_replica1`

### 6. Testing the Log Shipping

```bash
docker exec -it postgres_primary bash
su postgres
psql 

```

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

- **`trigger_file`:**
  - Specifies the location of the trigger file that can be used to promote the replica to become the primary.

This tutorial provides a basic setup for WAL Streaming Synchronous Replication in PostgreSQL. Adjust the configuration parameters based on your specific requirements and environment.











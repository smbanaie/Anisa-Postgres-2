### Log-Shipping Archiving Overview

 **- Enable Archiving in Master**

 **- Enable Restore Command in Replica**

 **- Create Standby Server without the Primary Connection Info** 

### 1. Setup the Master

- remove :
  - db data folders.
  - `archive` folder
  - `backup` folder

- run the `docker compose up `
- then change the following config in the `db_data_primary` folder: 

```bash
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'  # Unix

archive_command = 'copy "%p" "C:\\server\\archivedir\\%f"'  # Windows
```

disable `trust` mode in `hba` and add this Setting for `populate_db.py`  (use docker inspect tool & find out the gateway address - or just run the `populate.db` and check the error) to be work properly



```bash
host    all  all    172.18.0.1/32    md5  #Docker Gateway


```

- **Now stop & start primary again**

- check the `archive` folder : it must contains some WAL files


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

- **Create a Base Backup :**

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
recovery_target_timeline = 'latest'
```

- start the replica : `docker compose up postgres_replica1`

you will see some messages like this in the replica console :

```bash
postgres_replica1  | 2024-04-18 06:49:00.302 UTC [30] LOG:  completed backup recovery with redo LSN 0/20000F8 and end LSN 0/2071D80
postgres_replica1  | 2024-04-18 06:49:00.306 UTC [30] LOG:  consistent recovery state reached at 0/2071D80
postgres_replica1  | 2024-04-18 06:49:00.307 UTC [1] LOG:  database system is ready to accept read-only connections
postgres_replica1  | cp: cannot stat '/archive/000000010000000000000003': No such file or directory
postgres_replica1  | 2024-04-18 06:49:00.388 UTC [39] LOG:  started streaming WAL from primary at 0/3000000 on timeline 1
```



### 3. Monitor Replication Status

Check the replication status on the primary server:

```sql
-- On the primary server
SELECT * FROM pg_stat_replication;
```



### Replicator User

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


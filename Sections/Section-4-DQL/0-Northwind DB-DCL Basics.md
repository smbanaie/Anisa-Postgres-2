#### Load Northwind Database 



First we need to create the database

- `psql -f`

  ```bash
  $ psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE northwind;"
  $ cd "E:\Anisa\Sample DBs"
  $ psql -U postgres -d northwind -f northwind.sql
  $ psql -d postgres -U postgres -d northwind
  $ postgres=# \dt
  ```

  

- `psql -i`

  ```bash
  $ psql -d postgres -U postgres -d postgres
  postgres=# CREATE DATABASE northwind;
  postgres=# \c northwind
  postgres=# \i 'E:/Anisa/Sample DBs/northwind.sql'
  postgres=# \dt
  ```

  - note the `/` ans `'` single qoute around the path

- **DBeaver**

  - open ***dbeaver***, connect to the postgres, create a new DB namde `northwind`&  copy-paste the scripts and execute the sql file

- **pgAdmin**

  - open **pgAdmin**
  - create database `northwind`
  - right click on `northwind` and select `Query Tool`
  - copy & paste the SQL file contents

## Create Anisa User

create `anisa` user in `dbeaver` an assign the whole grant on some tables and not any grant on other ones. 

- create new connection or another terminal to login using these new credentials 
- try to test `\dt+` 
- insert or delete some records or select some  other ones and tell us what actually happens with this limited user. 

### System (invisible )Columns 

Here's a table with all the invisible columns in PostgreSQL along with a brief description:

| Column Name      | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| `ctid`           | The physical location of the row within its table (a compound of the file node number and the index within that file). |
| `xmin`           | The `TransactionId` of the transaction that inserted or updated the row most recently. |
| `xmax`           | The `TransactionId` of the transaction that deleted or updated the row most recently. 0 if the row is not deleted or updated. |
| `cmin`           | The `CommandId` of the command that inserted or updated the row most recently. |
| `cmax`           | The `CommandId` of the command that deleted or updated the row most recently. 0 if the row is not deleted or updated. |
| `xmin_committed` | The `TransactionId` of the transaction that marked the row as "committed" after it was inserted (used for `HOT` feature). |
| `xmin_visible`   | The oldest `TransactionId` that needs to see this row version (used for `HOT` feature). |
| `xmax_committed` | Similar to `xmin_committed` but for deleted or updated rows. |
| `xmax_visible`   | Similar to `xmin_visible` but for deleted or updated rows.   |
| `oid`            | The object identifier (OID) of the row, a unique identifier assigned to each row in a table. Not recommended for use as a primary key or foreign key. |

Note that these columns are not directly visible or accessible to users, as they are used internally by PostgreSQL for managing transactions, concurrency control, and other internal operations. They play a crucial role in ensuring the integrity and consistency of the database.

- run this query :

  ```sql
  select oid, ctid, xmin_visible , *
  from orders; 
  ```

  
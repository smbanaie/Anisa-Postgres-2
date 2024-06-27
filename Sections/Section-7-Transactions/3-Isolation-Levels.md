## [Transaction Isolation in PostgreSQL](https://pgdash.io/blog/postgres-transactions.html)

How isolation levels affect transaction behavior

PostgreSQL comes with solid, time-tested features that lets you define exactly what should happen when multiple clients try to update the same data concurrently. One of them is the isolation level of transactions.

Read on to learn more about how transaction isolation works in PostgreSQL.

### Transactions and Isolation Level

Transactions are the fundamental way to mutate data in an RDBMS. Modern RDBMS allow more than one transaction to run concurrently, and consequently come with a variety of tools – some standard, some RDBMS-specific – for application developers to specify how their transactions should or should not interact with other transactions.

Transaction isolation levels and pessimistic locks are two such tools. Although these are necessary for data integrity and performance, they are unfortunately not intutive to understand or use.

The isolation level of a transaction, in PostgreSQL, can be one of:

- **Read Committed**
- **Repeatable Read**
- **Serializable**

Every transaction has it’s isolation level set to one of these when it is created. **The default level is “read committed”.**

>  Note that the SQL standard also defines “read uncommitted”, which is not supported in Postgres. You have to use the nearest, higher level of “read committed”.

Let’s see what these levels mean.

### Read Committed

What happens when one (unfinished) transaction inserts rows in a table and the other (also unfinished) transaction tries to read all rows in the table? If the second transaction is able to see the rows inserted by the first, then that read is called a **dirty read** – because the first transaction can rollback and the second transaction would have read “phantom” rows that never existed.

The *read committed* isolation level guarantees that dirty reads will never happen. Here is an example:

<iframe src="https://asciinema.org/a/199567/iframe?" id="asciicast-iframe-199567" name="asciicast-iframe-199567" scrolling="no" allowfullscreen="true" style="box-sizing: border-box; overflow: hidden; margin: 0px; border: 0px; display: inline-block; width: 750px; visibility: visible; height: 370px;"></iframe>

- Open 2 Postgres connections

- run this in one of them :

  - ` create table t(int a, int b);` 

- run this in Window #1

  ```sql 
  begin;
  
  insert into t values(1,100);
  
  ```

  

- in the Window#2

  ```sql
  select * from t ; 
  ```

- in the Window#1

  ```sql
  commit; 
  ```

  

As you can see, the second transaction could not read the first transaction’s as-yet-uncommitted data. ***In PostgreSQL, it is not possible to lower the isolation level to below this level so that dirty reads are allowed.***

### Repeatable Read

Yet another problem is that of non-repeatable reads. These happen when a transaction reads a row, and then reads it again a bit later but gets a different result – because the row was updated in between by another transaction. The read has become **non-repeatable**, as shown in this example:

<iframe src="https://asciinema.org/a/199568/iframe?" id="asciicast-iframe-199568" name="asciicast-iframe-199568" scrolling="no" allowfullscreen="true" style="box-sizing: border-box; overflow: hidden; margin: 0px; border: 0px; display: inline-block; width: 750px; visibility: visible; height: 370px;"></iframe>


- Open 2 Postgres connections

- run this in one of them :

  - ` create table t(int a, int b);` 

- run this in Window #1

  ```sql 
  begin;
  
  select * from t ; 
  
  ```

  

- in the Window#2

  ```sql
  begin ; 
  
  select * from t ; 
  
  update t set b = 20 where a=1; 
  
  commit; 
  ```

- in the Window#1

  ```sql
  select * from t ; 
  ```

  - **See the Issue?** 

    - To fix this problem, set the isolation level of the transaction to “repeatable read”. 
    
    - Start Over and this time set Isolation level to repeatable read : 
    
      ```sql
      begin transaction isolation level repeatable read ; 
      .....
      
      ```
    
      

Note that the isolation level was specified along with the [BEGIN](https://www.postgresql.org/docs/10/static/sql-begin.html) statement. It is also possible to specify this at connection level (as a connection parameter), as a configuration paramter (`default_transaction_isolation`) and using the [SET TRANSACTION](https://www.postgresql.org/docs/10/static/sql-set-transaction.html) statement.

### Serializable

The next isolation level addresses the problem of **lost updates**. Updates performed in one transaction can be “lost”, or overwritten by another transaction that happens to run concurrently, as shown here:

<iframe src="https://asciinema.org/a/199573/iframe?" id="asciicast-iframe-199573" name="asciicast-iframe-199573" scrolling="no" allowfullscreen="true" style="box-sizing: border-box; overflow: hidden; margin: 0px; border: 0px; display: inline-block; width: 750px; visibility: visible; height: 370px;"></iframe>

Here the second transaction’s UPDATE blocks, because PostgreSQL places a lock to prevent another update until the first transaction is finished. However, the first transaction’s change is lost, because the second one “overwrote” the row.

- Open 2 Postgres connections

- run this in one of them :

  - ` create table t(int a, int b);` 

- run this in Window #1

  ```sql 
  begin;
  
  select * from t ; 
  
  update t set b = 200 where a=1; 
  ```

  

- in the Window#2

  ```sql
  begin;
  
  select * from t ; 
  
  update t set b = 300 where a=1; 
  
  ```

- in the Window#1

  ```sql
  commit ; 
  ```

- in the Window#2

  ```sql
  commit; 
  
  select * from t ; 
  
  ```

  

- in the Window#1

  ```sql
  select * from t ;
  ```

  

- If this sort of behavior is not acceptable, you can upgrade the isolation level to serializable:



<iframe src="https://asciinema.org/a/199575/iframe?" id="asciicast-iframe-199575" name="asciicast-iframe-199575" scrolling="no" allowfullscreen="true" style="box-sizing: border-box; overflow: hidden; margin: 0px; border: 0px; display: inline-block; width: 750px; visibility: visible; height: 370px;"></iframe>

- set the transaction level :`serializable`
- start over and see the Error. 

At this level, the commit of the second transaction fails. The second transaction’s actions were based on facts that were rendered invalid by the time it was about to commit.

While serialization provides the highest level of safety, it also means that the application has to detect such commit failures and retry the entire transaction.
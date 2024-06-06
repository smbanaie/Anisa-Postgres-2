# An Introduction to PostgreSQL Concurrency Control

As a long-time database consultant, I’ve fixed more blocking problems in database systems than I can count. Often this blocking has resulted from conflicts between processes needing to read rows while those rows are being modified.

PostgreSQL uses an optimistic isolation system known as Multi-Version Concurrency Control (MVCC). MVCC ensures transactions writing data to the database don’t block concurrent transactions needing to read the data being modified. This works through the magic of row-versioning—PostgreSQL creates versions of rows in the database tables to minimize blocking from concurrent access. As more and more versions are generated, a garbage control mechanism called VACUUM must be used to ensure the tables are properly maintained. In this article, I’ll explain how all this works via a series of examples.

## Some Background Internals

PostgreSQL uses the Read Committed transaction isolation level as the default isolation level, and the SQL examples below assume this is the isolation level being used. The others in the SQL standard are read uncommitted, repeatable read, and serializable. You can read more about them and their various possible behaviors (like nonrepeatable reads and phantom reads) [here](https://www.postgresql.org/docs/current/transaction-iso.html).

Every transaction occurring on a PostgreSQL installation is assigned a unique numeric identifier. This identifier is a 32-bit integer and monotonically increases as transactions occur. You can use the function txid_current () to find the current transaction ID. Note that calling this function increases the transaction ID of the database.



``````sql
select txid_current();
``````





![Select txid_current](images\02_5F00_Select-txid_5F00_current.png)

The reason this transaction ID is important to know about is because it’s used to keep track of which rows are visible to the PostgreSQL MVCC system.

The code below creates a table that will be used for all the examples in this article. Notice the autovacuum_enabled flag on the table is explicitly set to off—more on this later.



```sql
create table mvcctable 
(
idcol integer,
valcol char (255)
) with (autovacuum_enabled = off);

create index idx_mvcctable on mvcctable (idcol);
```



The following code will insert 100,000 rows into the mvcctable, with the idcol containing an increasing set of values and the valcol containing a randomly generated string value:



```sql
insert into mvcctable (idcol, valcol)
select *, substr (md5 (random ()::text), 0, 255)
from generate_series (1, 100000);
```



Rows in a table are either a current row (called ‘alive’) or a previous version that is no longer needed (called ‘dead’). The pg_stat_user_tables system table can be queried to find the number of live and dead rows for a given table. The following code queries the system table to show how many alive and dead rows are in the mvcctable:



```sql
select 
relname as tablename,
n_live_tup as livetuples,
n_dead_tup as deadtuples
from
pg_stat_user_tables
where
relname = 'mvcctable';


```





![pg_stat_user_table](images\03_5F00_pg_5F00_stat_5F00_user_5F00_table.png)

Tables in PostgreSQL have several hidden system columns, including:

- **tableoid**: the object identifier of the table
- **xmin**: the transaction ID of the transaction causing the row to be created (either through an insert or update)
- **xmax**: the transaction ID of the transaction causing the row to be marked for eventual deletion (either through a delete or an update)
- **ctid**: the physical location of the row in the table (page number and row index number on the page)

The following query returns all the rows from the mvcctable along with four hidden system columns:



```sql
select
tableoid,
xmin,
xmax,
ctid,
*
from
mvcctable;
```



![mvcctable1](images\04_5F00_mvcctable1.png)

You can see the transaction identifier was set to 104472 for the first transaction that inserted the original 100,000 rows into this table. None of these records have been modified yet, so the xmax values are set to 0.

One final piece of background information is you can use the pg_size_pretty function and pass in the name of the table to find the table size. The following code shows this for the mvcctable:



```sql
select pg_size_pretty(pg_relation_size('mvcctable'));
```



![results1 table](https://thwack.solarwinds.com/resized-image/__size/2094x1456/__key/communityserver-blogs-components-weblogfiles/00-00-00-00-78/05_5F00_results1-table.png)

## MVCC in Action

The simple test scenario to show MVCC in action is to **have two connection windows**; in the first window, start an explicit transaction and run an update command on rows without committing the transaction, and in the second window, run a select statement to see what happens when there’s a concurrent update.

The code for the first window is below. It updates the first 100 rows of the mvcctable to set the valcol to ‘newvalue’ and then leaves the transaction open:



```sql
begin;
update mvcctable 
set valcol = 'newvalue'
where idcol <= 100;
```



The select query for the second window selects the first 100 rows:



```sql
select * 
from mvcctable 
where idcol <= 100;
```







![mvcctable Selected Rows](images\06_5F00_mvcctable-Selected-Rows.png)

The query returns instantly and returns the state of the 100 rows *PRIOR* to the other transaction updating them (as read committed doesn’t allow ‘dirty reads,’ and in fact, Postgres doesn’t allow them even if read uncommitted is used). The magic of MVCC is it compares the current transaction ID of the database to the xmin and xmax values for the rows being queried in the mvcctable and returns the correct ones. As the updating transaction hasn’t been committed yet, the second query isn’t permitted to see the updated rows.

Back in the first window, with the still-open transaction, I’ll run the code below:



```sql
select
tableoid,
xmin,
xmax,
ctid,
*
from
mvcctable
order by idcol asc;
```



![mvcctable Min Max Values](images\07_5F00_mvcctable-Min-Max-Values.png)

You can see the rows with idcol values 1 through 100 have had their valcol value updated to ‘newvalue’ and **have a new xmin value, which represents the transaction ID of the still-open transaction which inserted those new versions**. ***The ctid values (page number and row index on the page) have also been updated to represent the location of the new records***. MVCC made sure this query returned the new rows and didn’t see the old versions.

And then if I run the same code in the second window:



```sql

select
tableoid,
xmin,
xmax,
ctid,
*
from
mvcctable
order by idcol asc 
```





![mvcctable Original 100 Rows](images\08_5F00_mvcctable-Original-100-Rows.png)

You can see the original 100 rows have an xmax value of transaction ID 104511, which is the same transaction ID in the xmin column for the 100 new rows from the update statement.

Finally, I’ll commit the transaction in the first window:



```sql
commit;
```

And now, in the second window, retry the select again:

```sql
select
tableoid,
xmin,
xmax,
ctid,
*
from
mvcctable
order by idcol asc;
```

![mvcctable Updated Rows](images\09_5F00_mvcctable-Updated-Rows.png)

You can see now the updating transaction has committed; MVCC ensures only the updated rows are visible. **The old versions of the rows, which are now marked as deleted, are no longer visible to any transactions**—they’re now ‘dead.’ However, these rows are *STILL* in the table and will remain in the table until the VACUUM process happens.

Querying pg_stat_user_tables again shows there are now 100 dead rows in the mvcctable:



```sql
select 
relname as tablename,
n_live_tup as livetuples,
n_dead_tup as deadtuples
from
pg_stat_user_tables
where
relname = 'mvcctable';
```





![pg_stat_user_tables1](images\10_5F00_pg_5F00_stat_5F00_user_5F00_tables1.png)

## **The VACUUM Process**

**When a row is modified in a PostgreSQL table, it’s marked as deleted**. *After its xmax value is older than the system transaction ID and the updating transaction has committed, it’s no longer needed and can be removed*. However, removal of dead rows is not automatic. **The VACUUM process is responsible for reclaiming the space used by the dead rows in a table**. VACUUM also has options to perform other maintenance tasks such as updating the statistics for the indexes associated with the table, updating Visibility Maps to speed up index-only scans as well as providing protection when the transaction ID values in a PostgreSQL instance exhaust the 32-bit integer value and must wrap around. There are several options for vacuuming.

### **Standard VACUUM**

**The standard VACUUM process scans a table, marking rows no longer needed as free space**. (Note if no table name is specified, VACUUM removes dead rows for all tables in the database.) **This space can then be reused for inserted/updated data, but the space isn’t returned to the OS**—the table doesn’t shrink in size. VACUUM will typically generate a large amount of I/O, which can cause performance issues for active sessions. The table structure can’t be modified while running VACUUM. In most cases, you’ll not need to use this in production environments as the autovacuum daemon takes care of this work instead.

### **The Autovacuum Daemon**

The [autovacuum daemon](https://www.postgresql.org/docs/14/routine-vacuuming.html) is a multi-threaded background process automating the execution of the VACUUM command to keep table statistics up-to-date, which is critical for the query optimization engine (the Planner) to create accurate execution plans. The autovacuum daemon is optional to use but is the right choice for cleaning up dead rows and updating statistics in most cases. It’s ‘on’ by default, and it’s recommended to keep it on. This process works by finding tables incurring a large amount of insert/update/delete activity and then running the VACUUM and ANALYZE processes against those tables. Because this process relies on the collection of database activity information, the track_counts system setting is required for the autovacuum daemon to run. The overhead of this process is typically low, and it generally doesn’t block other session activity. There are several configuration options for autovacuum, which are explained [here](https://www.postgresql.org/docs/current/runtime-config-autovacuum.html).

### **VACUUM FULL**

The VACUUM FULL process is used to shrink a table to its minimum size and return the disk space to the OS. Generally, this version of VACUUM is only needed for specific tables containing mostly dead rows—such as an ETL staging table. This isn’t a process that should be regularly used for several reasons. First, for normal transactional processing tables, it’s not typically necessary to release the space allocated to dead rows back to the OS. This space will be needed again by the table eventually. Second, this process always creates a copy of the table and new indexes for it and will always touch all the data in the table, not only the dead rows. Because of the copying of the data into a new set of heap and index structures, the table is locked for the duration of the operation. This can be a significant problem for tables expecting concurrency during normal transaction processing. It’s much better to have a scheduled standard VACUUM or rely on the autovacuum daemon.

## VACUUM Example

Now I’ll build on the previous example and show how VACUUM can affect table size and the number of dead rows. Querying pg_stat_user_tables and pg_size_pretty shows the mvcctable has 100,000 rows and 100 of them are marked as dead, and the table is 29MB in size:

```sql
select 
relname as tablename,
n_live_tup as livetuples,
n_dead_tup as deadtuples
from
pg_stat_user_tables
where
relname = 'mvcctable';


```





![VACUUM pg_stat_user_tables1](images\11_5F00_VACUUM-pg_5F00_stat_5F00_user_5F00_tables1.png)



```sql
select pg_size_pretty(pg_relation_size('mvcctable'));
```



![pg_size_pretty](images\12_5F00_pg_5F00_size_5F00_pretty.png)

The following update statement creates 50,000 more dead rows in the table:

```sql
update mvcctable
set valcol = 'MassiveUpdate'
where idcol <= 50000;
```



Querying pg_size_pretty again shows the mvcctable has grown to 43MB in size:

```sql
select pg_size_pretty(pg_relation_size('mvcctable'));
```



![pg_size_pretty 43MB](images\13_5F00_pg_5F00_size_5F00_pretty-43MB.png)

Usually, the autovacuum process would kick in and clean up the dead rows, but when I created the table, I disabled the daemon from working on this table by setting the autovacuum_enabled option to off.

The following code runs the VACUUM process for the mvcctable:

```sql
vacuum mvcctable;
```



And querying pg_stat_user_tables again shows all the dead rows have been removed:

```sql
select 
relname as tablename,
n_live_tup as livetuples,
n_dead_tup as deadtuples
from
pg_stat_user_tables
where
relname = 'mvcctable';
```





![VACUUM pg-stat-user-tables1 Without Dead Rows](images\14_5F00_VACUUM-pg_2D00_stat_2D00_user_2D00_tables1-Without-Dead-Rows.png)

However, the table is still the same size:



```sql
select pg_size_pretty(pg_relation_size('mvcctable'));
```





![VACUUM pg_size_pretty](images\15_5F00_VACUUM-pg_5F00_size_5F00_pretty.png)

This is expected, as the standard VACUUM only removes dead rows from the table so the space can be reused by the table—it doesn’t give any space back to the OS. To do this, and you should RARELY need to do this, you can use the VACUUM FULL command, as shown below:



```sql
vacuum full mvcctable;
```



And now the table has been shrunk down to its original size:



```sql
select pg_size_pretty(pg_relation_size('mvcctable'));
```



![pg_size_pretty Shrunk to Original Size](images\16_5F00_pg_5F00_size_5F00_pretty-Shrunk-to-Original-Size.png)

## **PostgreSQL Concurrency Control Summary**

PostgreSQL leverages Multi-Version Concurrency Control for optimistic isolation to ensure writers don’t block readers and readers don’t block writers. To facilitate this, modified rows are marked with the transaction ID of the transaction that changed them. Transactions then compare their transaction IDs to the transaction IDs of the rows requested to see which rows are valid to be read. The VACUUM process is then used to remove the dead rows from the table, so the space can be reused.

As PostgreSQL databases continue to grow in size and complexity, so does the need to keep track of all that’s going on in these environments. [SolarWinds Database Mapper](https://www.sentryone.com/products/sentryone-document) is built to help you automate and maintain updated database documentation, create data dictionaries, and track data origin with data lineage and impact analysis to more easily ensure compliance with business rules and data privacy regulations.
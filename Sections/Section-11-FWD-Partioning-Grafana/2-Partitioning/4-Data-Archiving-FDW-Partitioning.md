# [Data archive solution in PostgreSQL](https://medium.com/@pawanpg0963/data-archive-solution-in-postgresql-6f6a96ccda03)

[PAWAN SHARMA](https://medium.com/@pawanpg0963?source=post_page-----6f6a96ccda03--------------------------------)

> Waiting from long time to write something for community. finally today I am here with this article not sure if this will help others or not.
>
> There are multiple options to archive the data , the data which is rarely or sometime used by the application team in different cases and the most common cases are, which I have figured out that the most of the application team will keep the last year or the older data for auditing purpose. where we perform the very less **INSERT** or **UPSERT** and mostly **SELECT’s** queries to fetch the data.

![Single DB Instance with three partition tables](images\1)

How to archive data for such use cases.

1. *Partition’s table approach, where will detach the partition which is not in used.*
2. *Take a backup and keep it safe for longer duration and restore it if there is a need in future.*
3. *Create a separate DB cluster, take a dump and restore the data.*
4. *There is another approach to archive the date using partition tables using FDW.*

![Each Partition data is archived to seperate DB](images\2.png)

**Advantages of partition based FDW data archive solution.**

1. ***Single Endpoint(hostname) for application:\*** *Using this approach the hostname or application DB endpoint will always remain same.*
2. ***Backup size will reduce:\*** *We can take backup of each instance separately. which will help to reduce the backup size*
3. ***Restore Time will reduce:\*** *In case of any issue we can quickly bring up the DB cluster (Instance 1) with partition table_2023.*
4. ***Operational efforts will reduce.\*** *Keeping the distribute data on each shards, the operational day to day efforts will reduce.*
5. *Using this approach we can easily perform any kind of transaction like select/insert /update and delete directly through app.*
6. *Easy to Delete/Drop the unused data.*

**How ?**

1. *Create FDW extension on instance1.*

```
// Instance1

CREATE DATABASE appdb;

CREATE TABLE EMP(id INT, name TEXT, time TIMESTAMP NOT NULL ) PARTITION BY RANGE (time);

CREATE TABLE EMP_2023 PARTITION OF EMP for values from ('2023-01-01') to ('2023-12-31') ;

CREATE EXTENSION postgres_fdw;
```

*2. Create Foreign server and user mapping on instance1 for accessing the instance2 and instance3.*

```
CREATE SERVER instance2 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'postgres2', dbname 'dblab', port '5432');
CREATE SERVER instance3 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'postgres3', dbname 'dblab', port '5432');


CREATE USER MAPPING FOR postgres SERVER instance2 OPTIONS (user 'postgres', password 'postgres123');
CREATE USER MAPPING FOR postgres SERVER instance3 OPTIONS (user 'postgres', password 'postgres123');


```

*3. Create child partition table on instance2 and instance3 respectively.*

```
CREATE TABLE EMP_2021 (id INT, name TEXT, time TIMESTAMP NOT NULL );  // Instance2

CREATE TABLE EMP_2022 (id int, name text, time TIMESTAMP NOT NULL);   // Instance3
```

*4. Create a foreign table on instance1.*

```
CREATE FOREIGN TABLE EMP_2021 PARTITION OF EMP for values from ('2021-01-01') to ('2021-12-31') SERVER instance2;

CREATE FOREIGN TABLE EMP_2022 PARTITION OF EMP for values from ('2022-01-01') to ('2022-12-31') SERVER instance3;
```

*5. Dump the data of partition emp_2021 and partition emp_2022 from instance1 and restore it on instance2 and instance3 respectively.*

Using the above approach you can access the data of each partition from instance1 and whenever purge of data is required for unused partitions. Decommission that particular instance without affecting the other partition tables.

```sql

insert into emp values(1, 'Ali', '2021-01-25');

insert into emp values(2, 'Zahra', '2022-06-25');

insert into emp values(3, 'Saman', '2023-11-25');
```





**Conclusion:**

> There are multiple options and ways to archive data in market, but according the future requirement of your data and business cases, we can decide which approach we have used to archive our data. so that we can fulfill the business requirements quick and with less operational efforts.

*Thanks you for reading the article…*
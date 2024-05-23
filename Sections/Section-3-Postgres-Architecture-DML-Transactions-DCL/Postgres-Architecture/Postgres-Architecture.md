# **PostgreSQL Architecture**

![AGEDB](https://miro.medium.com/v2/resize:fill:55:55/1*1s3eHvdf3gF6YUwMeRJVyQ.jpeg)

![Opensource relational database with graph analytics](https://miro.medium.com/v2/resize:fill:30:30/1*I7jAMxjj3sxfEl1bDvaqZw.jpeg)

Let’s dive into the world of [PostgreSQL](https://www.postgresql.org/) Architecture — or Postgres, as it’s fondly known. At first glance, its architecture might seem pretty straightforward, but there’s a lot of magic happening under the hood. It’s a blend of shared memory, a handful of background processes, and data files. (*See* ***Figure 1–1\***).

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\1.png)

**Figure 1–1.** *PostgreSQL (Postgres) Architecture*

**1–1. Shared Memory**

At the heart of shared memory lies the Shared Buffer and the WAL Buffer. Utilizing tools like [pgAdmin](https://www.pgadmin.org/), administrators can gain insights into the utilization and performance of these buffers, aiding in the efficient management of PostgreSQL databases. Here we will explain a little more of each of them:

**Shared Buffer**

The purpose of the Shared Buffer is to minimize disk I/O, as all databases do. To do this, it must meet the following criteria:

- Very large (tens or hundreds of GB) buffers need to be accessed quickly
- Minimize contention when accessed by many users simultaneously
- Frequently used blocks should stay in the buffer as long as possible

**WAL Buffer**

The WAL Buffer is a buffer that temporarily stores changes to the database. The content stored in the WAL Buffer is written to a WAL file at a fixed point in time. From a backup and recovery perspective, the WAL Buffer and WAL files are very important. (Like Oracle’s Redo Log Buffer and Redo Log File).

If you use [pgAdmin](https://www.pgadmin.org/), you can use it to monitor the WAL Buffer’s activity, including the frequency and volume of data being written. This visibility is good for understanding the impact of the WAL Buffer on overall database performance and for making decisions about backup and recovery strategies.

**1–2. Process Types**

Postgres plays host to four main types of processes:

- Postmaster (Daemon) Process
- Background Process
- Backend Process
- Client Process

**1–3. Postmaster Process**

The Postmaster Process is like the welcoming committee when you boot up Postgres. It gets the ball rolling with recovery operations, warming up shared memory, and waking up background processes. Plus, it’s the one calling the shots by creating backend processes for client connections.

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\2.png)

**Figure 1–2.** *Process relationship diagram*

If we check the relationship between the processes with the pstree command, we can see that the Postmaster process is the parent process of all the processes.

**For clarity, we’ve added the process name and argument after the process ID*

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\3.png)

**1–4. Background Process**

The essential background processes for PostgreSQL’s operation are outlined below. With the exception of the Autovacuum Launcher, these processes are commonly encountered within [*ORACLE*](http://oracle.com/), underscoring their foundational role in database management.

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\4.png)

**1–5. Backend Process**

The max number of backend processes is decided by the `**max_connections`** parameter, typically set to 100. These processes are the muscle, doing the heavy lifting by executing queries and passing results back to users. They rely on a bunch of memory structures, affectionately known as local memory, to get the job done.

**The main parameters related to local memory are as follows:**

*work_mem parameter*

This is the space used for sort operations, Bitmap operations, Hash join and Merge join operations. The default setting is 4 MB.

*maintenance_work_mem parameter*

Space used for Vacuum and Create Index operations. The default value is 64 MB.

*temp_buffers parameter*

Space for storing temporary tables. The default value is 8 MB.

**1–6. PostgreSQL (Postgres) Database Structure**

## Database Essentials

1. PostgreSQL, often abbreviated as Postgres, consists of multiple databases, collectively known as a **database cluster**
2. Upon executing `**initdb`**, three databases are created: **`template0`**, **`template1`**, and **`postgres`**.
3. **`template0`** and **`template1`** serve as template databases for creating user databases and include system catalog tables
4. Right after `**initdb`** is run, both **`template0`** and **`template1`** have identical table lists. However, template1 allows for the creation of objects necessary for users
5. User databases are created by duplicating the **`template1`** database, simplifying the process of creating specific objects in each user database

## Tablespace Details

1. Immediately after executing **`initdb`**, two tablespaces are created: `**pg_default`** and `**pg_global`**
2. If a tablespace is not specified when creating a table, it is stored in the `**pg_default tablespace`**
3. Tables managed at the database cluster level are stored in the `**pg_global`** tablespace
4. The physical location of **pg_default** is `**$PGDATA\base`**
5. The physical location of **pg_global** is `**$PGDATA\global`**
6. A single tablespace can be utilized by multiple databases. Within the tablespace directory, subdirectories are created for each database, named after the database’s OID
7. When a user tablespace is created, a symbolic link related to the user tablespace is generated in the `**$PGDATA\tblspc`** directory

## Table-Specific Information

1. Each table is associated with three files
2. One for storing table data, named after the table’s OID
3. One for managing the table’s free space, named `**OID_fsm`**
4. One for managing the visibility of table blocks, named `**OID_vm`**
5. Indexes lack a vm file, thus consisting of only two files: **`OID`** and `**OID_fsm`**

> **Note:** At the point of table and index creation, the file name is the OID, and at this moment, the OID and `**pg_class.relfilenode`** values match. However, after operations like Truncate, Cluster, Vacuum Full, or Reindex, the affected object’s `**relfilenode`** value changes, and so does the file name, to match the **`relfilenode`** value.

For convenience, the `**pg_relation_filepath(‘object_name’)`** function can easily reveal the file’s location and name.

## `template0`, `template1`, and postgres databases

Let’s verify the previously discussed points through testing!

After running `**initdb`**, querying `**pg_database view`** confirms the creation of `**template0`**, **`template1`**, and `**postgres`** databases.

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\5.png)

- **datistemplate Column:** This indicates whether the database is a template for creating user databases. Both `**template0`** and **`template1`** are template databases designed for this purpose.
- **datallowconn Column:** It signifies the database’s accessibility for connections. The **`template0`** database cannot be accessed, thus its contents cannot be altered.
- **Purpose of Two Template Databases:** `**template0`** is provided as an initial state template, while `**template1`** allows users to add custom templates. This facilitates user-specific customizations right from database creation.
- **The postgres Database:** By default, this is the primary database created using the **`template1`** database. If no specific database is mentioned upon connection, it defaults to the postgres database.
- **Database Location:** All databases reside under the **`$PGDATA/base`** directory. The directory name corresponds to the database’s OID number.

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\6.png)

**Creating User Databases**

User databases are generated by cloning the `**template1`** database. To illustrate this, we first create a sample table T1 within the `**template1`** database. Next, we proceed to create a new database named **`mydb01`** and verify the presence of the T1 table.

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\7.png)

*Illustrating this process graphically yields the following depiction:*

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\8.png)

**Figure 1–3** *Relationship between the template database and the user database*

**The pg_default Tablespace**

After running initdb(), checking the pg_tablespace will reveal the creation of both the `**pg_default`** and `**pg_global tablespaces`**.

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\9.ong)

The pg_default tablespace is located at `**$PGDATA\base`**. This directory contains subdirectories for each database OID, representing the physical structure where each database directory exists under its respective tablespace. ***(Refer to Figure 1–4)\***

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\10.png)

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\11.png)

**Figure 1–4**. *Relationship of the pg_default tablespace to the database from a physical configuration perspective*

**The pg_global Tablespace**

The `**pg_global tablespace`** serves to store data that needs to be managed at the **‘database cluster’** level.

- For instance, tables like pg_database provide the same information regardless of which database accesses them, underscoring their cluster-wide relevance (Refer to Figure 1–5)
- The location of the `**pg_global`** tablespace is at `**$PGDATA\global`**

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\12.png)

**Figure 1–5.** *Relationship between the pg_global tablespace and the database*

**Creating User Tablespace**

Let’s dive into how changes unfold after creating a user tablespace.

![img](C:\Users\smbanaie\Desktop\13-Patroni-HA\4-Postgres-Architecture\images\13.png)

In PostgreSQL, the entire directory specified by the **`PGDATA`** environment variable is utilized as the database. Subsequently, tables within this database are created as files. This implies that even without explicitly creating a separate tablespace, user tables can be established within the database. Essentially, the directory designated as the database is recognized as a basic tablespace.

According to [PostgreSQL’s official site](https://www.postgresql.org/docs/16/manage-ag-tablespaces.html), tablespaces are defined as file system paths where database objects can be stored, as determined by the database administrator.

Once a tablespace is created, it can be referred by name when creating database objects.

The capability to create tablespaces, as enabled by the disk layout upon PostgreSQL installation, proves invaluable from two perspectives:

1. **Expansion:** When the volume or partition where the DB is created runs low on space, tablespaces can be created on different partitions or disks. This flexibility allows the DB to be expanded until the system can be reorganized
2. **Performance Optimization:** For instance, high-performance SSDs can be utilized for tablespaces to host frequently updated, high-usage indexes, thereby enhancing performance. This optimization technique can significantly improve the efficiency of database objects.

# **Conclusion: \*PostgreSQL as a Foundational Relational Database\***

Exploring PostgreSQL’s architecture offers insight into a relational database designed for high efficiency and flexibility. From its shared memory and process management to the strategic use of tablespaces, PostgreSQL stands out as a comprehensive solution for modern data management challenges.

As a relational database, PostgreSQL is not just a tool for data storage but a foundation for scaling, optimizing, and transforming data landscapes.

[*Ready to see what PostgreSQL can do for your database needs?*](https://agedb.io/)
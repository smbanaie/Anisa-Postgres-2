### PG Data Folder

- check out the `pg_wall`
- check out the whole folder size



### Go to the Postgres Container  CLI

```bash
docker exec -it postgres bash 
```



### Create a Sample DB

```bash
export PGUSER=postgres
createdb sample
pgbench -i -s 50 sample
```

- check out the `pg_wall`

- checkout the folder size (total/base/pg_wall)


### Simple Backup/Restore

- take a physical backup

```bash
pg_basebackup -D /backup/standalone-"$(date +%Y-%m-%dT%H-%M)" -c fast -P -R 
```

- check the new `pg_wall` -> checkpoint writes all old WAL unsaved data . 
- check the ` \backup\standalone\standby.signal `  
- No transaction logs 

#### Simulate the Recovery Process

- stop the postgres container.
- remove the `db_data` folder. 
- copy the content of pg_basebakup into `db_data`
- remove the `standby.signal`
- start the postgres container

```bash
database system was shut down in recovery at 2024-02-10 22:48:59 UTC
postgres  | 2024-02-10 22:52:21.588 UTC [25] LOG:  database system was not properly shut down; automatic recovery in progress
postgres  | 2024-02-10 22:52:21.653 UTC [25] LOG:  redo starts at 0/29000028
postgres  | 2024-02-10 22:52:21.656 UTC [25] LOG:  redo done at 0/29000138 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
```



- check out the `sample` db in `dbeaver/pgadmin/psql`

  

### Create a Tablespace

- create a folder for storing new tablespace

  - we already made this on docker-compose mount points.

  ```bash
  mkdir /tblspace
  ```

  

- create a tablespace

  - make sure the target dir is empty :` '/tblspace'`

  - change the `/tblspace` owner  (root user access)

    ```bash
    chown -R postgres:postgres /tblspace
    ```

    

  - use `psql` (su postgres)

  ```sql
  CREATE TABLESPACE bench_space
  OWNER postgres
  LOCATION '/tblspace';
  
  ```

- change the tablespace of `pgbench_accounts`

  ```sql
  \c sample
  ALTER TABLE pgbench_accounts SET TABLESPACE bench_space;
  \d+ pgbench_accounts
  ```

  

- it gradually insert new records (updated/inserted) into this tablespace but we can enforce moving it :

  ```sql
  CLUSTER pgbench_accounts USING pgbench_accounts_pkey;
  
  ```

- exit `psql` : `\q`

- ##### Pg_BaseBackup

   ```bash
   pg_basebackup -D /backup/standalone-"$(date +%Y-%m-%dT%H-%M)" -c fast -P -R -T 	/tblspace/=/backup/tblspace-"$(date +%Y-%m-%dT%H-%M)"
   ```



#### Simulate the Recovery Process - Tablespace Version 

- Because of permission error on `/tblspace` on Windows, to test this section , you have to install `postgres` on ubuntu (wsl or a docker container -> commit changes) to be able to use `pg_ctl` stop the `postgres`  without  stopping the `postgres` container .

- stop the postgres service inside the custom container (as mentioned before) or in`WSL`.

```bash
su postgres
pg_ctl stop -D /var/lib/postgresql/data
```



- remove the `db_data` folder contents.  
- remove tablesapce : `rm -r /tblspace/*`
- copy the content of recently taken `pg_basebakup` into `db_data`
- copy the content of recently taken `tblspace` into `tblspace` folder
- check that the owner of `/data` and `/tblspace` is **postgres:postgres**
- remove the `standby.signal`
- start the postgres container



#### [Continuous Archiving and Point-in-Time Recovery (PITR)](https://www.postgresql.org/docs/current/continuous-archiving.html)

#### Backup Plan

- weekly base backup + WAL archiving 
- Recover to a point in time  (PITR) using Basebackup+Archived Wals



#### Basic Backup Plan

##### Setting Up WAL Archiving

- To enable WAL archiving, set the [wal_level](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-LEVEL) configuration parameter to `replica` or higher, [archive_mode](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-ARCHIVE-MODE) to `on`, specify the shell command to use in the [archive_command](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-ARCHIVE-COMMAND) configuration parameter or specify the library to use in the [archive_library](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-ARCHIVE-LIBRARY) configuration parameter. In practice these settings will always be placed in the `postgresql.conf` file.
- remove the `db_data`
- run `postgres` to `db_data` initialized.
- create a `basebackup`

```bash
export PGUSER=postgres
pg_basebackup -D /backup/standalone-"$(date +%Y-%m-%dT%H-%M)" -c fast -P -R 
```
- create the archive folder (we created this using mount point in `docker-compose` )
- add or `uncommant ` the `archive_command` in `postgres` config file:

```bash
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'  # Unix

archive_command = 'copy "%p" "C:\\server\\archivedir\\%f"'  # Windows
```

- restart the `postgres`

- create sample bench data (as explained before)

- check out the `./archive` folder.

  





























- check out the `sample` db in `dbeaver/pgadmin/psql`	


- 
- Restore using second postgres docker container 
- 

- 
- 
#### Basic Sample

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
- add some sample data (pg_bench)
- check out the `./archive` folder.

### PITR

- let do some PITR :

- stop the server change these setting while copying the wal files :

  ```sql 
  archive_mode = off 
  restore_command = 'cp /archive/%f %p’ 
  recovery_target_timeline = 'latest'
  
  ```

  

-  start the server 

- check these settings as well :

```bash 
recovery_target = 'immediate’ 

recovery_target_time = '2023-04-14 12:54:23'

recovery_target_lsn = '0/2000060'

recovery_target_xid = 569865

recovery_target_timeline = 'latest’


recovery_target_timeline = 2

recovery_target_name = ‘1402-Bahman-30’
This parameter specifies the named restore point (created with pg_create_restore_point()) to which recovery will proceed.

recovery_target_inclusive = true 

recovery_target_action = 'promote'

```

- Some Useful Function:

  ```sql
  now()
  pg_create_restore_point()
  pg_current_wal_lsn()
  pg_current_wal_insert_lsn()
  pg_waldump() (`$ pg_waldump -s 76/7E000060 -e 76/7E000108 00000001000000760000007E`)
  
  
  ```

  

  































- check out the `sample` db in `dbeaver/pgadmin/psql`	


- 
- Restore using second postgres docker container 
- 

- 
- 
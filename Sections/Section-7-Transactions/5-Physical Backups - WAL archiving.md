### [Physical Backups & WAL archiving](https://www.crunchydata.com/blog/introduction-to-postgres-backups#physical-backups--wal-archiving)

Beyond basic dump files, the more sophisticated methods of Postgres backup all depend on saving the database’s Write-Ahead-Log (WAL) files. WAL tracks changes to all the database blocks, saving them into segments that default to 16MB in size. The continuous set of a server’s WAL files are referred to as its WAL stream. You have to start archiving the WAL stream’s files before you can safely copy the database, followed by a procedure that produces a “Base Backup”, i.e. `pg_basebackup`. The incremental aspect of WAL makes possible a series of other restoration features lumped under the banner of [Point In Time Recovery](https://www.postgresql.org/docs/current/continuous-archiving.html) tools.

#### [Create a basebackup with pg_basebackup](https://www.crunchydata.com/blog/introduction-to-postgres-backups#create-a-basebackup-with-pg_basebackup)

You can use something like this:

```shell
$ sudo -u postgres pg_basebackup -h localhost -p 5432 -U postgres \
	-D /var/lib/pgsql/16/backups -Ft -z -Xs -P -c fast
```

A few comments on the command above.

- This command should be run as the `postgres` user.
- The `-D` parameter specifies where to save the backup.
- The `-Ft` parameter indicates the tar format should be used.
- The `-Xs` parameter indicates that WAL files will stream to the backup. This is important because substantial WAL activity could occur while the backup is taken and you may not want to retain those files in the primary during this period. This is the default behavior, but worth pointing out.
- The `-z` parameter indicates that tar files will be compressed.
- The `-P` parameter indicates that progress information is written to stdout during the process.
- The `-c` fast parameter indicates that a checkpoint is taken immediately. If this parameter is not specified, then the backup will not begin until Postgres issues a checkpoint on its own, and this could take a significant amount of time.

Once the command is entered, the backup should begin immediately. Depending upon the size of the cluster, it may take some time to finish. However, it will not interrupt any other connections to the database.

### [Steps to restore from a backup taken with pg_basebackup](https://www.crunchydata.com/blog/introduction-to-postgres-backups#steps-to-restore-from-a-backup-taken-with-pg_basebackup)

They are simplified from the [official documentation](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-PITR-RECOVERY). If you are using some features like tablespaces you will need to modify these steps for your environment.

1. Ensure the database is shutdown.

   ```shell
   sudo systemctl stop postgresql-16.service
   sudo systemctl status postgresql-16.service
   ```

2. Remove the contents of the Postgres data directory to simulate the disaster.

   ```shell
   sudo rm -rf /var/lib/pgsql/16/data/*
   ```

3. Extract base.tar.gz into the data directory.

   ```shell
   $ sudo -u postgres ls -l /var/lib/pgsql/16/backups
   total 29016
   -rw-------. 1 postgres postgres   182000 Nov 23 21:09 backup_manifest
   -rw-------. 1 postgres postgres 29503703 Nov 23 21:09 base.tar.gz
   -rw-------. 1 postgres postgres	17730 Nov 23 21:09 pg_wal.tar.gz
   
   
   $ sudo -u postgres tar -xvf /var/lib/pgsql/16/backups/base.tar.gz \
        -C /var/lib/pgsql/16/data
   ```

4. Extract pg_wal.tar.gz into a new directory outside the data directory. In our case, we create a directory called pg_wal inside our backups directory.

   ```shell
   $ sudo -u postgres ls -l /var/lib/pgsql/16/backups
   total 29016
   -rw-------. 1 postgres postgres   182000 Nov 23 21:09 backup_manifest
   -rw-------. 1 postgres postgres 29503703 Nov 23 21:09 base.tar.gz
   -rw-------. 1 postgres postgres	17730 Nov 23 21:09 pg_wal.tar.gz
   
   $ sudo -u postgres mkdir -p /var/lib/pgsql/16/backups/pg_wal
   
   $ sudo -u postgres tar -xvf /var/lib/pgsql/16/backups/pg_wal.tar.gz \
         -C /var/lib/pgsql/16/backups/pg_wal/
   ```

5. Create the recovery.signal file.

   ```shell
   sudo -u postgres touch /var/lib/pgsql/16/data/recovery.signal
   ```

6. Set the restore_command in postgresql.conf to copy the WAL files streamed during the backup.

   ```shell
   echo "restore_command = 'cp /var/lib/pgsql/16/backups/pg_wal/%f %p'" | \
         sudo tee -a /var/lib/pgsql/16/data/postgresql.conf
   ```

7. Start the database.

   ```shell
   $ sudo systemctl start postgresql-16.service sudo systemctl status
   postgresql-16.service
   ```

8. Now your database is up and running based on the information contained in the previous basebackup.

#### [Automating physical backups](https://www.crunchydata.com/blog/introduction-to-postgres-backups#automating-physical-backups)

Building upon the `pg_basebackup`, you could write a series of scripts to use this backup, add WAL segments to it, and manage a complete physical backup scenario. There are several tools out there including WAL-E, WAL-G, and pgBackRest that will do all this for you. WAL-G is the next generation of WAL-E and works for quite a few other databases including MySQL and Microsoft SQL Server. WAL-G is also used extensively at the enterprise level with some large Postgres environments, including Heroku. When we first built Crunchy Bridge, we had a choice between WAL-G and pgBackRest since we employ the maintainers of both and each has its perks. In the end, we selected pgBackRest.
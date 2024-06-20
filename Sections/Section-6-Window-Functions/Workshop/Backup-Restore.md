### PG_DUMP

- Open Terminal

- Create a sample directory named `backups` 

- cd `backups`

- run the following commands :

  ```bash
  pg_dump -U postgres
  
  pg_dump -U postgres > postgres_db.sql
  
  ```

  - it backups the `postgres` DB

  ```bash
  pg_dump -U postgres -d northwind > northwind.bak
  
  pg_dump -U postgres -d northwind -Fp -f northwind.sql
  pg_dump -U postgres -d northwind -Fc -f northwind.custom
  
  pg_dump -U postgres -d northwind -Fd -f northwind
  
  pg_dump -U postgres -d northwind --table orders -F c -f northwind_orders_table.custom
  
  pg_dump -U postgres -d northwind --format p --file northwind.txt  --exclude-table=employees
  
  pg_dump -U postgres -d northwind --format p --file northwind.txt --exclude-table=employees --exclude-table=orders
  
  pg_dump -U postgres -d northwind --format p --file northwind.txt --exclude-table=temp_*
  
  
  
  ```

  #### What About FKs? Views? 

  ```sql
  pg_dump -U postgres -d northwind --format p --file northwind.txt --exclude-table-data=employees
  
  ```

  ### Only DB Structure

  ```bash
  pg_dump -U postgres -d northwind -f northwind.sql --schema-only 
  ```

  

#### Backup All Database structures

```bash
pg_dumpall -U postgres  -f alldb.sql --schema-only


```

### Suppress Password Prompts

#### ENV Variable

- **Linux**

```bash
export PGPASSWORD=<your_password>
```

- **Windows - Powershell**

```bash
$env:PGPASSWORD=<your_password>
```

- run the `pg_dumpall` with -w

```bash
pg_dumpall -U postgres  -f alldb.sql --schema-only -w
```

#### Restore the DBs

- run another postgres instance using docker file provided on port:5434

```bash
psql -U postgres -p 5434 -f .\alldb.sql
```



#### pg_restore

```bash
$env:PGPASSWORD='postgres123'
pg_dumpall -U postgres --schema-only -w --exclude-database=pagila -f all_except_pagila.sql
#Error
pg_dump -U postgres -j 4 northwind --data-only -w -Fd -f northwind  
#Debug 
pg_dump --help | grep only
# Correction
pg_dump -U postgres -j 4 -d northwind --data-only -w -Fd -f northwind  

psql -U postgres -p 5434 -f .\all_except_pagila.sql

###Error
pg_restore -U postgres -j 4 -p 5434 -d northwind -Fd northwind

### Dump Schema Again
pg_dumpall -U postgres --schema-only -w -c --if-exists -f all_schema.sql
 
psql -U postgres -p 5434 -f all_schema.sql

pg_restore -U postgres --disable-triggers -j 4 -p 5434 -d northwind -Fd northwind  
```



#### Cron Jobs

suppose we want to backup a daily schema backup

To create a daily cron job for our PostgreSQL database backup with the specified requirements, we can use a script that sets the `PGPASSWORD` environment variable and appends the date to the filename. go to **WSL**, start postgres instance (section1 / port 5433) and :

1. Create a backup folder such as `/home/smbanaie/crons/backups`, then create a script (e.g., `/home/smbanaie/crons/backup_script.sh`) with the following content:

```bash
#!/bin/bash

export PGPASSWORD='postgres123'

# Get the current date in the format YYYY-MM-DD
current_date=$(date +"%Y-%m-%d")

# Run pg_dumpall with schema-only option and append the date to the filename
pg_dumpall -U postgres -h localhost -p 5433 --schema-only -w -f "/home/smbanaie/crons/backups/all_schema_${current_date}.sql"
```

2. Save the script and make it executable:

```bash
chmod +x backup_script.sh
```

3. Set up a daily cron job. Edit the crontab file using:

```bash
crontab -e
```

Add the following line to run the script every day at a specific time :

```bash
0 2 * * * /home/smbanaie/crons/backup_script.sh
```

This example sets the cron job to run at 2:00 AM every day. Adjust the timing based on your preferences.

change the cron job into :`*/3 * * * * /home/smbanaie/crons/backup_script.sh` and 

- quick ref : https://crontab.guru/

Make sure to update the script and cron job according to your system's specific paths and requirements. Additionally, ensure that the script has appropriate permissions and access controls for security.

### Airflow Workshop

- watch the video

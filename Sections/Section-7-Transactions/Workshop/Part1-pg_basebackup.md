### pg_dump

- create a `db` named `northwind2` and restore the `northwind.sql`

- take a dump of all tables

- restore it using pg_restore in a new `DB` named `northwind20`

  ##### Suppress Password Prompts

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

  

  ```sql
  pg_dumpall -U postgres --schema-only -w --exclude-database=pagila -f all_except_pagila.sql
  
  pg_dump -U postgres -j 4 -d northwind --data-only -w -Fd -f northwind  
  
  
  pg_restore -U postgres --disable-triggers -j 4 -p 5434 -d northwind -Fd northwind  
  
  ```
  
  
  
- do it using `DBeaver` and `PG_Admin`

### pg_basebackup

- create the `jobs` db
- populate it 
- use pg_basebackup to take a snapshot
- remove the db . 
- recover it !



###  Observing Checkpoint Effects in PostgreSQL

In this tutorial, we'll walk through the process of observing the effects of checkpoints in PostgreSQL using SQL commands. We'll examine the state before and after a checkpoint, and explain what each command does.

Step 1: Examining the state before a checkpoint

1.1. Check the current WAL (Write-Ahead Log) position:

```sql
SELECT pg_current_wal_lsn();
```

This command returns the current write-ahead log (WAL) write location. The WAL is a log of all changes made to the database, used for crash recovery and replication.

1.2. View the last checkpoint location:

```sql
SELECT pg_control_checkpoint();
```

This function returns information about the last checkpoint, including its location in the WAL, timestamp, and next TransactionId.

Step 2: Manually triggering a checkpoint

To force a checkpoint, use:

```sql
CHECKPOINT;
```

This command forces PostgreSQL to perform a checkpoint, which writes all buffered data to disk and creates a known good point in the transaction log.

Step 3: Examining the state after a checkpoint

3.1. Check the new WAL position:

```sql
SELECT pg_current_wal_lsn();
```

Compare this with the result from step 1.1. You should see that the WAL position has advanced.

3.2. View the updated last checkpoint location:

```sql
SELECT pg_control_checkpoint();
```

Compare with the result from step 1.2. The checkpoint location and timestamp should have changed.

3.4. View checkpoint statistics:

```sql
SELECT * FROM pg_stat_bgwriter;
```

This query returns statistics about the background writer process, including:
- Number of scheduled and requested checkpoints
- Amount of time spent in checkpoint processing
- Number of buffers written during checkpoints
- WAL files added and recycled

Interpreting the Results:

1. WAL position (pg_current_wal_lsn): This should increase after the checkpoint, indicating new data has been written.

2. Checkpoint location (pg_control_checkpoint): This should update to reflect the new checkpoint's position in the WAL.

3. Checkpoint time: This should match the time you ran the CHECKPOINT command.

4. Checkpoint statistics: You should see an increase in the number of checkpoints and possibly in the number of buffers written.

By comparing these values before and after the checkpoint, you can observe how PostgreSQL manages data persistence and prepares for potential crash recovery.

###  Understanding and Abbreviating LSN

**LSN Structure:**

LSN stands for Log Sequence Number. It's a 64-bit integer that represents a position in the Write-Ahead Log (WAL). The LSN is structured as follows:

- The upper 32 bits represent the WAL file number.
- The lower 32 bits represent the byte offset within that file.

Each WAL file is typically 16MB in size (which is 2^24 bytes).

Viewing LSN in a More Readable Format:

PostgreSQL provides a function to convert the raw LSN to a more human-readable format:

```sql
SELECT pg_walfile_name(pg_current_wal_lsn());
```

This will return a string like '000000010000000000000001', which represents:
- The first 8 hexadecimal digits: the timeline ID
- The next 16 hexadecimal digits: the WAL file number

To get both the file name and the exact byte position:

```sql
SELECT pg_walfile_name_offset(pg_current_wal_lsn());
```

This returns a tuple with the WAL filename and the byte offset within that file.

Abbreviating LSN for Comparison:

For easier comparison of LSNs, you can use the `pg_lsn` data type and some PostgreSQL functions:

1. Convert LSN to pg_lsn type:

```sql
SELECT '0/15E1C88'::pg_lsn;
```

2. Subtract two LSNs to see the difference in bytes:

```sql
SELECT '0/15E1C88'::pg_lsn - '0/15E1B70'::pg_lsn AS lsn_diff;
```

3. Use `pg_size_pretty` to format byte differences:

```sql
SELECT pg_size_pretty(('0/15E1C88'::pg_lsn - '0/15E1B70'::pg_lsn)::numeric) AS lsn_diff_pretty;
```

Now, let's integrate this into our checkpoint observation tutorial:

Step 4: Comparing LSNs before and after checkpoint

4.1. Before checkpoint, get the current LSN in a readable format:

```sql
SELECT pg_walfile_name(pg_current_wal_lsn()) AS wal_file,
       pg_walfile_name_offset(pg_current_wal_lsn()) AS wal_file_offset;
```

4.2. After running the CHECKPOINT command, repeat the above query and compare.

4.3. Calculate the difference in bytes:

```sql
SELECT pg_size_pretty((
    (SELECT pg_current_wal_lsn())::numeric - 
    (SELECT pg_lsn FROM pg_control_checkpoint())::numeric
) AS lsn_diff_pretty;
```

This query calculates the difference between the current WAL position and the last checkpoint position, giving you an idea of how much WAL data has been generated since the last checkpoint.

Interpreting the Results:

1. The WAL file name will change when PostgreSQL moves to a new WAL file.
2. The byte offset will increase as new transactions are logged.
3. The difference between current LSN and checkpoint LSN indicates how much data needs to be replayed in case of a crash.

By using these methods to view and compare LSNs, you can get a clearer picture of WAL progression and checkpoint behavior in PostgreSQL.

### LSN Compact Version

The compact version of `(000000010000000000000071,5365880)` would be `0/71005368`.

To understand and convert this format:

1. `000000010000000000000071` is the WAL file name.
   - The last 8 characters (`00000071`) represent the hexadecimal file number.

2. `5365880` is the byte offset within the file.

To convert to the compact format:

1. Take the last 8 characters of the file name (hexadecimal): `00000071`
2. Convert the byte offset to hexadecimal: 
   5365880 in decimal = 005368 in hexadecimal

3. Combine these, separating with a '/':
   `71/005368`

4. Add a leading '0/' if needed for consistency:
   `0/71005368`



To go from the compact format back to the full format, you can use:

```sql
SELECT pg_walfile_name_offset('0/71005368'::pg_lsn);
```

This will return `(000000010000000000000071,5365880)`.


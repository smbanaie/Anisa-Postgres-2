# [An Introduction to PostgreSQL Performance Tuning and Optimization](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization)

![img](https://www.enterprisedb.com/sites/default/files/styles/square_thumbnail/public/vik-fearing.jpg?itok=E-yz2kpT)

##### [Vik Fearing](https://www.enterprisedb.com/blog/author/vik-fearing)

January 19, 2023

This document provides an introduction to tuning PostgreSQL and EDB Postgres Advanced Server (EPAS), versions 10 through 13. The system used is the RHEL family of linux distributions, version 8. These are only general guidelines and actual tuning details will vary by workload, but they should provide a good starting point for the majority of deployments.

 

When tuning, we start with the hardware and work our way up the stack finishing with the application's SQL queries. The workload dependent aspect of tuning tends to get higher as we move up the stack, so we begin with the most general aspects and move on to the most workload-specific aspects.

 

### **Table of content**

| **Designing the Machine**              | [3](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#designingthemachine) |
| -------------------------------------- | ------------------------------------------------------------ |
| Bare Metal                             | [3](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#baremetal) |
| CPU                                    | [3](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#cpu) |
| RAM                                    | [3](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#ram) |
| Disk                                   | [3](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#disk) |
| Network card                           | [3](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#networkcard) |
| Virtual Machines                       | [5](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#virtualmachines) |
| **Tuning the System**                  | [5](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#tuningthesystem) |
| tuned daemon                           | [6](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#tuneddaemon) |
| Optimizing the filesystem              | [9](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#optimizingfile) |
| Huge pages                             | [9](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#hugepages) |
| **PostgreSQL Tuning Starting Points**  | [11](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#postgreSQLtuning) |
| Configuration & Authentication         | [11](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#configuration) |
| max_connections                        | [11](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#maxconnections) |
| password_encryption                    | [12](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#passwordencryption) |
| Resource Usage                         | [12](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#resourceusage) |
| shared_buffers                         | [12](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#sharedbuffers) |
| work_mem                               | [12](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#workmem) |
| maintenance_work_mem                   | [12](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#maintenancework) |
| effective_io_concurrency               | [12](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#effectiveio) |
| Write-Ahead Log                        | [13](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#writeahead) |
| wal_compression                        | [13](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#walcompression) |
| wal_log_hints                          | [13](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#wallog) |
| wal_buffers                            | [13](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#walbuffers) |
| checkpoint_timeout                     | [13](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#checkpointtimeout) |
| checkpoint_completion_target           | [13](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#checkpointcompletion) |
| max_wal_size                           | [14](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#maxwalsize) |
| archive_mode                           | [14](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#archivemode) |
| archive_command                        | [14](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#archivecommand) |
| Query Tuning                           | [14](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#querytuning) |
| random_page_cost                       | [14](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#randompage) |
| effective_cache_size                   | [14](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#effectivecache) |
| cpu_tuple_cost                         | [14](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#cputuple) |
| Reporting and Logging                  | [15](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#reportingandloggging) |
| logging_collector                      | [15](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#loggingcollector) |
| log_directory                          | [15](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#logdirectory) |
| log_checkpoints                        | [15](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#logcheckpoints) |
| log_line_prefix                        | [15](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#loglineprefix) |
| log_lock_waits                         | [15](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#loglockwaits) |
| log_statement                          | [15](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#logstatement) |
| log_temp_files                         | [15](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#logtempfiles) |
| timed_statistics (EPAS)                | [16](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#timedstatistics) |
| Autovacuum                             | [16](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#autovacuum) |
| log_autovacuum_min_duration            | [16](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#logautovacuummin) |
| autovacuum_max_workers                 | [16](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#autovacuummax) |
| autovacuum_vacuum_cost_limit           | [16](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#autovacuumcost) |
| Client Connection Defaults             | [16](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#clientconnection) |
| idle_in_transaction_session_timeout    | [16](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#ideintransaction) |
| lc_messages                            | [17](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#lcmessages) |
| shared_preload_libraries               | [17](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#sharedpreload) |
| Fine Tuning Based on Workload Analysis | [17](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#finetuning) |
| Finding Slow Queries                   | [17](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#findingslowqueries) |
| Rewriting Queries                      |                                                              |
| Naked Columns                          | [18](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#nakedcolumns) |
| Never Use NOT IN with a Subquery       | [19](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#neveruse) |
| Using EXPLAIN (ANALYZE, BUFFERS)       | [20](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#usingexplain) |
| Wrong Estimates                        | [20](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#wrongestimates) |
| External Sorts                         | [20](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#externalsorts) |
| Hash Batches                           | [22](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#hashbatches) |
| Heap Fetches                           | [23](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#heapfetches) |
| Lossy Bitmap Scans                     | [24](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#lossybitmap) |
| Wrong Plan Shapes                      | [26](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#wrongplan) |
| **Partitioning**                       | [26](https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization#partitioning) |

##  



## Designing the Machine

This document focuses on bare metal and virtualized machines. Future versions may include cloud and containerized designs.

###  



### Bare Metal

When designing a bare metal server for PostgreSQL, there are a few things that need to be taken into consideration. These are CPU, RAM, Disk, and also network card in a minority of cases.



###  

### CPU

Choosing the right CPU may be a crucial point in the PostgreSQL performance. When dealing with larger data, CPUs speed will be important — but also CPUs with larger L3 caches will boost performance as well. For OLTP performance, having more and faster cores will help the operating system and PostgreSQL to be more efficient in utilizing them. On the other hand, using CPUs with larger L3 caches is good for larger sets of data./div>

 

So, what is L3 cache?

 

CPUs have at least 2 caches: L1 (a.k.a. primary cache) and L2 (a.k.a. secondary cache). L1 is the smallest and the fastest cache, which is embedded into the CPU core. L2 cache is just a bit slower than L1, but also larger than L1. L2 is used to feed the L1 cache.

 

Unlike L1 and L2 caches, which are unique to each core, L3 cache is shared between cores. L3 cache is slower when compared to L1 and L2 — however, it is shared across all of the cores available. Also please note that L3 cache is still faster than RAM. Having a larger L3 cache will boost CPU performance while dealing with a larger set of data. This will also be beneficial for PostgreSQL for parallel queries.



###  

### RAM

Cheapest among the rest of the hardware, and also the better for PostgreSQL performance. Operating systems tend to utilize the available memory and try to cache as much data as possible. More caching will end up with less disk I/O, and faster query times. When buying new hardware, we suggest adding as much RAM as possible in the first place. Adding more RAM in the future will be more expensive from the financial side and also the technical side (will require downtime unless you have a system with hotswap RAM). There are multiple PostgreSQL parameters that will be changed based on the available memory, which are mentioned below.



###  

### Disk

If the application is I/O bound (read and/or write intensive), choosing a faster drive set will improve the performance significantly. There are multiple solutions available, including NMVe and SSD drives.

 

The first rule of the thumb is separating the WAL disk from the data disk. WAL may be a bottleneck (on write-intensive databases), so keeping WAL on a separate and fast drive will solve this problem. Always use at least RAID 1, even though there are some cases where you may need RAID 10 if the database is really writing a lot.

 

Using separate tablespaces and drives for indexes and data will also increase the performance especially if PostgreSQL runs on SATA drives. This is usually not needed for SSD and NVMe drives. We suggest using RAID 10 for data.

 

Please refer to the “optimizing file system” section for more information about optimizing drives.

In addition, this blog post discusses the storage and RAID options that can be used with PostgreSQL.

 

 



### Network card

Even though network cards seem to be irrelevant to the performance of PostgreSQL, when the data grows a lot, faster or bonded network cards will speed up base backups as well.

 

 



## Virtual Machines

As compared to bare metal servers, virtual machines have a performance deficit due to the virtualization layer, albeit relatively small these days. In addition, the available CPU and disk I/O will decrease due to shared resources.

 

There are a few tips to get better performance out of PostgreSQL in VMs:There are a few tips to get better performance out of PostgreSQL in VMs:

- Consider pinning the VM to specific CPUs and disks. That will eliminate (or limit) the performance bottleneck that will occur because of other VMs running on the host machine.
- Consider pre-allocating the disks prior to the installation. That will prevent the host from allocating the disk space during database operations. If you cannot do this, you can change these 2 parameters in postgresql.conf:
  - Disable the *wal_recycle* parameter in postgresql.conf. By default, PostgreSQL recycles the WAL files by renaming them. However, on Copy-On-Write (COW) filesystems creating new WAL files may be faster so disabling this parameter will help in the VMs.
  - Disable the *wal_init_zero* parameter in postgresql.conf. By default, WAL space is allocated before WAL records are inserted. This will slow down WAL operations on COW filesystems. Disabling this parameter will disable this feature, helping VMs to perform better. If set to off, only the final byte is written when the file is created so that it has the expected size.

##  



## Tuning the System

When it comes to PostgreSQL performance, tuning the operating system gives you extra opportunities for better performance. As noted in the introduction, this guide focuses on tuning PostgreSQL for the Red Hat Enterprise Linux (RHEL) family.

 



### *tuned* daemon

Most of the tuning on RHEL is done with the tuned daemon. This daemon adapts the operating system to perform better for the workload.

 

Note that the commands shown below are for RHEL 8. If you're using RHEL 7, you should use the yum command wherever dnf is shown in the examples.

 

The tuned daemon comes installed by default. If it does not (perhaps due to configuration of kickstart files), install it with:

```
dnf -y install tuned
```

And enable it with:

```
systemctl enable --now tuned
```

*tuned* helps sysadmins to change kernel settings easily and dynamically, and they no longer **need to** make changes in /etc/sysctl — this is done via *tuned*.

 

*tuned* comes with a few predefined profiles. You can get the list using the

```
tuned-adm list
```

command. The RHEL installer will pick up a good default based on the environment. The bare metal default is *“throughput-performance”*, which aims at increasing throughput. You can run the following command to see what tuned daemon will recommend after assessing your system:

```
tuned-adm recommend
```

Use the command below to see the preconfigured value:

```
tuned-adm active
Current active profile: virtual-guest
```

However, the defaults may end up slowing down PostgreSQL — they may prefer power saving, which will slow down CPUs. Similar arguments are valid for network and I/O tuning as well. To solve this problem, we will create our own profile for PostgreSQL performance.

 

Creating a new profile is quite easy. Let’s call this profile “edbpostgres”. Run these commands as root:

```
#  This directory name will also be the
#  name of the profile:
mkdir /etc/tuned/edbpostgres
# Create the profile file:
echo "
[main]
summary=Tuned profile for EDB PostgreSQL Instances
[bootloader]
cmdline=transparent_hugepage=never
[cpu]
governor=performance
energy_perf_bias=performance
min_perf_pct=100
[sysctl]
vm.swappiness = 10
vm.dirty_expire_centisecs = 500
vm.dirty_writeback_centisecs = 250
vm.dirty_ratio = 10
vm.dirty_background_ratio = 3
vm.overcommit_memory=0
net.ipv4.tcp_timestamps=0

[vm]
transparent_hugepages=never
" > /etc/tuned/edbpostgres/tuned.conf
```

The lines that include [ and ] are called “tuned plugins”, and are used to interact with the given part of the system.

 

Let’s examine these parameters and values:

- [main] plugin includes summary information, and can also be used to include values from other tuned profiles with include statements.
- [cpu] plugin includes settings around CPU governor, and cpu power settings.
- [sysctl] plugin includes the values that interact with procfs.
- [vm] and [bootloader] plugins enable/disable transparent huge pages (bootloader plugin will help us to interact with GRUB command line parameters).

With these changes, we aim to achieve the following:

- CPUs will not enter power saving modes (PostgreSQL won’t suffer from random performance slowdowns)
- Linux will be much less likely to swap.
- The kernel will help Postgres to flush dirty pages, reducing load of bgwriter and checkpointer.
- The pdflush daemon will run more frequently
- It is a good practice to turn TCP timestamps off, to avoid (or, at least, reduce) spikes caused by timestamp generation.
- Disabling transparent huge pages is a great benefit to PostgreSQL performance.

To enable these changes, run this command:

```
tuned-adm profile edbpostgres
```

This command may take some time to complete.

 

To disable transparent huge pages completely, run this command:

```
grub2-mkconfig -o /boot/grub2/grub.cfg
```

and reboot your system:

```
systemctl start reboot.target
```



## Optimizing the filesystem

Another tuning point is disks. PostgreSQL does not rely on atime (the timestamp at which the file was last accessed) for the data files, so disabling them will save cpu cycles.

 

Open /etc/fstab, and add noatime just near the defaults value for the drive that PostgreSQL data and WAL files are kept.

```
/dev/mapper/pgdata-01-data /pgdata xfs 	defaults,noatime 1 1
```

To activate it immediately, run:

```
mount -o remount,noatime,nodiratime /pgdata
```

Please note that these suggestions are good for a start, and you need to monitor both the operating system and PostgreSQL to gather more data for finer tuning.

##  



## Huge pages

By default, the page size on Linux is 4kB. A typical PostgreSQL instance may allocate many GBs of memory, which will end up with potential performance problems with such a small page size. Also, given that these pages will be fragmented, using them for large data sets will end up with extra time for mapping them.

 

Enabling huge pages on Linux will give a performance boost to PostgreSQL as it will allocate large blocks (huge pages) of memory all together.

 

By default, huge pages are not enabled on Linux, which is also suitable for PostgreSQL’s default huge_pages setting, which is “try”, which basically means “use huge pages if available on the OS, otherwise no.”

 

There are two aspects to setting up huge pages for PostgreSQL: Configuring the OS, and configuring PostgreSQL.

 

Let’s start by finding how many huge pages are needed on your system for PostgreSQL. When a PostgreSQL instance is started, postmaster creates a file called postmaster.pid file in $PGDATA. You can find the pid of the main process there:

```
$ head -n 1 $PGDATA/postmaster.pid
1991
```

Now, find VmPeak for this instance:

```
$ grep -i vmpeak /proc/1991/status
VmPeak:     8823028 kB
```

*Tip: If you are running more than one PostgreSQL instance on the same server, please calculate the sum of all VmPeak values in the next step.*

Let’s confirm the huge page size:

```
$ grep -i hugepagesize /proc/meminfo
Hugepagesize:     2048 kB
```

Finally, let’s calculate the number of huge pages that the instance(s) will need:

 

8823028 / 2048 = 4308.12

 

The ideal number of huge pages is just a bit higher than this — just a bit. If you increase this value too much, processes that need small pages that also need space in the OS will fail to start. This may even end up with the operating system failing to boot or other PostgreSQL instances on the same server failing to start.

 

Now edit the tuned.conf file created above, and add the following line to the [sysctl] section:

```
vm.nr_hugepages=4500
```

and run this command to enable new settings:

```
tuned-adm profile edbpostgres
```

Now you can set

```
huge_pages=on
```

in postgresql.conf , and (re)start PostgreSQL.

 

We also need to make sure that tuned service will start before PostgreSQL service after reboot. Edit unit file:

```
systemctl edit postgresql-13.service
```

and add these 2 lines:

```
[Unit]
After=tuned.service
```

Run:

```
systemctl daemon-reload
```

for the changes to take effect.

 



## PostgreSQL Tuning Starting Points

The following configuration options are those that should typically be changed from the default values in PostgreSQL. Other values can have a significant effect on performance but are not discussed here as their defaults are already considered optimal.

###  



### Configuration & Authentication



### max_connections

The optimal number for max_connections is roughly 4 times the number of CPU cores. This formula often gives a very small number which doesn’t leave much room for error. The recommended number is the GREATEST(4 x CPU cores, 100). Beyond this number, a connection pooler such as pgbouncer should be used.

 

It is important to avoid setting *max_connections* too high as it will increase the size of various data structures in Postgres which can result in CPU cycles being wasted. Conversely, we also need to ensure that enough resources are allocated to support the required workload.

##  



## Resource Usage



### shared_buffers

This parameter has the most variance of all. Some workloads work best with very small values (such as 1GB or 2GB) even with very large database volumes. Other workloads require large values. A reasonable starting point is the LEAST(RAM/2, 10GB).

 

There is no specific reason for this formula beyond the years of collective wisdom and experience of the PostgreSQL community. There are complex interactions between the kernel cache and *shared_buffers* that make it near impossible to describe exactly why this formula generally provides good results.

 

### work_mem

The recommended starting point for work_mem is ((Total RAM - shared_buffers)/(16 x CPU cores)). The logic behind this formula is that if you have so many queries that you risk running out of memory, then you will already be CPU bound; and this formula provides for a relatively large limit for the general case.

 

It can be tempting to set *work_mem* to a much higher value, however this should be avoided as the amount of memory specified here may be used by each node within a single query plan, thus a single query could use multiples of *work_mem* in total, for example in a nested string of hash joins.

 



### maintenance_work_mem

This determines the maximum amount of memory used for maintenance operations like VACUUM, CREATE INDEX, ALTER TABLE ADD FOREIGN KEY, and data-loading operations. These may increase the I/O on the database servers while performing such activities, so allocating more memory to them may lead to these operations finishing more quickly. A value of 1GB is a good start since these are commands that are explicitly run by the DBA.

 



### autovacuum_work_mem

Setting *maintenance_work_mem* to a high value will also allow autovacuum workers to use that much memory each. A vacuum worker uses 6 bytes of memory for each dead tuple it wants to clean up, so a value of just 8MB will allow for about 1.4 million dead tuples.

 



### effective_io_concurrency

This parameter is used for read-ahead during certain operations and should be set to the number of disks used to store the data. It was originally intended to help Postgres understand how many reads were likely to occur in parallel when using striped RAID arrays of spinning disks, however, improvements have been observed by using a multiple of that number, likely due to the fact that good quality RAID adaptors can re-order and pipeline requests for efficiency. For SSD disks, it is recommended to set this value to 200 as their behaviour is quite different from spinning disks.



##  

## Write-Ahead Log

###  



### wal_compression

When this parameter is on, the PostgreSQL server compresses a full-page image written to WAL when *full_page_writes* is on or during a base backup. Set this parameter to 'on' as most database servers are likely to be bottlenecked on I/O rather than CPU.

 



### wal_log_hints

This parameter is required in order to use pg_rewind. Set it to 'on'.



 

### wal_buffers

This controls the amount of space available for back ends to write WAL data in memory so the WALWriter can then write it to the WAL log on disk in the background. WAL segments are 16MB each by default, so buffering a segment is very inexpensive memory-wise. Larger buffer sizes have been observed to have a potentially very positive effect on performance in testing. Set this parameter to 64MB.



 

### checkpoint_timeout

Longer timeouts reduce overall WAL volume but make crash recovery take longer. The recommended value is a minimum of 15 minutes but ultimately, the RPO of business requirements dictates what this should be.



 

### checkpoint_completion_target

This determines the amount of time in which PostgreSQL aims to complete a checkpoint. This means a checkpoint need not result in an I/O spike and instead aims to spread the writes over this fraction of the checkpoint_timeout value. The recommended value is 0.9 (which will become the default in PostgreSQL 14).



 

### max_wal_size

Checkpoints should always be triggered by a timeout for better performance and predictability. The *max_wal_size* parameter should be used to protect against running out of disk space by ensuring a checkpoint occurs when we reach this value to enable WAL to be recycled. The recommended value is half to two-thirds of the available disk space where the WAL is located.



 

### archive_mode

Because changing this requires a restart, it should be set to ‘on’, unless you know you are never going to use WAL archiving.



 

### archive_command

A valid archive_command is required if archive_mode is on. Until archiving is ready to be configured, a default of ': to be configured' is suggested.

The ':' primitive simply returns success on POSIX systems (including Windows), telling Postgres that the WAL segment may be recycled or removed. The “to be configured” is a set of arguments that will be ignored.



##  

## Query Tuning



###  

### random_page_cost

This parameter gives the PostgreSQL optimizer a hint about the cost of reading a random page from disk, allowing it to make decisions about when to use index scans vs. sequential scans. If using SSD disks, the recommended value is 1.1. For spinning disks, the default value is often adequate. This parameter should be set globally and per tablespace. (If you have a tablespace containing historical data on a tape drive, you might want to set this very high to discourage random access; a sequential scan and a filter will likely be faster than using an index.)



 

### effective_cache_size

This should be set to the smaller value of either 0.75* total ram amount, "or the sum of buff/cache, free ram and shared buffers in the output of **free** command",  and is used to give PostgreSQL a hint about how much total cache space is available to it. Note that this refers to caches in main memory, not CPU cache.

 



![postgres free command](https://www.enterprisedb.com/sites/default/files/images/Screenshot%202022-02-16%20105554.png)

In this example, effective_cache_size will be least (64304 * .75, 58113 + 5808 + 8192) (assuming that shared_buffers is 8GB, so 48228 MB. 

![effective_cache_size example](https://www.enterprisedb.com/sites/default/files/images/Screenshot%202022-02-16%20105900.png)

###  

### cpu_tuple_cost

Specifies the relative cost of processing each row during a query. Its default value is 0.01, but this is likely to be lower than optimal and experience shows it should usually be increased to 0.03 for a more realistic cost.



##  

## Reporting and Logging



###  

### logging_collector

This parameter should be on if log_destination includes stderr or csvlog to collect the output into log files.



 

### log_directory

If the *logging_collector* is on, this should be set to a location outside of the data directory. This way the logs are not part of base backups.



 

### log_checkpoints

This should be set to on for future diagnostic purposes — in particular, to verify that checkpoints are happening by *checkpoint_timeout* and not by *max_wal_size*.



 

### log_line_prefix

This defines the format of the prefix prepended to lines in the log file. The prefix should at least contain the time, the process ID, the line number, the user and database, and the application name to aid in diagnostics.

 

Suggested value: '%m [%p-%l] %u@%d app=%a '

 

Note: Don’t forget the space at the end!



 

### log_lock_waits

Set to on. This parameter is essential in diagnosing slow queries.



 

### log_statement

Set to 'ddl'. In addition to leaving a basic audit trail, this will help determine at what time a catastrophic human error occurred, such as dropping the wrong table.

 



### log_temp_files

Set to 0. This will log all temporary files created, suggesting that work_mem is incorrectly tuned.



 

### timed_statistics (EPAS)

Controls the collection of timing data for the Dynamic Runtime Instrumentation Tools Architecture (DRITA) feature. When set to on, timing data is collected. Set this parameter to on.

 



 

## Autovacuum



### log_autovacuum_min_duration

Monitoring autovacuum activity will help with tuning it. Suggested value: 0 which will log all autovacuum activity.



 

### autovacuum_max_workers

This is the number of workers that autovacuum has. The default value is 3 and requires a database server restart to be updated. Please note that each table can have only one worker working on it, so increasing workers only helps in parallel and more frequent vacuuming across tables. The default value is low, therefore it is recommended to increase this value to 5 as a starting point.



 

### autovacuum_vacuum_cost_limit

To prevent excessive load on the database server due to autovacuum, there is an I/O quota imposed by Postgres. Every read/write causes depletion of this quota and once it is exhausted the autovacuum processes sleep for a fixed time. This configuration increases the quota limit, therefore increasing the amount of I/O that the vacuum can do. The default value is low, we recommend increasing this value to 3000.

 



 



## Client Connection Defaults

### idle_in_transaction_session_timeout

Sessions that remain idle in a transaction can hold locks and prevent vacuum. This timer will terminate sessions that remain idle in a transaction for too long so the application must be prepared to recover from such an ejection.

 

Suggested value: 10 minutes, if the application can handle it.



 

### lc_messages

Log analyzers only understand untranslated messages. Set this to 'C' to avoid translation.



 

### shared_preload_libraries

Adding pg_stat_statements is low overhead and high value. This is recommended but optional (see below).

 



 

# Fine Tuning Based on Workload Analysis



##  

## Finding Slow Queries

There are two main ways to find slow queries:

- The *log_min_duration_statement* parameter; and
- the *pg_stat_statements* module and extension.

The *log_min_duration_statement* parameter is a time setting (granularity milliseconds) that indicates how long a query must run before it is sent to the log file. To get all the queries, set this to 0, but be warned: this can cause quite a lot of I/O!

 

Generally, this is set to ‘1s’ (one second), and then all the queries are optimized as described below. Then, it is gradually lowered and the process repeated until a reasonable threshold is reached and then kept there for ongoing optimization. What constitutes a reasonable threshold is entirely dependent on your workload and cannot be defined in a generic document such as this one.

 

This is a good technique for finding slow queries, but it isn’t the best. Imagine you have a query that takes 1min to execute and is run every ten minutes. Now you have a query that takes 20ms to execute but is run twenty times per second. Which one is more important to optimize? Normalized to ten minutes, the first query takes one minute of your server’s time, and the second takes four minutes total time. So the second is more important than the first, but it will likely fly under your *log_min_duration_statement* radar.

 

Enter the *pg_stat_statements* module. One downside of this one is it needs to be set in *shared_preload_libraries*, which requires a restart of the server. Fortunately, its overhead is so low and the rewards so high that we recommend always having it installed in production.

 

What this module does is record every single (completed) query that the server executes, normalizes it in various ways such as replacing constants with parameters, and then aggregates “same” queries into a single data point with interesting statistics such as total execution time, number of calls, maximum and minimum execution time, total number of rows returned, total size of temporary files created, and many more.

 

Two queries are considered the “same” if their normalized internal structures after parsing are the same. So SELECT * FROM t WHERE pk = 42; is the “same” query as SeLeCt * FrOm T wHeRe Pk=56; despite the value of pk being different.

 

In order to see the statistics collected by the pg_stat_statements module, you first need to install the pg_stat_statements extension with “CREATE EXTENSION pg_stat_statements;” which will create a pg_stat_statements view.

 

A word about security. The module collects statistics from all queries to the server, regardless of which combination of user/database they were run against. The extension can be installed in any database, even multiple databases if desired. By default, any user can select from the view, but they are limited to only their queries (the same as with the pg_stat_activity view). Superusers and users granted to the *pg_read_all_stats* or *pg_monitor* roles can see all of the contents.

 

Note: EDB’s PostgreSQL Enterprise Manager (PEM) has an [SQL Profiler](https://www.enterprisedb.com/docs/pem/8.0/pem_ent_feat/08_sql_profiler/) that can display this very nicely.



 

## Rewriting Queries

Sometimes rewriting parts of a query can drastically improve performance.



 

### Naked Columns

One very common mistake is writing something like this:

 

```
SELECT * FROM t

WHERE t.a_timestamp + interval ‘3 days’ < CURRENT_TIMESTAMP 
```

Instead of this:

SELECT * FROM t
WHERE t.a_timestamp < CURRENT_TIMESTAMP - interval ‘3 days’

 

The results of these two queries will be the same, there is no semantic difference; but the second one can use an index on t.a_timestamp and the first one cannot. As a general rule, keep the table columns “naked” on the left side and put all expressions on the right side.



###  

### Never Use NOT IN with a Subquery

There are two forms of the IN predicate: x IN (a, b, c) and x IN (SELECT …). For the positive version, you can use either one. For the negative, only use the first. The reason why is all about how nulls are handled.

 

Consider:

```
demo=# select 1 in (1, 2);
 ?column?
----------
 t
(1 row)

demo=# select 1 in (1, null);
 ?column?
----------
 t
(1 row)

demo=# select 1 in (2, null);
 ?column?
----------
 (null)
(1 row)
```

What this shows is that in the presence of nulls, the IN predicate will only return true or null; never false. It follows that NOT IN will only return false or null; never true!

 

When giving a list of constants like that, it is easy to spot when there are nulls and see that the query will never give the desired results. But if you use the subquery version, it is not so easy to see. More importantly, even if the result of the subquery is guaranteed to not have any nulls, Postgres won’t optimize it into an Anti Join. Use NOT EXISTS instead.

 



 

## Using EXPLAIN (ANALYZE, BUFFERS)

If your query never terminates (at least before you lose patience and give up) then you should contact an expert or become an expert yourself to study the simple EXPLAIN plan. In all other cases, you must always use the ANALYZE option in order to optimize a query.

 



 

### Bad Estimates

The most common cause of bad performance is bad estimates. If the table statistics are not up to date, Postgres might predict only two rows will be returned, when in fact two *hundred rows* will be returned. For just a scan, this is not important; it will take a little longer than predicted but that’s it.

 

The real problem is the butterfly effect. If Postgres thinks a scan will produce two rows, it might choose a nested loop for a join against it. When it gets 200 rows, that’s a slow query; and if it knew there would be that many rows it would have chosen a hash join or perhaps a merge join. Updating the statistics with ANALYZE can fix the problem.

 

Alternatively, you may have strongly correlated data that the planner does not know about. You can solve this problem with CREATE STATISTICS.

 



 

### External Sorts

If there is not enough *work_mem* for a sort operation, Postgres will spill to disk. Since RAM is much faster than disks (even SSDs), this can be a cause of slow queries. Consider increasing *work_mem* if you see this.

```
demo=# create table t (c bigint);
CREATE TABLE
demo=# insert into t select generate_series(1, 1000000);
INSERT 0 1000000
demo=# explain (analyze on, costs off) table t order by c;
                          	QUERY PLAN                         	 
----------------------------------------------------------------------
 Sort (actual time=158.066..245.686 rows=1000000 loops=1)
   Sort Key: c
   Sort Method: external merge  Disk: 17696kB
   ->  Seq Scan on t (actual time=0.011..51.972 rows=1000000 loops=1)
 Planning Time: 0.041 ms
 Execution Time: 273.973 ms
(6 rows)

demo=# set work_mem to '100MB';
SET
demo=# explain (analyze on, costs off) table t order by c;
                          	QUERY PLAN                         	 
----------------------------------------------------------------------
 Sort (actual time=183.841..218.555 rows=1000000 loops=1)
   Sort Key: c
   Sort Method: quicksort  Memory: 71452kB
   ->  Seq Scan on t (actual time=0.011..56.573 rows=1000000 loops=1)
 Planning Time: 0.043 ms
 Execution Time: 243.031 ms
(6 rows)
```

The difference isn’t flagrant here because of the small dataset. Real-world queries can be much more noticeable. Sometimes, as is the case here, it is best to add an index to avoid the sort altogether.

 

In order to prevent pathological, runaway queries, set the *temp_file_limit* parameter. A query that generates this much in temporary files is automatically cancelled.

 



 

### Hash Batches

Another indicator that *work_mem* is set too low is if a hashing operation is done in batches. In this next example, we set *work_mem* to its lowest possible setting before running the query. Then we reset it and run the query again to compare plans.

```
demo=# create table t1 (c) as select generate_series(1, 1000000);
SELECT 1000000
demo=# create table t2 (c) as select generate_series(1, 1000000, 100);
SELECT 10000
demo=# vacuum analyze t1, t2;
VACUUM
demo=# set work_mem to '64kB';
SET
demo=# explain (analyze on, costs off, timing off)
demo-# select * from t1 join t2 using (c);
                        	QUERY PLAN                       	 
------------------------------------------------------------------
 Gather (actual rows=10000 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Hash Join (actual rows=3333 loops=3)
     	Hash Cond: (t1.c = t2.c)
     	->  Parallel Seq Scan on t1 (actual rows=333333 loops=3)
     	->  Hash (actual rows=10000 loops=3)
           	Buckets: 2048  Batches: 16  Memory Usage: 40kB
           	->  Seq Scan on t2 (actual rows=10000 loops=3)
 Planning Time: 0.077 ms
 Execution Time: 115.790 ms
(11 rows)

demo=# reset work_mem;
RESET
demo=# explain (analyze on, costs off, timing off)
demo-# select * from t1 join t2 using (c);
                        	QUERY PLAN                       	 
------------------------------------------------------------------
 Gather (actual rows=10000 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Hash Join (actual rows=3333 loops=3)
     	Hash Cond: (t1.c = t2.c)
     	->  Parallel Seq Scan on t1 (actual rows=333333 loops=3)
     	->  Hash (actual rows=10000 loops=3)
           	Buckets: 16384  Batches: 1  Memory Usage: 480kB
           	->  Seq Scan on t2 (actual rows=10000 loops=3)
 Planning Time: 0.081 ms
 Execution Time: 63.893 ms
(11 rows)
```

The execution time was reduced by half by only doing one batch.



###  

### Heap Fetches

Whether a row is visible or not to the transaction running a query is stored in the row itself on the table. The Visibility Map is a bitmap that indicates whether all rows on a page are visible to all transactions. An Index Scan therefore must check the table (also called the heap here) when it finds a matching row to see if the row it found is visible or not.

 

An Index-Only Scan uses the Visibility Map to avoid fetching the row from the heap if it can. If the Visibility Map indicates that not all rows on the page are visible, then what should be an Index-Only scan ends up doing more I/O than it should. Worst case, it completely devolves into a regular Index Scan.

 

The explain plan will show how many times it had to go to the table because the Visibility Map was not up to date.

```
demo=# create table t (c bigint)
demo-# with (autovacuum_enabled = false);
CREATE TABLE
demo=# insert into t select generate_series(1, 1000000);
INSERT 0 1000000
demo=# create index on t (c);
CREATE INDEX
demo=# analyze t;
ANALYZE
demo=# explain (analyze on, costs off, timing off, summary off)
demo-# select c from t where c <= 2000;
                      	QUERY PLAN                      	 
---------------------------------------------------------------
 Index Only Scan using t_c_idx on t (actual rows=2000 loops=1)
   Index Cond: (c <= 2000)
   Heap Fetches: 2000
(3 rows)
```

Ideally, this would be zero, but it depends on the activity on the table. If you are constantly modifying and querying the same pages, that will show here. If that is not the case, then that means the Visibility Map needs to be updated. This is done by vacuum (which is why we turned autovacuum off for this demo).

```
demo=# vacuum t;
VACUUM
demo=# explain (analyze on, costs off, timing off, summary off)
demo-# select c from t where c <= 2000;
                      	QUERY PLAN                      	 
---------------------------------------------------------------
 Index Only Scan using t_c_idx on t (actual rows=2000 loops=1)
   Index Cond: (c <= 2000)
   Heap Fetches: 0
(3 rows)
```



### Lossy Bitmap Scans

When the data is scattered all over the place, Postgres will do what is called a Bitmap Index Scan. It builds a bitmap of the pages and offsets within the page of every matching row it finds. Then it scans the table (heap) getting all the rows with just one fetch of each page.

 

That is, if it has enough work_mem to do so. If it doesn’t, it will “forget” the offsets and just remember that there is at least one matching row on the page. The heap scan will have to check all of the rows and filter out ones that don’t match.

```
demo=# create table t (c1, c2) as
demo-# select n, n::text from generate_series(1, 1000000) as g (n)
demo-# order by random();
SELECT 1000000
demo=# create index on t (c1);
CREATE INDEX
demo=# analyze t;
ANALYZE
demo=# explain (analyze on, costs off, timing off)
demo-# select * from t where c1 <= 200000;
                        	QUERY PLAN                       	 
------------------------------------------------------------------
 Bitmap Heap Scan on t (actual rows=200000 loops=1)
   Recheck Cond: (c1 <= 200000)
   Heap Blocks: exact=5406
   ->  Bitmap Index Scan on t_c1_idx (actual rows=200000 loops=1)
     	Index Cond: (c1 <= 200000)
 Planning Time: 0.065 ms
 Execution Time: 48.800 ms
(7 rows)

demo=# set work_mem to '64kB';
SET
demo=# explain (analyze on, costs off, timing off)
demo-# select * from t where c1 <= 200000;
                        	QUERY PLAN                       	 
------------------------------------------------------------------
 Bitmap Heap Scan on t (actual rows=200000 loops=1)
   Recheck Cond: (c1 <= 200000)
   Rows Removed by Index Recheck: 687823
   Heap Blocks: exact=752 lossy=4654
   ->  Bitmap Index Scan on t_c1_idx (actual rows=200000 loops=1)
     	Index Cond: (c1 <= 200000)
 Planning Time: 0.138 ms
 Execution Time: 85.208 ms
(8 rows)
```



### Wrong Plan Shapes

This is the hardest problem to detect and only comes with experience. We saw earlier that insufficient *work_mem* can make a hash use multiple batches. But what if Postgres decides that it’s cheaper to not use a Hash Join at all and maybe go for a Nested Loop instead? Now there is nothing that “stands out” like we’ve seen in the rest of this section, but increasing *work_mem* will make it go back to the Hash Join. Learning when your query should have a certain plan shape and noticing when it has a different one can provide for some really good **PostgreSQL optimization opportunities**.

 



 

## Partitioning

There are two reasons for partitioning: maintenance and parallelization.

 

When a table becomes very large, the number of dead rows allowed per the default autovacuum settings also grows. For a table with just one billion rows, cleanup won’t begin until 200,000,000 rows have been updated or deleted. In most workloads, that takes a while to achieve. When it does happen—or worse, when wraparound comes—then it is time to pay the piper and a single autovacuum worker must scan the whole table collecting a list of dead rows. This list uses six bytes per dead row, so roughly 1.2GB of RAM to store it. Then it must scan each index of the table one at a time and remove entries it finds in the list. Finally, it scans the table again to remove the rows themselves.

 

If you haven’t—or can’t—allow for 1.2GB of *autovacuum_work_mem* then this whole process is repeated in batches. If at any point during that operation, a query requires a lock that conflicts with autovacuum, the latter will politely bow out and start again from the beginning. However, if the autovacuum is to prevent wraparound, the query will have to wait.

 

Autovacuum uses a *visibility map* to skip large swaths of the table that haven’t been touched since the last vacuum, and 9.6 took this a step further for anti-wraparound vacuums, but no such optimization exists on the index methods, they are fully scanned every single time. What’s more, the holes left behind in the table can be filled by future inserts/updates, but it is much more difficult to reuse empty space in an index since the values there are ordered. Fewer vacuums means the indexes need to be reindexed more often to keep their performance. Up until PostgreSQL 11, that required locking the table against writes, but PostgreSQL 12 can reindex concurrently.

 

By partitioning your data into smaller chunks, each partition and its indexes can be handled by different workers, and there is less work for each to do, and they do it more frequently.

 

Sometimes partitioning can be used to eliminate the need to vacuum at all. If your table holds something like time series data where you basically “Insert and Forget”, the above is much less of a problem. Once the old rows have been frozen, autovacuum will never look at them again (since 9.6, as mentioned). The problem here is retention policies. If the data is only kept for ten years and then deleted after possibly archiving it on cold storage, that will create a hole that new data will end up filling and the table will become fragmented. This will render any BRIN indexes completely useless.

 

A common solution for this is to partition by month (or whatever granularity desired) and then the procedure becomes: detach old partition, dump it for the archives, drop table. Now there is nothing to vacuum at all.

 

As for parallelization, if you have large tables that are randomly accessed such as a multitenant setup, it can be desirable to partition by tenant in order to put each tenant (or group of tenants) on a separate tablespace for improved I/O.

 

One reason that is generally not valid for partitioning is the erroneous belief that multiple small tables are better for query performance than one large table. This can often decrease performance.

 



 

## Conclusion

These instructions should provide a good starting point for most OLTP workloads. Monitoring and adjusting these and other settings is essential for getting the most performance out of PostgreSQL for your specific workload. We will cover monitoring and other day-to-day tasks of a good DBA in a future document.
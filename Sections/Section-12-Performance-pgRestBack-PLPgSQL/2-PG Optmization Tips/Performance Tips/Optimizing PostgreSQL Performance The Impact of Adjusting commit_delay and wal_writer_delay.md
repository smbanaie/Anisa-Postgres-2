# [Optimizing PostgreSQL Performance: The Impact of Adjusting commit_delay and wal_writer_delay](https://demirhuseyinn-94.medium.com/optimizing-postgresql-performance-the-impact-of-adjusting-commit-delay-and-wal-writer-delay-0f4dd0402cca)

This article aims to provide practical insights into optimizing PostgreSQL database performance by adjusting the `commit_delay` and `wal_writer_delay` configuration parameters. The focus is on improving system responsiveness, reducing write latency, and enhancing the efficiency of Write-Ahead Logging (WAL) processes.

![img](https://miro.medium.com/v2/resize:fit:875/0*_Ko6NVYeQ3XlNxVh.png)

# What are commit_delay and wal_writer_delay in PostgreSQL?

**commit_delay**: This parameter controls the delay imposed on transaction commit. It represents the time, in microseconds, that a transaction commit will wait before it is acknowledged. Increasing this delay can have implications on the overall throughput and latency of the database.

**wal_writer_delay**: The Write-Ahead Logging (WAL) process in PostgreSQL involves writing changes to a transaction log before committing them to the main database. The `wal_writer_delay` parameter introduces a pause between WAL flushes, affecting the frequency of writes to the transaction log.

# What is the impact on performance?

The impact of adjusting `commit_delay` and `wal_writer_delay` on performance is closely tied to the nature of the workload and the system's architecture.

commit_delay impact: Increasing `commit_delay` can lead to improved transaction throughput, as it allows multiple transactions to be batched and committed simultaneously. However, this may come at the cost of increased latency for individual transactions.

When `commit_delay` is set to a non-zero value, PostgreSQL accumulates multiple transactions in a queue, and commits them in batches after the specified delay. This delay allows the system to gather additional transactions and execute them together, reducing the overhead associated with individual commits.

Here’s how batching and the `commit_delay` parameter are related:

1. Improved Throughput: By delaying the commit of transactions, PostgreSQL can accumulate multiple transactions and commit them together. This can result in fewer disk I/O operations and less contention, leading to improved throughput. Batching transactions is particularly useful in scenarios with a high volume of small transactions, as it helps amortize the overhead of commit operations.
2. Reduced Disk I/O: Committing transactions individually can generate a significant amount of disk I/O, especially in scenarios where there are many small transactions. Batching transactions with a delay provided by `commit_delay` allows PostgreSQL to group multiple changes into a single write operation to the disk, reducing the overall I/O load on the system.
3. Impact on Latency: While batching transactions can enhance throughput, it may increase the average latency for individual transactions. This is because each transaction must wait for the specified `commit_delay` before being acknowledged. Therefore, the choice of an appropriate `commit_delay` value is crucial to balancing improved throughput with acceptable latency for your specific use case.

wal_writer_delay impact: Similarly, adjusting `wal_writer_delay` influences the frequency of WAL flushes. A higher delay might result in fewer, larger writes to the transaction log, potentially enhancing disk I/O efficiency and reducing contention.

Reduced Frequency of WAL Flushes: When you increase the `wal_writer_delay`, PostgreSQL waits for a specified duration before flushing the changes accumulated in the WAL to the disk. This introduces a form of batching for WAL writes, as multiple changes are grouped together and written to disk in a single operation after the delay.

# How can we change these parameters?

To change these parameters, you need to modify the PostgreSQL configuration file (`postgresql.conf`). Open the configuration file in a text editor and locate the lines pertaining to `commit_delay` and `wal_writer_delay`. Adjust the values according to your requirements.

Example:

```
# postgresql.conf
# Set commit_delay to 10 milliseconds
commit_delay = 10ms
# Set wal_writer_delay to 5 milliseconds
wal_writer_delay = 5ms
```

After making these changes, restart the PostgreSQL server for the new configurations to take effect.

Alternatively, if you’re using tools like Patroni you can change or update parameters via REST api by updating configuration on DCS. We can change or update a parameter in PostgreSQL via the following bash.

```
def update_batch_confs(node_address):
        url =f'http://{node_address}:8008/config'
        headers = {'Content-Type': 'application/json'}
        data = {
            'postgresql': {
                'parameters': {
                    'wal_writer_delay': '200ms',
                     'commit_delay': '30ms' 
                }
            }
        }     
        response = requests.patch(url, json=data, headers=headers)
        if response.status_code==200:
            print(f'Configurations updated. {node_address}')
        else:
            return False
```

Finally, you can also change configurations inside database by using ALTER SYSTEM command.

```
ALTER SYSTEM SET commit_delay TO '30ms';
ALTER SYSTEM SET wal_writer_delay TO '200ms';
```

# How can we test via pgbench?

To assess the impact of your parameter adjustments, you can use `pgbench`, a simple benchmarking tool provided with PostgreSQL. Perform the following steps:

- Prepare the Database: Before running benchmarks, initialize a PostgreSQL database and generate some test data using `pgbench`.

```
pgbench -i -s 150 benchmark_delay
```

Here, `-s 150` indicates a scale factor of 150, generating data suitable for testing.

- Run pgbench Tests: Execute the actual benchmark tests with your specified parameters.

```
pgbench -c 50 -j 2 -T 180 benchmark_delay
```

In this example, `-c` sets the number of client connections, `-T` defines the duration of the test in seconds, and `-U` specifies the user.

- Analyze Results: Examine the output of `pgbench` for metrics such as Transactions Per Second (TPS) and average latency. Compare results across different configurations to observe the impact of adjusted `commit_delay` and `wal_writer_delay`.

![img](https://miro.medium.com/v2/resize:fit:755/1*rjcbh3t8YTcDxAjWjcZRNA.png)

By systematically adjusting and testing these parameters, you can fine-tune your PostgreSQL configuration to achieve optimal performance for your specific workload. Keep in mind that the optimal values may vary depending on the characteristics of your application and database usage patterns. Regular monitoring and further tuning may be necessary as your system evolves.

In conclusion, the adjustment of PostgreSQL parameters, specifically `commit_delay` and `wal_writer_delay`, can have a significant impact on database performance, especially in scenarios where write-heavy workloads are prevalent. The results obtained from benchmarking using tools like `pgbench` indicate that increasing these parameters can lead to notable improvements in average latency and transaction processing capacity.

By strategically introducing delays before transaction commits (`commit_delay`) and Write-Ahead Logging (WAL) flushes (`wal_writer_delay`), PostgreSQL allows for the batching of transactions and WAL writes. This batching approach enhances throughput by reducing the frequency of disk I/O operations and optimizing resource utilization.

However, it is crucial to emphasize that there is no one-size-fits-all configuration for these parameters, especially `commit_delay`. The optimal values depend on various factors, including the nature of the workload, system architecture, and performance expectations. Balancing the benefits of increased throughput with the potential impact on individual transaction latency is a delicate task.

Database administrators and developers must conduct thorough analyses of their database workload and understand the specific requirements of their applications. Regular monitoring and performance testing are essential to identify the optimal configuration for `commit_delay` and `wal_writer_delay` based on evolving system demands.

In the dynamic landscape of database management, where workload patterns can change over time, ongoing evaluation and adjustments to PostgreSQL configurations are critical. The key takeaway is that successful performance tuning in PostgreSQL requires a nuanced understanding of the database environment and a commitment to continuous optimization to ensure the best possible outcomes for your specific use case.

If you have questions or feedbacks please feel free to reach me via [Linkedin](https://www.linkedin.com/in/demirhuseyinnn/),[Twitter](https://twitter.com/d3rh5n) or [Gmail](http://huseyin.d3r@gmail.com/).

# References

- https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT
- https://pganalyze.com/blog/5mins-postgres-optimizing-bulk-loads-copy-vs-insert
- [https://medium.com/@hnasr/batching-in-postgresql-4b92bc1e2f87#:~:text=PostgreSQL%20has%20a%20commit_delay%20configuration,saving%20multiple%20disk%20I%2FOs](https://medium.com/@hnasr/batching-in-postgresql-4b92bc1e2f87#:~:text=PostgreSQL has a commit_delay configuration,saving multiple disk I%2FOs)
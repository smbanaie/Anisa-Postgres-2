![](images\image2.png)

In PostgreSQL, the publication/replication mechanism is used to synchronize data between different databases or instances of PostgreSQL. It works on the principle of a publisher-subscriber model, where one database acts as the publisher (also known as the master or primary) and one or more databases act as subscribers (also known as replicas or secondaries). Here's a breakdown of how the process works:

**Publisher Part:**

1. **Publication:** The publisher database creates a publication, which is a set of tables or a subset of tables whose data needs to be replicated to the subscribers.
2. **Logical Replication:** PostgreSQL uses logical replication, where the changes made to the published tables are captured in a stream of logical replication messages (known as the "write-ahead log" or WAL).
3. **Replication Slot:** The publisher creates a replication slot, which is a stream of logical replication messages that the subscribers can consume. Each subscriber has its own replication slot.
4. **WAL Shipping:** The logical replication messages are written to the WAL stream on the publisher's disk. These messages contain all the changes made to the published tables, including inserts, updates, and deletes.

**Subscriber Part:**

1. **Subscription:** The subscriber database creates a subscription to a specific publication on the publisher. This establishes a replication connection between the subscriber and the publisher.
2. **Replication Stream:** The subscriber connects to the replication slot on the publisher and starts receiving the logical replication messages from the WAL stream.
3. **Logical Decoding:** The subscriber decodes the logical replication messages and applies the changes to its local copy of the published tables. This process is called logical decoding.
4. **Conflict Resolution:** If there are any conflicts between the changes received from the publisher and the local data on the subscriber (e.g., conflicting updates), PostgreSQL provides various conflict resolution strategies that can be configured based on the application's requirements.
5. **Consistency:** The subscriber ensures that the applied changes maintain the consistency and integrity of the data, including enforcing constraints, triggers, and other database rules.

The data transfer between the publisher and the subscriber happens through the replication stream, which is a continuous flow of logical replication messages. The publisher writes these messages to the WAL stream, and the subscriber reads and applies them to its local copy of the data.

It's important to note that logical replication in PostgreSQL is asynchronous, meaning that there can be a delay between when changes are made on the publisher and when they are applied on the subscriber. However, PostgreSQL ensures that the changes are applied in the correct order, maintaining data consistency.

Additionally, PostgreSQL supports various replication topologies, such as cascading replication (where a subscriber can also act as a publisher for other subscribers), bi-directional replication, and multi-master replication with conflict resolution.

In PostgreSQL's logical replication, the entire write-ahead log (WAL) is not transferred from the publisher to the subscriber. Instead, only the relevant portions of the WAL are streamed to the subscriber.

Here's how it works:

1. **WAL Streaming**: When a subscriber establishes a replication connection with the publisher, it creates a replication slot on the publisher. The replication slot is a stream of logical replication messages from the WAL that the subscriber can consume.
2. **Logical Replication Messages**: The WAL on the publisher contains all the changes made to the database, including changes to both published and non-published tables. However, the logical replication messages streamed to the subscriber only contain changes related to the published tables.
3. **Decoding and Filtering**: The publisher has a component called the logical decoding output plugin, which decodes the WAL and filters out the changes that are not relevant to the subscriber's subscribed publications. Only the logical replication messages pertaining to the subscribed publications are streamed to the subscriber.
4. **WAL Segments**: The WAL on the publisher is divided into segments (files) of a fixed size (e.g., 16MB by default). When a subscriber connects to the replication slot, it starts streaming the logical replication messages from the WAL segment where the slot was created. As the publisher writes new WAL segments, the subscriber continues to stream the relevant messages from those new segments.
5. **Batch Streaming**: The logical replication messages are not streamed one-by-one to the subscriber. Instead, they are batched together and sent in chunks to improve efficiency and reduce network overhead.

So, in summary, the entire WAL is not transferred from the publisher to the subscriber. Instead, only the logical replication messages relevant to the subscribed publications are decoded, filtered, and streamed to the subscriber. This selective streaming of logical replication messages ensures that only the necessary data is transferred, reducing the network bandwidth and resource consumption on both the publisher and the subscriber.

Additionally, PostgreSQL provides mechanisms to manage the WAL segments on the publisher, allowing for the removal of old segments that are no longer needed by any of the subscribers, thereby freeing up disk space.
#### Download Kafka & Zookeeper

- Download  Kafka

  - [Apache Kafka official Download Page](https://kafka.apache.org/downloads)
    - Binaries : Scala 2.13  - [kafka_2.13-3.6.1.tgz](https://downloads.apache.org/kafka/3.6.1/kafka_2.13-3.6.1.tgz)
  
- **In Linux or WSL :**
  
  ```bash
  $ wsl
  $ java -version
  $ tar xfvz kafka_2.13-3.6.1.tgz
  $ cd kafka_2.13-3.6.1
  ```
  
     NOTE: Your local environment must have Java 8+ installed.    
      Run the following commands in order to start all services in the correct order:
      
  
  ```bash
  # Start the ZooKeeper service
  # Note: Soon, ZooKeeper will no longer be required by Apache Kafka.
  $ bin/zookeeper-server-start.sh config/zookeeper.properties
  ```
  
    Open another terminal session and run:    
  ```bash
  # Start the Kafka broker service
  $ bin/kafka-server-start.sh config/server.properties
  ```
  
-  **Windows** :
   
  - install `JAVA`
    - [دانلود Java SE Runtime Environment 8.0.291 + JDK Win/Mac/Linux - دانلود نرم افزار اجرای جاوا (soft98.ir)](https://soft98.ir/software/692-sun-java-se-runtime-environment.html)
    - set `JAVA_HOME` Environment Variable.
    - check ` java -version` in bash.
  - first `unzip` kafka_2.13-3.6.1.tgz 
  - rename   kafka_2.13-3.6.1.tgz  to kafka (to prevent error : `input line is too long`)
  - check out that in Kafka installation folder, there is not a Folder-Name that contains `Space`
  
  ```bash
  $ cd kafka
  ```
  
  ​    Run the following commands in order to start all services in the correct order:    
  
  - in `config/zookeeper.properties` , change `dataDir` to a correct folder 
    - `dataDir=data/zookeeper`
  
  ```bash
  
  # Note: Soon, ZooKeeper will no longer be required by Apache Kafka.
  $  .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
  ```
  
    **Open another terminal session and run:**    
  ```bash
  # Start the Kafka broker service
  $ .\bin\windows\kafka-server-start.bat .\config\server.properties
  ```
  
  Once all services have successfully launched, you will have a basic Kafka environment running and ready to use

#### Working With Topic

- Open new console & go to Kafka folder 

  - Create Topic `users`

  ```bash
  .\bin\windows\kafka-topics.bat --bootstrap-server localhost:9092 --create  --topic users  --partitions 4 --replication-factor 1
  
  or 
  
  ./bin/kafka-topics.sh --create --topic users --bootstrap-server localhost:9092 --partitions 4 --replication-factor 1
  ```
  
  - List topics 
  
  ```bash
  .\bin\windows\kafka-topics.bat --bootstrap-server localhost:9092 --list
  ```
  
  - Describe topic `users`
  
  ```bash
  .\bin\windows\kafka-topics.bat --bootstrap-server localhost:9092 --describe --topic users
  Topic: users    TopicId: rfNJN88nTpirIno2z9LKMQ PartitionCount: 4       ReplicationFactor: 1    Configs: segment.bytes=1073741824
          Topic: users    Partition: 0    Leader: 0       Replicas: 0     Isr: 0
          Topic: users    Partition: 1    Leader: 0       Replicas: 0     Isr: 0
          Topic: users    Partition: 2    Leader: 0       Replicas: 0     Isr: 0
          Topic: users    Partition: 3    Leader: 0       Replicas: 0     Isr: 0
  ```
  
  
  Example of `--describe` option :
  
  ```
  Topic: orders
  Partition: 2
  Leader: 1
  Replicas: 1,2,3
  Isr: 1,3
  ```
  
  In this example:
  
  - The topic is "orders."
  
  - We're describing partition 2 of the "orders" topic.
  
  - The leader for partition 2 is broker 1.
  
  - There are three replicas for partition 2, located on brokers 1, 2, and 3.
  
  - The In-Sync Replicas (ISR) for partition 2 are brokers 1 and 3. This means that brokers 1 and 3 are currently synchronized with the leader (broker 1) and are actively participating in the replication process.
  
---

  - Produce some data

  ```bash
  .\bin\windows\kafka-console-producer.bat --bootstrap-server localhost:9092 --property key.separator=, --property parse.key=true --topic users
  >1, ali
  >2, ahmad
  >3, sara
  >1, ali2
  >2, ahmad2
  >3, sara2
  (Ctrl+C to terminate )
  ```

1. `--property key.separator=,`: This sets a property for the producer. It specifies that the key and value of each message should be separated by a comma (`,`). This is relevant when you're producing messages with a key-value pair format.
2. `--property parse.key=true`: This property tells the producer to parse the message keys. When you set `parse.key=true`, the producer expects the input messages to be in a format where the key and value are separated by the specified `key.separator`. The key will be extracted and used as the message key, and the remaining part of the input will be used as the message value.

  - Consume these data

  ```bash
  .\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic users --from-beginning
   ali
   sara
   ali2
   sara2
   ahmad
   ahmad2
  Processed a total of 6 messages
  Terminate batch job (Y/N)? y
  
  ```

  - show messages with details

  ```bash
  .\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic users --from-beginning  --property print.timestamp=true --property print.key=true --property print.value=true
  CreateTime:1624556004432        1        ali
  CreateTime:1624556019408        3        sara
  CreateTime:1624556075869        1        ali2
  CreateTime:1624556087056        3        sara2
  CreateTime:1624556721897        60      kamran
  CreateTime:1624556626796        10      ali
  CreateTime:1624556630190        20      sara
  CreateTime:1624556712556        40      elham
  CreateTime:1624556010087        2        ahmad
  CreateTime:1624556081285        2        ahmad2
  
  ```

  - Delete topics

  ```bash
  .\bin\windows\kafka-topics.bat --bootstrap-server localhost:9092 --delete  --topic users 
  ```

  


# Setting up High Availability PostgreSQL Cluster using Patroni, PGBouncer, Docker, Consul and HAProxy

![Nicola Vitaly](https://miro.medium.com/v2/resize:fill:55:55/1*07_guWF_uSdK4Qwvso3eWQ.jpeg)

This article will cover how to setup a Highly Available (HA) PostgreSQL database cluster at multiple VMs that will run on docker containers using docker-compose.

**The Concept**

High availability database cluster can support load balancing and hot-standby, so if one of the node fails, other node can be promoted to be master node automatically. Keep in mind that only master node can write to database, slave nodes only capable of processing read-only queries.

![img](https://miro.medium.com/v2/resize:fit:875/0*sdHjLBldn47HWiSw.jpeg)

https://blog.timescale.com/blog/high-availability-timescaledb-postgresql-patroni-a4572264a831/

![img](https://miro.medium.com/v2/resize:fit:875/0*Bst5j9kRTzH3oIsJ.png)

https://images.app.goo.gl/XBxgwzhbTfEdVoQN6

User will connect to the database through HAProxy’s (Load balancer) IP that will forward the session to [PGBouncer](https://www.pgbouncer.org/). PGBouncer here will act as a lightweight connection pooler for PostgreSQL. Each PGBouncer is connected to one PostgreSQL node.

> Each PostgreSQL node has a Patroni bot deployed on it. The bots are capable both of managing the PostgreSQL database and updating the distributed consensus system (etcd in this case although Zookeeper, Consul, and the Kubernetes API, which is backed by etcd, are also perfectly fine options). Etcd must be deployed in an HA fashion that allows its individual nodes to reach a quorum about the state of the cluster. This requires a minimum deployment of 3 etcd nodes.
>
> Leader election is handled by attempting to set an expiring key in etcd. The first PostgreSQL instance to set the etcd key via its bot becomes the primary. Etcd ensures against race conditions with a Raft-based consensus algorithm. When a bot receives acknowledgement that it has the key, it sets up the PostgreSQL instance as a primary. All other nodes will see that a primary has been elected and their bots will set their PostgreSQL instances up as replicas.

In the upcoming setup we will use [Consul](https://www.consul.io/) cluster instead of *etcd.*

**HAProxy**

[HAProxy](http://www.haproxy.org/) in this case will act not only as proxy but also act as load balancer. We can separate read and write connection to separate ports.

Example of *haproxy.cfg*

```
listen postgres_write
    bind *:5432
    mode            tcp
    option httpchk
    http-check expect status 200
    default-server inter 10s fall 3 rise 3 on-marked-down shutdown-sessions
    server postgresql_1 postgresql_1_ip:5432 check port 8008
    server postgresql_2 postgresql_2_ip:5432 check port 8008

listen postgres_read
    bind *:5433
    mode            tcp
    balance leastconn
    option pgsql-check user admin
    default-server inter 10s fall 3 rise 3 on-marked-down shutdown-sessions
    server postgresql_1 postgresql_1_ip:5432
    server postgresql_2 postgresql_2_ip:5432
```

HAProxy will process connection from port 5432 as write connection and port 5433 as read only connection to PGBouncer (port 5432) node.. Write connection will only be sent to master database node. HAProxy can check which node is master by checking port 8008 (Patroni API). For the read only connection will be balanced to all database nodes with `balance leastconn` option at HAProxy config.

HAProxy docker-compose file

```
haproxy:
  image: haproxy
  ports:
    - "5432:5432"
    - "5433:5433"
  restart: unless-stopped
```

**PostgreSQL and Patroni**

In this setup, we will install [Patroni](https://patroni.readthedocs.io/en/latest/) inside PostgreSQL base image using *python pip* because patroni will need access to PostgreSQL binaries.

*Dockerfile* example

```
FROM postgres

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
RUN pip3 install wheel

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./patroni.yml /patroni.ymlENTRYPOINT ["patroni", "patroni.yml"]
```

inside *requirements.txt*

```
urllib3>=1.19.1,!=1.21
boto
PyYAML
six >= 1.7
kazoo>=1.3.1
python-etcd>=0.4.3,<0.5
python-consul>=0.7.1
click>=4.1
prettytable>=0.7
tzlocal
python-dateutil
psutil>=2.0.0
cdiff
psycopg2-binary
psycopg2>=2.5.4
patroni
```

Patroni configuration

```
patroni.yml
scope: cluster_1

restapi:
    listen: 0.0.0.0:8008 
    connect_address: 10.128.0.18:8008
bootstrap:
    dcs:
        ttl: 130
        loop_wait: 10
        retry_timeout: 60
        maximum_lag_on_failover: 1048576
        postgresql:
            use_pg_rewind: true
            parameters:
                max_connections: 550
                max_locks_per_transaction: 512
                max_worker_processes: 27

    initdb:
    - encoding: UTF8
    - data-checksums


    users:
        admin:
            password: admin
            options:
                - createrole
                - createdb



postgresql:
    listen: 0.0.0.0:5432
    connect_address: 10.128.0.18:6432
    config_dir: /config
    data_dir: /var/lib/postgresql/data
    pg_hba:
        - host replication replicator 127.0.0.1/32 md5
        - host replication replicator 10.128.0.18/32 md5
        - host replication replicator 10.128.0.98/32 md5 
        - host replication replicator 10.128.0.99/32 md5
        - host all all 0.0.0.0/0 md5
    authentication:
        replication:
            username: replicator
            password: replicator
        superuser:
            username: postgres
            password: supersecret

tags:
    nofailover: false
    noloadbalance: false
    clonefrom: false
    nosync: false
```

Some PGSQL configuration parameters like `max_connections` need to be the same across all nodes, this will be managed by Patroni.

Patroni docker-compose file

```
patroni:
  image: patroni-image 
  networks:
    - postgres-backend
  ports:
    - "8008:8008"
    - "6432:5432"
  user: postgres
  volumes:
    - postgres-data:/var/lib/postgresql/data
  environment:
    TZ: Asia/Jakarta
    PATRONI_NAME: member_1
    PATRONI_POSTGRESQL_DATA_DIR: /var/lib/postgresql/data/node1
    PATRONI_CONSUL_HOST: http://consul-ip:8500
    PATRONI_CONSUL_URL: http://consul-ip:8500/v1/
  restart: unless-stopped
```

Node name `PATRONI_NAME: member_1` must be unique for each node. We use port 6432 as published database port because we will use port 5432 for PGBouncer.

**PGBouncer**

PGBouncer docker-compose file

```
pgbouncer:
  image: edoburu/pgbouncer   
  networks:
    - postgres-backend
  ports:
    - "5432:5432"
  depends_on:
    - patroni
  environment:
    TZ: Asia/Jakarta
    ADMIN_USERS: admin
    DB_HOST: patroni
    DB_USER: admin
    DB_PASSWORD: admin
    POOL_MODE: transaction
    MAX_CLIENT_CONN: 1000
    DEFAULT_POOL_SIZE: 300
  restart: unless-stopped
```

> **pgbouncer** is a PostgreSQL connection pooler. Any target application can be connected to **pgbouncer** as if it were a PostgreSQL server, and **pgbouncer** will create a connection to the actual server, or it will reuse one of its existing connections.
>
> The aim of **pgbouncer** is to lower the performance impact of opening new connections to PostgreSQL.

**Consul**

Consul cluster will act as voter to determine which node is master or slave. An odd number of consul node is advised, in this case we will use 3 consul nodes.

Consul docker-compose file

```
consul:
    image: consul
    hostname: "${HOSTNAME}"
    environment:
      TZ: Asia/Jakarta
    ports:
      - "8300:8300"
      - "8301:8301"
      - "8301:8301/udp"
      - "8302:8302"
      - "8302:8302/udp"
      - "8400:8400"
      - "8500:8500"
      - "8600:8600/udp"
    volumes:
      - consul-data:/data
    restart: unless-stopped
    command: agent -server -advertise 10.128.0.18 -bootstrap-expect 3 -client 0.0.0.0 -retry-join 10.128.0.18 -retry-join 10.128.0.98 -retry-join 10.128.0.99
volumes:
  consul-data:
```

Advertise IP need to be adjusted in each consul node docker-compose file
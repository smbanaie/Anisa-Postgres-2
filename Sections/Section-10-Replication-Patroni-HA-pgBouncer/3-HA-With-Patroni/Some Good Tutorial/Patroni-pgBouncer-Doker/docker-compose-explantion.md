### Diagram

Here is a high-level diagram of the architecture:

```plaintext
                         +--------------+
                         |              |
                         |   HAProxy    |
                         |   (Load      |
                         |   Balancer)  |
                         |              |
                         +------+-------+
                                |
                                |
            +-------------------+-------------------+
            |                                       |
            |                                       |
  +---------v----------+                   +--------v---------+
  |                    |                   |                  |
  |    PGBouncer       |                   |     PGBouncer    |
  |    (Connection     |                   |    (Connection   |
  |    Pooler)         |                   |    Pooler)       |
  |                    |                   |                  |
  +--------------------+                   +------------------+
            |                                       |
            |                                       |
  +---------v----------+                   +--------v---------+
  |                    |                   |                  |
  |   Patroni +        |                   |   Patroni +      |
  |   PostgreSQL       |                   |   PostgreSQL     |
  |   (Primary/Replica)|                   |   (Primary/Replica)|
  |                    |                   |                  |
  +--------------------+                   +------------------+
            |                                       |
            +-------------------+-------------------+
                                |
                                |
                         +------+-------+
                         |              |
                         |   Consul     |
                         |   (Quorum)   |
                         |              |
                         +--------------+
```

### Complete Docker-Compose File

Here's the complete `docker-compose.yml` file incorporating all the services:

```yaml
version: '3'

services:
  haproxy:
    image: haproxy
    ports:
      - "5432:5432"
      - "5433:5433"
    restart: unless-stopped
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg

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
      - ./patroni.yml:/etc/patroni.yml
    environment:
      TZ: Asia/Jakarta
      PATRONI_NAME: member_1
      PATRONI_POSTGRESQL_DATA_DIR: /var/lib/postgresql/data/node1
      PATRONI_CONSUL_HOST: http://consul:8500
      PATRONI_CONSUL_URL: http://consul:8500/v1/
    restart: unless-stopped

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

networks:
  postgres-backend:

volumes:
  postgres-data:
  consul-data:
```

### Additional Configuration Files

**haproxy.cfg**

```plaintext
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

**Dockerfile for Patroni**

```Dockerfile
FROM postgres

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
RUN pip3 install wheel

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./patroni.yml /etc/patroni.yml
ENTRYPOINT ["patroni", "/etc/patroni.yml"]
```

**requirements.txt for Patroni**

```plaintext
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

**patroni.yml**

```yaml
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

With these configurations, you should be able to set up a highly available PostgreSQL cluster using Patroni, PGBouncer, Docker, Consul, and HAProxy.
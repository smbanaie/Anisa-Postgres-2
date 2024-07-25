# How to launch a pgbouncer container

## Safely scale out the application servers while maintaining a minimal number of database connections



# What is pgbouncer

**pgbouncer is connection pooling middleware software** between the application servers & Postgres DB instance. The purpose of connection pooling is **to make it efficient for applications to connect to Postgres instances**. How does pgbouncer do this? By reusing the connections to the database.

In Postgres (and generally most databases), it's really costly to establish a connection, taking **around 1.5–14.5 MB per connection.** If you have 100 open connections to the database, that will take a maximum of ~1.45GB of RAM just to maintain the connections, which is a waste. Remember, any wasted resources translate to money loss. Moreover, most DBaaS offerings today limit the number of connections per database instance. For example, Heroku Postgres Standard 0 instance priced at $50 only allows up to 120 connections. When you need to scale out your backend servers beyond that limit, that's when you need connection pooling between application servers and Postgres instances.

![img](E:\BigDataCourses\Anisa\Sections\Section-13-Patroni-HA-pgBouncer\2-HA-With-Patroni\3-Patroni-pgBouncer\1.png)

Comparison between systems with and without connection pooling

From the application server's point of view, it thinks it's connected to a regular Postgres server. It doesn't have that connection pool notion. Application server here refers to your backend software, whether they're written in Laravel PHP, Python Django, Ruby on Rails, etc.

## Advantages

- **You can scale out your application server well**. In my experience, it doesn't mean that you can scale your server limitlessly; instead, it lifts the limit. For example, previously, your Postgres instance can support up to 100 servers. With pgbouncer, it probably can support up to 500 servers. This number depends on your workload.
- **pgbouncer can act as database routing**. You can connect a single pgbouncer instance to multiple different database instances. From there, you can set the routing accordingly.
- **It can protect your database instance from massive connections establishments.** In pgbouncer, you can set the maximum number of connections to the Postgres server and the maximum number of connections to application servers. If your system tries to open connections beyond the maximum number of allowed connections, the pgbouncer will reject the connection before reaching the upstream database server.

## Disadvantages

Everything comes at a cost.

- **It adds a new element to your existing system.** This means your system complexity has increased. Operating a new piece of software require skills and effort to keep them running correctly.
- **It may be the single point of failure in your system** unless you set up a high availability model using HAproxy or AWS Network Load Balancer. Again, high availability setup is not an easy task.

## Don't get confused with application-level connection pooling

You may have noticed that many ORMs, database adapters, and web frameworks today have built-in connection pooling features. You can see in their documentations: [Ruby on Rails](https://api.rubyonrails.org/classes/ActiveRecord/ConnectionAdapters/ConnectionPool.html), [Django](https://docs.djangoproject.com/en/4.0/ref/databases/#persistent-connections), [Sequelize.js](https://sequelize.org/master/manual/connection-pool.html), [Prisma](https://www.prisma.io/docs/concepts/components/prisma-client/working-with-prismaclient/connection-pool), [Elixir Ecto](https://hexdocs.pm/phoenix/ecto.html#repo-configuration), [Go Database](https://go.dev/doc/database/manage-connections), etc.

![img](E:\BigDataCourses\Anisa\Sections\Section-13-Patroni-HA-pgBouncer\2-HA-With-Patroni\3-Patroni-pgBouncer\2.png)

Application-level connection pooling

**The application-level connection pooling only manages the threads among the server-level threads**. If you spin up hundreds of servers, each of them will establish connections to the database servers, resulting in a high number of connections. This does not solve the high connection number issue when you’re adding servers to your system.

## When to use pgbouncer

In my opinion, you should only **use pgbouncer when you are scaling out application servers, and your database connection is exhausting**. For example, your database allows up to 100 connections, but you have 200 application servers (and each runs multiple threads). Theoretically, your database instances won't be able to handle that 200+ database connections from the application servers, and this is the ideal use case for pgbouncer.

If you do not need many servers to support your users, you better NOT use connection pooling as the benefit is minimal.

## When NOT to use pgbouncer

**You should NOT use pgbouncer to speed up your queries**. Consider doing the low-hanging fruit optimizations first, like adding relevant table indexing, building materialized views, scaling up your database server, etc., before actually installing pgbouncer in your system.

Installing pgbouncer won't help much if your queries are slow.

## Which companies are using pgbouncer

They are pretty popular among large scale internet companies



# Let's start

## #1 Launch Postgres container (Optional)

```
$ docker run \
    -e POSTGRES_PASSWORD=password 
    --network=host
    --name postgres
    postgres
```

You can skip this step if you already have a database running on your laptop or in the cloud.

Note that we're using the host network when launching this Docker container so that the pgbouncer container in step #2 can reach it.

## #2 Launch pgbouncer container

To launch a pgbouncer container, you'll need the following environment variables:

```
$ docker run \
    -e "POSTGRESQL_HOST=localhost" \
    -e "POSTGRESQL_USERNAME=postgres" \
    -e "POSTGRESQL_PASSWORD=password" \
    -e "POSTGRESQL_DATABASE=postgres" \
    -e "PGBOUNCER_POOL_MODE=transaction" \
    -e "PGBOUNCER_PORT=6432" \
    --network=host \
    --name=pgbouncer \
    bitnami/pgbouncer
```

In this code snippet, we're using `transaction pool mode`. Generally, this is what you want as this is the efficient one, but this comes with a caveat. Transaction pool mode does work with prepared statements, which is the default in Ruby on Rails. If you're using Ruby on Rails, [you can disable this in database.yml](https://stackoverflow.com/questions/22813750/how-to-disable-prepared-statement-in-heroku-with-postgres-database).

There are multiple pgbouncer Docker images available. Personally, I prefer the [Bitnami pgbouncer Docker image](https://github.com/bitnami/bitnami-docker-pgbouncer) because they are more up-to-date than the others.

## #3 Connect to the database

```
$ psql -h localhost -U postgres -d postgres -p 6432 -W
$ <PASSWORD>
```

Remember to set the database to `postgres` as that's the default database name specified in the Docker container.

## #4 Teardown

To remove the containers created, run the following command

```
$ docker rm -f pgbouncer postgres
```

# What's next

If you just want to use pgbouncer for a single database instance, then you're good to go. However, the pgbouncer has many more things to offer. Please consider learning how to manually configure `pgbouncer.ini` file. From there, you can change its logging configuration, admin user credentials, upstream database user credentials, etc. It's also essential for you to understand which `pool mode` suits your workload.

Bear in mind that there are several other connection pooling software alternatives out there. For Postgres, you can check out [pgpool](https://www.pgpool.net/mediawiki/index.php/Main_Page) and [Yandex Odessey](https://github.com/yandex/odyssey). If you're using MySQL, you can check out [ProxySQL](https://proxysql.com/) and [Vitess](https://vitess.io/docs/12.0/overview/whatisvitess/).

# **Bonus: Connecting pgbouncer to Heroku**

To connect to Heroku Postgres, we'll need to use an SSL connection from the pgbouncer to the Postgres server.

```
$ docker run \
    -e "POSTGRESQL_HOST=<HEROKU PG HOST>" \
    -e "POSTGRESQL_USERNAME=<HEROKU PG USERNAME>" \
    -e "POSTGRESQL_PASSWORD=<HEROKU PG PASSWORD>" \
    -e "POSTGRESQL_DATABASE=<HEROKU PG DBNAME>" \
    -e "PGBOUNCER_POOL_MODE=transaction" \
    -e "PGBOUNCER_SERVER_TLS_SSLMODE=require" \
    -e "PGBOUNCER_SERVER_TLS_PROTOCOLS=secure" \
    -p 6432:6432 \
    --name=pgbouncer \
    bitnami/pgbouncer
```

## How did I discover this

*This part is more about ranting about my first experience with the pgbouncer container. You can skip this part if you're not interested.*

Recently, I hit a scalability issue where I needed to scale my Sidekiq workers into a specific number, but that's huge enough to hurt my Heroku Postgres instance. For testing, I wanted to launch pgbouncer from my laptop and connect to the remote Heroku Postgres instance.

After hours of searching, I discovered that Heroku does actually offer a pgbouncer buildpack. However, I don't want to launch that pgbouncer in my Heroku Dyno but instead on my local laptop. I've always wanted to use connection pooling software before, but it wasn't always the time.

After hours of debugging, I wondered why I couldn't establish a connection between my pgbouncer and the Heroku. The good thing is source code is available here on Github.



In the [gen-pgbouncer-conf.sh](https://github.com/heroku/heroku-buildpack-pgbouncer/blob/main/bin/gen-pgbouncer-conf.sh) file, we can see that it is using the secure server connection.

```
server_tls_sslmode = prefer
server_tls_protocols = secure
server_tls_ciphers = HIGH:!ADH:!AECDH:!LOW:!EXP:!MD5:!3DES:!SRP:!PSK:@STRENGTH
```

It turns out that I need to enforce the SSL connection to the Heroku server. From there, I can replicate the same settings in my local Docker container, and then voila! It works perfectly fine!
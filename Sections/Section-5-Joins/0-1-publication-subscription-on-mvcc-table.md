#### Publication/Subscription

- create a new postgres service in docker-compose and name it `postgres2` 
- start the services.
- change the `wal_level` to `logical` in both postgres instances.
- restart the postgres instances. 
- create the table `mvcc` as we done before 
- create a `pub_mvcc` publisher in the postgres1 . 
- create a `mvcc` table in the  `postgres2`
- create a `sub_mvcc` on `postgres2`
- insert some data on `postgres1` 
- check out the second table!
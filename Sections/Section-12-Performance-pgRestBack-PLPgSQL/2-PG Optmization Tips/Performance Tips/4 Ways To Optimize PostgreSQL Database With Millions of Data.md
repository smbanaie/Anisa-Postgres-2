# [4 Ways To Optimize PostgreSQL Database With Millions of Data](https://medium.com/geekculture/4-ways-to-optimise-postgresql-database-with-millions-of-data-c70e11d27a94)

This series consists of two articles:

1. [How to create 37.5 million data in PostgreSQL in a matter of seconds](https://medium.com/geekculture/how-to-create-37-5-million-data-in-postgresql-in-a-matter-of-seconds-858693976d17?sk=888ccfc6d0747b5df266955497ce7e7a)
2. [4 Ways To Optimise PostgreSQL Database With Millions of Data](https://josipvojak.com/4-ways-to-optimise-postgresql-database-with-millions-of-data-c70e11d27a94?sk=d2c6b400b64e89304a0a2da28eb83531)

![img](https://miro.medium.com/v2/resize:fit:875/1*AgHClKqVbgWRiCV8Z_pi0A.jpeg)

Database optimisation is actually a set of techniques by which we usually want some of the following:

- **speed up database operations**
- **reduce the load**
- **reduce the size of the database**
- **take advantage of the out-of-the-box feature to help with overall database optimization**

In a previous article, we generated real data using the **generate_series()** function — which helps create large amounts of test data in a short amount of time.

If you are interested to read it, here’s a link:

## How to create 37.5 million data in PostgreSQL in a matter of seconds

### Create a ton of predefined data using this simple and effective technique.

medium.com

For those who have read, let me remind you — and for those who have not read, let me introduce you to what happened:

We imitated the behavior of miners for an imaginary cryptocurrency — we had several miners, which differed according to the number of graphics cards:

We created three tables:

- **hours**
- **miners**
- **miner_data**

The ***hours\*** table contained the intensity of the computer cooler at certain hours of the day
The ***miners\*** table contains basic data, such as name and number of graphic cards:

```
+-----+------------+----------------+
| id  |    name    |  graphic_cards |
+-----+------------+----------------+
|  1  |  Diamond   |             10 |
|  2  |  Platinum  |              7 |
|  3  |  Gold      |              4 |
|  4  |  Silver    |              3 |
|  5  |  Bronze    |              2 |
|  6  |  Default   |              1 |
+-----+------------+----------------+
```

The ***miner_data\*** table contained a total of 37.5 million data on the behavior of the computer fan over the days, for a period of one year (*Oct 14 2020 — Oct 14 2021*):

```
// ascending (first entry)
select * from miner_data order by time asc limit 1;          time          | miner_name |  fan_percentage   
------------------------+------------+-------------------
 2020-10-14 00:00:00+02 | Silver     | 80.02813264708547
(1 row)
Time: 10228.051 ms (00:10.228)// descending (last entry)
select * from miner_data order by time desc limit 1;          time          | miner_name |  fan_percentage
------------------------+------------+------------------
 2021-10-14 00:00:00+02 | Platinum   | 74.8233384374659
(1 row)
```

The data was generated with 5-minute time intervals.

**As you can see above, simple queries like SELECT, where data is sorted by time and a limit of 1 or 10 records is set, last for an awful 10–12 seconds.**

## EXPLAIN vs. EXPLAIN ANALYZE

PostgreSQL offers two interesting commands — **EXPLAIN** and **EXPLAIN** **ANALYZE**.

The difference is that EXPLAIN shows you query cost based on collected statistics about your database, and EXPLAIN ANALYZE actually runs it to show the processed time for each stage.

There’s a high recommendation to use EXPLAIN ANALYZE because there are a lot of cases when EXPLAIN shows a higher query cost, while the time to execute is actually less and vice versa. The most important thing is that the EXPLAIN command will help you to understand if a specific index is used and how.
The ability to see indexes is the first step to learning PostgreSQL query optimization.

Here are the results on the example of the query above:

<iframe src="https://medium.com/media/e7bba13f680e5084f42126b6f4358f43" allowfullscreen="" frameborder="0" height="649" width="680" title="explain_analyze.txt" class="fp n gf dv bg" scrolling="no" style="box-sizing: inherit; top: 0px; width: 680px; height: 649px; left: 0px;"></iframe>

EXPLAIN vs EXPLAIN ANALYZE

Now, let’s see the four simple steps which can improve your database performance.

# 1. Database Indexing

A database index is **a data structure that improves the speed of data retrieval operations** on a database table **at the cost of additional writes and storage space** to maintain the index data structure.

How to see which indexes are automatically set by PostgreSQL when creating the table?

```
SELECT
  tablename,
  indexname,
  indexdef
FROM
  pg_indexes
WHERE
  schemaname = ‘miner_data’
ORDER BY
  tablename,
  indexname;
```

Let’s try to create a simple index on the time and miner name columns:

```
CREATE INDEX ON miner_data(“time”, “miner_name”);SELECT * FROM miner_data LIMIT 1;
+-------------------------+--------------+--------------------+
|     time                |  miner_name  |    fan_percentage  |
+-------------------------+--------------+--------------------+
| 2020-10-14 00:00:00+02  |  Silver      |  80.02813264708547 |
+-------------------------+--------------+--------------------+(1 row)
Time: 0.469 ms
```

**Pre-optimization: 12004.737 ms**

**Post-optimization: 0.469 ms**

As we can see, the simplest addition of the index led us to an improvement of a huge **25,596 times!**

So, indexing is something you need to pay attention to if you are dealing with larger amounts of data.

# 2. Query optimization

Let’s say we want to retrieve the maximum value of a computer cooler for each individual miner through the time.

Query could look something like this:

```
SELECT 
 miner_name, 
  MAX(fan_percentage) 
FROM miner_data 
WHERE miner_name IN 
  (SELECT DISTINCT "name" 
   FROM miners) 
GROUP BY 1 
ORDER BY 1; miner_name |        max        
------------+-------------------
 Bronze     |  94.9998652175735
 Default    | 94.99994839358486
 Diamond    | 94.99999006095052
 Gold       |  94.9998083591985
 Platinum   | 94.99982552531682
 Silver     | 94.99996029210493Time: 9173.750 ms (00:09.174)
```

Regardless of setting the index, this operation is expensive.

It took us **more than 9 seconds** to do that. Imagine that one of the features on your website is that you allow the user to view such a set of data and that the page loads for a minimum of 9 seconds (not taking into account other data and queries, additional data processing, latency, etc.).

Who would want to wait for 10 seconds to get the data?

What we can do here, for example, is to rewrite the query in a different way, in order to reduce the number of required operations, the number of viewed and compared rows and thus speed up query:

```
SELECT 
  DISTINCT ON (miner_name) miner_name, 
  MAX(fan_percentage) 
FROM miner_data 
GROUP BY miner_name;miner_name |        max        
------------+-------------------
 Bronze     |  94.9998652175735
 Default    | 94.99994839358486
 Diamond    | 94.99999006095052
 Gold       |  94.9998083591985
 Platinum   | 94.99982552531682
 Silver     | 94.99996029210493Time: 2794.690 ms (00:02.795)
```

By writing query in a smarter way, we saved ourselves time.

**Pre-optimization: 9173.750 ms**

**Post-optimization: 2794.690 ms**

For this case, by writing query in a better way, **we speeded up the process by 3.28x.**

# 3. Creating Materialized View

A materialized view is **a pre-computed data set derived from a query specification** (the SELECT in the view definition) and stored for later use. Because the data is pre-computed, querying a materialized view is faster than executing a query against the base table of the view.

If we use the query from above:

```
SELECT 
 DISTINCT ON (miner_name) miner_name,
 MAX(fan_percentage) 
FROM miner_data 
GROUP BY miner_name;
```

and make it a materialized view, named **max_fan_percentage_by_miner**:

```
CREATE MATERIALIZED VIEW max_fan_percentage_by_miner AS 
SELECT 
 DISTINCT ON (miner_name) miner_name,
 MAX(fan_percentage) FROM miner_data
GROUP BY miner_name;
```

Let’s look at the time to retrieve the maximum value of a computer cooler per miner using materialized view:

```
SELECT * FROM max_fan_percentage_by_miner; miner_name |        max        
------------+-------------------
 Bronze     |  94.9998652175735
 Default    | 94.99994839358486
 Diamond    | 94.99999006095052
 Gold       |  94.9998083591985
 Platinum   | 94.99982552531682
 Silver     | 94.99996029210493Time: 0.247 ms
```

**Pre-optimization: 2794.690 ms**

**Post-optimization: 0.247 ms**

Data retrieval was improved 11,314.53 times.

# 4. Normalizing Tables (Using Foreign Keys)

This is a pretty basic one, but it should be noted. As it can be seen from the attached — although there is a ***miners\*** table that contains the miner **id** (which is an integer), the miner name with some other things — in the **miner_data** table we use the miner name instead of its ID.

We can normalise the table, use the foreign key as a relation to the miners table (column “**id”**).

**INT (integer) comparisons are faster than VARCHAR comparisons, for the simple fact that INTs take up much less space than VARCHAR.**

This holds true both for unindexed and indexed access. **The fastest way to go is an INDEXED INT column.**

# Conclusion

While these are some basic optimization techniques, they can bear very big fruit. Also, although these techniques are simple, it is not always easy to:

- know how to **optimize query**
- create a sufficient and valid number of **database indexes** without creating huge amounts of data on disk — thereby perhaps doing a counter effect and encouraging the database to search in the wrong way
- know when it is better to use **VIEW** and when to use **MATERIALIZED VIEW**

You will need to play with the data, until you find an adequate formula that will suit your model.
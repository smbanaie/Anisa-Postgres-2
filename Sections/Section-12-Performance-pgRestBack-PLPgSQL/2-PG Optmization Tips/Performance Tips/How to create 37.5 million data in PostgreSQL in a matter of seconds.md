# [How to create 37.5 million data in PostgreSQL in a matter of seconds](https://medium.com/geekculture/how-to-create-37-5-million-data-in-postgresql-in-a-matter-of-seconds-858693976d17)

This series consists of two articles:

1. [How to create 37.5 million data in PostgreSQL in a matter of seconds](https://medium.com/geekculture/how-to-create-37-5-million-data-in-postgresql-in-a-matter-of-seconds-858693976d17?sk=888ccfc6d0747b5df266955497ce7e7a)
2. [4 Ways To Optimise PostgreSQL Database With Millions of Data](https://josipvojak.com/4-ways-to-optimise-postgresql-database-with-millions-of-data-c70e11d27a94?sk=d2c6b400b64e89304a0a2da28eb83531)

![img](https://miro.medium.com/v2/resize:fit:875/1*6HRU03UvgOt_5ih3ssEDXw.jpeg)

There are a couple of obvious reasons when you require access to a big chunk of data, formed and modeled in a specific way:

- to test out a functionality
- to run a benchmark
- for learning purposes (e.g. to learn a library for creating charts)
- for testing and learning database optimization techniques

# Data, data, and more data.

Fortunately, there is an out-of-the-box solution, provided by PostgreSQL to create a ton of sample data. That awesome feature comes in a form of a PostgreSQL function.

It’s always best to have real data, but getting the data from real users and devices can be clumsy, and it may take weeks, months, or years to get that much information.

But sometimes, that is not possible, and you need the data now, momentarily. Indeed, there is an intrinsic function that belongs to PostgreSQL and I’ll show you how to use it, from a very basic perspective to more advanced techniques to get more random, but at the same time, more realistic data.

## PostgreSQL function — generate_series()

So, what’s it all about? There is a generate_series() function to create large datasets.
First of all, let’s take a look at the function statement, which comes in three ways:

![img](https://miro.medium.com/v2/resize:fit:875/1*yikm-D1fK9_I4IfqG-Zi9A.png)

PostgreSQL Set Returning Functions

Before diving deeper into the function abilities, let’s create a sample database. I called it *dummy_data.*

```
CREATE DATABASE dummy_data;
\c dummy_dataYou are now connected to database "dummy_data" as user "postgres".
```

**generate_series**() lets us easily create ordered tables of numbers or dates, and PostgreSQL calls it a [Set Returning Function](https://www.postgresql.org/docs/13/functions-srf.html) because it can return more than one row.

## 1. generate_series(start, stop)

Let’s start by learning to use the first definition.

```
SELECT * FROM generate_series(1,5);generate_series
-----------------
1
2
3
4
5(5 rows)
```

This will generate a series of integers, starting with 1, and ending with a 5.

## 2. generate_series(start, stop, step)

The second would be, generating a series with a step. This would generate a series starting with 0, ending on 10, with a step of 2.

```
SELECT * from generate_series(0,10,2);generate_series
— — — — — — — -
0
2
4
6
8
10(6 rows)
```

## 3. generate_series(start, stop, step interval)

We can also use the generate_series() with dates, as shown below if we provide a step interval as a third argument:

```
SELECT * from generate_series(
   ‘2021–10–14’,
   ‘2021–10–15’, 
   INTERVAL ‘1 hour’
);generate_series
— — — — — — — — — — — 
2021–10–14 00:00:00+02
2021–10–14 01:00:00+02
2021–10–14 02:00:00+02
2021–10–14 03:00:00+02
2021–10–14 04:00:00+02
2021–10–14 05:00:00+02
2021–10–14 06:00:00+02
2021–10–14 07:00:00+02
2021–10–14 08:00:00+02
2021–10–14 09:00:00+02
2021–10–14 10:00:00+02
2021–10–14 11:00:00+02
2021–10–14 12:00:00+02
2021–10–14 13:00:00+02
2021–10–14 14:00:00+02
2021–10–14 15:00:00+02
2021–10–14 16:00:00+02
2021–10–14 17:00:00+02
2021–10–14 18:00:00+02
2021–10–14 19:00:00+02
2021–10–14 20:00:00+02
2021–10–14 21:00:00+02
2021–10–14 22:00:00+02
2021–10–14 23:00:00+02
2021–10–15 00:00:00+02(25 rows)
```

Returned dates are inclusive of the start and stop values, just as it was with the numeric example.

The output returned 25 rows, instead of maybe the expected 24 because the **stop value can be reached using the one-hour INTERVAL** (step parameter). However, **if the interval is skipped, it won’t be included**, which we can check by modifying the above query:

```
SELECT * from generate_series(
   '2021-10-14',
   '2021-10-15',
   INTERVAL '1 hour 25 minutes'
);generate_series
------------------------
2021-10-14 00:00:00+02
2021-10-14 01:25:00+02
2021-10-14 02:50:00+02
2021-10-14 04:15:00+02
2021-10-14 05:40:00+02
2021-10-14 07:05:00+02
2021-10-14 08:30:00+02
2021-10-14 09:55:00+02
2021-10-14 11:20:00+02
2021-10-14 12:45:00+02
2021-10-14 14:10:00+02
2021-10-14 15:35:00+02
2021-10-14 17:00:00+02
2021-10-14 18:25:00+02
2021-10-14 19:50:00+02
2021-10-14 21:15:00+02
2021-10-14 22:40:00+02(17 rows)
```

This returned **17 rows, instead of 18**, because if we added 1hour and 25 minutes, it would result in a date 2021–10–15 00:05:00+02, which is out of bounds.

# Crypto Miner — Data Generator Example

Now that we understand the basics, we can start with a more concrete example.

Let’s say that we want to artificially create metrics for Cryptocoin miners — we would probably want to track CPU usage, average megahash/s, miner temperature, fan percentage.

## Setting up a table

We can start by creating a sample table, called miners, and say that I own three miners. We can name them:

1. Diamond
2. Platinum
3. Gold

```
CREATE TABLE IF NOT EXISTS miners (
id smallint,
name varchar(20),
graphic_cards smallint 
);INSERT INTO 
   miners (id, name, graphic_cards) 
   VALUES 
      (1, 'Diamond', 10), 
      (2, 'Platinum', 7), 
      (3, 'Gold', 4);SELECT * FROM miners;
 id |   name   | graphic_cards 
----+----------+---------------
  1 | Diamond  |            10
  2 | Platinum |             7
  3 | Gold     |             4
```

Now, let’s create one-day data for those three miners — one entry per miner, for each hour.

```
SELECT 
   miners.name, 
   s1.time as time, 
   random() * (100–0) + 0 AS cpu_usage, 
   random() * (30–26) + 26 * graphic_cards AS average_mhs, 
   random() * (90–50) + 50 AS temperature, 
   random() * (100–0) + 0 AS fan 
FROM generate_series(
   ‘2021–10–14’, 
   ‘2021–10–15’, 
   INTERVAL ‘1 hour’) AS s1(time) 
CROSS JOIN(
   SELECT 
      id,
      name, 
      graphic_cards 
   FROM miners
) miners 
ORDER BY 
  miners.id, 
  s1.time;
```

Query explanation, if you’re not able to follow:

- We have the **name**, **time**, **cpu_usage**, **average_mhs**, **temperature**, and **fan** values:
- cpu_usage, average_mhs, temperature & fan values are purely random
- **cpu_usage** can go from 0% — 100%
- **average_mhs** — I used an example where a graphic card can produce between 26–30 Mh/s
- **temperature** — goes between 50 and 90 degrees
- **fan** — goes from 0% — 100%
- **series is generated for each hour** between 2021–10–14 and 2021–10–15 with a step increment of 1 hour (01:00, 02:00, 03:00, and so on)
- **cross joined previously created miners table** that has information about the miner name and number of graphic cards
- **ordered by the id of the miner first**, and then each sub group is ordered by time ascending

This will produce an output similar to this (it will differ because of the random() function that is used for cpu_usage, average_mhs, temperature, and fan).

<iframe src="https://medium.com/media/59f507c0720d5cf0ee950a560a62b03a" allowfullscreen="" frameborder="0" height="1463" width="680" title="Miner Random Data" class="fp n gf dv bg" scrolling="no" style="box-sizing: inherit; top: 0px; width: 680px; height: 1463px; left: 0px;"></iframe>

## Jupyter Notebook

To display values in a chart, I decided to use a simple **jupyter notebook**, so we get a feeling of what’s going on with the data.

If you’re unfamiliar with jupyter, that’s fine — it’s an interactive web tool used to combine software code, computational output, explanatory text, and multimedia resources in a single document. It’s powered by Python, but you can use a lot of other languages to plot the data.

This is a sample code I will be using for displaying a table or plotting a graph:

```
import psycopg2 as pg
import pandas.io.sql as psql
import matplotlib.pyplot as pltconn = pg.connect(host=”localhost”, database=”dummy_data”, user=”postgres”, password=”password”)df = psql.read_sql(‘SELECT * FROM generate_series(1,5)’, conn)df.head()
```

which produces the same output as if you would query the Postgres database from the command line:

![img](https://miro.medium.com/v2/resize:fit:365/0*txZE5vfizLP659cE)

Using jupyter notebook to display table data

All in all, this is just python code run in a jupyter notebook:

- connecting to a database
- executing the query
- displaying data in a table.

## Plotting Data

I can plot, for example, temperature for the Diamond miner (using the query we already saw above):

```
import psycopg2 as pg
import pandas.io.sql as psql
import matplotlib.pyplot as pltconn = pg.connect(host="localhost", database="dummy_data", user="postgres", password="password")query_string = """
   SELECT miners.name, s1.time,
      random() * (100-0) + 0 AS cpu_usage,
      random() * (30-26) + 26 * graphic_cards AS  average_mhs,
      random() * (90-50) + 50 AS temperature,
      random() * (100-0) + 0 AS fan
   FROM generate_series(
      '2021-10-14', 
      '2021-10-15', 
      INTERVAL '1 hour') AS s1(time)
   CROSS JOIN(
      SELECT id, name, graphic_cards 
      FROM miners 
      WHERE 
         name = 'Diamond'
   ) miners
   ORDER BY miners.id, s1.time;
"""df = psql.read_sql(query_string, conn)
#dfplt.figure(figsize=(15,8))
plt.plot(df["time"], df["temperature"])
plt.show
```

I slightly changed the query, to only return data for the **Diamond** miner. I also added plt.figure, plt.plot & plt.show. This creates a figure, defines the x and y-axis, and shows the plot. It produces the plot below:

![img](https://miro.medium.com/v2/resize:fit:875/0*6--CMm-I-fI1t-VZ)

Displaying temperature over time for Diamond miner

But, this doesn’t seem very realistic. We can try playing with around the idea to get more realistic data

# More Realistic Approach

We can, for example, say that the miner will only work between 6 PM and 10 AM since the electricity is cheaper then.

This will directly affect the temperature, fan, average_mhs, and cpu_usage. So, let’s determine a schedule and say that from 10 AM to 6 PM we use it for work, and from 6 PM to 10 AM we use it to mine crypto.

That way, we can still expect some moving and randomness in our work time, while the values will be close to peak while the miner is used for mining crypto.

Additionally, we can also assume that maybe, half of our day, we render videos & do some medium data processing, so it’s a little bit higher intensity in that period, while the rest of the time it is casual usage, maybe readings, documentation, and so on.

## Adding More Dispersion

So, to conclude, we have 3 periods with 3 different intensities:

- **6 PM — 10 AM — HIGH intensity**
- **10 AM — 2 PM — MEDIUM intensity**
- **2 PM — 6 PM — LOW intensity**

To proceed, create a table that will have intensity, described from 0–1 for each hour of the day, to add more dispersion.
The table will be simple:

```
CREATE TABLE hours ( 
  hour INT NOT NULL, 
  intensity NUMERIC NOT NULL
);
```

There are 24 hours in the day, and we will define an intensity for each hour, by the rules below:

- **LOW intensity is from 0–20%**
- **MEDIUM intensity is from 21–75%**
- **HIGH intensity is over 75%**

```
INSERT INTO hours(hour, intensity) VALUES
 (1,.9),
 (2,.92),
 (3,.89),
 (4,.95),
 (5,.94),
 (6,.80),
 (7,.88),
 (8,.79),
 (9,.78),
 (10,.56),
 (11,.55),
 (12,.63),
 (13,.28),
 (14,.14),
 (15,.18),
 (16,.07),
 (17,.07),
 (18,.89),
 (19,.8),
 (20,.78),
 (21,.92),
 (22,.86),
 (23,.82),
 (0,.87);
```

Now, we have a table looking like this:

```
SELECT * FROM hours;hour  | intensity 
------+-----------
    1 |       0.9
    2 |      0.92
    3 |      0.89
    4 |      0.95
    5 |      0.94
    6 |      0.80
    7 |      0.88
    8 |      0.79
    9 |      0.78
   10 |      0.56
   11 |      0.55
   12 |      0.63
   13 |      0.28
   14 |      0.14
   15 |      0.18
   16 |      0.07
   17 |      0.07
   18 |      0.89
   19 |       0.8
   20 |      0.78
   21 |      0.92
   22 |      0.86
   23 |      0.82
   0  |      0.87
```

We can use the aforementioned values to define the peak usage values (or maximum allowed value for a certain period), and use a query like this:

```
SELECT 
   a.HOURLY, 
   ABS(intensity - rval)*100 as value
FROM( 
   SELECT 
      HOURLY, 
      date_part('hour', HOURLY) _hour, 
      random()*0.2 as rval, 
      intensity                    
   FROM generate_series(
      '2021-10-14', 
      '2021-10-30', 
      INTERVAL '1 hour'
   ) HOURLY
   INNER JOIN hours h ON date_part('hour', HOURLY) = h.hour 
   ORDER BY hourly
) AS a;
```

..to get a random value, that will be lower up to 20% from the peak value.
What happens in that query?

We can start by inspecting the inner query:

```
SELECT * FROM generate_series(
   '2021-10-14', 
   '2021-10-30', 
   INTERVAL '1 hour'
) HOURLY;
```

This will produce a series of times, starting from 2021–10–14 00:00:00, and ending with 2021–10–30 00:00:00, with a one-hour increment.

Example:

```
2021-10-14 00:00:00+02
2021-10-14 01:00:00+02
2021-10-14 02:00:00+02
2021-10-14 03:00:00+02
2021-10-14 04:00:00+02
...
2021-10-30 00:00:00+02
```

Next, we can continue by using the INNER JOIN on our previously created ***hours\*** table:

```
SELECT * FROM generate_series(
   '2021-10-14', 
   '2021-10-30', 
   INTERVAL '1 hour'
) HOURLY
INNER JOIN hours h ON date_part('hour', HOURLY) = h.hour 
ORDER BY hourly;
```

This would create a table, that has three columns:

- **hourly**
- **hour**
- **intensity**

And would apply (hour, intensity) pair to each hour in our previously generated series of hours from **2021–10–14 00:00:00** to **2021–10–30 00:00:00**

This is how the output looks like:

```
hourly                  | hour | intensity 
------------------------+------+-----------
 2021-10-14 00:00:00+02 |    0 |      0.87
 2021-10-14 01:00:00+02 |    1 |       0.9
 2021-10-14 02:00:00+02 |    2 |      0.92
 2021-10-14 03:00:00+02 |    3 |      0.89
 2021-10-14 04:00:00+02 |    4 |      0.95
 2021-10-14 05:00:00+02 |    5 |      0.94
 2021-10-14 06:00:00+02 |    6 |      0.80
 2021-10-14 07:00:00+02 |    7 |      0.88
 ...
 2021-10-30 00:00:00+02 |    0 |      0.87
```

If we add that into an outer query:

```
SELECT * FROM( 
   SELECT 
      HOURLY, 
      date_part(‘hour’, HOURLY) _hour, 
      random()*0.2 as rval, 
      intensity
   FROM generate_series(
      ‘2021–10–14’, 
      ‘2021–10–30’, 
      INTERVAL ‘1 hour’
   ) HOURLY
   INNER JOIN hours h ON date_part(‘hour’, HOURLY) = h.hour 
   ORDER BY hourly
) AS a;
```

This would get us four columns:

- **hourly**
- **_hour**
- **rval**
- **intensity**

from which, three of them are previously known, now we just calculated a rval, which is a random number from 0–0.2 (0–20%), **which would be subtracted in the last query from the intensity** (and wrapped with ABS, so that we don’t get a negative value ever).

The final product is shown below:

![img](https://miro.medium.com/v2/resize:fit:875/1*GTyEAYT9RB9BAgZs5q5y_Q.png)

Displaying temperature data for period 10/14/2021–10/30/2021 randomly generated with three intensity factors — low, medium, and high

We can see that it behaves as we described it in our initial statement:

**6 PM — 10 AM — HIGH intensity
10 AM — 2 PM — MEDIUM intensity
2 PM — 6 PM — LOW intensity**

Maybe it’s even better to see three different intensity levels on an interval of 10 minutes:

![img](https://miro.medium.com/v2/resize:fit:875/0*L4volJKQtgFf0KZE)

10-minute interval with 3 intensity levels

As the values go from 0–100%, this can imitate the behavior of **fan** values of a miner. By applying simple, or more complex math, we can get other values as well.

Let’s assume that’s a model that suits our needs. Now, we have to create data for all our devices, for one year, with a one-hour increment?

Voila.

```
SELECT 
   name, 
   HOURLY, 
   abs(intensity - rval)*100 as fan                
FROM( 
   SELECT 
      miners.name, 
      HOURLY, 
      date_part('hour', HOURLY) _hour, 
      random()*0.2 as rval
   FROM generate_series(
      '2020-10-14', 
      '2021-10-14', 
      INTERVAL '1 hour'
) HOURLY
CROSS JOIN(
   SELECT DISTINCT(name) 
   FROM miners
) miners
) m
INNER JOIN hours h ON date_part('hour', HOURLY) = h.hour 
ORDER BY hourly;
```

If we count that, that’s a total of **26283 rows — (3 devices x 24h x 365 days) + 3 entries** for the 2021–10–14 00:00:00 (for each device) = 26283.

# Inserting Ton of Data

Let’s use a 5-second step increment instead of a 1-hour increment, and add three more devices: **SILVER, BRONZE, and DEFAULT**.

```
INSERT INTO 
   miners (id, name, graphic_cards) 
VALUES 
   (4, 'Silver', 3), 
   (5, 'Bronze', 2), 
   (6, 'Default', 1);
```

Turn the PostgreSQL timing on with **\timing on.**

Count the number of rows:

```
#InputSELECT COUNT(*) FROM(
   SELECT 
      name, 
      HOURLY, 
     abs(intensity - rval)*100 as fan                
   FROM( 
      SELECT 
         miners.name, 
         HOURLY, 
         date_part('hour', HOURLY) _hour, 
         random()*0.2 as rval
      FROM generate_series(
         '2020-10-14', 
         '2021-10-14', 
         INTERVAL '5 second') HOURLY
   CROSS JOIN(
      SELECT DISTINCT(name) 
      FROM miners) 
   miners) m
INNER JOIN hours h ON date_part('hour', HOURLY) = h.hour 
ORDER BY hourly) e;# Outputcount   
----------
 37843206
(1 row)Time: 48916.613 ms (00:48.917)
```

**It took us 48 seconds to create 37.843 million of data.**
Finally, let’s insert this into a table so that we don’t have to calculate the data on the go each time:

```
CREATE TABLE IF NOT EXISTS miner_data(
 time TIMESTAMPTZ NOT NULL,
 miner_name VARCHAR(20),
 fan_percentage FLOAT
);
```

Add the random data (this will take some time):

```
INSERT INTO miner_data(
   miner_name, 
   time, 
   fan_percentage) 
SELECT 
   name, 
   HOURLY, 
   abs(intensity - rval)*100 as fan
FROM( 
   SELECT 
      miners.name, 
      HOURLY, 
      date_part('hour', HOURLY) _hour, 
      random()*0.2 as rval
   FROM generate_series(
      '2020-10-14', 
      '2021-10-14', 
      INTERVAL '5 second'
   ) HOURLY
CROSS JOIN(
   SELECT DISTINCT(name) 
   FROM miners) 
miners) m
INNER JOIN hours h ON date_part('hour', HOURLY) = h.hour 
ORDER BY hourly;INSERT 0 37843206
Time: 161775.825 ms (02:41.776)
```

Almost 3 minutes to get that done.

To see what we have, say we plot our Diamond and Default miner fan percentages for the last 10 minutes (12 records per minute * 10 minutes = 120 entries on the plot, per each device).

Here’s the jupyter notebook/python code:

```
import psycopg2 as pg
import pandas.io.sql as psql
import matplotlib.pyplot as plt
conn = pg.connect(host="localhost", database="dummy_data", user="postgres", password="password")query_string1 = """
                SELECT * FROM miner_data WHERE miner_name = 'Diamond' ORDER BY TIME DESC LIMIT 120;
                """query_string2 = """
                SELECT * FROM miner_data WHERE miner_name = 'Default' ORDER BY TIME DESC LIMIT 120;
                """df1 = psql.read_sql(query_string1, conn)
df2 = psql.read_sql(query_string2, conn)
#dfplt.figure(figsize=(15,8))
plt.plot(df1["time"], df1["fan_percentage"])
plt.plot(df2["time"], df2["fan_percentage"])
plt.show
```

And the final output:

![img](https://miro.medium.com/v2/resize:fit:875/0*eQavFBpZM7dlV3VC)

**We have successfully created 37.843 million of fully random, but realistic data, and also stored them in the database. This can further be used for testing purposes.**

However, querying such a large data set takes time.
As an example, here’s a simple SELECT query from above:

```
SELECT * FROM miner_data 
WHERE 
   miner_name = ‘Diamond’ 
ORDER BY TIME LIMIT 120;Time: 9403.223 ms (00:09.403)
```

It took almost 9.5 seconds to query that. You don’t want to wait 10 seconds before you see the chart, don’t you?
If you’re interested to learn how to optimize querying data, follow me in the next series — **4 Ways To Optimise PostgreSQL Database With Millions of Data**
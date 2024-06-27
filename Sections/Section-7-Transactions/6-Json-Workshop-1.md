### [Working with Postgres JSON Query](https://hevodata.com/learn/postgres-json-query/)

This article will help you discover several operators and functions to query JSON data in PostgreSQL, as well as how to work it out with **PostgreSQL JSON Query**. Postgres allows you to combine relational and non-relational data effortlessly, giving users/applications flexibility in accessing and handling the data.

It also includes native support for querying and processing JSON data. Read along to learn more about Postgres JSON Query.

## What are PostgreSQL JSON Data types?

- JSON
- JSONB

These are two native data types in PostgreSQL that can be used to store JSON Data. The main distinction between them is that JSONB keeps data in a unique binary format while JSON stores data in a raw form. 

The input values for the JSON and JSONB data types are nearly identical. Efficiency is the main practical difference.

JSON data stores an exact copy of the input text, requiring processing functions to reparse each iteration. JSONB data is saved in a decomposed binary format, which makes it faster to process but slightly slower to input due to additional conversion overhead. Indexing is another feature that JSONB offers, which is a big plus.

## JSON vs. JSONB

Most developers widely use JSONB because of its faster processing time & better performance. However, JSON performs better in the below-mentioned cases:

- JSON ingestion is quicker than JSONB, but JSONB is faster while conducting additional processing. When the formatting & the originality of the data is expected to be preserved (also known as whitespace), JSON is preferred.
- When there’s a need to retain duplicate keys.

***Do you know?\*** *JSON might be a better alternative when you’re just absorbing JSON logs and not querying them.*

## Advantages of Postgres JSON Query

The best option for storing and processing your JSON Data is PostgreSQL. You can gain from inserting JSON into PostgreSQL for the reasons listed below:

- Developers frequently employ two or more data stores, such as PostgreSQL and MongoDB, and then send application data to those stores using a REST API. You can now overcome the complexity of using two database designs by inserting JSON into PostgreSQL.
- Your JSON data can be readily indexed and queried in PostgreSQL. You can experience a significant performance gain and scalability. The ability to search for data and access it using SQL commands is another benefit of inserting JSON into PostgreSQL.
- One of the most popular choices today is the JSONB Data type, an extension of JSON that guarantees high-quality, faster speed, and efficient storage.

***Do you know?\*** *After PostgreSQL supported JSON Query, the data search performance was comparable and gave competition to the most widely used NoSQL databases, such as MongoDB.*

## Working with Postgres JSON Query

To work on Postgres JSON Query, you must first follow the below-mentioned sequence of action:

- [Postgres JSON Query: Create Table](https://hevodata.com/learn/postgres-json-query/#jsoncreate)
- [Postgres JSON Query: Insert Data](https://hevodata.com/learn/postgres-json-query/#jsoninsert)
- [Postgres JSON Query: Query JSON Data](https://hevodata.com/learn/postgres-json-query/#jsonquery)
- [Postgres JSON Query: JSON Operators & Functions](https://hevodata.com/learn/postgres-json-query/#jsonfunction)

***\*Move Data from a Source to PostgreSQL Effortlessly\****

Do you have concerns about replicating your PostgreSQL data? Hevo’s Data Pipeline Platform can help to integrate data from over [150+ sources](https://hevodata.com/integrations/pipeline/) in a matter of minutes. Hevo puts complete control in the hands of data teams with intuitive dashboards for pipeline monitoring, auto-schema management, and custom ingestion/loading schedules. 

All of this combined with [transparent pricing](https://hevodata.com/pricing/pipeline/) and 24×7 support makes us the most loved data pipeline software on review sites. Take our 14-day free trial to experience a better way to manage data pipelines.

[GET STARTED FOR FREE WITH HEVO!](https://hevodata.com/signup/)

**JSON File Format:** 

Before diving deep into the working of Postgres JSON Query, let’s first understand the JSON File Format. The data in JSON File is stored in the form of “key: value” pairs using a simple format that is easy to understand.

***For example,\*** *here’s a JSON file with an array called “Eatables” with these three objects:- type, name, and price.*

```
{
	"Eatables": [

		{
			"type": "fruit",
			"name": "banana",
			"price": 1.49
		},
		{
			"type": "vegetable",
			"name": "tomato",
			"price": 0.64
		},
		{
			"type": "vegetable",
			"name": "potato",
			"price": 0.81
		}
	]
}
```

***Note\****: In JSON, values must be one of the following data types:- string, number, object, array, boolean, null.*

### Postgres JSON Query: Create Table

Let’s get started by [creating a new table](https://hevodata.com/learn/postgresql-tables/) with JSON data type in your PostgreSQL editor by writing the following code:

```
CREATE TABLE TakeOrder (
	id serial NOT NULL PRIMARY KEY,
	info json NOT NULL
);
```

This will create a table consisting of the next 2 columns:

- id Column: It acts as the primary key and identifies the order placed.
- info Column: It stores your data as JSON documents.

### Postgres JSON Query: Insert Data

Now, after the successful creation of a Table in PostgreSQL. Use the INSERT function to insert JSON data into PostgreSQL tables. 

```
INSERT INTO TakeOrder (info)
VALUES('{ "customer": "Steve", "items": {"product": "Coffee","qty": 6}}');
```

The above code represents that Steve bought 6 cups of Coffee. Now, you can use the below code to insert multiple rows into your table at the same time:

```
INSERT INTO orders (info)
VALUES('{ "customer": "Edward", "items": {"product": "Bread","qty": 1}}'),
      ('{ "customer": "Bella", "items": {"product": "Chocolate","qty": 10}}'),
      ('{ "customer": "Jacob", "items": {"product": "Pens","qty": 2}}');
```

### Postgres JSON Query: Query JSON Data

Now, it’s time to Query JSON Data that you just successfully inserted into PostgreSQL. To show your data like other native data types, you may use the SELECT statement as follows:

```
SELECT info FROM orders;
```

#### JSON Operator in WHERE clause

We can utilize the JSON operators in the WHERE clause to filter out the returning rows. For instance, if we only want results where the purchased item is Chocolate, we can write the following code:

```
SELECT info ->> 'customer' AS customer
FROM orders
WHERE info -> 'items' ->> 'product' = Chocolate;
```

To filter out the results for the records where the quantity bought is precisely 10.

```
SELECT info ->> 'customer' AS customer,
	info -> 'items' ->> 'product' AS product
FROM orders
WHERE CAST ( info -> 'items' ->> 'qty' AS INTEGER) = 10
```

***Note\****: We have used the* [*PostgreSQL Cast*](https://hevodata.com/learn/postgresql-cast/) *Function to convert one data type into another.* 

### Postgres JSON Query: JSON Operators & Functions 

In PostgreSQL, we have two native operators -> and ->> that enable us to query JSON Data. 

- The operator -> returns a JSON object field by key.
- The operator ->> produces a JSON object field by text.

As an example, if you run a SELECT query to get all the customers from your table in JSON format:

```
SELECT info -> 'customer' AS customer
FROM TakeOrder;
```

To get all the customers from your table in Text format, enter:

```
SELECT info ->> 'customer' AS customer
FROM TakeOrder;
```

Since the “->” operator returns a JSON object, you can chain it with the “->>” operator to retrieve a specific node. For instance, the following query returns all products sold:

```
SELECT info -> 'items' ->> 'product' as product
FROM TakeOrder
ORDER BY product;
```

***Note\****: Items will first be returned as JSON objects by info -> “items.” The info->’ items’ ->>’ product’ command will generate a text list of all the products.*

PostgreSQL JSON gives you a wide range of operators to manipulate your data effectively. A few more are listed below:

- \#> Operator: This operation is handy when choosing an element from the main JSON object using its path. You can use the “#>” operator to access entities in the needed path, such as element names and array indexes. This operator can also be used for sequential data access.

-  \#>> Operator: You can retrieve JSON data by its path using the “#>>” operator, just like you can with the “#>” operator. It cannot, however, provide you with sequential access.

Usually, by pointing to valid elements and indexes, you can construct a chain using the “->” and “#>” operators.

***Note\****: Any of the four operators indicated above can end this chain. Remember that you must conclude the operator chain with “->>” or “#>>” if you intend to use the outcome of your chain with a function that utilizes a text data type.*

Additionally, you can alter the JSON data by using aggregate functions like **MIN, MAX, AVERAGE, SUM**, etc.
For instance, the minimum, maximum, average, and total quantities of products sold will be returned by the following statement:

```
SELECT 
   MIN (CAST (info -> 'items' ->> 'qty' AS INTEGER)),
   MAX (CAST (info -> 'items' ->> 'qty' AS INTEGER)),
   SUM (CAST (info -> 'items' ->> 'qty' AS INTEGER)),
   AVG (CAST (info -> 'items' ->> 'qty' AS INTEGER))
FROM TakeOrder;
```

- **json_each** function: We can convert the outermost JSON object into a set of key-value pairs using the json_each() function by writing the code:

```
SELECT json_each (info)
FROM orders;
```

- **json_object_keys** function: The JSON object keys() function can be used to retrieve a set of keys from a JSON object’s outermost object. The following search returns all keys from the object of nested items in the info column.

```
SELECT json_object_keys (info->'items')
FROM orders;
```

Visit the [official documentation](https://www.postgresql.org/docs/12/functions-json.html) to learn more about Postgres JSON Functions & operators. 

#### JSON Operator in WHERE clause

We can utilize the JSON operators in the WHERE clause to filter out the returning rows. For instance, if we only want results where the purchased item is Chocolate, we can write the following code:

```
SELECT info ->> 'customer' AS customer
FROM orders
WHERE info -> 'items' ->> 'product' = Chocolate;
```

To filter out the results for the records where the quantity bought is precisely 10.

```
SELECT info ->> 'customer' AS customer,
	info -> 'items' ->> 'product' AS product
FROM orders
WHERE CAST ( info -> 'items' ->> 'qty' AS INTEGER) = 10
```

***Note\****: We have used the* [*PostgreSQL Cast*](https://hevodata.com/learn/postgresql-cast/) *Function to convert one data type into another.* 

## Working with Postgres JSONB Query

To begin working with Postgres JSONB Query, you must first go through the steps listed below:

- [Postgres JSONB Query: Create Table](https://hevodata.com/learn/postgres-json-query/#jsonbcreate)
- [Postgres JSONB Query: Insert Data](https://hevodata.com/learn/postgres-json-query/#jsonbinsert)
- [Postgres JSONB Query: Query JSON Data](https://hevodata.com/learn/postgres-json-query/#jsonbquery)
- [Postgres JSONB Query: JSON Operators & Functions](https://hevodata.com/learn/postgres-json-query/#jsonbfunction)

### Postgres JSONB Query: Create Table

Let’s begin by creating a Table that we will use as an example to demonstrate the working of Postgres JSONB Query.

```
CREATE TABLE cars(
    id SERIAL PRIMARY KEY,
    cars_info JSONB NOT NULL);
```

### Postgres JSONB Query: Insert Data

Now, successfully creating a Table in Postgres, let’s insert data into them.

```
INSERT INTO cars(cars_info)
VALUES('{"brand": "Toyota", "color": ["red", "black"], "price": 285000, "sold": true}'),
      ('{"brand": "Honda", "color": ["blue", "pink"], "price": 25000, "sold": false}'),
      ('{"brand": "Mitsubishi", "color": ["black", "gray"], "price": 604520, "sold": true}');
```

We can use the SELECT statement to view how our data in the table looks.

```
id | cars_info                                      
----+------------------------------------------------------------------------------------
  1 | {"sold": true, "brand": "Toyota", "color": ["red", "black"], "price": 285000}
  2 | {"sold": false, "brand": "Honda", "color": ["blue", "pink"], "price": 25000}
  3 | {"sold": true, "brand": "Mitsubishi", "color": ["black", "gray"], "price": 604520}
```

### Postgres JSONB Query: Query JSON Data

Now let’s perform a Postgres JSONB Query to get the names of the Car Brands.

```
SELECT cars_info -> 'brand' AS car_name FROM cars;
  car_name  
--------------
 "Toyota"
 "Honda"
 "Mitsubishi"
```

**PostgreSQL JSONB query using WHERE clause**

Here let’s write a code to filter out the rows where the car has been sold.

```
SELECT * FROM cars WHERE cars_info -> 'sold' = 'true';

id | cars_info                                      
----+------------------------------------------------------------------------------------
  1 | {"sold": true, "brand": "Toyota", "color": ["red", "black"], "price": 285000}
  3 | {"sold": true, "brand": "Mitsubishi", "color": ["black", "gray"], "price": 604520}
```

### Postgres JSONB Query: JSON Operators & Functions

- With JSONB data, a variety of built-in functions are available. Let’s have a look at a **jsonb_each** function query as an example:

```
SELECT jsonb_each('{"brand": "Toyota", "sold": "true"}'::jsonb);
    jsonb_each      
----------------------
 (sold,"""true""")
 (brand,"""Toyota""")
```

Here we have retrieved the rows for which the Car brand was ‘Toyota’ and the sold attribute was ‘true.’

- Let’s see a **jsonb_object_keys** function example:

```
SELECT jsonb_object_keys( '{"brand": "Mitsubishi", "sold": true}'::jsonb );
jsonb_object_keys
-------------------
 sold
 Brand
```

- The following example illustrates the use of the **jsonb_extract_path** function:

```
SELECT jsonb_extract_path('{"brand": "Honda", "sold": false}'::jsonb, 'brand');
jsonb_extract_path
--------------------
 "Honda"
```

- Let us now demonstrate an example to learn about the **jsonb_pretty** function:

```
SELECT jsonb_pretty('{"brand": "Honda", "sold": false}'::jsonb);
  jsonb_pretty    
----------------------
 { +
     "sold": false, +
     "brand": "Honda"+
 }
```

Before wrapping up, let’s cover some basics of JSON.

## What is JSON Data?



[![Postgres JSON Data](data:image/svg+xml;utf8,%26%23x26A0%3B%EF%B8%8E)%26%23x26A0%3B︎" class="">](data:image/svg+xml;utf8,%26%23x26A0%3B︎" class="lightgallery-link">

[Image Source](https://mariadb.com/resources/blog/using-json-in-mariadb/)

[JSON](https://hevodata.com/learn/json-modeling/) (JavaScript Object Notation) data types store JSON data. JSON is mostly used to transfer data from a server to a web application. JSON is the text that humans can read, unlike other forms. Such data may also be kept as text, but JSON data types ensure that each value is true to JSON norms.

In scenarios where requirements are changeable, representing data as JSON can be significantly more adaptable than the conventional relational data architecture. Within the same application, it is entirely conceivable for both approaches to coexist and benefit one another.

## Why store JSON Data in PostgreSQL?

The PostgreSQL database’s capacity to store & query JSON data is one of its distinctive characteristics. Previously to process JSON Data, Data Analysts and Data Engineers had to turn to specialized document storage like MongoDB. Check out this article to learn about [MongoDB vs PostgreSQL](https://hevodata.com/learn/mongodb-vs-postgresql/).

The allure of relational databases is the ability to “save data now, sort out schema afterward.” Any data structure could be stored as plain text in databases like [PostgreSQL and MySQL](https://hevodata.com/learn/postgresql-vs-mysql/). Processing and speed, however, were issues since the database lacked intrinsic knowledge of the document’s schema. 

Previously, the database had to load and parse the complete text blob for each query. Furthermore, complicated regular expressions had to be used when querying deeply into the JSON record.

However, the requirement for an external document store is no longer necessary because of the robust JSON functionality included in PostgreSQL*(after [version 9.2](https://www.postgresql.org/about/news/postgresql-92-released-1415/)*).
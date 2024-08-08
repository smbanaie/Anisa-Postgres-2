# [PostgreSQL Triggers and Stored Function Basics](https://severalnines.com/blog/postgresql-triggers-and-stored-function-basics/)



*Note from Severalnines: This blog is being published posthumously as Berend Tober passed away on July 16, 2018. We honor his contributions to the PostgreSQL community and wish peace for our friend and guest writer.*

In [a previous article](https://severalnines.com/blog/overview-serial-pseudo-datatype-postgresql) we discussed the [PostgreSQL](https://severalnines.com/product/clustercontrol/for_postgresql) serial pseudo-type, which is useful for populating synthetic key values with incrementing integers. We saw that employing the serial data type keyword in a table data definition language (DDL) statement is implemented as an integer type column declaration that is populated, upon a database insert, with a default value derived from a simple function call. This automated behavior of invoking functional code as part of the integral response to data manipulation language (DML) activity is a powerful feature of sophisticated relational database management systems (RDBMS) like [PostgreSQL](https://severalnines.com/product/clustercontrol/for_postgresql). In this article we delve further into another more capable aspect to automatically invoke custom code, namely the use of triggers and stored functions.Introduction

## Use Cases for Triggers and Stored Functions

Let’s talk about why you might want to invest in understanding triggers and stored functions. By building DML code into the database itself, you can avoid duplicate implementation of data-related code in multiple separate applications that may be built to interface with the database. This ensures consistent execution of DML code for data validation, data cleansing, or other functionality such as data auditing (i.e., logging changes) or maintaining a summary table independently of any calling application. Another common use of triggers and stored functions is to make views writable, i.e., to enable inserts and/or updates on complex views or to protect certain column data from unauthorized modification. Additionally, data processed on the server rather than in application code does not cross the network, so there is some lesser risk of data being exposed to eavesdropping as well as a reduction in network congestion. Also, in PostgreSQL stored functions can be configured to execute code at a higher privilege level than the session user, which admits some powerful capabilities. We’ll do some examples later.

## The Case Against Triggers and Stored Functions

A review of commentary on the [PostgreSQL General mailing list](https://www.postgresql.org/list/pgsql-general/) revealed some opinions unfavorable toward the use of triggers and stored functions which I mention here for completeness and to encourage you and your team to weigh the pros and cons for your implementation.

Amongst the objections were, for example, the perception that stored functions are not easy to maintain, thus requiring an experienced person with sophisticated skills and knowledge in database administration to manage them. Some software professionals have reported that corporate change controls on database systems are typically more vigorous than on application code, so that if business rules or other logic is implemented within the database, then making changes as requirements evolve is prohibitively cumbersome. Another point of view considers triggers as an unexpected side effect of some other action and as such, may be obscure, easily missed, difficult to debug, and frustrating to maintain and so should usually be the last choice, not the first.

These objections might have some merit, but if you think about it, data is a valuable asset and so you probably do in fact want a skilled and experienced person or team responsible for the RDBMS in a corporate or government organization anyway, and similarly, Change Control Boards are a proven component of sustainable maintenance for an information system of record, and one person’s side effect is just as well another’s powerful convenience, which is the point of view adopted for the balance of this article.

## Declaring a Trigger

Let’s get about learning the nuts and bolts. There are many options available in the [general DDL syntax for declaring a trigger](https://www.postgresql.org/docs/10/static/sql-createtrigger.html), and it would take a significant time to treat all possible permutations, so for the sake of brevity we’ll talk about only a minimally-required subset of them in examples that follow using this abridged syntax:

```sql
CREATE TRIGGER name { BEFORE | AFTER | INSTEAD OF } { event [ OR ... ] }
    ON table_name
    FOR EACH ROW EXECUTE PROCEDURE function_name()

where event can be one of:

    INSERT
    UPDATE [ OF column_name [, ... ] ]
    DELETE
    TRUNCATE
```

The required configurable elements besides a *name* are the *when*, the *why*, the *where*, and the *what*, i.e., the timing for the trigger code to be invoked relative to the triggering action (when), the specific type of triggering DML statement (why), the acted-upon table or tables (where), and the stored function code to execute (what).

## Declaring a Function

The trigger declaration above requires specification of a function name, so technically the trigger declaration DDL cannot be executed until after the trigger function has been previously defined. The [general DDL syntax for a function declaration](https://www.postgresql.org/docs/10/static/sql-createfunction.html) also has many options so for manageability we’ll use this minimally sufficient syntax for our purposes here:

```sql
CREATE [ OR REPLACE ] FUNCTION
    name () RETURNS TRIGGER
  { LANGUAGE lang_name
    | SECURITY DEFINER
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
  }...
```

A trigger function takes no parameters, and the return type must be TRIGGER. We’ll talk about the optional modifiers as we encounter them in examples below.

## A Naming Scheme for Triggers and Functions

Respected computer scientist [Phil Karlton](http://www.meerkat.com/karlton/) has been attributed as [declaring](https://skeptics.stackexchange.com/questions/19836/has-phil-karlton-ever-said-there-are-only-two-hard-things-in-computer-science) (in paraphrased form here) that naming things is one of the biggest challenges for software teams. I’m going to present here an easy-to-use trigger and stored function naming convention which has served me well and encourage you to consider adopting it for your own RDBMS projects. The naming scheme in the examples for this article follow a pattern of using the associated table name suffixed with an abbreviation indicating the declared trigger *when* and *why* attributes: The first suffix letter will be either a “b”, “a”, or “i” (for “before”, “after”, or “instead of”), next will be one or more of an “i”, “u”, “d”, or “t” (for “insert”, “update”, “delete”, or “truncate”), and the last letter is just a “t” for trigger. (I use a similar naming convention for [rules](https://www.postgresql.org/docs/10/static/rules.html), and in that case the last letter is “r”). So for example, the various minimal trigger declaration attribute combinations for a table named “my_table” would be:

```sql
|-------------+-------------+-----------+---------------+-----------------|
|  TABLE NAME |  WHEN       |  WHY      |  TRIGGER NAME |  FUNCTION NAME  |
|-------------+-------------+-----------+---------------+-----------------|
|  my_table   |  BEFORE     |  INSERT   |  my_table_bit |  my_table_bit   |
|  my_table   |  BEFORE     |  UPDATE   |  my_table_but |  my_table_but   |
|  my_table   |  BEFORE     |  DELETE   |  my_table_bdt |  my_table_bdt   |
|  my_table   |  BEFORE     |  TRUNCATE |  my_table_btt |  my_table_btt   |
|  my_table   |  AFTER      |  INSERT   |  my_table_ait |  my_table_ait   |
|  my_table   |  AFTER      |  UPDATE   |  my_table_aut |  my_table_aut   |
|  my_table   |  AFTER      |  DELETE   |  my_table_adt |  my_table_adt   |
|  my_table   |  AFTER      |  TRUNCATE |  my_table_att |  my_table_att   |
|  my_table   |  INSTEAD OF |  INSERT   |  my_table_iit |  my_table_iit   |
|  my_table   |  INSTEAD OF |  UPDATE   |  my_table_iut |  my_table_iut   |
|  my_table   |  INSTEAD OF |  DELETE   |  my_table_idt |  my_table_idt   |
|  my_table   |  INSTEAD OF |  TRUNCATE |  my_table_itt |  my_table_itt   |
|-------------+-------------+-----------+---------------+-----------------|
```

The exact same name can be used for both the trigger and the associated stored function, which is completely permissible in PostgreSQL because the RDBMS keeps track of triggers and stored functions separately by the respective purposes, and the context in which the item name is used makes clear which item the name refers to.

So for example, a trigger declaration corresponding to the first row scenario from the table above would be seen implemented as

```sql
CREATE TRIGGER my_table_bit 
    BEFORE INSERT
    ON my_table
    FOR EACH ROW EXECUTE PROCEDURE my_table_bit();
```

In the case when a trigger is declared with multiple *why* attributes, just expand the suffix appropriately, e.g., for an *insert or update* trigger, the above would become

```sql
CREATE TRIGGER my_table_biut 
    BEFORE INSERT OR UPDATE
    ON my_table
    FOR EACH ROW EXECUTE PROCEDURE my_table_biut();
```

## Show Me Some Code Already!

Let’s make it real. We’ll start with a simple example and then expand on that to illustrate further features. The trigger DDL statements require a pre-existing function, as mentioned, and also a table upon which to act, so first we need a table to work on. For example purposes let’s say we need to store basic account identity data

```sql
CREATE TABLE person (
    login_name varchar(9) not null primary key,
    display_name text
);
```

Some data integrity enforcement can be handled simply with proper column DDL, such as in this case a requirement that the login_name exist and be no more than nine characters long. Attempts to insert a NULL value or a too-long value of login_name fail and report meaningful error messages:

```sql
INSERT INTO person VALUES (NULL, 'Felonious Erroneous');
ERROR:  null value in column "login_name" violates not-null constraint
DETAIL:  Failing row contains (null, Felonious Erroneous).

INSERT INTO person VALUES ('atoolongusername', 'Felonious Erroneous');
ERROR:  value too long for type character varying(9)
```

Other enforcements can be handled with check constraints, such as requiring a minimum length and rejecting certain characters:

```sql
ALTER TABLE person 
    ADD CONSTRAINT PERSON_LOGIN_NAME_NON_NULL 
    CHECK (LENGTH(login_name) > 0);

ALTER TABLE person 
    ADD CONSTRAINT person_login_name_no_space 
    CHECK (POSITION(' ' IN login_name) = 0);

INSERT INTO person VALUES ('', 'Felonious Erroneous');
ERROR:  new row for relation "person" violates check constraint "person_login_name_non_null"
DETAIL:  Failing row contains (, Felonious Erroneous).

INSERT INTO person VALUES ('space man', 'Major Tom');
ERROR:  new row for relation "person" violates check constraint "person_login_name_no_space"
DETAIL:  Failing row contains (space man, Major Tom).
```

but notice that the error message is not as fully informative as before, conveying only as much as is encoded in the trigger name rather than a meaningful explanatory textual message. By implementing the check logic in a stored function instead, you can use an exception to emit a more helpful text message. Also, check constraint expressions cannot contain subqueries nor refer to variables other than columns of the current row nor other database tables.

So let’s drop the check constraints

```sql
ALTER TABLE PERSON DROP CONSTRAINT person_login_name_no_space;
ALTER TABLE PERSON DROP CONSTRAINT person_login_name_non_null;
```

and get on with triggers and stored functions.

## Show Me Some More Code

We have a table. Moving on to the function DDL, we define an empty-bodied function, which we can fill in later with specific code:

```sql
CREATE OR REPLACE FUNCTION person_bit() 
    RETURNS TRIGGER
    SET SCHEMA 'public'
    LANGUAGE plpgsql
    SET search_path = public
    AS '
    BEGIN
    END;
    ';
```

This allows us to finally get to the trigger DDL connecting the table and the function so we can do some examples:

```sql
CREATE TRIGGER person_bit 
    BEFORE INSERT ON person
    FOR EACH ROW EXECUTE PROCEDURE person_bit();
```

PostgreSQL allows stored functions to be written in a variety of different languages. In this case and the following examples, we are composing functions in the PL/pgSQL language which is designed specifically for PostgreSQL and supports the use of all the data types, operators, and functions of the PostgreSQL RDBMS. The SET SCHEMA option sets the schema search path that will be used for the duration of the function execution. Setting the search path for every function is a good practice, as it saves having to prefix database objects with a schema name and protects against certain [vulnerabilities](https://wiki.postgresql.org/wiki/A_Guide_to_CVE-2018-1058:_Protect_Your_Search_Path) related to the search path.

### EXAMPLE 0 – Data Validation

As a first example, let’s implement the earlier checks, but with more human-friendly messaging.

```sql
CREATE OR REPLACE FUNCTION person_bit()
    RETURNS TRIGGER
    SET SCHEMA 'public'
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF LENGTH(NEW.login_name) = 0 THEN
        RAISE EXCEPTION 'Login name must not be empty.';
    END IF;

    IF POSITION(' ' IN NEW.login_name) > 0 THEN
        RAISE EXCEPTION 'Login name must not include white space.';
    END IF;
    RETURN NEW;
    END;
    $$;
```

The “NEW” qualifier is a reference to the row of data about to be inserted. It is one of a number of special variables available within a trigger function. We’ll introduce some others below. Note also, PostgreSQL permits substitution of the single quotation marks delimiting the function body with other delimiters, in this case following a common convention of using double dollar signs as the delimiter, since the function body itself includes single quotation characters. Trigger functions must exit by returning either the NEW row to be inserted or NULL to silently abort the action.

The same insert attempts fail as expected, but now with friendly messaging:

```sql
INSERT INTO person VALUES ('', 'Felonious Erroneous');
ERROR:  Login name must not be empty.

INSERT INTO person VALUES ('space man', 'Major Tom');
ERROR:  Login name must not include white space.
```

### EXAMPLE 1 – Audit Logging

With stored functions, we have wide latitude as to what the invoked code does, including referencing other tables (which is not possible with check constraints). As a more complex example we’ll walk through the implementation of an audit table, that is, maintaining a record, in a separate table, of inserts, updates, and deletes to a principal table. The audit table typically contains the same attributes as the principal table, which are used to record the changed values, plus additional attributes to record the operation executed to make the change, as well as a transaction timestamp, and a record of the user making the change:

```sql
CREATE TABLE person_audit (
    login_name varchar(9) not null,
    display_name text,
    operation varchar,
    effective_at timestamp not null default now(),
    userid name not null default session_user
);
```

In this case, implementing auditing is very easy, we simply modify the existing trigger function to include DML to effect the audit table insert, and then redefine the trigger to fire on updates as well as inserts. Note that we have elected not to change the trigger function name suffix to “biut”, but if the audit functionality had been a known requirement at initial design time, that would be the name used:

```sql
CREATE OR REPLACE FUNCTION person_bit()
    RETURNS TRIGGER
    SET SCHEMA 'public'
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF LENGTH(NEW.login_name) = 0 THEN
        RAISE EXCEPTION 'Login name must not be empty.';
    END IF;

    IF POSITION(' ' IN NEW.login_name) > 0 THEN
        RAISE EXCEPTION 'Login name must not include white space.';
    END IF;

    -- New code to record audits

    INSERT INTO person_audit (login_name, display_name, operation) 
        VALUES (NEW.login_name, NEW.display_name, TG_OP);

    RETURN NEW;
    END;
    $$;


DROP TRIGGER person_bit ON person;

CREATE TRIGGER person_biut 
    BEFORE INSERT OR UPDATE ON person
    FOR EACH ROW EXECUTE PROCEDURE person_bit();
```

Note that we have introduced another special variable “TG_OP” which the system sets to identify the DML operation which fired the trigger as either “INSERT”, “UPDATE”, “DELETE”, of “TRUNCATE”, respectively.

We need to handle deletes separately from inserts and updates since the attribute validation tests are superfluous and because the NEW special value is not defined upon entry to a *before delete* trigger function and so define corresponding stored function and trigger:

```sql
CREATE OR REPLACE FUNCTION person_bdt()
    RETURNS TRIGGER
    SET SCHEMA 'public'
    LANGUAGE plpgsql
    AS $$
    BEGIN

    -- Record deletion in audit table

    INSERT INTO person_audit (login_name, display_name, operation) 
      VALUES (OLD.login_name, OLD.display_name, TG_OP);

    RETURN OLD;
    END;
    $$;
        
CREATE TRIGGER person_bdt 
    BEFORE DELETE ON person
    FOR EACH ROW EXECUTE PROCEDURE person_bdt();
```

Note the use of the OLD special value as a reference to the row that is about to be deleted, i.e., the row as it exists *before* the delete happens.

We make a couple of inserts to test the functionality and confirm that the audit table includes a record of the inserts:

```sql
INSERT INTO person VALUES ('dfunny', 'Doug Funny');
INSERT INTO person VALUES ('pmayo', 'Patti Mayonnaise');

SELECT * FROM person;
 login_name |   display_name   
------------+------------------
 dfunny     | Doug Funny
 pmayo      | Patti Mayonnaise
(2 rows)

SELECT * FROM person_audit;
 login_name |   display_name   | operation |        effective_at        |  userid  
------------+------------------+-----------+----------------------------+----------
 dfunny     | Doug Funny       | INSERT    | 2018-05-26 18:48:07.6903   | postgres
 pmayo      | Patti Mayonnaise | INSERT    | 2018-05-26 18:48:07.698623 | postgres
(2 rows)
```

Then we make an update to one row and confirm that the audit table includes a record of the change adding a middle name to one of the data record display names:

```sql
UPDATE person SET display_name = 'Doug Yancey Funny' WHERE login_name = 'dfunny';

SELECT * FROM person;
 login_name |   display_name    
------------+-------------------
 pmayo      | Patti Mayonnaise
 dfunny     | Doug Yancey Funny
(2 rows)

SELECT * FROM person_audit ORDER BY effective_at;
 login_name |   display_name    | operation |        effective_at        |  userid  
------------+-------------------+-----------+----------------------------+----------
 dfunny     | Doug Funny        | INSERT    | 2018-05-26 18:48:07.6903   | postgres
 pmayo      | Patti Mayonnaise  | INSERT    | 2018-05-26 18:48:07.698623 | postgres
 dfunny     | Doug Yancey Funny | UPDATE    | 2018-05-26 18:48:07.707284 | postgres
(3 rows)
```

And lastly we exercise the delete functionality and confirm that the audit table includes that record as well:

```sql
DELETE FROM person WHERE login_name = 'pmayo';

SELECT * FROM person;
 login_name |   display_name    
------------+-------------------
 dfunny     | Doug Yancey Funny
(1 row)

SELECT * FROM person_audit ORDER BY effective_at;
 login_name |   display_name    | operation |        effective_at        |  userid  
------------+-------------------+-----------+----------------------------+----------
 dfunny     | Doug Funny        | INSERT    | 2018-05-27 08:13:22.747226 | postgres
 pmayo      | Patti Mayonnaise  | INSERT    | 2018-05-27 08:13:22.74839  | postgres
 dfunny     | Doug Yancey Funny | UPDATE    | 2018-05-27 08:13:22.749495 | postgres
 pmayo      | Patti Mayonnaise  | DELETE    | 2018-05-27 08:13:22.753425 | postgres
(4 rows)
```

### EXAMPLE 2 – Derived Values

Let’s take this a step further and imagine we want to store some free-form text document within each row, say a plain-text formatted resume or conference paper or [entertainment character abstract](https://en.wikipedia.org/wiki/List_of_Doug_characters), and we want to support use of the powerful full-text search capabilities of PostgreSQL on these free-form text documents.

We first add two attributes to support storage of the document and of an associated text search vector to the principal table. Since the text search vector is derived on a per row basis, there is no point in storing it in the audit table, be we do add the document storage column to the associated audit table:

```sql
ALTER TABLE person ADD COLUMN abstract TEXT;
ALTER TABLE person ADD COLUMN ts_abstract TSVECTOR;

ALTER TABLE person_audit ADD COLUMN abstract TEXT;
```

Then we modify the trigger function to process these new attributes. The plain-text column is handled the same way as other user-entered data, but the text search vector is a derived value and so is handled by a function call which reduces the document text to a [tsvector data type](https://www.postgresql.org/docs/9.6/static/functions-textsearch.html) for efficient searching.

```sql
CREATE OR REPLACE FUNCTION person_bit()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    SET SCHEMA 'public'
    AS $$
    BEGIN
    IF LENGTH(NEW.login_name) = 0 THEN
        RAISE EXCEPTION 'Login name must not be empty.';
    END IF;

    IF POSITION(' ' IN NEW.login_name) > 0 THEN
        RAISE EXCEPTION 'Login name must not include white space.';
    END IF;

    -- Modified audit code to include text abstract

    INSERT INTO person_audit (login_name, display_name, operation, abstract) 
        VALUES (NEW.login_name, NEW.display_name, TG_OP, NEW.abstract);

    -- New code to reduce text to text-search vector

    SELECT to_tsvector(NEW.abstract) INTO NEW.ts_abstract;

    RETURN NEW;
    END;
    $$;
```

As a test, we update an existing row with some detail text from Wikipedia:

```sql
UPDATE person SET abstract = 'Doug is depicted as an introverted, quiet, insecure and gullible 11 (later 12) year old boy who wants to fit in with the crowd.' WHERE login_name = 'dfunny';
```

and then confirm that the text search vector processing was successful:

```sql
SELECT login_name, ts_abstract  FROM person;
 login_name |                                                                                                                ts_abstract                                                                                                                
------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 dfunny     | '11':11 '12':13 'an':5 'and':9 'as':4 'boy':16 'crowd':24 'depicted':3 'doug':1 'fit':20 'gullible':10 'in':21 'insecure':8 'introverted':6 'is':2 'later':12 'old':15 'quiet':7 'the':23 'to':19 'wants':18 'who':17 'with':22 'year':14
(1 row)
```

### EXAMPLE 3 – Triggers & Views

The derived text search vector from the above example is not intended for human consumption, i.e, it is not user-entered, and we never expect to present the value to an end-user. If a user does attempt to insert a value for the ts_abstract column, anything provided will be discarded and replaced with the value derived internally to the trigger function, so we have protection against poisoning the search corpus. To hide the column completely, we can define an abridged view that does not include that attribute, but we still get the benefit of trigger activity on the underlying table:

```sql
CREATE VIEW abridged_person AS SELECT login_name, display_name, abstract FROM person;
```

For a simple view, PostgreSQL automatically makes it writable so we don’t have to do anything else to successfully insert or update data. When the DML takes effect on the underlying table, the triggers activate as if the statement were applied directly to the table so we still get both the text search support executed in the background populating the search vector column of the person table as well as appending the change information to the audit table:

```sql
INSERT INTO abridged_person VALUES ('skeeter', 'Mosquito Valentine', 'Skeeter is Doug''s best friend. He is famous in both series for the honking sounds he frequently makes.');


SELECT login_name, ts_abstract FROM person WHERE login_name = 'skeeter';
 login_name |                                                                                   ts_abstract                                                                                    
------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 skeeter    | 'best':5 'both':11 'doug':3 'famous':9 'for':13 'frequently':18 'friend':6 'he':7,17 'honking':15 'in':10 'is':2,8 'makes':19 's':4 'series':12 'skeeter':1 'sounds':16 'the':14
(1 row)


SELECT login_name, display_name, operation, userid FROM person_audit ORDER BY effective_at;
 login_name |    display_name    | operation |  userid  
------------+--------------------+-----------+----------
 dfunny     | Doug Funny         | INSERT    | postgres
 pmayo      | Patti Mayonnaise   | INSERT    | postgres
 dfunny     | Doug Yancey Funny  | UPDATE    | postgres
 pmayo      | Patti Mayonnaise   | DELETE    | postgres
 dfunny     | Doug Yancey Funny  | UPDATE    | postgres
 skeeter    | Mosquito Valentine | INSERT    | postgres
(6 rows)
```

For [more complicated views](https://www.postgresql.org/docs/9.5/static/sql-createview.html#SQL-CREATEVIEW-UPDATABLE-VIEWS) that don’t meet the requirements for automatically being writable, either the rule system or *instead of* triggers can do the job to support writes and deletes.

### EXAMPLE 4 – Summary Values

Let’s embellish further and treat the scenario where there is some type of transaction table. It might be a record of hours worked, inventory additions and reductions of warehouse or retail stock, or maybe a check register with debits and credits for each person:

```sql
CREATE TABLE transaction (
    login_name character varying(9) NOT NULL,
    post_date date,
    description character varying,
    debit money,
    credit money,
    FOREIGN KEY (login_name) REFERENCES person (login_name)
);
```

And let’s say that while it is important to retain the transaction history, business rules entail using the net balance in application processing rather than any of the transaction detail. To avoid having to frequently recalculate the balance by summing over all the transactions every time the balance is needed, we can denormalize and keep a current balance value right there in the person table by appending a new column and using a trigger and stored function to maintain the net balance as transactions are inserted:

```sql
ALTER TABLE person ADD COLUMN balance MONEY DEFAULT 0;

CREATE FUNCTION transaction_bit() RETURNS trigger
    LANGUAGE plpgsql
    SET SCHEMA 'public'
    AS $$
    DECLARE
    newbalance money;
    BEGIN

    -- Update person account balance

    UPDATE person 
        SET balance = 
            balance + 
            COALESCE(NEW.debit, 0::money) - 
            COALESCE(NEW.credit, 0::money) 
        WHERE login_name = NEW.login_name
                RETURNING balance INTO newbalance;

    -- Data validation

    IF COALESCE(NEW.debit, 0::money) < 0::money THEN
        RAISE EXCEPTION 'Debit value must be non-negative';
    END IF;

    IF COALESCE(NEW.credit, 0::money) < 0::money THEN
        RAISE EXCEPTION 'Credit value must be non-negative';
    END IF;

    IF newbalance < 0::money THEN
        RAISE EXCEPTION 'Insufficient funds: %', NEW;
    END IF;

    RETURN NEW;
    END;
    $$;



CREATE TRIGGER transaction_bit 
      BEFORE INSERT ON transaction 
      FOR EACH ROW EXECUTE PROCEDURE transaction_bit();
```

It may seem odd to do the update first in the stored function before validating non-negativity of the debit, credit, and balance values, but in terms of data validation the order does not matter because the body of a trigger function is executed as a database transaction, so if those validation checks fail, then the entire transaction is rolled back when the exception is raised. The advantage of doing the update first is that the update locks the affected row for the duration of the transaction and so any other session attempting to update the same row is blocked until the current transaction completes. The further validation test assures that the resulting balance is non-negative, and the exception information message can include a variable, which in this case will return the offending attempted insert transaction row for debugging.

To demonstrate that it actually works, here are a few sample entries and a check showing the updated balance at each step:

```sql
SELECT login_name, balance FROM person WHERE login_name = 'dfunny';
 login_name | balance 
------------+---------
 dfunny     |   $0.00
(1 row)

INSERT INTO transaction (login_name, post_date, description, credit, debit) VALUES ('dfunny', '2018-01-11', 'ACH CREDIT FROM: FINANCE AND ACCO ALLOTMENT : Direct Deposit', NULL, '$2,000.00');

SELECT login_name, balance FROM person WHERE login_name = 'dfunny';
 login_name |  balance  
------------+-----------
 dfunny     | $2,000.00
(1 row)
INSERT INTO transaction (login_name, post_date, description, credit, debit) VALUES ('dfunny', '2018-01-17', 'FOR:BGE PAYMENT ACH Withdrawal', '$2780.52', NULL);
ERROR:  Insufficient funds: (dfunny,2018-01-17,"FOR:BGE PAYMENT ACH Withdrawal",,"$2,780.52")
```

Note how the above transaction fails on insufficient funds, i.e., it would produce a negative balance and successfully rolls back. Also note that we returned the entire row with the NEW special variable as extra detail in the error message for debugging.

```sql
SELECT login_name, balance FROM person WHERE login_name = 'dfunny';
 login_name |  balance  
------------+-----------
 dfunny     | $2,000.00
(1 row)

INSERT INTO transaction (login_name, post_date, description, credit, debit) VALUES ('dfunny', '2018-01-17', 'FOR:BGE PAYMENT ACH Withdrawal', '$278.52', NULL);

SELECT login_name, balance FROM person WHERE login_name = 'dfunny';
 login_name |  balance  
------------+-----------
 dfunny     | $1,721.48
(1 row)

INSERT INTO transaction (login_name, post_date, description, credit, debit) VALUES ('dfunny', '2018-01-23', 'FOR: ANNE ARUNDEL ONLINE PMT ACH Withdrawal', '$35.29', NULL);

SELECT login_name, balance FROM person WHERE login_name = 'dfunny';
 login_name |  balance  
------------+-----------
 dfunny     | $1,686.19
(1 row)
```

### EXAMPLE 5 - Triggers and Views Redux

There is a problem with the above implementation, though, and that is that nothing prevents a malicious user from printing money:

```sql
BEGIN;
UPDATE person SET balance = '1000000000.00';

SELECT login_name, balance FROM person WHERE login_name = 'dfunny';
 login_name |      balance      
------------+-------------------
 dfunny     | $1,000,000,000.00
(1 row)

ROLLBACK;
```

We have rolled back the theft above for now and will show a way to build in protection against by using a trigger on a view to prevent updates to the balance value.

We first augment the abridged view from earlier to expose the balance column:

```sql
CREATE OR REPLACE VIEW abridged_person AS
  SELECT login_name, display_name, abstract, balance FROM person;
```

This obviously allows read access to the balance, but it still does not solve the problem because for simple views like this based on a single table, PostgreSQL automatically makes the view writeable:

```sql
BEGIN;
UPDATE abridged_person SET balance = '1000000000.00';
SELECT login_name, balance FROM abridged_person WHERE login_name = 'dfunny';
 login_name |      balance      
------------+-------------------
 dfunny     | $1,000,000,000.00
(1 row)

ROLLBACK;
```

We could use a rule, but to illustrate that triggers can be defined on views as well as tables, we will take the latter route and use an *instead of update* trigger on the view to block unwanted DML, preventing non-transactional changes to the balance value:

```sql
CREATE FUNCTION abridged_person_iut() RETURNS TRIGGER
    LANGUAGE plpgsql
    SET search_path TO public
    AS $$
    BEGIN

    -- Disallow non-transactional changes to balance

      NEW.balance = OLD.balance;
    RETURN NEW;
    END;
    $$;

CREATE TRIGGER abridged_person_iut
    INSTEAD OF UPDATE ON abridged_person
    FOR EACH ROW EXECUTE PROCEDURE abridged_person_iut();
```

The above *instead of update* trigger and stored procedure discards any attempted updates to the balance value and instead forces use of the value present in the database prior to the triggering update statement:

```sql
UPDATE abridged_person SET balance = '1000000000.00';

SELECT login_name, balance FROM abridged_person WHERE login_name = 'dfunny';
 login_name |  balance  
------------+-----------
 dfunny     | $1,686.19
(1 row)
```

which affords protection against un-auditable changes to the balance value.

### EXAMPLE 6 - Elevated Privileges

So far all the example code above has been executed at the database owner level by the *postgres* login role, so any of our anti-tampering efforts could be obviated… that’s just a fact of the database owner super-user privileges.

Our final example illustrates how triggers and stored functions can be used to allow the execution of code by a non-privileged user at a higher privilege than the logged in session user normally has by employing the SECURITY DEFINER attribute associated with stored functions.

First, we define a non-privileged login role, *eve* and confirm that upon instantiation there are no privileges:

```sql
CREATE USER eve;
dp
                                  Access privileges
 Schema |      Name       | Type  | Access privileges | Column privileges | Policies 
--------+-----------------+-------+-------------------+-------------------+----------
 public | abridged_person | view  |                   |                   | 
 public | person          | table |                   |                   | 
 public | person_audit    | table |                   |                   | 
 public | transaction     | table |                   |                   | 
(4 rows)
```

We grant read, update, and create privileges on the abridged person view and read and create to the transaction table:

```sql
GRANT SELECT,INSERT, UPDATE ON abridged_person TO eve;
GRANT SELECT,INSERT ON transaction TO eve;
dp
                                      Access privileges
 Schema |      Name       | Type  |     Access privileges     | Column privileges | Policies 
--------+-----------------+-------+---------------------------+-------------------+----------
 public | abridged_person | view  | postgres=arwdDxt/postgres+|                   | 
        |                 |       | eve=arw/postgres          |                   | 
 public | person          | table |                           |                   | 
 public | person_audit    | table |                           |                   | 
 public | transaction     | table | postgres=arwdDxt/postgres+|                   | 
        |                 |       | eve=ar/postgres           |                   | 
(4 rows)
```

By way of confirmation we see that *eve* is denied access to the person and person_audit tables:

```sql
SET SESSION AUTHORIZATION eve;

SELECT * FROM person;
ERROR:  permission denied for relation person

SELECT * from person_audit;
ERROR:  permission denied for relation person_audit
```

and that she does have appropriate read access to the abridged_person and transaction tables:

```sql
SELECT * FROM abridged_person;
 login_name |    display_name    |                                                            abstract                                                             |  balance  
------------+--------------------+---------------------------------------------------------------------------------------------------------------------------------+-----------
 skeeter    | Mosquito Valentine | Skeeter is Doug's best friend. He is famous in both series for the honking sounds he frequently makes.                          |     $0.00
 dfunny     | Doug Yancey Funny  | Doug is depicted as an introverted, quiet, insecure and gullible 11 (later 12) year old boy who wants to fit in with the crowd. | $1,686.19
(2 rows)

SELECT * FROM transaction;
 login_name | post_date  |                         description                          |   debit   | credit  
------------+------------+--------------------------------------------------------------+-----------+---------
 dfunny     | 2018-01-11 | ACH CREDIT FROM: FINANCE AND ACCO ALLOTMENT : Direct Deposit | $2,000.00 |        
 dfunny     | 2018-01-17 | FOR:BGE PAYMENT ACH Withdrawal                               |           | $278.52
 dfunny     | 2018-01-23 | FOR: ANNE ARUNDEL ONLINE PMT ACH Withdrawal                  |           |  $35.29
(3 rows)
```

However, even though she has write privilege on the transaction table, a transaction insert attempt fails due to lack of privilege on the *person* table.

```sql
SET SESSION AUTHORIZATION eve;

INSERT INTO transaction (login_name, post_date, description, credit, debit) VALUES ('dfunny', '2018-01-23', 'ACH CREDIT FROM: FINANCE AND ACCO ALLOTMENT : Direct Deposit', NULL, '$2,000.00');
ERROR:  permission denied for relation person
CONTEXT:  SQL statement "UPDATE person 
        SET balance = 
            balance + 
            COALESCE(NEW.debit, 0::money) - 
            COALESCE(NEW.credit, 0::money) 
        WHERE login_name = NEW.login_name"
PL/pgSQL function transaction_bit() line 6 at SQL statement
```

The error message context shows this hold up occurs when inside the trigger function DML to update the balance is invoked. The way around this need to deny Eve direct write access to the person table but still effect updates to the person balance in a controlled manner is to add the SECURITY DEFINER attribute to the stored function:

```sql
RESET SESSION AUTHORIZATION;
ALTER FUNCTION transaction_bit() SECURITY DEFINER;

SET SESSION AUTHORIZATION eve;

INSERT INTO transaction (login_name, post_date, description, credit, debit) VALUES ('dfunny', '2018-01-23', 'ACH CREDIT FROM: FINANCE AND ACCO ALLOTMENT : Direct Deposit', NULL, '$2,000.00');

SELECT * FROM transaction;
 login_name | post_date  |                         description                          |   debit   | credit  
------------+------------+--------------------------------------------------------------+-----------+---------
 dfunny     | 2018-01-11 | ACH CREDIT FROM: FINANCE AND ACCO ALLOTMENT : Direct Deposit | $2,000.00 |        
 dfunny     | 2018-01-17 | FOR:BGE PAYMENT ACH Withdrawal                               |           | $278.52
 dfunny     | 2018-01-23 | FOR: ANNE ARUNDEL ONLINE PMT ACH Withdrawal                  |           |  $35.29
 dfunny     | 2018-01-23 | ACH CREDIT FROM: FINANCE AND ACCO ALLOTMENT : Direct Deposit | $2,000.00 |        
(4 rows)

SELECT login_name, balance FROM abridged_person WHERE login_name = 'dfunny';
 login_name |  balance  
------------+-----------
 dfunny     | $3,686.19
(1 row)
```

Now the transaction insert succeeds because the stored function is executed with privilege level of its definer, i.e., the postgres user, which does have the appropriate write privilege on the person table.

## Conclusion

As lengthy as this article is, there’s still a lot more to say about triggers and stored functions. What we covered here is a basic introduction with a consideration of pros and cons of triggers and stored functions. We illustrated six use-case examples showing data validation, change logging, deriving values from inserted data, data hiding with simple updatable views, maintaining summary data in separate tables, and allowing safe invocation of code at elevated privilege. Look for a future article on using triggers and stored functions to prevent missing values in sequentially-incrementing (serial) columns.
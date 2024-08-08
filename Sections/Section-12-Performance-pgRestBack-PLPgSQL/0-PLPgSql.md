### Functions

```sql
CREATE TABLE foo (fooid INT, foosubid INT, fooname TEXT);
INSERT INTO foo VALUES (1, 2, 'three');
INSERT INTO foo VALUES (4, 5, 'six');


```

#### Return Single Value

a PL/pgSQL function that returns the maximum `fooid` from the foo table:

```sql
CREATE OR REPLACE FUNCTION get_max_fooid() RETURNS INT AS
$$
DECLARE
    max_fooid INT;
BEGIN
    SELECT MAX(fooid) INTO max_fooid FROM foo;
    
    RETURN max_fooid;
END;
$$
LANGUAGE plpgsql;

-- Usage:
SELECT get_max_fooid();

```

##### Return the Max sub_id for a given ID

```sql
CREATE OR REPLACE FUNCTION get_max_subid_for_fooid(input_fooid INT) RETURNS INT AS
$$
DECLARE
    max_subid INT;
BEGIN
    SELECT MAX(foosubid) INTO max_subid FROM foo WHERE fooid = input_fooid;
    
    RETURN max_subid;
END;
$$
LANGUAGE plpgsql;

-- Usage:
SELECT get_max_subid_for_fooid(1);
```



### Return a New Table

An example of a PL/pgSQL function that takes a fooid as input and returns the maximum subid for that fooid:

```sql

CREATE OR REPLACE FUNCTION get_fooname_or_nullvalue(null_value TEXT)
RETURNS TABLE (
    fooid INT,
    foosubid INT,
    fooname TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT f.fooid,
           f.foosubid,
           COALESCE(f.fooname, null_value) AS fooname
    FROM foo f;
END;
$$ LANGUAGE plpgsql;


-- Usage:
SELECT * FROM get_fooname_or_nullvalue('Null Names');


CREATE OR REPLACE FUNCTION get_all_foo() RETURNS SETOF foo AS
$BODY$
DECLARE
    r foo%rowtype;
BEGIN
    FOR r IN
        SELECT * FROM foo WHERE fooid > 0
    LOOP
        -- can do some processing here
        RETURN NEXT r; -- return current row of SELECT
    END LOOP;
    RETURN;
END;
$BODY$
LANGUAGE plpgsql;

SELECT * FROM get_all_foo();


CREATE OR REPLACE FUNCTION get_odd_foo() RETURNS SETOF foo AS
$$
DECLARE
    r foo%rowtype;
BEGIN
    FOR r IN
        SELECT * FROM foo WHERE fooid % 2 = 1
    LOOP
        RETURN NEXT r;
    END LOOP;
    RETURN;
END;
$$
LANGUAGE plpgsql;

-- Usage:
SELECT * FROM get_odd_foo();



CREATE OR REPLACE FUNCTION get_foo_stats() RETURNS TABLE(avg_fooid FLOAT, min_fooid INT, max_fooid INT) AS
$$
DECLARE
    avg_fooid FLOAT;
    min_fooid INT;
    max_fooid INT;
BEGIN
    SELECT AVG(fooid), MIN(fooid), MAX(fooid) INTO avg_fooid, min_fooid, max_fooid FROM foo;
    
    RETURN QUERY SELECT avg_fooid, min_fooid, max_fooid;
END;
$$
LANGUAGE plpgsql;

-- Usage:
SELECT * FROM get_foo_stats();

```



### Procedures

A procedure does not have a return value. A procedure can therefore end without a `RETURN` statement. If you wish to use a `RETURN` statement to exit the code early, write just `RETURN` with no expression.

If the procedure has output parameters, the final values of the output parameter variables will be returned to the caller.

```sql
CREATE PROCEDURE triple(INOUT x int)
LANGUAGE plpgsql
AS $$
BEGIN
    x := x * 3;
END;
$$;

DO $$
DECLARE myvar int := 5;
BEGIN
  CALL triple(myvar);
  RAISE NOTICE 'myvar = %', myvar;  -- prints 15
END;
$$

call triple(8);
```

### IN/OUT/INOUT

```sql
CREATE OR REPLACE PROCEDURE update_fooname_by_id(
    IN in_fooid INT,
    IN new_fooname TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE foo
    SET fooname = new_fooname
    WHERE fooid = in_fooid;
END;
$$;

-- Call the procedure
CALL update_fooname_by_id(1, 'new_name');



CREATE OR REPLACE PROCEDURE get_fooname_by_id(
    IN in_fooid INT,
    OUT out_fooname TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT fooname INTO out_fooname
    FROM foo
    WHERE fooid = in_fooid;
END;
$$;

-- Call the procedure
DO $$
DECLARE
    result TEXT;
BEGIN
    CALL get_fooname_by_id(1, result);
    RAISE NOTICE 'Fooname: %', result;
END;
$$;


CREATE OR REPLACE PROCEDURE update_fooname(
    INOUT inout_fooname TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT inout_fooname || ' (updated)' INTO inout_fooname;
END;
$$;

-- Call the procedure
DO $$
DECLARE
    fooname TEXT := 'three';
BEGIN
    CALL update_fooname(fooname);
    RAISE NOTICE 'Updated fooname: %', fooname;
END;
$$;


```

### Tutorials 

- [Conditional Statements](https://www.postgresqltutorial.com/postgresql-plpgsql/plpgsql-if-else-statements/)

Here is a table containing some of the main PostgreSQL `ALTER` commands along with sample usage:

| Command                                          | Description                                             | Sample Usage                                                 |
| ------------------------------------------------ | ------------------------------------------------------- | ------------------------------------------------------------ |
| `ALTER TABLE table_name ADD COLUMN`              | Adds a new column to an existing table.                 | `ALTER TABLE employees ADD COLUMN birthdate DATE;`           |
| `ALTER TABLE table_name DROP COLUMN`             | Removes a column from an existing table.                | `ALTER TABLE employees DROP COLUMN salary;`                  |
| `ALTER TABLE table_name ALTER COLUMN`            | Modifies the data type or other properties of a column. | `ALTER TABLE employees ALTER COLUMN name TYPE VARCHAR(100);` |
| `ALTER TABLE table_name RENAME COLUMN`           | Renames a column in an existing table.                  | `ALTER TABLE employees RENAME COLUMN name TO full_name;`     |
| `ALTER TABLE table_name ADD CONSTRAINT`          | Adds a constraint to a table.                           | `ALTER TABLE employees ADD CONSTRAINT salary_check CHECK (salary > 0);` |
| `ALTER TABLE table_name DROP CONSTRAINT`         | Removes a constraint from a table.                      | `ALTER TABLE employees DROP CONSTRAINT salary_check;`        |
| `ALTER TABLE table_name RENAME TO`               | Renames an existing table.                              | `ALTER TABLE old_table_name RENAME TO new_table_name;`       |
| `ALTER TABLE table_name OWNER TO`                | Changes the owner of a table.                           | `ALTER TABLE employees OWNER TO new_owner;`                  |
| `ALTER TABLE table_name SET SCHEMA`              | Moves a table to a different schema.                    | `ALTER TABLE employees SET SCHEMA new_schema;`               |
| `ALTER TABLE table_name ENABLE TRIGGER`          | Enables a trigger on a table.                           | `ALTER TABLE employees ENABLE TRIGGER trigger_name;`         |
| `ALTER TABLE table_name DISABLE TRIGGER`         | Disables a trigger on a table.                          | `ALTER TABLE employees DISABLE TRIGGER trigger_name;`        |
| `ALTER TABLE table_name CLUSTER ON`              | Reorders the table based on the specified index.        | `ALTER TABLE employees CLUSTER ON index_name;`               |
| `ALTER TABLE table_name SET WITHOUT OIDS`        | Disables OID storage for a table.                       | `ALTER TABLE employees SET WITHOUT OIDS;`                    |
| `ALTER TABLE table_name SET WITH OIDS`           | Enables OID storage for a table.                        | `ALTER TABLE employees SET WITH OIDS;`                       |
| `ALTER TABLE table_name SET TABLESPACE`          | Moves a table to a different tablespace.                | `ALTER TABLE employees SET TABLESPACE new_tablespace;`       |
| `ALTER TABLE table_name SET (storage_parameter)` | Sets storage parameters for a table.                    | `ALTER TABLE employees SET (fillfactor = 70);`               |

Note: Make sure to adapt the sample usage to your specific table and column names, data types, and constraints.
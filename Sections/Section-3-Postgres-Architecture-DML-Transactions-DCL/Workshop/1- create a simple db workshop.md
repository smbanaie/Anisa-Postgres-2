### A Sample DB

let's create this db using psql

![](E:\BigDataCourses\Anisa\Anisa-2\Sections\Section-3-Postgres-Architecture-DML-Transactions-DCL\Workshop\db-sample.png)

```sql
CREATE TABLE rooms (
  room_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rom_number INT UNIQUE
);
```


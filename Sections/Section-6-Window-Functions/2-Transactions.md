### Transactions  Using Northwind Dataset

### 1. Simple Transaction
- **Objective**: Perform a simple transaction to insert a new customer into the Customers table.
- **SQL**:
  ```sql
  BEGIN;
  INSERT INTO Customers (CustomerID, CompanyName) VALUES ('ABC', 'ABC Inc');
  COMMIT;
  ```

### 2. Rollback on Error
- **Objective**: Rollback the transaction if an error occurs during an update operation.
- **SQL**:
  ```sql
  BEGIN;
  UPDATE Orders SET ShipCity = 'New City' WHERE OrderID = 10248;
  
  -- Simulating an error
  UPDATE NonExistentTable SET DummyColumn = 'Error';
  
  COMMIT; -- This line won't be reached if an error occurs
  ```

### 3. Savepoint for Partial Rollback
- **Objective**: Use a savepoint to perform a partial rollback if an error occurs.
- **SQL**:
  ```sql
  BEGIN;
  UPDATE Products SET UnitPrice = UnitPrice * 1.1 WHERE CategoryID = 1;
  
  SAVEPOINT price_increase;
  
  -- Simulating an error
  UPDATE NonExistentTable SET DummyColumn = 'Error';
  
  ROLLBACK TO SAVEPOINT price_increase;
  COMMIT;
  ```

### 4. Nested Transactions
- **Objective**: Demonstrate nested transactions with a commit and rollback within.
- **SQL**:
  ```sql
  BEGIN;
  INSERT INTO Shippers (ShipperID, CompanyName) VALUES (4, 'New Shipper');
  
  SAVEPOINT nested_transaction;
  UPDATE Shippers SET CompanyName = 'Updated Shipper' WHERE ShipperID = 4;
  
  -- Simulating an error
  UPDATE NonExistentTable SET DummyColumn = 'Error';
  
  ROLLBACK TO SAVEPOINT nested_transaction;
  COMMIT;
  ```

### 5. Isolation Level - Read Committed
- **Objective**: Set the isolation level to `READ COMMITTED` and read uncommitted data.
- **SQL**:
  ```sql
  -- Session 1
  BEGIN;
  SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
  SELECT * FROM Orders WHERE CustomerID = 'VINET';
  
  -- Session 2
  BEGIN;
  UPDATE Orders SET ShipCity = 'New City' WHERE OrderID = 10248;
  COMMIT;
  ```

### 6. Isolation Level - Repeatable Read
- **Objective**: Set the isolation level to `REPEATABLE READ` and demonstrate repeatable reads.
- **SQL**:
  ```sql
  -- Session 1
  BEGIN;
  SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
  SELECT * FROM Customers WHERE Country = 'France';
  
  -- Session 2
  BEGIN;
  UPDATE Customers SET ContactName = 'New Contact' WHERE Country = 'France';
  COMMIT;
  ```

### 7. Isolation Level - Serializable
- **Objective**: Set the isolation level to `SERIALIZABLE` and demonstrate serializable transactions.
- **SQL**:
  ```sql
  -- Session 1
  BEGIN;
  SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
  SELECT * FROM Employees WHERE Title = 'Sales Representative';
  
  -- Session 2
  BEGIN;
  UPDATE Employees SET Title = 'New Title' WHERE EmployeeID = 1;
  COMMIT;
  ```

### 8. Concurrency Control - Optimistic Locking
- **Objective**: Implement optimistic locking for concurrent updates.
- **SQL**:
  ```sql
  -- Session 1
  BEGIN;
  SELECT * FROM Products WHERE ProductID = 1;
  
  -- Session 2
  BEGIN;
  UPDATE Products SET UnitPrice = UnitPrice * 1.1 WHERE ProductID = 1;
  COMMIT;
  
  -- Session 1 (continued)
  UPDATE Products SET UnitsInStock = UnitsInStock - 5 WHERE ProductID = 1;
  COMMIT;
  ```

### 9. Concurrency Control - Pessimistic Locking
- **Objective**: Implement pessimistic locking for exclusive access during updates.
- **SQL**:
  ```sql
  -- Session 1
  BEGIN;
  SELECT * FROM Suppliers WHERE SupplierID = 1 FOR UPDATE;
  
  -- Session 2
  BEGIN;
  UPDATE Suppliers SET ContactName = 'New Contact' WHERE SupplierID = 1;
  COMMIT;
  
  -- Session 1 (continued)
  UPDATE Suppliers SET Phone = 'New Phone' WHERE SupplierID = 1;
  COMMIT;
  ```

### 10. Transaction Management in PL/pgSQL
- **Objective**: Use PL/pgSQL to create a function with transaction management logic.
- **SQL**:
  ```sql
  CREATE OR REPLACE FUNCTION update_order_status(order_id INT, new_status VARCHAR) RETURNS VOID AS $$
  BEGIN
      BEGIN;
      UPDATE Orders SET Status = new_status WHERE OrderID = order_id;
      COMMIT;
  EXCEPTION
      WHEN others THEN
          ROLLBACK;
          RAISE;
  END;
  $$ LANGUAGE plpgsql;
  
  -- Example usage
  SELECT update_order_status(10248, 'Shipped');
  ```

These examples cover a range of scenarios, from simple transactions to advanced topics like isolation levels and concurrency control. They provide a comprehensive understanding of working with transactions in PostgreSQL using the Northwind dataset.
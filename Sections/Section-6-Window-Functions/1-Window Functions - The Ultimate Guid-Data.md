# [The Ultimate Guide to SQL Window Functions](https://www.stratascratch.com/blog/the-ultimate-guide-to-sql-window-functions/)

![](.\images\window_functions.webp)

### twitch_sessions




| user_id    | session_start | session_end | session_id  | session_type|
| ---- | ------------------- | ------------------- | ---- | -------- |
| 0    | 2020-08-11 05:51:31 | 2020-08-11 05:54:45 | 539  | streamer |
| 2    | 2020-07-11 03:36:54 | 2020-07-11 03:37:08 | 840  | streamer |
| 3    | 2020-11-26 11:41:47 | 2020-11-26 11:52:01 | 848  | streamer |
| 1    | 2020-11-19 06:24:24 | 2020-11-19 07:24:38 | 515  | viewer   |
| 2    | 2020-11-14 03:36:05 | 2020-11-14 03:39:19 | 646  | viewer   |
| 0    | 2020-03-11 03:01:40 | 2020-03-11 03:01:59 | 782  | streamer |
| 0    | 2020-08-11 03:50:45 | 2020-08-11 03:55:59 | 815  | viewer   |
| 3    | 2020-10-11 22:15:14 | 2020-10-11 22:18:28 | 630  | viewer   |
| 1    | 2020-11-20 06:59:57 | 2020-11-20 07:20:11 | 907  | streamer |
| 2    | 2020-07-11 14:32:19 | 2020-07-11 14:42:33 | 949  | viewer   |

```sql
CREATE TABLE twitch_sessions (
    user_id SERIAL PRIMARY KEY,
    session_start TIMESTAMP NOT NULL,
    session_end TIMESTAMP NOT NULL,
    session_id INTEGER NOT NULL,
    session_type VARCHAR(20) NOT NULL
);

INSERT INTO twitch_sessions (user_id, session_start, session_end, session_id, session_type)
VALUES
    (0,'2020-08-11 05:51:31', '2020-08-11 05:54:45', 539, 'streamer'),
    (2,'2020-07-11 03:36:54', '2020-07-11 03:37:08', 840, 'streamer'),
    (3,'2020-11-26 11:41:47', '2020-11-26 11:52:01', 848, 'streamer'),
    (1,'2020-11-19 06:24:24', '2020-11-19 07:24:38', 515, 'viewer'),
    (2,'2020-11-14 03:36:05', '2020-11-14 03:39:19', 646, 'viewer'),
    (0,'2020-03-11 03:01:40', '2020-03-11 03:01:59', 782, 'streamer'),
    (0,'2020-08-11 03:50:45', '2020-08-11 03:55:59', 815, 'viewer'),
    (3,'2020-10-11 22:15:14', '2020-10-11 22:18:28', 630, 'viewer'),
    (1,'2020-11-20 06:59:57', '2020-11-20 07:20:11', 907, 'streamer'),
    (2,'2020-07-11 14:32:19', '2020-07-11 14:42:33', 949, 'viewer');

    
```

#### Question 1 : Calculate the average session duration for each session type?
**Normal Way**
```sql
SELECT session_type,
       avg(session_end - session_start) AS duration
FROM twitch_sessions
GROUP BY session_type
```
**Window Functions **

- First Try

```sql
SELECT *,
       avg(session_end -session_start) OVER (PARTITION BY session_type) 
       AS duration
FROM twitch_sessions
```

- The Right Way

```sql
SELECT DISTINCT session_type,
       avg(session_end -session_start) OVER (PARTITION BY session_type)
       AS duration
FROM twitch_sessions

```

##### Filter

```sql
SELECT
    session_type,
    AVG(session_end - session_start) FILTER (WHERE EXTRACT(MONTH FROM session_start) = 10) AS duration_10,
    AVG(session_end - session_start) FILTER (WHERE EXTRACT(MONTH FROM session_start) = 11) AS duration_11
FROM
    twitch_sessions
GROUP BY
    session_type;
```



### Employee Salary



> ***We have a table with employees and their salaries, however, some of the records are old and contain outdated salary information. Find the current salary of each employee assuming that salaries increase each year. Output their id, first name, last name, department ID, and current salary. Order your list by employee ID in ascending order.***




| id   | first_name | last_name | salary | department_id |
| ---- | ---------- | --------- | ------ | ------------- |
| 1    | Todd       | Wilson    | 110000 | 1006          |
| 1    | Todd       | Wilson    | 106119 | 1006          |
| 2    | Justin     | Simon     | 128922 | 1005          |
| 2    | Justin     | Simon     | 130000 | 1005          |
| 3    | Kelly      | Rosario   | 42689  | 1002          |
| 4    | Patricia   | Powell    | 162825 | 1004          |
| 4    | Patricia   | Powell    | 170000 | 1004          |
| 5    | Sherry     | Golden    | 44101  | 1002          |
| 6    | Natasha    | Swanson   | 79632  | 1005          |
| 6    | Natasha    | Swanson   | 90000  | 1005          |
| 7    | Diane      | Gordon    | 74591  | 1002          |
| 8    | Mercedes   | Rodriguez | 61048  | 1005          |
| 9    | Christy    | Mitchell  | 137236 | 1001          |
| 9    | Christy    | Mitchell  | 140000 | 1001          |
| 9    | Christy    | Mitchell  | 150000 | 1001          |
| 10   | Sean       | Crawford  | 182065 | 1006          |
| 10   | Sean       | Crawford  | 190000 | 1006          |


```sql
-- Create ms_employee_salary table
CREATE TABLE ms_employee_salary (
    id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    salary INT,
    department_id INT
);

-- Insert data into ms_employee_salary table
INSERT INTO ms_employee_salary (id, first_name, last_name, salary, department_id) VALUES
(1, 'Todd', 'Wilson', 110000, 1006),
(1, 'Todd', 'Wilson', 106119, 1006),
(2, 'Justin', 'Simon', 128922, 1005),
(2, 'Justin', 'Simon', 130000, 1005),
(3, 'Kelly', 'Rosario', 42689, 1002),
(4, 'Patricia', 'Powell', 162825, 1004),
(4, 'Patricia', 'Powell', 170000, 1004),
(5, 'Sherry', 'Golden', 44101, 1002),
(6, 'Natasha', 'Swanson', 79632, 1005),
(6, 'Natasha', 'Swanson', 90000, 1005),
(7, 'Diane', 'Gordon', 74591, 1002),
(8, 'Mercedes', 'Rodriguez', 61048, 1005),
(9, 'Christy', 'Mitchell', 137236, 1001),
(9, 'Christy', 'Mitchell', 140000, 1001),
(9, 'Christy', 'Mitchell', 150000, 1001),
(10, 'Sean', 'Crawford', 182065, 1006),
(10, 'Sean', 'Crawford', 190000, 1006),
(11, 'Kevin', 'Townsend', 166861, 1002),
(12, 'Joshua', 'Johnson', 123082, 1004),
(13, 'Julie', 'Sanchez', 185663, 1001),
(13, 'Julie', 'Sanchez', 200000, 1001),
(13, 'Julie', 'Sanchez', 210000, 1001),
(14, 'John', 'Coleman', 152434, 1001),
(15, 'Anthony', 'Valdez', 96898, 1001),
(16, 'Briana', 'Rivas', 151668, 1005),
(17, 'Jason', 'Burnett', 42525, 1006),
(18, 'Jeffrey', 'Harris', 14491, 1002),
(18, 'Jeffrey', 'Harris', 20000, 1002),
(19, 'Michael', 'Ramsey', 63159, 1003),
(20, 'Cody', 'Gonzalez', 112809, 1004),
(21, 'Stephen', 'Berry', 123617, 1002),
(22, 'Brittany', 'Scott', 162537, 1002),
(23, 'Angela', 'Williams', 100875, 1004),
(24, 'William', 'Flores', 142674, 1003),
(25, 'Pamela', 'Matthews', 57944, 1005),
(26, 'Allison', 'Johnson', 128782, 1001),
(27, 'Anthony', 'Ball', 34386, 1003),
(28, 'Alexis', 'Beck', 12260, 1005),
(29, 'Jason', 'Olsen', 51937, 1006),
(30, 'Stephen', 'Smith', 194791, 1001),
(31, 'Kimberly', 'Brooks', 95327, 1003),
(32, 'Eric', 'Zimmerman', 83093, 1006),
(33, 'Peter', 'Holt', 69945, 1002),
(34, 'Justin', 'Dunn', 67992, 1003),
(35, 'John', 'Ball', 47795, 1004),
(36, 'Jesus', 'Ward', 36078, 1005),
(37, 'Philip', 'Gillespie', 36424, 1006),
(38, 'Nicole', 'Lewis', 114079, 1001),
(39, 'Linda', 'Clark', 186781, 1002),
(40, 'Colleen', 'Carrillo', 147723, 1004),
(41, 'John', 'George', 21642, 1001),
(42, 'Traci', 'Williams', 138892, 1003),
(42, 'Traci', 'Williams', 150000, 1003),
(42, 'Traci', 'Williams', 160000, 1003),
(42, 'Traci', 'Williams', 180000, 1003),
(43, 'Joseph', 'Rogers', 22800, 1005),
(44, 'Trevor', 'Carter', 38670, 1001),
(45, 'Kevin', 'Duncan', 45210, 1003),
(46, 'Joshua', 'Ewing', 73088, 1003),
(47, 'Kimberly', 'Dean', 71416, 1003),
(48, 'Robert', 'Lynch', 117960, 1004),
(49, 'Amber', 'Harding', 77764, 1002),
(50, 'Victoria', 'Wilson', 176620, 1002),
(51, 'Theresa', 'Everett', 31404, 1002),
(52, 'Kara', 'Smith', 192838, 1004),
(53, 'Teresa', 'Cohen', 98860, 1001),
(54, 'Wesley', 'Tucker', 90221, 1005),
(55, 'Michael', 'Morris', 106799, 1005),
(56, 'Rachael', 'Williams', 103585, 1002),
(57, 'Patricia', 'Harmon', 147417, 1005),
(58, 'Edward', 'Sharp', 41077, 1005),
(59, 'Kevin', 'Robinson', 100924, 1005),
(60, 'Charles', 'Pearson', 173317, 1004),
(61, 'Ryan', 'Brown', 110225, 1003),
(61, 'Ryan', 'Brown', 120000, 1003),
(62, 'Dale', 'Hayes', 97662, 1005),
(63, 'Richard', 'Sanford', 136083, 1001),
(64, 'Danielle', 'Williams', 98655, 1006),
(64, 'Danielle', 'Williams', 110000, 1006),
(64, 'Danielle', 'Williams', 120000, 1006),
(65, 'Deborah', 'Martin', 67389, 1004),
(66, 'Dustin', 'Bush', 47567, 1004),
(67, 'Tyler', 'Green', 111085, 1002),
(68, 'Antonio', 'Carpenter', 83684, 1002),
(69, 'Ernest', 'Peterson', 115993, 1005),
(70, 'Karen', 'Fernandez', 101238, 1003),
(71, 'Kristine', 'Casey', 67651, 1003),
(72, 'Christine', 'Frye', 137244, 1004),
(73, 'William', 'Preston', 155225, 1003),
(74, 'Richard', 'Cole', 180361, 1003),
(75, 'Julia', 'Ramos', 61398, 1006),
(75, 'Julia', 'Ramos', 70000, 1006),
(75, 'Julia', 'Ramos', 83000, 1006),
(75, 'Julia', 'Ramos', 90000, 1006),
(75, 'Julia', 'Ramos', 105000, 1006);

```

######  The Classic  Way

```sql
SELECT id,
       first_name,
       last_name,
       department_id,
       max(salary)
FROM ms_employee_salary
GROUP BY id,
         first_name,
         last_name,
         department_id
```

###### Window Functions
```sql
SELECT DISTINCT id,
       first_name,
       last_name,
       department_id,
       max(salary) OVER(PARTITION BY id, first_name, last_name, 
       department_id)
FROM ms_employee_salary
```

### employee

> Compare each employee's salary with the average salary of the corresponding department. Output the department, first name, and salary of employees along with the average salary of that department.



| id   | first_name | last_name | age  | sex  | employee_title | department | salary | target | bonus | email                | city       | address              | manager_id |
| ---- | ---------- | --------- | ---- | ---- | -------------- | ---------- | ------ | ------ | ----- | -------------------- | ---------- | -------------------- | ---------- |
| 5    | Max        | George    | 26   | M    | Sales          | Sales      | 1300   | 200    | 150   | Max@company.com      | California | 2638 Richards Avenue | 1          |
| 13   | Katty      | Bond      | 56   | F    | Manager        | Management | 150000 | 0      | 300   | Katty@company.com    | Arizona    |                      | 1          |
| 11   | Richerd    | Gear      | 57   | M    | Manager        | Management | 250000 | 0      | 300   | Richerd@company.com  | Alabama    |                      | 1          |
| 10   | Jennifer   | Dion      | 34   | F    | Sales          | Sales      | 1000   | 200    | 150   | Jennifer@company.com | Alabama    |                      | 13         |

```sql
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    sex CHAR(1),
    employee_title VARCHAR(50),
    department VARCHAR(50),
    salary INT,
    target INT,
    bonus INT,
    email VARCHAR(100),
    city VARCHAR(50),
    address VARCHAR(100),
    manager_id INT
);

INSERT INTO employee VALUES
(5, 'Max', 'George', 26, 'M', 'Sales', 'Sales', 1300, 200, 150, 'Max@company.com', 'California', '2638 Richards Avenue', 1),
(13, 'Katty', 'Bond', 56, 'F', 'Manager', 'Management', 150000, 0, 300, 'Katty@company.com', 'Arizona', NULL, 1),
(11, 'Richerd', 'Gear', 57, 'M', 'Manager', 'Management', 250000, 0, 300, 'Richerd@company.com', 'Alabama', NULL, 1),
(10, 'Jennifer', 'Dion', 34, 'F', 'Sales', 'Sales', 1000, 200, 150, 'Jennifer@company.com', 'Alabama', NULL, 13),
(19, 'George', 'Joe', 50, 'M', 'Manager', 'Management', 100000, 0, 300, 'George@company.com', 'Florida', '1003 Wyatt Street', 1),
(18, 'Laila', 'Mark', 26, 'F', 'Sales', 'Sales', 1000, 200, 150, 'Laila@company.com', 'Florida', '3655 Spirit Drive', 11),
(20, 'Sarrah', 'Bicky', 31, 'F', 'Senior Sales', 'Sales', 2000, 200, 150, 'Sarrah@company.com', 'Florida', '1176 Tyler Avenue', 19),
(21, 'Suzan', 'Lee', 34, 'F', 'Sales', 'Sales', 1300, 200, 150, 'Suzan@company.com', 'Florida', '1275 Monroe Avenue', 19),
(22, 'Mandy', 'John', 31, 'F', 'Sales', 'Sales', 1300, 200, 150, 'Mandy@company.com', 'Florida', '2510 Maryland Avenue', 19),
(23, 'Britney', 'Berry', 45, 'F', 'Sales', 'Sales', 1200, 200, 100, 'Britney@company.com', 'Florida', '3946 Steve Hunt Road', 19),
(25, 'Jack', 'Mick', 29, 'M', 'Sales', 'Sales', 1300, 200, 100, 'Jack@company.com', 'Hawaii', '3762 Stratford Drive', 19),
(26, 'Ben', 'Ten', 43, 'M', 'Sales', 'Sales', 1300, 150, 100, 'Ben@company.com', 'Hawaii', '3055 Indiana Avenue', 19),
(27, 'Tom', 'Fridy', 32, 'M', 'Sales', 'Sales', 1200, 200, 150, 'Tom@company.com', 'Hawaii', '801 Stratford Drive', 1),
(29, 'Antoney', 'Adam', 34, 'M', 'Sales', 'Sales', 1300, 180, 150, 'Antoney@company.com', 'Hawaii', '3533 Randall Drive', 1),
(28, 'Morgan', 'Matt', 25, 'M', 'Sales', 'Sales', 1200, 200, 150, 'Morgan@company.com', 'Hawaii', '2641 Randall Drive', 1),
(6, 'Molly', 'Sam', 28, 'F', 'Sales', 'Sales', 1400, 100, 150, 'Molly@company.com', 'Arizona', '3632 Polk Street', 13),
(7, 'Nicky', 'Bat', 33, 'F', 'Sales', 'Sales', 1400, 400, 100, 'Molly@company.com', 'Arizona', '3461 Preston Street', 13),
(9, 'Monika', 'William', 33, 'F', 'Sales', 'Sales', 1000, 200, 100, 'Molly@company.com', 'Alabama', NULL, 13),
(17, 'Mick', 'Berry', 44, 'M', 'Senior Sales', 'Sales', 2200, 200, 150, 'Mick@company.com', 'Florida', NULL, 11),
(12, 'Shandler', 'Bing', 23, 'M', 'Auditor', 'Audit', 1100, 200, 150, 'Shandler@company.com', 'Arizona', NULL, 11),
(14, 'Jason', 'Tom', 23, 'M', 'Auditor', 'Audit', 1000, 200, 150, 'Jason@company.com', 'Arizona', NULL, 11),
(16, 'Celine', 'Anston', 27, 'F', 'Auditor', 'Audit', 1000, 200, 150, 'Celine@company.com', 'Colorado', NULL, 11),
(15, 'Michale', 'Jackson', 44, 'F', 'Auditor', 'Audit', 700, 150, 150, 'Michale@company.com', 'Colorado', NULL, 11),
(24, 'Adam', 'Morris', 30, 'M', 'Sales', 'Sales', 1300, 200, 100, 'Adam@company.com', 'Alabama', '4541 Ferry Street', 19),
(30, 'Mark', 'Jon', 28, 'M', 'Sales', 'Sales', 1200, 200, 150, 'Mark@company.com', 'Alabama', '2522 George Avenue', 1),
(8, 'John', 'Ford', 26, 'M', 'Senior Sales', 'Sales', 1500, 140, 100, 'Molly@company.com', 'Alabama', '4832 New Creek Road', 13),
(1, 'Allen', 'Wang', 55, 'F', 'Manager', 'Management', 200000, 0, 300, 'Allen@company.com', 'California', '1069 Ventura Drive', 1),
(2, 'Joe', 'Jack', 32, 'M', 'Sales', 'Sales', 1000, 200, 150, 'Joe@company.com', 'California', '995 Jim Rosa Lane', 1),
(3, 'Henry', 'Ted', 31, 'M', 'Senior Sales', 'Sales', 2000, 200, 150, 'Henry@company.com', 'California', '1609 Ford Street', 1),
(4, 'Sam', 'Mark', 25, 'M', 'Sales', 'Sales', 1000, 120, 150, 'Sam@company.com', 'California', '4869 Libby Street', 1);

```

> Compare each employee's salary with the average salary of the corresponding department. Output the department, first name, and salary of employees along with the average salary of that department.



```sql
SELECT department, 
       first_name, 
       salary, 
       AVG(salary) over (PARTITION BY department) 
FROM employee;
```

> Is there any difference between departments in terms of average salaries? what about gender ? gender and department ?



## Ranking Functions

#### User Email Activity 

> Find the email activity rank for each user. Email activity rank is defined by the total number of emails sent. The user with the highest number of emails sent will have a rank of 1, and so on. Output the user, total emails, and their activity rank. Order records by the total emails in descending order. Sort users with the same number of emails in alphabetical order. In your rankings, return a unique value (i.e., a unique rank) even if multiple users have the same number of emails. For tie breaker use alphabetical order of the user usernames.
>
> 

### google_gmail_emails

| id   | from_user          | to_user            | day  |
| ---- | ------------------ | ------------------ | ---- |
| 0    | 6edf0be4b2267df1fa | 75d295377a46f83236 | 10   |
| 1    | 6edf0be4b2267df1fa | 32ded68d89443e808  | 6    |
| 2    | 6edf0be4b2267df1fa | 55e60cfcc9dc49c17e | 10   |
| 3    | 6edf0be4b2267df1fa | e0e0defbb9ec47f6f7 | 6    |
| 4    | 6edf0be4b2267df1fa | 47be2887786891367e | 1    |
| 5    | 6edf0be4b2267df1fa | 2813e59cf6c1ff698e | 6    |
| 6    | 6edf0be4b2267df1fa | a84065b7933ad01019 | 8    |
| 7    | 6edf0be4b2267df1fa | 850badf89ed8f06854 | 1    |
| 8    | 6edf0be4b2267df1fa | 6b503743a13d778200 | 1    |
| 9    | 6edf0be4b2267df1fa | d63386c884aeb9f71d | 3    |
| 10   | 6edf0be4b2267df1fa | 5b8754928306a18b68 | 2    |

```sql
CREATE TABLE google_gmail_emails (
    id INT PRIMARY KEY,
    from_user VARCHAR(50),
    to_user VARCHAR(50),
    day INT
);

INSERT INTO google_gmail_emails (id, from_user, to_user, day) VALUES
(0, '6edf0be4b2267df1fa', '75d295377a46f83236', 10),
(1, '6edf0be4b2267df1fa', '32ded68d89443e808', 6),
(2, '6edf0be4b2267df1fa', '55e60cfcc9dc49c17e', 10),
(3, '6edf0be4b2267df1fa', 'e0e0defbb9ec47f6f7', 6),
(4, '6edf0be4b2267df1fa', '47be2887786891367e', 1),
(5, '6edf0be4b2267df1fa', '2813e59cf6c1ff698e', 6),
(6, '6edf0be4b2267df1fa', 'a84065b7933ad01019', 8),
(7, '6edf0be4b2267df1fa', '850badf89ed8f06854', 1),
(8, '6edf0be4b2267df1fa', '6b503743a13d778200', 1),
(9, '6edf0be4b2267df1fa', 'd63386c884aeb9f71d', 3),
(10, '6edf0be4b2267df1fa', '5b8754928306a18b68', 2),
(11, '6edf0be4b2267df1fa', '6edf0be4b2267df1fa', 8),
(12, '6edf0be4b2267df1fa', '406539987dd9b679c0', 9),
(13, '6edf0be4b2267df1fa', '114bafadff2d882864', 5),
(14, '6edf0be4b2267df1fa', '157e3e9278e32aba3e', 2),
(15, '75d295377a46f83236', '75d295377a46f83236', 6),
(16, '75d295377a46f83236', 'd63386c884aeb9f71d', 8),
(17, '75d295377a46f83236', '55e60cfcc9dc49c17e', 3),
(18, '75d295377a46f83236', '47be2887786891367e', 10),
(19, '75d295377a46f83236', '5b8754928306a18b68', 10),
(20, '75d295377a46f83236', '850badf89ed8f06854', 7),
(21, '75d295377a46f83236', '5eff3a5bfc0687351e', 2),
(22, '75d295377a46f83236', '5dc768b2f067c56f77', 8),
(23, '75d295377a46f83236', '114bafadff2d882864', 3),
(24, '75d295377a46f83236', 'e0e0defbb9ec47f6f7', 3),
(25, '75d295377a46f83236', '7cfe354d9a64bf8173', 10),
(26, '5dc768b2f067c56f77', '114bafadff2d882864', 3),
(27, '5dc768b2f067c56f77', '2813e59cf6c1ff698e', 5),
(28, '5dc768b2f067c56f77', '91f59516cb9dee1e88', 6),
(29, '5dc768b2f067c56f77', '5b8754928306a18b68', 6),
(30, '5dc768b2f067c56f77', '6b503743a13d778200', 5),
(31, '5dc768b2f067c56f77', 'aa0bd72b729fab6e9e', 10),
(32, '5dc768b2f067c56f77', '55e60cfcc9dc49c17e', 7),
(33, '5dc768b2f067c56f77', '75d295377a46f83236', 9),
(34, '5dc768b2f067c56f77', 'e0e0defbb9ec47f6f7', 7),
(35, '5dc768b2f067c56f77', 'a84065b7933ad01019', 3),
(36, '5dc768b2f067c56f77', '32ded68d89443e808', 6),
(37, '5dc768b2f067c56f77', '157e3e9278e32aba3e', 3),
(38, '5dc768b2f067c56f77', '850badf89ed8f06854', 6),
(39, '5dc768b2f067c56f77', 'b37650899e52128b58', 4),
(40, '5dc768b2f067c56f77', 'e7c12e2c77855a46b6', 8),
(41, '5dc768b2f067c56f77', '406539987dd9b679c0', 4),
(42, '5dc768b2f067c56f77', '8e0b4cb865a5e7a0f1', 7),
(43, '5dc768b2f067c56f77', '62a2f6060c1f5753d9', 2),
(44, '5dc768b2f067c56f77', '3b0340f94ec93a6945', 7),
(45, '5dc768b2f067c56f77', 'd73a0d983f2e28d574', 9),
(46, '5dc768b2f067c56f77', 'a61486209d157312b2', 5),
(47, '5dc768b2f067c56f77', 'e8ac5fcf1261890d63', 5),
(48, '5dc768b2f067c56f77', '59c1a9c6a09725890c', 6),
(49, '5dc768b2f067c56f77', '3cd0a296348ac105e9', 10),
(50, 'e8ac5fcf1261890d63', '157e3e9278e32aba3e', 4),
(51, 'e8ac5fcf1261890d63', 'd73a0d983f2e28d574', 5),
(52, 'e8ac5fcf1261890d63', '6edf0be4b2267df1fa', 1),
(53, 'e8ac5fcf1261890d63', '91f59516cb9dee1e88', 7),
(54, 'e8ac5fcf1261890d63', '5eff3a5bfc0687351e', 4),
(55, 'e8ac5fcf1261890d63', '55e60cfcc9dc49c17e', 1),
(56, 'e8ac5fcf1261890d63', '2813e59cf6c1ff698e', 5),
(57, 'e8ac5fcf1261890d63', '6b503743a13d778200', 7),
(58, 'e8ac5fcf1261890d63', '75d295377a46f83236', 8),
(59, 'e8ac5fcf1261890d63', '47be2887786891367e', 4),
(60, 'e8ac5fcf1261890d63', '5b8754928306a18b68', 5)
;
```



```sql
SELECT  from_user, 
        COUNT(*) as total_emails 
FROM google_gmail_emails 
GROUP BY from_user
ORDER BY 2 DESC


# Window Functions

SELECT  from_user, 
        COUNT(*) as total_emails, 
        ROW_NUMBER() OVER ( ORDER BY count(*) desc, from_user asc)
FROM google_gmail_emails 
GROUP BY from_user


#1
SELECT from_user,
       total_emails
FROM
  (SELECT from_user,
          COUNT(*) AS total_emails,
          RANK() OVER (
                       ORDER BY count(*) DESC) rnk
   FROM google_gmail_emails
   GROUP BY from_user) a
WHERE rnk = 1


SELECT  from_user, 
        COUNT(*) as total_emails, 
        DENSE_RANK() OVER (ORDER BY count(*) desc)
FROM google_gmail_emails 
GROUP BY from_user




## Ntile

SELECT  from_user, 
        COUNT(*) as total_emails, 
        NTILE(2) OVER (ORDER BY count(*) desc)
FROM google_gmail_emails 
GROUP BY from_user


```

## Value Window Functions

- LAG()
- LEAD()
- FIRST_VALUE()
- LAST_VALUE()
- NTH_VALUE()



### [Daily Violation Counts](https://platform.stratascratch.com/coding/9740-daily-violation-counts?code_type=1)

> Determine the change in the number of daily violations by calculating the difference between the count of current and previous violations by inspection date. Output the inspection date and the change in the number of daily violations. Order your results by the earliest inspection date first.



#### Fact_Events

> Write a query that returns the number of unique users per client per month



```sql
create database windows; 

CREATE TABLE fact_events (
    id serial PRIMARY KEY,
    time_id DATE NOT NULL,
    user_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    client_id VARCHAR(20) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_id INTEGER NOT NULL
);

INSERT INTO fact_events (id, time_id, user_id, customer_id, client_id, event_type, event_id) VALUES
(1, '2020-02-28', '3668-QPYBK', 'Sendit', 'desktop', 'message sent', 3),
(2, '2020-02-28', '7892-POOKP', 'Connectix', 'mobile', 'file received', 2),
(3, '2020-04-03', '9763-GRSKD', 'Zoomit', 'desktop', 'video call received', 7),
(4, '2020-04-02', '9763-GRSKD', 'Connectix', 'desktop', 'video call received', 7),
(5, '2020-02-06', '9237-HQITU', 'Sendit', 'desktop', 'video call received', 7),
(6, '2020-02-27', '8191-XWSZG', 'Connectix', 'desktop', 'file received', 2),
(7, '2020-04-03', '9237-HQITU', 'Connectix', 'desktop', 'video call received', 7),
(8, '2020-03-01', '9237-HQITU', 'Connectix', 'mobile', 'message received', 4),
(9, '2020-04-02', '4190-MFLUW', 'Connectix', 'mobile', 'video call received', 7),
(10, '2020-04-21', '9763-GRSKD', 'Sendit', 'desktop', 'file received', 2),
(11, '2020-02-28', '5129-JLPIS', 'Electric Gravity', 'mobile', 'video call started', 6),
(12, '2020-03-31', '6713-OKOMC', 'Connectix', 'desktop', 'file received', 2),
(13, '2020-03-21', '6388-TABGU', 'Connectix', 'desktop', 'message sent', 3),
(14, '2020-03-03', '7469-LKBCI', 'Connectix', 'mobile', 'video call received', 7),
(15, '2020-02-11', '9237-HQITU', 'Connectix', 'desktop', 'video call received', 7),
(16, '2020-03-01', '5575-GNVDE', 'Zoomit', 'desktop', 'file received', 2),
(17, '2020-03-02', '6388-TABGU', 'Connectix', 'desktop', 'message sent', 3),
(18, '2020-04-06', '9305-CDSKC', 'Connectix', 'desktop', 'message received', 4),
(19, '2020-02-13', '3668-QPYBK', 'Connectix', 'mobile', 'file sent', 1),
(20, '2020-04-03', '9959-WOFKT', 'Connectix', 'desktop', 'file received', 2),
(21, '2020-03-15', '9305-CDSKC', 'Zoomit', 'mobile', 'message received', 4),
(22, '2020-04-01', '7892-POOKP', 'eShop', 'mobile', 'voice call started', 8),
(23, '2020-04-09', '8191-XWSZG', 'Connectix', 'mobile', 'file received', 2),
(24, '2020-04-08', '3668-QPYBK', 'eShop', 'desktop', 'message sent', 3),
(25, '2020-03-05', '8191-XWSZG', 'Zoomit', 'mobile', 'file received', 2),
(26, '2020-02-24', '3668-QPYBK', 'Connectix', 'mobile', 'api message received', 5),
(27, '2020-03-26', '6388-TABGU', 'Zoomit', 'desktop', 'message received', 4),
(28, '2020-02-03', '7795-CFOCW', 'Connectix', 'mobile', 'api message received', 5),
(29, '2020-03-19', '7892-POOKP', 'Connectix', 'desktop', 'message received', 4),
(30, '2020-04-07', '9763-GRSKD', 'Connectix', 'mobile', 'message sent', 3),
(31, '2020-04-06', '9959-WOFKT', 'Connectix', 'desktop', 'message received', 4),
(32, '2020-02-15', '9237-HQITU', 'Connectix', 'mobile', 'message sent', 3),
(33, '2020-04-06', '4183-MYFRB', 'Sendit', 'desktop', 'file received', 2),
(34, '2020-03-13', '9305-CDSKC', 'Connectix', 'desktop', 'video call received', 7),
(35, '2020-04-05', '9959-WOFKT', 'Connectix', 'mobile', 'message received', 4),
(36, '2020-03-28', '6388-TABGU', 'Connectix', 'desktop', 'message sent', 3),
(37, '2020-04-03', '4183-MYFRB', 'Connectix', 'desktop', 'message received', 4),
(38, '2020-03-15', '5575-GNVDE', 'Electric Gravity', 'desktop', 'video call started', 6),
(39, '2020-03-06', '8091-TTVAX', 'Zoomit', 'desktop', 'file received', 2),
(40, '2020-03-25', '4190-MFLUW', 'Connectix', 'mobile', 'file received', 2),
(41, '2020-04-13', '9959-WOFKT', 'Zoomit', 'mobile', 'video call received', 7),
(42, '2020-02-20', '7590-VHVEG', 'Sendit', 'desktop', 'file received', 2),
(43, '2020-03-13', '9305-CDSKC', 'Connectix', 'mobile', 'voice call received', 9),
(44, '2020-02-22', '1452-KIOVK', 'Zoomit', 'mobile', 'voice call started', 8),
(45, '2020-04-18', '9959-WOFKT', 'Connectix', 'desktop', 'file received', 2),
(46, '2020-02-04', '9305-CDSKC', 'Connectix', 'mobile', 'file sent', 1),
(47, '2020-04-14', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(48, '2020-04-04', '6388-TABGU', 'Connectix', 'desktop', 'video call received', 7),
(49, '2020-02-14', '9763-GRSKD', 'Zoomit', 'mobile', 'file sent', 1),
(50, '2020-02-18', '9763-GRSKD', 'Connectix', 'desktop', 'message sent', 3),
(51, '2020-02-26', '8191-XWSZG', 'Connectix', 'mobile', 'video call received', 7),
(52, '2020-02-16', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(53, '2020-03-08', '9763-GRSKD', 'Connectix', 'desktop', 'video call received', 7),
(54, '2020-03-06', '9959-WOFKT', 'Connectix', 'mobile', 'message sent', 3),
(55, '2020-03-02', '9763-GRSKD', 'Connectix', 'mobile', 'file received', 2),
(56, '2020-02-09', '9763-GRSKD', 'Zoomit', 'mobile', 'file received', 2),
(57, '2020-04-11', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(58, '2020-02-10', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(59, '2020-03-06', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(60, '2020-02-05', '9763-GRSKD', 'Connectix', 'desktop', 'message received', 4),
(61, '2020-04-02', '9763-GRSKD', 'Connectix', 'desktop', 'file sent', 1),
(62, '2020-02-19', '9763-GRSKD', 'Zoomit', 'desktop', 'video call received', 7),
(63, '2020-04-17', '9763-GRSKD', 'Connectix', 'mobile', 'file received', 2),
(64, '2020-02-29', '9763-GRSKD', 'Connectix', 'desktop', 'message received', 4),
(65, '2020-03-25', '9763-GRSKD', 'Connectix', 'mobile', 'file received', 2),
(66, '2020-02-21', '9763-GRSKD', 'Connectix', 'desktop', 'message received', 4),
(67, '2020-03-03', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(68, '2020-04-12', '9763-GRSKD', 'Zoomit', 'desktop', 'message received', 4),
(69, '2020-03-20', '9763-GRSKD', 'Connectix', 'mobile', 'file received', 2),
(70, '2020-04-03', '9763-GRSKD', 'Connectix', 'desktop', 'video call received', 7),
(71, '2020-02-22', '9763-GRSKD', 'Connectix', 'desktop', 'video call received', 7),
(72, '2020-02-23', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(73, '2020-02-18', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(74, '2020-02-24', '9763-GRSKD', 'Zoomit', 'desktop', 'file received', 2),
(75, '2020-04-03', '9763-GRSKD', 'Connectix', 'desktop', 'message received', 4),
(76, '2020-02-29', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(77, '2020-04-11', '9763-GRSKD', 'Zoomit', 'desktop', 'message sent', 3),
(78, '2020-04-13', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(79, '2020-02-15', '9763-GRSKD', 'Connectix', 'desktop', 'message received', 4),
(80, '2020-02-03', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(81, '2020-04-06', '9763-GRSKD', 'Connectix', 'desktop', 'message received', 4),
(82, '2020-02-25', '9763-GRSKD', 'Connectix', 'mobile', 'message sent', 3),
(83, '2020-02-16', '9763-GRSKD', 'Zoomit', 'desktop', 'message received', 4),
(84, '2020-02-27', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(85, '2020-04-05', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(86, '2020-02-01', '9763-GRSKD', 'Zoomit', 'desktop', 'message received', 4),
(87, '2020-02-07', '9763-GRSKD', 'Connectix', 'desktop', 'message sent', 3),
(88, '2020-03-22', '9763-GRSKD', 'Connectix', 'desktop', 'file received', 2),
(89, '2020-04-04', '9763-GRSKD', 'Zoomit', 'mobile', 'file received', 2),
(90, '2020-04-01', '9959-WOFKT', 'Connectix', 'mobile', 'video call started', 6),
(91, '2020-03-26', '7795-CFOCW', 'Sendit', 'desktop', 'file received', 2),
(92, '2020-04-08', '7795-CFOCW', 'Zoomit', 'mobile', 'message received', 4),
(93, '2020-03-28', '9305-CDSKC', 'Connectix', 'desktop', 'file sent', 1),
(94, '2020-03-06', '6713-OKOMC', 'Connectix', 'desktop', 'file received', 2),
(95, '2020-02-23', '9305-CDSKC', 'Sendit', 'desktop', 'message sent', 3),
(96, '2020-03-19', '5575-GNVDE', 'Sendit', 'desktop', 'voice call received', 9),
(97, '2020-03-28', '3668-QPYBK', 'eShop', 'desktop', 'message received', 4),
(98, '2020-03-22', '8091-TTVAX', 'Connectix', 'mobile', 'voice call received', 9),
(99, '2020-02-09', '3655-SNQYZ', 'Connectix', 'desktop', 'file received', 2),
(100, '2020-03-18', '6388-TABGU', 'Sendit', 'desktop', 'message received', 4),
(101, '2020-03-27', '4183-MYFRB', 'Connectix', 'desktop', 'voice call received', 9),
(102, '2020-04-03', '5129-JLPIS', 'Connectix', 'desktop', 'file received', 2),
(103, '2020-03-01', '0280-XJGEX', 'Connectix', 'desktop', 'video call started', 6),
(104, '2020-04-16', '9763-GRSKD', 'Connectix', 'desktop', 'message sent', 3),
(105, '2020-03-07', '6388-TABGU', 'Connectix', 'desktop', 'api message received', 5),
(106, '2020-03-20', '9305-CDSKC', 'Zoomit', 'mobile', 'message sent', 3),
(107, '2020-03-10', '8091-TTVAX', 'Sendit', 'desktop', 'video call started', 6),
(108, '2020-03-20', '0280-XJGEX', 'Zoomit', 'mobile', 'message sent', 3),
(109, '2020-02-23', '5129-JLPIS', 'Connectix', 'mobile', 'file received', 2),
(110, '2020-02-18', '7590-VHVEG', 'Connectix', 'mobile', 'file sent', 1),
(111, '2020-02-18', '1452-KIOVK', 'Connectix', 'mobile', 'file received', 2),
(112, '2020-02-08', '3668-QPYBK', 'Sendit', 'desktop', 'message received', 4),
(113, '2020-04-13', '7469-LKBCI', 'Sendit', 'desktop', 'video call received', 7),
(114, '2020-03-22', '6388-TABGU', 'eShop', 'mobile', 'file sent', 1),
(115, '2020-03-13', '0280-XJGEX', 'Sendit', 'desktop', 'message sent', 3),
(116, '2020-03-07', '6388-TABGU', 'Connectix', 'desktop', 'voice call received', 9),
(117, '2020-03-21', '8091-TTVAX', 'Connectix', 'mobile', 'message sent', 3),
(118, '2020-04-03', '8191-XWSZG', 'Connectix', 'desktop', 'file received', 2),
(119, '2020-02-22', '7795-CFOCW', 'Connectix', 'desktop', 'message received', 4),
(120, '2020-02-14', '7590-VHVEG', 'Connectix', 'desktop', 'message received', 4),
(121, '2020-03-09', '5575-GNVDE', 'Connectix', 'mobile', 'file sent', 1),
(122, '2020-03-22', '8091-TTVAX', 'Connectix', 'mobile', 'video call received', 7),
(123, '2020-03-02', '7469-LKBCI', 'Connectix', 'mobile', 'video call started', 6),
(124, '2020-03-23', '5575-GNVDE', 'Connectix', 'mobile', 'voice call received', 9),
(125, '2020-03-30', '9305-CDSKC', 'eShop', 'desktop', 'message sent', 3),
(126, '2020-03-25', '4190-MFLUW', 'Connectix', 'desktop', 'video call started', 6),
(127, '2020-03-09', '7590-VHVEG', 'Connectix', 'mobile', 'api message received', 5),
(128, '2020-03-14', '7795-CFOCW', 'Sendit', 'desktop', 'file received', 2),
(129, '2020-04-04', '9959-WOFKT', 'Connectix', 'mobile', 'message received', 4),
(130, '2020-03-31', '5129-JLPIS', 'Connectix', 'desktop', 'video call received', 7),
(131, '2020-03-27', '4183-MYFRB', 'Connectix', 'desktop', 'voice call received', 9),
(132, '2020-04-03', '5129-JLPIS', 'Connectix', 'desktop', 'file received', 2),
(133, '2020-03-01', '0280-XJGEX', 'Connectix', 'desktop', 'video call started', 6),
(134, '2020-04-16', '9763-GRSKD', 'Connectix', 'desktop', 'message sent', 3),
(135, '2020-03-07', '6388-TABGU', 'Connectix', 'desktop', 'api message received', 5),
(136, '2020-03-20', '9305-CDSKC', 'Zoomit', 'mobile', 'message sent', 3),
(137, '2020-03-10', '8091-TTVAX', 'Sendit', 'desktop', 'video call started', 6),
(138, '2020-03-20', '0280-XJGEX', 'Zoomit', 'mobile', 'message sent', 3),
(139, '2020-02-23', '5129-JLPIS', 'Connectix', 'mobile', 'file received', 2),
(140, '2020-02-18', '7590-VHVEG', 'Connectix', 'mobile', 'file sent', 1),
(141, '2020-02-18', '1452-KIOVK', 'Connectix', 'mobile', 'file received', 2),
(142, '2020-02-08', '3668-QPYBK', 'Sendit', 'desktop', 'message received', 4),
(143, '2020-04-13', '7469-LKBCI', 'Sendit', 'desktop', 'video call received', 7),
(144, '2020-03-22', '6388-TABGU', 'eShop', 'mobile', 'file sent', 1),
(145, '2020-03-13', '0280-XJGEX', 'Sendit', 'desktop', 'message sent', 3),
(146, '2020-03-07', '6388-TABGU', 'Connectix', 'desktop', 'voice call received', 9),
(147, '2020-03-21', '8091-TTVAX', 'Connectix', 'mobile', 'message sent', 3),
(148, '2020-04-03', '8191-XWSZG', 'Connectix', 'desktop', 'file received', 2),
(149, '2020-02-22', '7795-CFOCW', 'Connectix', 'desktop', 'message received', 4),
(150, '2020-02-14', '7590-VHVEG', 'Connectix', 'desktop', 'message received', 4);


```

| id   | time_id    | user_id    | customer_id      | client_id | event_type           | event_id |
| ---- | ---------- | ---------- | ---------------- | --------- | -------------------- | -------- |
| 1    | 2020-02-28 | 3668-QPYBK | Sendit           | desktop   | message sent         | 3        |
| 2    | 2020-02-28 | 7892-POOKP | Connectix        | mobile    | file received        | 2        |
| 3    | 2020-04-03 | 9763-GRSKD | Zoomit           | desktop   | video call received  | 7        |
| 4    | 2020-04-02 | 9763-GRSKD | Connectix        | desktop   | video call received  | 7        |
| 5    | 2020-02-06 | 9237-HQITU | Sendit           | desktop   | video call received  | 7        |
| 6    | 2020-02-27 | 8191-XWSZG | Connectix        | desktop   | file received        | 2        |
| 7    | 2020-04-03 | 9237-HQITU | Connectix        | desktop   | video call received  | 7        |
| 8    | 2020-03-01 | 9237-HQITU | Connectix        | mobile    | message received     | 4        |
| 9    | 2020-04-02 | 4190-MFLUW | Connectix        | mobile    | video call received  | 7        |
| 10   | 2020-04-21 | 9763-GRSKD | Sendit           | desktop   | file received        | 2        |



```sql
SELECT client_id,
       EXTRACT(month from time_id) as month,
       count(DISTINCT user_id) as users_num
FROM fact_events
GROUP BY 1,2


SELECT client_id,
       EXTRACT(month from time_id) as month,
       count(DISTINCT user_id) as users_num,
       FIRST_VALUE(count(DISTINCT user_id)) OVER(
ORDER BY client_id, EXTRACT(month from time_id))
FROM fact_events
GROUP BY 1,2

SELECT client_id,
       EXTRACT(month from time_id) as month,
       count(DISTINCT user_id) as users_num,
       FIRST_VALUE(count(DISTINCT user_id)) OVER(
            PARTITION BY client_id 
            ORDER BY EXTRACT(month from time_id))
FROM fact_events
GROUP BY 1,2

SELECT client_id,
       EXTRACT(month from time_id) as month,
       count(DISTINCT user_id) as users_num,
       LAST_VALUE(count(DISTINCT user_id)) OVER(
            PARTITION BY client_id)
FROM fact_events
GROUP BY 1,2


SELECT client_id,
       EXTRACT(month from time_id) as month,
       count(DISTINCT user_id) as users_num,
       NTH_VALUE(count(DISTINCT user_id), 2) OVER(
            PARTITION BY client_id)
FROM fact_events
GROUP BY 1,2


```



#### Amazon_Purchases

> Find the 3-month rolling average of total revenue from purchases given a table with users, their purchase amount, and date purchased. Do not include returns which are represented by negative purchase values. Output the year-month (YYYY-MM) and 3-month rolling average of revenue, sorted from earliest month to latest month.
>
> 
>
> A 3-month rolling average is defined by calculating the average total revenue from all user purchases for the current month and previous two months. The first two months will not be a true 3-month rolling average since we are not given data from last year. Assume each month has at least one purchase.

Amazon_Purchases

| user_id | created_at | purchase_amt |
| ------- | ---------- | ------------ |
| 10      | 2020-01-01 | 3742         |
| 11      | 2020-01-04 | 1290         |
| 12      | 2020-01-07 | 4249         |
| 13      | 2020-01-10 | 4899         |
| 14      | 2020-01-13 | -4656        |
| 15      | 2020-01-16 | -655         |
| 16      | 2020-01-19 | 4659         |
| 17      | 2020-01-22 | 3813         |
| 18      | 2020-01-25 | -2623        |
| 19      | 2020-01-28 | 3640         |
| 20      | 2020-01-31 | -1028        |
| 21      | 2020-02-03 | 2715         |
| 22      | 2020-02-06 | 1592         |
| 23      | 2020-02-09 | 1516         |
| 24      | 2020-02-12 | 2700         |
| 25      | 2020-02-15 | 1543         |
| 26      | 2020-02-18 | 4210         |
| 27      | 2020-02-21 | -608         |
| 28      | 2020-02-24 | 2855         |
| 29      | 2020-02-27 | 3564         |
| 30      | 2020-03-01 | 3037         |
| 31      | 2020-03-04 | 2552         |
| 32      | 2020-03-07 | 2487         |
| 33      | 2020-03-10 | -1933        |
| 34      | 2020-03-13 | 4973         |
| 35      | 2020-03-16 | 4475         |
| 36      | 2020-03-19 | -913         |
| 37      | 2020-03-22 | 2265         |
| 38      | 2020-03-25 | 3525         |
| 39      | 2020-03-28 | 3251         |
| 40      | 2020-03-31 | 3055         |
| 41      | 2020-04-03 | 4828         |
| 42      | 2020-04-06 | -3230        |
| 43      | 2020-04-09 | 4772         |
| 44      | 2020-04-12 | -775         |
| 45      | 2020-04-15 | 2051         |
| 46      | 2020-04-18 | 1974         |
| 47      | 2020-04-21 | 2311         |
| 48      | 2020-04-24 | -593         |
| 49      | 2020-04-27 | 2583         |
| 50      | 2020-04-30 | 3414         |
| 51      | 2020-05-03 | 4216         |
| 52      | 2020-05-06 | 2420         |
| 53      | 2020-05-09 | 3138         |
| 54      | 2020-05-12 | 1036         |
| 55      | 2020-05-15 | 2543         |
| 56      | 2020-05-18 | 2127         |
| 57      | 2020-05-21 | 1026         |
| 58      | 2020-05-24 | 1650         |
| 59      | 2020-05-27 | 3514         |
| 60      | 2020-05-30 | 3030         |
| 61      | 2020-06-02 | 4014         |
| 62      | 2020-06-05 | 4390         |
| 63      | 2020-06-08 | 4459         |
| 64      | 2020-06-11 | -2850        |
| 65      | 2020-06-14 | 4369         |
| 66      | 2020-06-17 | 1895         |
| 67      | 2020-06-20 | 2184         |
| 68      | 2020-06-23 | -765         |
| 69      | 2020-06-26 | 2001         |
| 70      | 2020-06-29 | 4375         |
| 71      | 2020-07-02 | 4104         |
| 72      | 2020-07-05 | 4223         |
| 73      | 2020-07-08 | 633          |
| 74      | 2020-07-11 | 3352         |
| 75      | 2020-07-14 | 4421         |
| 76      | 2020-07-17 | -4284        |
| 77      | 2020-07-20 | 1904         |
| 78      | 2020-07-23 | 4928         |
| 79      | 2020-07-26 | -1680        |
| 80      | 2020-07-29 | 1744         |
| 81      | 2020-08-01 | 3797         |
| 82      | 2020-08-04 | 4053         |
| 83      | 2020-08-07 | -1829        |
| 84      | 2020-08-10 | 2196         |
| 85      | 2020-08-13 | 1792         |
| 86      | 2020-08-16 | 4050         |
| 87      | 2020-08-19 | 1468         |
| 88      | 2020-08-22 | 2191         |
| 89      | 2020-08-25 | -594         |
| 90      | 2020-08-28 | 2318         |
| 91      | 2020-08-31 | 1631         |
| 92      | 2020-09-03 | 3804         |
| 93      | 2020-09-06 | -2032        |
| 94      | 2020-09-09 | 3599         |
| 95      | 2020-09-12 | 3043         |
| 96      | 2020-09-15 | 1999         |
| 97      | 2020-09-18 | -1334        |
| 98      | 2020-09-21 | 4344         |
| 99      | 2020-09-24 | -3960        |
| 100     | 2020-09-27 | 4316         |
| 101     | 2020-09-30 | 3722         |
| 102     | 2020-10-03 | 1433         |
| 103     | 2020-10-06 | -1045        |
| 104     | 2020-10-09 | 3035         |
| 105     | 2020-10-12 | 4865         |
| 106     | 2020-10-15 | -3330        |
| 107     | 2020-10-18 | 4228         |
| 108     | 2020-10-21 | -1834        |
| 109     | 2020-10-24 | 1749         |

```sql
-- SQL Create Table Statement
CREATE TABLE Amazon_Purchases (
    user_id INT,
    created_at DATE,
    purchase_amt INT
);

-- SQL Insert Statements
INSERT INTO Amazon_Purchases (user_id, created_at, purchase_amt) VALUES
(10, '2020-01-01', 3742),
(11, '2020-01-04', 1290),
(12, '2020-01-07', 4249),
(13, '2020-01-10', 4899),
(14, '2020-01-13', -4656),
(15, '2020-01-16', -655),
(16, '2020-01-19', 4659),
(17, '2020-01-22', 3813),
(18, '2020-01-25', -2623),
(19, '2020-01-28', 3640),
(20, '2020-01-31', -1028),
(21, '2020-02-03', 2715),
(22, '2020-02-06', 1592),
(23, '2020-02-09', 1516),
(24, '2020-02-12', 2700),
(25, '2020-02-15', 1543),
(26, '2020-02-18', 4210),
(27, '2020-02-21', -608),
(28, '2020-02-24', 2855),
(29, '2020-02-27', 3564),
(30, '2020-03-01', 3037),
(108, '2020-04-21', -1834),
(109, '2020-04-24', 1749);



```



```sql
SELECT to_char(created_at::date, 'YYYY-MM') AS MONTH,
          sum(purchase_amt) AS monthly_revenue
FROM amazon_purchases
WHERE purchase_amt>0
GROUP BY to_char(created_at::date, 'YYYY-MM')
ORDER BY to_char(created_at::date, 'YYYY-MM')

SELECT t.month,
       AVG(t.monthly_revenue) OVER(
                                   ORDER BY t.month ROWS BETWEEN 2 PRECEDING
                                   AND CURRENT ROW) AS avg_revenue
FROM
  (SELECT to_char(created_at::date, 'YYYY-MM') AS MONTH,
          sum(purchase_amt) AS monthly_revenue
   FROM amazon_purchases
   WHERE purchase_amt>0
   GROUP BY to_char(created_at::date, 'YYYY-MM')
   ORDER BY to_char(created_at::date, 'YYYY-MM')) t;
   


SELECT t.month,
       monthly_revenue,
       AVG(t.monthly_revenue) OVER(
                                   ORDER BY t.month ROWS BETWEEN 1 PRECEDING 
                                   AND 1 FOLLOWING EXCLUDE CURRENT ROW) 
                                   AS avg_revenue
FROM
  (SELECT to_char(created_at::date, 'YYYY-MM') AS MONTH,
          sum(purchase_amt) AS monthly_revenue
   FROM amazon_purchases
   WHERE purchase_amt>0
   GROUP BY to_char(created_at::date, 'YYYY-MM')
   ORDER BY to_char(created_at::date, 'YYYY-MM')) t
   
   
   
   
   SELECT t.month,
       monthly_revenue,
       AVG(t.monthly_revenue) FILTER(WHERE monthly_revenue > 20000) 
OVER(ORDER BY t.month ROWS BETWEEN 1 PRECEDING AND 1 
FOLLOWING EXCLUDE CURRENT ROW) AS avg_revenue
FROM
  (SELECT to_char(created_at::date, 'YYYY-MM') AS MONTH,
          sum(purchase_amt) AS monthly_revenue
   FROM amazon_purchases
   WHERE purchase_amt>0
   GROUP BY to_char(created_at::date, 'YYYY-MM')
   ORDER BY to_char(created_at::date, 'YYYY-MM')) t
```



#### Restaurant Health Violations

> Determine the change in the number of daily violations by calculating the difference between the count of current and previous violations by inspection date. Output the inspection date and the change in the number of daily violations. Order your results by the earliest inspection date first.

Table: sf_restaurant_health_violations




| business_id | business_name                    | inspection_date | violation_id             |
|-------------|----------------------------------|------------------|--------------------------|
| 5800        | John Chin Elementary School      | 2017-10-17       | 5800_20171017_103149    |
| 64236       | Sutter Pub and Restaurant        | 2017-07-25       | 64236_20170725_103133   |
| 1991        | SRI THAI CUISINE                 | 2017-11-29       | 1991_20171129_103139    |
| 3816        | Washington Bakery & Restaurant    | 2016-07-28       | 3816_20160728_103108    |
| 39119       | Brothers Restaurant              | 2016-07-18       | 39119_20160718_103133   |
| 6643        | T & L FOOD MARKET                | 2016-06-09       | 6643_20160609_103102    |
| 79974       | Antonelli Brothers Meat, Fish... | 2016-10-17       | 79974_20161017_103161   |
| 1939        | STARBUCKS COFFEE CO. #603        | 2016-12-14       | 1939_20161214_103154   |
| 68872       | Jiang Ling Cuisine Restaurant    | 2017-12-12       | 68872_20171212_103105   |
| 80242       | Wing Lee BBQ Restaurant          | 2016-05-09       | 80242_20160509_103149   |


```sql
CREATE TABLE sf_restaurant_health_violations (
    business_id INT,
    business_name VARCHAR(255),
    inspection_date DATE,
    violation_id VARCHAR(255)
);

-- Sample data for 40 rows
INSERT INTO sf_restaurant_health_violations (business_id, business_name, inspection_date, violation_id)
VALUES
(5800, 'John Chin Elementary School', '2017-10-17', '5800_20171017_103149'),
(64236, 'Sutter Pub and Restaurant', '2017-07-25', '64236_20170725_103133'),
(1991, 'SRI THAI CUISINE', '2017-11-29', '1991_20171129_103139'),
(3816, 'Washington Bakery & Restaurant', '2016-07-28', '3816_20160728_103108'),
(39119, 'Brothers Restaurant', '2016-07-18', '39119_20160718_103133'),
(6643, 'T & L FOOD MARKET', '2016-06-09', '6643_20160609_103102'),
(79974, 'Antonelli Brothers Meat, Fish, and Poultry Inc.', '2016-10-17', '79974_20161017_103161'),
(1939, 'STARBUCKS COFFEE CO. #603', '2016-12-14', '1939_20161214_103154'),
(68872, 'Jiang Ling Cuisine Restaurant', '2017-12-12', '68872_20171212_103105'),
(80242, 'Wing Lee BBQ Restaurant', '2016-05-09', '80242_20160509_103149'),
(76218, 'Tenderloin Market & Deli', '2017-03-13', NULL),
(89686, 'Big Fish Little Fish Poke', '2018-02-27', '89686_20180227_103120'),
(75448, 'Laguna Café', '2018-07-11', '75448_20180711_103119'),
(87447, 'The Castro Republic', '2017-08-30', '87447_20170830_103135'),
(7747, 'SAFEWAY STORE #964', '2016-06-24', NULL),
(79414, 'Home Plate', '2016-10-17', '79414_20161017_103103'),
(509, 'Cafe Bakery', '2016-03-28', NULL),
(5862, 'MARTIN L. KING MIDDLE SCHOOL', '2015-09-23', NULL),
(1204, 'ROYAL GROUND COFFEE', '2017-12-22', NULL),
(71131, 'Rico Pan', '2016-10-05', '71131_20161005_103154'),
(87620, 'Dolores Park Outpost', '2017-10-06', NULL),
(61861, 'SO', '2017-12-14', '61861_20171214_103105'),
(4421, 'Crepe Cafe', '2018-03-26', '4421_20180326_103144'),
(80591, 'L & G Vietnamese Sandwich', '2017-10-24', '80591_20171024_103154'),
(86990, 'Allstars Cafe Inc', '2017-08-29', '86990_20170829_103119'),
(74866, 'Tacolicious', '2017-05-08', '74866_20170508_103144'),
(86780, 'Peet Coffee & Tea', '2017-03-27', '86780_20170327_103119'),
(79196, 'Veraci Pizza', '2017-02-23', '79196_20170223_103124'),
(81680, 'Sharetea', '2016-03-31', '81680_20160331_103120'),
(63210, 'Lets Be Frank', '2016-05-13', '63210_20160513_103116'),
(1031, 'IL BORGO', '2018-03-28', '1031_20180328_103131'),
(85824, 'Boss Supermarket', '2017-10-03', '85824_20171003_103124'),
(78965, 'Dragoneats', '2017-07-12', NULL);


-- Add 30 more INSERT statements for sample data
-- ...



```



```sql
SELECT inspection_date::DATE,
       COUNT(violation_id)
FROM sf_restaurant_health_violations
GROUP BY 1

SELECT inspection_date::DATE,
       COUNT(violation_id),
       LAG(COUNT(violation_id)) OVER(ORDER BY inspection_date::DATE)
FROM sf_restaurant_health_violations
GROUP BY 1

SELECT inspection_date::DATE,
       COUNT(violation_id) - LAG(COUNT(violation_id)) OVER(
                                     ORDER BY inspection_date::DATE) 
     						diff
FROM sf_restaurant_health_violations
GROUP BY 1;

SELECT inspection_date::DATE,
       COUNT(violation_id),
       LEAD(COUNT(violation_id)) OVER(
                                     ORDER BY inspection_date::DATE),
       COUNT(violation_id) - LEAD(COUNT(violation_id)) OVER(
                                     ORDER BY inspection_date::DATE) 
     						diff
FROM sf_restaurant_health_violations
GROUP BY 1


```
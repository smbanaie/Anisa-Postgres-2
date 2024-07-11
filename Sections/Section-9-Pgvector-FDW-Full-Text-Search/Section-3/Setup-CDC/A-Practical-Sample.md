## Sample CDC Workflow using Postgres/Kafka/Debezium

#### Prerequisites:



- Ensure you have Docker and docker-compose installed on your system. If not, please follow the official [Docker](https://docs.docker.com/) installation guide for your operating system.

### Step 1: Run The Docker-Compose

- run docker compose 
- checkout the :
  - Kafka UI : http://localhost:8095/
  - Kafka Connect UI : http://localhost:8085/

### Step 2 : Create a  PostgreSQL Kafka Connect Entry 

run this in `WSL` :

```bash
$ curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{
  "name": "shopping-db-postgreSQL",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "connector.displayName": "PostgreSQL-ShoppingDB",
    "topic.prefix": "shopping_cdc",
    "database.user": "postgres",
    "database.dbname": "shopping",
    "decimal.handling.mode": "string",
    "database.hostname": "postgres-main",
    "database.password": "postgres123",
    "name": "shopping-db-postgreSQL",
    "schema.include.list": "public",
    "connector.id": "shopping_postgres",
    "plugin.name": "pgoutput",
    "table.include.list": "public.*",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "snapshot.mode": "initial",
    "tombstones.on.delete": "false",
    "time.precision.mode": "connect",
    "transforms": "flatten,convertTimestamp",
    "transforms.flatten.type": "org.apache.kafka.connect.transforms.Flatten$Value",
    "transforms.flatten.delimiter": ".",
    "transforms.convertTimestamp.type": "org.apache.kafka.connect.transforms.TimestampConverter$Value",
    "transforms.convertTimestamp.field": "order_date",
    "transforms.convertTimestamp.target.type": "Timestamp",
    "transforms.convertTimestamp.format": "yyyy-MM-dd HH:mm:ss"
  }
}'


```



- check it in the Debezium UI
- check out the Kafka message  flow
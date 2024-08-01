# Monitoring PostgreSQL with Grafana and Prometheus

## Introduction

This tutorial will guide you through setting up a monitoring system for PostgreSQL using Grafana and Prometheus. This setup is particularly useful for developers and database administrators who want to gain insights into their PostgreSQL database's performance and health.

### What is Grafana?

Grafana is an open-source analytics and interactive visualization web application. It allows you to query, visualize, alert on, and understand your metrics no matter where they are stored. In this setup, we'll use Grafana to create dashboards that display PostgreSQL metrics.

### What is Prometheus?

Prometheus is an open-source systems monitoring and alerting toolkit. It collects and stores its metrics as time series data, i.e., metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels.

## Steps

### 1. Setup Docker Compose

Create a `docker-compose.yml` file with the following content:

```yaml
version: "3.9"
services:
  grafana:
    image: grafana/grafana
    ports:
      - 3000:3000
    volumes:
      - grafana-storage:/var/lib/grafana
    networks:
      - services

  prometheus:
    image: prom/prometheus
    ports:
      - 9090:9090
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-storage:/prometheus
    networks:
      - services

  postgres:
    container_name: postgres
    hostname: postgres
    image: postgres:${PG_VERSION:-16}
    volumes:
      - ./db_data:/var/lib/postgresql/data
      - ./shopping_ddl.sql:/docker-entrypoint-initdb.d/shopping_ddl.sql
    environment:
      - POSTGRES_PASSWORD=${DB_PASS:-postgres123}
      - POSTGRES_USER=${DB_USER:-postgres}
      - POSTGRES_DB=${DB_NAME:-shopping}
      - POSTGRES_HOST_AUTH_METHOD=trust
    networks:
      - services
    restart: on-failure:10
    ports:
      - 5434:5432

  postgres-exporter:
    image: prometheuscommunity/postgres-exporter
    ports:
      - 9187:9187
    environment:
      DATA_SOURCE_NAME: "postgresql://${DB_USER:-postgres}:${DB_PASS:-postgres123}@postgres:5432/${DB_NAME:-dblab}?sslmode=disable"
    depends_on:
      - postgres
      - prometheus
    networks:
      - services

networks:
  services:
    name: ${APP_NAME:-anisa}_network

volumes:
  grafana-storage:
  prometheus-storage:
```

This Docker Compose file sets up four services:
- Grafana for visualization
- Prometheus for metrics collection
- PostgreSQL as our database
- postgres-exporter to expose PostgreSQL metrics to Prometheus

Note the addition of named volumes for Grafana and Prometheus to persist data across container restarts.

### 2. Configure Prometheus

Create a `prometheus.yml` file in the same directory as your `docker-compose.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]
  - job_name: postgres-exporter
    static_configs:
      - targets: ["postgres-exporter:9187"]
```

This configuration tells Prometheus to scrape metrics from itself and the postgres-exporter every 15 seconds.

### 3. Start the Services

Run the following command to start all services:

```bash
docker-compose up -d
```

The `-d` flag runs the containers in detached mode.

### 4. Verify Prometheus Targets

Open a web browser and navigate to:

```
http://localhost:9090/targets
```

You should see two targets: Prometheus itself and the postgres-exporter. Ensure both are in the "UP" state.

### 5. Configure Grafana

1. Open Grafana in your web browser:

```
http://localhost:3000
```

2. Log in with the default credentials:
   - Username: admin
   - Password: admin

3. You'll be prompted to change the password on first login.

4. Add Prometheus as a data source:
   - Click on the gear icon (⚙️) in the left sidebar to open the Configuration menu
   - Select "Data Sources"
   - Click "Add data source"
   - Choose "Prometheus"
   - Set the URL to `http://prometheus:9090`
   - Click "Save & Test"

### 6. Import PostgreSQL Dashboard

Grafana has pre-built dashboards available for various data sources. Let's import one for PostgreSQL:

1. Click the "+" icon in the left sidebar and select "Import"
2. Enter dashboard ID 9628 (a popular PostgreSQL dashboard)
3. Select your Prometheus data source in the dropdown
4. Click "Import"

You should now see a dashboard with various PostgreSQL metrics.

### 7. Explore and Customize

Spend some time exploring the dashboard. You can:
- Adjust time ranges
- Zoom in on specific graphs
- Add new panels or modify existing ones

### 8. (Optional) Set Up Alerting

Grafana allows you to set up alerts based on your metrics:

1. Go to a graph you want to create an alert for
2. Click on the graph title and select "Edit"
3. Go to the "Alert" tab
4. Click "Create Alert"
5. Define your alert conditions and notification channels

## Conclusion

You now have a fully functional PostgreSQL monitoring setup using Grafana and Prometheus. This system allows you to visualize your database's performance, set up alerts, and gain valuable insights into your PostgreSQL instance.

Remember to secure your setup if you plan to use it in a production environment. This might include setting up proper authentication, using HTTPS, and restricting network access.
# Realtime Clickstream Analytics Pipeline

This project demonstrates a complete real-time data engineering pipeline using only open-source and fully free tools. It simulates user clickstream events, ingests them via Kafka, processes them with Spark Structured Streaming, stores them in PostgreSQL, and supports downstream analytics and visualization.

---

## 🧱 Architecture

---

## ⚙️ Tech Stack

| Layer         | Tool/Service                     |
|---------------|----------------------------------|
| Data Source   | Python script simulating events |
| Messaging     | Apache Kafka + Zookeeper (Docker) |
| Stream Processor | Apache Spark (PySpark)       |
| Storage       | PostgreSQL (Docker)              |
| Orchestration | Manual / Optional: Apache Airflow |
| Analytics     | SQL, dbt (optional), Streamlit   |

---

## 💡 Key Features

- Simulates live user behavior (click, scroll, purchase)
- Ingests real-time data using Kafka
- Processes data with Spark Structured Streaming
- Writes micro-batches to PostgreSQL using `foreachBatch`
- Schema-first modeling and real-time querying
- Fully local and free — ideal for learning or showcasing data engineering skills

---

## 📂 Project Structure

```bash
realtime-analytics-pipeline/
│
├── simulation/               # Simulated event generator (Python)
│   └── event_producer.py
│
├── streaming/                # PySpark consumer + processor
│   └── process_stream.py
│
├── dashboard/                # Streamlit app for real-time viz (optional)
│   └── app.py
│
├── warehouse/                # dbt project for modeling (optional)
│
├── configs/                  # Environment/sample config
│
├── docker-compose.yml        # Kafka, Zookeeper, PostgreSQL
├── requirements.txt          # Python dependencies
├── README.md                 # This file
```
---
## 🚀 Getting Started
```bash
docker-compose up -d
```
```bash
python simulation/event_producer.py
```
```bash
spark-submit streaming/process_stream.py
```
```bash
docker exec -it realtime-analytics-pipeline-postgres-1 psql -U analytics -d analytics
```

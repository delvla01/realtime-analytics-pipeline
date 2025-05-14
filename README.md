# realtime-analytics-pipeline
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

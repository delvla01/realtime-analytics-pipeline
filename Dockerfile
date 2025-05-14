FROM apache/airflow:2.7.2-python3.10

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /opt/airflow/realtime-analytics-pipeline

# Set working directory
WORKDIR /opt/airflow
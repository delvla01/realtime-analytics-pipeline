from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, LongType, DoubleType
import time
import sys

# Define schema of incoming JSON
schema = StructType() \
    .add("user_id", LongType()) \
    .add("event_type", StringType()) \
    .add("timestamp", DoubleType())

# Create Spark session
spark = SparkSession.builder \
    .appName("ClickstreamProcessor") \
    .getOrCreate()

# Read stream from Kafka topic
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "clickstream") \
    .load()

# Parse JSON from Kafka value
parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Function to write each batch to PostgreSQL
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/analytics") \
        .option("dbtable", "clickstream_events") \
        .option("user", "") \
        .option("password", "") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    print(f"Batch {batch_id}: Wrote {batch_df.count()} records to PostgreSQL")

# Get timeout from command-line arguments (default: run indefinitely)
timeout_seconds = float('inf')  # Default: run indefinitely
if len(sys.argv) > 1:
    timeout_seconds = int(sys.argv[1])
    print(f"Stream will timeout after {timeout_seconds} seconds")

# Start the streaming query
query = parsed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

# Run for specified time or until termination
start_time = time.time()
try:
    if timeout_seconds < float('inf'):
        # Run for specified duration
        while time.time() - start_time < timeout_seconds and query.isActive:
            time.sleep(1)
        if query.isActive:
            print(f"Stopping stream after {timeout_seconds} seconds")
            query.stop()
    else:
        # Run indefinitely
        query.awaitTermination()
finally:
    if query.isActive:
        query.stop()
    print("Streaming job completed")
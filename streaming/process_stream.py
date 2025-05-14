from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, LongType, DoubleType

# Define schema of incoming JSON
schema = StructType() \
    .add("user_id", LongType()) \
    .add("event_type", StringType()) \
    .add("timestamp", DoubleType())

# Create Spark session with Kafka + JDBC support
spark = SparkSession.builder \
    .appName("ClickstreamProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.postgresql:postgresql:42.2.18") \
    .getOrCreate()

# Read stream from Kafka topic
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
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
        .option("url", "jdbc:postgresql://localhost:5432/analytics") \
        .option("dbtable", "clickstream_events") \
        .option("user", "analytics") \
        .option("password", "password") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# Stream: Process each micro-batch with the function above
query = parsed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

query.awaitTermination()
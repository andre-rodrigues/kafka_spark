import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 pyspark-shell'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME", "waia-events")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "localhost:9092")

if __name__ == "__main__":
    # Setup a new spark session.
    # Here we say what's the name of our application and how spark
    # should distribute the processing.
    spark = SparkSession.builder.appName("Real time average score") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Read data from the Kafka topic
    sampleDataframe = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
            .option("subscribe", KAFKA_TOPIC_NAME)
            .option("startingOffsets", "earliest")
            .load()
        )

    # Use Spark to parse the data from the Kafka topic and
    # calculate the average per name score every 10 seconds.
    base_df = sampleDataframe.selectExpr(
            "SPLIT_PART(CAST(value as STRING), ':', 1) AS name",
            "SPLIT_PART(CAST(value as STRING), ':', 2) AS score",
            "timestamp"
        ) \
        .withWatermark("timestamp", "1 minute") \
        .groupBy(col("name"), window(col("timestamp"), "10 minutes", "5 minutes")) \
        .agg(avg("score").alias("avg_score"))

    # Write the results to CSV files every 10 seconds.
    base_df.selectExpr("name", "avg_score", "window.start", "window.end") \
      .writeStream \
      .format("csv") \
      .trigger(processingTime="1 minute") \
      .option("header", True) \
      .option("delimiter", "\t") \
      .option("checkpointLocation", "checkpoint/") \
      .option("path", f"./avg-scores/") \
      .outputMode("append") \
      .start() \
      .awaitTermination()

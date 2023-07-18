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
    spark = (
        SparkSession.builder.appName("Kafka Pyspark Streaming Learning")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("INFO")

    # Read data from the Kafka topic.
    sampleDataframe = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
            .option("subscribe", KAFKA_TOPIC_NAME)
            .option("startingOffsets", "earliest")
            .load()
        )

    # Parse the content of the Kafka topic and split into separated columns.
    base_df = sampleDataframe.selectExpr(
        "SPLIT_PART(CAST(value as STRING), ':', 1) AS name",
        "SPLIT_PART(CAST(value as STRING), ':', 2) AS score",
        "timestamp"
    )

    # Write the results into CSV files.
    base_df.writeStream \
      .format("csv") \
      .trigger(processingTime="10 seconds") \
      .option("header", True) \
      .option("checkpointLocation", "checkpoint/") \
      .option("path", f"./{KAFKA_TOPIC_NAME}/") \
      .outputMode("append") \
      .start() \
      .awaitTermination()

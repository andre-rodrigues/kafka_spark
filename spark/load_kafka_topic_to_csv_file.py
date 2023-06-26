import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 pyspark-shell'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME", "quickstart-events")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "3.72.246.226:9092")

if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("Kafka Pyspark Streaming Learning")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("INFO")
    sampleDataframe = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
            .option("subscribe", KAFKA_TOPIC_NAME)
            .option("startingOffsets", "earliest")
            .load()
        )

    base_df = sampleDataframe.selectExpr("CAST(value as STRING)", "timestamp")
    base_df.writeStream \
      .format("csv") \
      .trigger(processingTime="10 seconds") \
      .option("checkpointLocation", "checkpoint/") \
      .option("path", f"./{KAFKA_TOPIC_NAME}/") \
      .outputMode("append") \
      .start() \
      .awaitTermination()

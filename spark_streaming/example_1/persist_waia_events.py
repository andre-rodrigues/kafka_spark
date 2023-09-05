import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.postgresql:postgresql:42.5.4 pyspark-shell'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME", "waia-events")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")

if __name__ == "__main__":
    # Setup a new spark session.
    # Here we say what's the name of our application and how spark
    # should distribute the processing.
    spark = SparkSession.builder.appName("Kafka Pyspark Streaming Learning") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

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

    # Option 1: Write to console
    # base_df.writeStream \
    #     .outputMode("complete") \
    #     .format("console") \
    #     .outputMode("append") \
    #     .start() \
    #     .awaitTermination()

    # Option 2: Write to CSV files
    # base_df.writeStream \
    #   .format("csv") \
    #   .trigger(processingTime="10 seconds") \
    #   .option("header", True) \
    #   .option("delimiter", "\t") \
    #   .option("checkpointLocation", "checkpoint/") \
    #   .option("path", f"./{KAFKA_TOPIC_NAME}/") \
    #   .outputMode("append") \
    #   .start() \
    #   .awaitTermination()


    # Option 3: Write to Database
    # def foreach_batch_function(df, epoch_id):
    #     df.write \
    #     .format("jdbc") \
    #     .mode("append") \
    #     .option("url", "jdbc:postgresql://waia-spark-stream-example-1-db:5432/waia") \
    #     .option("driver", "org.postgresql.Driver") \
    #     .option("dbtable", "waia_events") \
    #     .option("user", "postgres") \
    #     .option("password", "postgres") \
    #     .save()

    # base_df.writeStream.foreachBatch(foreach_batch_function).start().awaitTermination()

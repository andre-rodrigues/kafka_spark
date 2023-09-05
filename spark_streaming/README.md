# Spark+Kafka pipeline

This guide will shows a couple of examples on how to use Spark Streaming to process data from Kafka.
First, make sure the kafka Broker is running by following the [here](https://github.com/andre-rodrigues/kafka_spark/blob/main/kafka/README.md).


### Example 1

The first example is a script that reads data from the topic `waia-events` and sends to a data sink. (console, CSV files or Postgres)

Use the `docker-compose.yml` file inside the examples folder to start the application.

```
cd example_1/

docker compose up
```

### Example 2

The second example is a script that calculates the average score based on events from the topic `waia-events`.

Again, use the `docker-compose.yml` file inside the examples folder to start the application.

```
cd example_2/

docker compose up
```

-----------------------------------

### Step by Step of the pipeline.
1- Import the necessary packages to use Kafka as source. This is usualy not necessary for other sources.
```
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 pyspark-shell'

```

2- Create a new SparkSession.
```
spark = (
    SparkSession.builder.appName("Kafka Pyspark Streaming Learning")
    .master("local[*]")
    .getOrCreate()
)
```

3- Setup a DataFrame loading data from the Kafka topic.
```
sampleDataframe = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
        .option("subscribe", KAFKA_TOPIC_NAME)
        .option("startingOffsets", "earliest")
        .load()
    )
```

4- Write the results of that DataFrame to CSV files.
```
    base_df = sampleDataframe.selectExpr("CAST(value as STRING)", "timestamp")
    base_df.writeStream \
      .format("csv") \
      .trigger(processingTime="10 seconds") \
      .option("checkpointLocation", "checkpoint/") \
      .option("path", f"./{KAFKA_TOPIC_NAME}/") \
      .outputMode("append") \
      .start() \
      .awaitTermination()
```
# Spark+Kafka pipeline

This guide will shows a few steps to read data from a Kafka topic and send to CSV files.

### Requirements
- **pyspark**: `pip install pyspark`
- **kafka**: Refer to kafka guide to setup a cluster and create a topic.


### Running the pipeline
Use the file `load_kafka_topic_to_csv_file.py` to read data from a Kafka Topic and load into CSV files.
```
python load_kafka_topic_to_csv_file.py
```

Optionally, try to read from different topics and also changing the bootstrap server.
```
KAFKA_TOPIC_NAME=<my-topic> python load_kafka_topic_to_csv_file.py
KAFKA_TOPIC_NAME=<my-topic> KAFKA_BOOTSTRAP_SERVER=localhost:9092 python load_kafka_topic_to_csv_file.py

```


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
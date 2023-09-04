# Kafka Producer and Consumer

Use the `docker-compose.yml` file to start the containers with Kafka and a producer.
The logs will show the output of `./producer/scores.py`
```
docker compose up
```

In the `./consumer` folder, you can find another Dockerfile to start the consumer apart from the producer.
This example shows the producer and consumer running separetly and exchanging information through Kafka.


# Kafka CLI

The quickstart guide provided by Apache will come in handy for testing the command line interface.
https://kafka.apache.org/quickstart



## Step 1:
Start the kafka broker using the docker compose file in this directory:
```
docker compose up -d
```

## Step 2:
Connect to the docker container running the kafka broker and go to the binaries folder.
```
docker exec -ti -u root waia_kafka_broker bash
```
```
cd /opt/bitnami/kafka/bin
```

**Alternative**:
You can also download kafka binaries and use it directly, like the quick-start tutorial suggests.
```
curl https://dlcdn.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz --output kafka_2.13-3.5.0.tgz

tar -xzf kafka_2.13-3.5.0.tgz

cd kafka_2.13-3.5.0/
```

## Step 3:
The commands below were based on the kafka quickstart guide: **[STEP 3: CREATE A TOPIC TO STORE YOUR EVENTS](https://kafka.apache.org/quickstart#quickstart_createtopic)**.


1- Create a topic
```
kafka-topics.sh --create --topic waia-events --bootstrap-server localhost:9092
```
2- Describe the topic
```
kafka-topics.sh --describe --topic waia-events --bootstrap-server localhost:9092

Topic: waia-events TopicId: wliVuT52QWyQifvfqRgqwA PartitionCount: 1 ReplicationFactor: 1  Configs: segment.bytes=1073741824
  Topic: waia-events Partition: 0  Leader: 1 Replicas: 1 Isr: 1

```

## Step 4:
Send data to the topic. \
This will start an interactive session in your console waiting for inputs. Each line of input will generate one event in the topic.
```
kafka-console-producer.sh --topic waia-events --bootstrap-server localhost:9092
```

## Step 5:
Read data from the topic. \
This will read all events pushed to a topic and print them in the console. You can test variations of parameters to read from different points of the event stream.

Read everything.
```
kafka-console-consumer.sh --topic waia-events --from-beginning --bootstrap-server localhost:9092
```

Read only new events.
```
kafka-console-consumer.sh --topic waia-events --bootstrap-server localhost:9092
```


## Conclusion
This small guide shows only the basic functionalities of Kafka, and mostly with default arguments, but it is still the most important feature that Kafka provides.
Understanding how the command line interface works will help you investigate problems and explore different configurations for the Kafka broker and topics. 


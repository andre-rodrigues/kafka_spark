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
root@e4dc9249978e:/# cd /opt/bitnami/kafka/bin
root@e4dc9249978e:/opt/bitnami/kafka/bin#
```

## Step 3:
You can now follow the instructions from the quickstart guide on **[STEP 3: CREATE A TOPIC TO STORE YOUR EVENTS](https://kafka.apache.org/quickstart#quickstart_createtopic)**.

Alternatively, you can follow the commands and steps below.

1- Create a topic
```
kafka-topics.sh --create --topic events --bootstrap-server localhost:9092
```
2- Describe the topic
```
kafka-topics.sh --describe --topic events --bootstrap-server localhost:9092

Topic: events TopicId: wliVuT52QWyQifvfqRgqwA PartitionCount: 1 ReplicationFactor: 1  Configs: segment.bytes=1073741824
  Topic: events Partition: 0  Leader: 1 Replicas: 1 Isr: 1

```

## Step 4:
Send data to the topic. \
This will start an interactive session in your console waiting for inputs. Each line of input will generate one event in the topic.
```
kafka-console-producer.sh --topic events --bootstrap-server localhost:9092
```

## Step 5:
Read data from the topic. \
This will read all events pushed to a topic and print them in the console. You can test variations of parameters to read from different points of the event stream.

Read everything.
```
kafka-console-consumer.sh --topic events --from-beginning --bootstrap-server localhost:9092
```

Read only new events.
```
kafka-console-consumer.sh --topic events --from-beginning --bootstrap-server localhost:9092
```


## Conclusion
This small guide shows only the basic functionalities of Kafka, and mostly with default arguments, but it is still the most important feature that Kafka provides.
Understanding how the command line interface works will help you investigate problems and explore different configurations for the Kafka broker and topics. 
\
\
The last steps in the quickstart guide will be addressed in other pages.
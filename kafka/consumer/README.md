Build the image for the consumer and start the consumer providing the same network name as the kafka broker.

```
docker build --tag kafka-scores-consumer .

docker run --network=waia_containers --env PYTHONUNBUFFERED=1 kafka-scores-consumer
```

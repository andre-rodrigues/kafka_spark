import random
import time
from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'localhost:9092'})
names = [
    "John", "Mary", "Jeff", "Anna"
]

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.value().decode('utf-8')))

while True:
    for name in names:
        score = int(random.random()*100)
        data = f"{name}:{score}"

        # Asynchronously produce a message. The delivery report callback will
        # be triggered from the call to poll() above, or flush() below, when the
        # message has been successfully delivered or failed permanently.
        p.produce('waia-events', data.encode('utf-8'), callback=delivery_report)

        # Trigger any available delivery report callbacks from previous produce() calls
        p.poll(0)
        
        time.sleep(2)

    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    p.flush()

import json, time, random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def generate_event():
    return {
        "user_id": random.randint(1, 1000),
        "event_type": random.choice(["click", "scroll", "purchase"]),
        "timestamp": time.time()
    }

while True:
    event = generate_event()
    producer.send('clickstream', event)
    print(f"Sent: {event}")
    time.sleep(1)
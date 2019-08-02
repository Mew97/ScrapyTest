from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(
    bootstrap_servers=[
        "192.168.11.30:9092",
    ]
)

future = producer.send("test", b'I am rito yan')
try:
    record_metadata = future.get(timeout=10)
    print(record_metadata)
except KafkaError as e:
    print(e)

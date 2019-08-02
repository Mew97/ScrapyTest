from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "test",
    group_id="test-1",
    bootstrap_servers=[
        "192.168.11.30:9092",
    ]
)
for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))

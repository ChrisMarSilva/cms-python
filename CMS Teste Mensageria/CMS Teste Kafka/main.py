from dotenv import load_dotenv


def teste_consumer():
    from kafka import KafkaConsumer
    from kafka import TopicPartition

    print('KafkaConsumer - Ini')

    consumer = KafkaConsumer('customer_topic')
    # consumer = KafkaConsumer('product_topic')
    # consumer = KafkaConsumer(bootstrap_servers='localhost:9093')
    for msg in consumer:
        print(msg, msg.headers)

    # consumer = KafkaConsumer('my-topic', group_id='my-group', bootstrap_servers=['localhost:9092'])
    # for message in consumer:
    #     print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))

    # consumer = KafkaConsumer('my_favorite_topic', group_id='my_favorite_group')
    # for msg in consumer:
    #     print(msg)

    #
    # consumer.assign([TopicPartition('foobar', 2)])
    # msg = next(consumer)

    # consumer = KafkaConsumer(value_deserializer=msgpack.loads)
    # consumer.subscribe(['msgpackfoo'])
    # for msg in consumer:
    #     assert isinstance(msg.value, dict)

    # metrics = consumer.metrics()

    print('KafkaConsumer - Fim')

def teste_producer():
    from kafka import KafkaProducer
    import json

    print('KafkaProducer - Ini')

    #producer = KafkaProducer(bootstrap_servers='localhost:9092')
    # for _ in range(100):
    #     producer.send('customer_topic', b'some_message_bytes')

    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: str(v).encode('utf-8'))
    future = producer.send('my-topic', b'raw_bytes')
    record_metadata = future.get(timeout=10)

    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

    #  future = producer.send('foobar', b'another_message')
    # result = future.get(timeout=60)

    # producer.flush()

    #  producer.send('foobar', key=b'foo', value=b'bar')

    # producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # producer.send('fizzbuzz', {'foo': 'bar'})

    #  producer = KafkaProducer(key_serializer=str.encode)
    #  producer.send('flipflap', key='ping', value=b'1234')

    #  producer = KafkaProducer(compression_type='gzip')
    # for i in range(1000):
    # producer.send('foobar', b'msg %d' % i)

    #  producer.send('foobar', value=b'c29tZSB2YWx1ZQ==', headers=[('content-encoding', b'base64')])

    # metrics = producer.metrics()

    print('KafkaProducer - Fim')

if __name__ == '__main__':
    # teste_producer()
    teste_consumer()

# pip install kafka-python




from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=[ 'localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))
producer.send('artigo-medium', value=dados)


from kafka import KafkaConsumer
from IPython.display import clear_output
consumer = KafkaConsumer('artigo-medium', group_id = 'group1', bootstrap_servers =['localhost:9092'])
for messagem in consumer:
  clear_output()
   texto = json.loads(messagem.value.decode('utf-8'))


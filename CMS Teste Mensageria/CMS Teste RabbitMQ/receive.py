import pika
import time

def receive(host: str = "localhost", queue: str = "hello"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True,)
    def callback(ch, method, properties, body):
        print(" ==> receive [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" ==> receive [x] Done")
        # ch.basic_ack(delivery_tag = method.delivery_tag)
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
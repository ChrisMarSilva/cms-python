import pika
import time

def worker(host: str = "localhost", queue: str = "task_queue"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    print(' ==> worker [*] Waiting for messages. To exit press CTRL+C')
    def callback(ch, method, properties, body):
        print(" ==> worker [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" ==> worker [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()
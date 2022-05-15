import pika

def new_task(host: str = "localhost", queue: str = "task_queue", routing_key: str = "task_queue", message: str = "02.Hello World!"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(exchange='', routing_key=routing_key, body=message.encode(), properties=pika.BasicProperties(delivery_mode=2,))  # delivery_mode=2 == make message persistent
    print(" ==> new_task [x] Sent %r" % message)
    connection.close()
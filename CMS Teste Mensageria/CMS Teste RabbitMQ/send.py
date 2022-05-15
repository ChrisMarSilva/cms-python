import pika

def send(host: str = "localhost", queue: str = "hello", routing_key: str = "hello", message: str = "01.Hello World!"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True,)
    channel.basic_publish(exchange='', routing_key=routing_key, body=message)
    connection.close()
    print(" ==> send [x] Enviado %r" % message)
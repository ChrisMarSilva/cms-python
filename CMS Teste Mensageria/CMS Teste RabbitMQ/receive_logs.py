import pika

def receive_logs(host: str = "localhost", exchange: str = "logs", exchange_type: str = "fanout"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name)
    def callback(ch, method, properties, body):
        print(" ==> receive_logs [x] %r" % body)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

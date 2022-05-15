import pika
import sys

def receive_logs_direct(host: str = "localhost", exchange: str = "direct_logs", exchange_type: str = "direct"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    severities = sys.argv[1:]
    # if not severities:
    #     sys.stderr.write(" ==> receive_logs_direct Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    #     sys.exit(1)
    # for severity in severities:
    #     channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=severity)
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key="info")
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key="warning")
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key="error")
    def callback(ch, method, properties, body):
        print(" ==> receive_logs_direct [x] %r:%r" % (method.routing_key, body))
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
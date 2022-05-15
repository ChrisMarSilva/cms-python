import pika

def emit_log_topic(host: str = "localhost", exchange: str = "topic_logs", exchange_type: str = "topic", routing_key: str = "anonymous.info", message: str = "05.Hello World!"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    print(" ==> emit_log_topic [x] Sent %r:%r" % (routing_key, message))
    connection.close()
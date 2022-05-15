import pika

def emit_log_direct(host: str = "localhost", exchange: str = "direct_logs", exchange_type: str = "direct", severity: str = "info", message: str = "04.Hello World!"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    channel.basic_publish(exchange=exchange, routing_key=severity, body=message)
    print(" ==> emit_log_direct [x] Sent %r:%r" % (severity, message))
    connection.close()
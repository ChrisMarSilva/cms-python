import pika

def emit_log(host: str = "localhost", exchange: str = "logs", exchange_type: str = "fanout", message: str = "03.Hello World!"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    channel.basic_publish(exchange=exchange, routing_key='', body=message)
    print(" ==> emit_log [x] Sent %r" % message)
    connection.close()
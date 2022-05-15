import pika

def receive_logs_topic(host: str = "localhost", exchange: str = "topic_logs", exchange_type: str = "topic", binding_key: str = "anonymous.info"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    # binding_keys = sys.argv[1:]
    # if not binding_keys:
    #     sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    #     sys.exit(1)
    # for binding_key in binding_keys:
    #     channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=binding_key)
    def callback(ch, method, properties, body):
        print(" ==> receive_logs_topic [x] %r:%r" % (method.routing_key, body))
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
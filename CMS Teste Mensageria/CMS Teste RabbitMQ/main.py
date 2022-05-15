import sys
import os
import time
import datetime
import json
import asyncio
import pika
import aio_pika
from aio_pika import connect, connect_robust, Message, IncomingMessage
from aio_pika.pool import Pool
from send import send
from receive import receive
from worker import worker
from new_task import new_task
from emit_log import emit_log
from receive_logs import receive_logs
from emit_log_direct import emit_log_direct
from receive_logs_direct import receive_logs_direct
from emit_log_topic import emit_log_topic
from receive_logs_topic import receive_logs_topic
from rpc_server import rpc_server
from rpc_client import rpc_client
from dotenv import load_dotenv


# pip install pika --upgrade
# pip install pika-stubs --upgrade
# pip install aio-pika

def get_ini_proc() -> float:
    return time.time()

def get_fim_proc(hora: float = 0.0, texto: str = 'Tempo', logar: bool = True) -> str:
    elapsed = time.time() - hora
    return f'{texto}: {str(datetime.timedelta(seconds=elapsed))}'

async def aio_pika_teste_01(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/", loop=loop)
    async with connection:
        channel = await connection.channel() # publisher_confirms=True
        await channel.declare_queue('hello', durable=True)
        await channel.default_exchange.publish(aio_pika.Message(body="hello".encode()), routing_key="hello",)

async def aio_pika_teste_02(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/", loop=loop)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("test_queue", auto_delete=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)
                    if queue.name in message.body.decode():
                        break

async def aio_pika_teste_03(loop):
    async def process_message(message: aio_pika.IncomingMessage):
        async with message.process():
            print(message.body)
            await asyncio.sleep(1)
    connection = await aio_pika.connect_robust(        "amqp://guest:guest@127.0.0.1/", loop=loop    )
    queue_name = "test_queue"
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)# Maximum message count which will be    # processing at the same time.
    queue = await channel.declare_queue(queue_name, auto_delete=True)
    await queue.consume(process_message)
    return connection

async def aio_pika_teste_04(loop):
    connection = await connect_robust(        "amqp://guest:guest@127.0.0.1/", loop=loop    )
    queue_name = "test_queue"
    routing_key = "test_queue"
    channel = await connection.channel()
    exchange = await channel.declare_exchange("direct", auto_delete=True)
    queue = await channel.declare_queue(queue_name, auto_delete=True)
    await queue.bind(exchange, routing_key)
    await exchange.publish(Message(bytes("Hello", "utf-8"),content_type="text/plain",headers={"foo": "bar"},),routing_key,)
    incoming_message = await queue.get(timeout=5)
    await incoming_message.ack()
    await queue.unbind(exchange, routing_key)
    await queue.delete()
    await connection.close()

async def aio_pika_teste_05():
    loop = asyncio.get_event_loop()
    async def get_connection():
        return await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    connection_pool = Pool(get_connection, max_size=2, loop=loop)
    async def get_channel() -> aio_pika.Channel:
        async with connection_pool.acquire() as connection:
            return await connection.channel()
    channel_pool = Pool(get_channel, max_size=10, loop=loop)
    queue_name = "pool_queue"
    async def consume():
        async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
            await channel.set_qos(10)
            queue = await channel.declare_queue(queue_name, durable=False, auto_delete=False)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    print(message)
                    await message.ack()
    async def publish():
        async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
            await channel.default_exchange.publish(aio_pika.Message(("Channel: %r" % channel).encode()),queue_name,)
    async with connection_pool, channel_pool:
        task = loop.create_task(consume())
        await asyncio.wait([publish() for _ in range(10000)])
        await task

async def aio_pika_teste_06(loop):
    connection = await connect("amqp://guest:guest@localhost/", loop=loop)
    channel = await connection.channel()
    await channel.default_exchange.publish(Message(b"Hello World!"), routing_key="hello")
    print(" [x] Sent 'Hello World!'")
    await connection.close()

async def aio_pika_teste_07(loop):
    connection = await connect("amqp://guest:guest@localhost/", loop=loop)

    async def on_message(message: IncomingMessage):
        print(" [x] Received message %r" % message)
        print("Message body is: %r" % message.body)
        print("Before sleep!")
        await asyncio.sleep(5)  # Represents async I/O operations
        print("After sleep!")

    channel = await connection.channel()
    queue = await channel.declare_queue("hello")
    await queue.consume(on_message, no_ack=True)


async def aio_pika_teste_09(loop):
    connection = await aio_pika.connect("amqp://guest:guest@localhost/", loop=loop)
    async with connection:
        channel = await connection.channel() # publisher_confirms=False
        await channel.declare_queue('hello', durable=True)
        num_of_messages = 10000
        start = datetime.datetime.now()
        for _ in range(num_of_messages):
            await channel.default_exchange.publish(aio_pika.Message(body=b'hello'), routing_key="hello")
        tt = datetime.datetime.now() - start
        print("aio_pika", tt.total_seconds(), num_of_messages / tt.total_seconds())
        await connection.close()


def aio_pika_teste_08():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="hello", durable=True, )
    num_of_messages = 2

    message = 'hello'.encode()
    message = json.dumps({'id': 1, 'name': 'CMS'}).encode()
    #message = json.dumps({ 'ID': 1, 'IDUSUARIO': 1, 'DTHRREGISTRO': 20201111190233, 'DTENVIO': 20201111, 'TIPO': 'FATOS-02', 'MENSAGEM': '<i>#1290612 - CIA HERING</i><br>Aviso aos Acionistas<br><br>https://www.rad.cvm.gov.br/ENET/frmExibirArquivoIPEExterno.aspx?ID=807712',}).encode()

    start = get_ini_proc()  # start = datetime.datetime.now()
    for _ in range(num_of_messages):
        channel.basic_publish(exchange='', routing_key="hello", body=message, properties=pika.BasicProperties(delivery_mode=2,))
    # tt = datetime.datetime.now() - start
    # print("pika", tt.total_seconds(), num_of_messages / tt.total_seconds())
    print("pika", get_fim_proc(hora=start, texto=f'Tempo', logar=False))
    connection.close()

def gerar_msg_alerta_admin(tipo_envio: str = '', mensagem: str = '', dthr: str = '') -> str:
    msg = ''
    titulo = 'Alerta de Admin'
    mensagem = mensagem.replace('<br>', '\n', ).replace('&lt;br&gt;', '\n', ).replace(';br;', '\n', )
    msg += f'<u><b>{titulo}</b></u>\n\n'
    msg += f"{mensagem}\n\n"
    msg += f'<i><u>{dthr}</u></i>\n' if dthr.strip() != '' else ''
    return msg


def converter_str_to_datetime(data: str='', fmt: str='%Y%m%d'):
    return datetime.datetime.strptime(data, fmt)

def converter_datetime_str(data, istext: bool=True, fmt: str= '%Y%m%d'): # : dt.datetime
    return data.strftime(fmt) if istext else data

def aio_pika_teste_10():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="hello", durable=True,)
    start = datetime.datetime.now()

    def callback(ch, method, properties, body):
        tt = datetime.datetime.now() - start
        #print(tt.total_seconds(), f" ==> '{body.decode()}'")
        data = json.loads(body.decode())
        print(tt.total_seconds(), f" ==> '{data}'")
        # print(tt.total_seconds(), f" ==> '{gerar_msg_alerta_admin(tipo_envio='T', mensagem=str(data['MENSAGEM']), dthr=str(data['DTHRREGISTRO']))}'")

        # time.sleep(body.count(b'.'))
        # print(" ==> receive [x] Done")
        # ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    # method_frame, header_frame, body = channel.basic_get(queue='hello')
    # if method_frame.NAME == 'Basic.GetEmpty':
    #     connection.close()
    #     return ''
    # else:
    #     channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    #     connection.close()
    #     return json.loads(body), method_frame.message_count

'''

connection = pika.BlockingConnection()
channel = connection.channel()

method_frame, header_frame, body = channel.basic_get('test')
if method_frame:
    print(method_frame, header_frame, body)
    channel.basic_ack(method_frame.delivery_tag)
else:
    print('No message returned')



import pika

connection = pika.BlockingConnection()
channel = connection.channel()

# Get ten messages and break out
for method_frame, properties, body in channel.consume('test'):

    # Display the message parts
    print(method_frame)
    print(properties)
    print(body)

    # Acknowledge the message
    channel.basic_ack(method_frame.delivery_tag)

    # Escape out of the loop after 10 messages
    if method_frame.delivery_tag == 10:
        break

# Cancel the consumer and return any pending messages
requeued_messages = channel.cancel()
print('Requeued %i messages' % requeued_messages)

# Close the channel and the connection
channel.close()
connection.close()

'''

if __name__ == '__main__':
    try:

        loop = asyncio.get_event_loop()

        # send()
        # receive()
        # worker()
        # new_task()
        # emit_log()
        # receive_logs()
        # emit_log_direct()
        # receive_logs_direct()
        # emit_log_topic()
        # receive_logs_topic()
        # rpc_server()
        # rpc_client()

        # loop.run_until_complete(aio_pika_teste_01(loop))  # Simple publisher
        # loop.run_until_complete(aio_pika_teste_02(loop))  # Simple consumer
        # connection = loop.run_until_complete(aio_pika_teste_03(loop)) # Asynchronous message processing
        # loop.run_until_complete(connection.close())
        # loop.run_forever()
        # loop.run_until_complete(aio_pika_teste_04(loop))  # Get single message example
        # loop.run_until_complete(aio_pika_teste_05())  # Connection pooling
        # loop.run_until_complete(aio_pika_teste_06(loop))  # sender
        # loop.run_until_complete(aio_pika_teste_07(loop))  # receiv

        aio_pika_teste_08()  # pika 4.561166 2192.421850026945
        # loop.run_until_complete(aio_pika_teste_09(loop))  # aio_pika 0.763997 13089.05663242133
        aio_pika_teste_10()

        loop.close()

    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

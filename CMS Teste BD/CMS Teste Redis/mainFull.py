import redis
import json
import datetime
import time
from pprint import pprint
from cryptography.fernet import Fernet
import bz2
import hiredis

# try:
#     import hiredis
#     HIREDIS_AVAILABLE = True
# except ImportError:
#     HIREDIS_AVAILABLE = False


def main():

    # r = redis.Redis(host='localhost', port=6379, db=0, password='123')
    # r = redis.Redis(host='localhost', port=6379, db=1, password='123')
    #pool = redis.ConnectionPool(host='localhost', port=6379, db=0, password='123')
    #r = redis.Redis(connection_pool=pool)
    r = redis.StrictRedis(host='localhost', port=6379, db=0, password='123')

    # r.set('foo', 'bar')
    # print('#1', r.get('foo'))

    # r.set('foo1', 'bar1')
    # r.set('foo2', 'bar2')
    # r.set('foo3', 'bar3')

    # r.rpush('ferramentas', 'martelo')
    # r.rpush('ferramentas', 'serrote')
    # r.rpush('ferramentas', 'machado')
    # print('#2' , r.lrange('ferammentas', 0, -1))
    # print('#3' , r.llen('ferramentas'))
    # print('#4' , r.lindex('ferramentas', 1))
    # r.delete('ferramentas')
    # print('#2' , r.lrange('ferammentas', 0, -1))

    # print('#2' , r.sadd('ferramentas', 'martelo'))
    # print('#2' , r.sadd('ferramentas', 'serrote'))
    # print('#2' , r.sadd('ferramentas', 'machado'))
    # print('#2' , r.sadd('ferramentas', 'martelo'))
    # print('#2' , r.smembers('ferramentas'))

    # r.zadd('test:scores', 'testid:9000', 50)
    # r.zadd('test:scores', 'testid:8000', 20)
    # r.zadd('test:scores', 'testid:7000', 45)
    # r.zadd('test:scores', 'testid:7000', 45)
    # r.zrange('test:scores', 0, -1, withscores=True)

    # test = r.zrange('test:scores', 0, -1, withscores=True)
    # test.reverse()

    # capitals = {}
    # capitals["Bahamas"] = "Nassau"
    # capitals["Croatia"] = "Zagreb"
    # capitals.get("Croatia")
    # capitals.get("Japan")  # None

    # capitals.update(
    #     {"Lebanon": "Beirut", "Norway": "Oslo", "France": "Paris", })
    # [capitals.get(k) for k in ("Lebanon", "Norway", "Bahamas")]

    # data = {
    #     "realpython": {
    #         "url": "https://realpython.com/",
    #         "github": "realpython",
    #         "fullname": "Real Python",
    #     }
    # }

    # r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
    # r.get("Bahamas")

    # today = datetime.date.today()
    # stoday = today.isoformat()
    # visitors = {"dan", "jon", "alex"}
    # r.sadd(stoday, *visitors)
    # print(r.smembers(stoday))
    # print(r.scard(today.isoformat()))

    # r.hincrby("hat:56854717", "quantity", -1)
    # r.hget("hat:56854717", "quantity")
    # r.hincrby("hat:56854717", "npurchased", 1)

    # r.lpush("ips", "51.218.112.236")
    # r.lpush("ips", "90.213.45.98")
    # r.lpush("ips", "115.215.230.176")
    # r.lpush("ips", "51.218.112.236")

    # r.hset("mykey", "field1", "value1")

    # restaurant_484272 = {
    #     "name": "Ravagh",
    #     "type": "Persian",
    #     "address": {
    #         "street": {
    #             "line1": "11 E 30th St",
    #             "line2": "APT 1",
    #         },
    #         "city": "New York",
    #         "state": "NY",
    #         "zip": 10016,
    #     }
    # }
    # r.set(484272, json.dumps(restaurant_484272))
    # pprint(json.loads(r.get(484272)))

    # cipher = Fernet(Fernet.generate_key())
    # info = {"cardnum": 2211849528391929, "exp": [2020, 9], "cv2": 842, }
    # r.set("user:1000", cipher.encrypt(json.dumps(info).encode("utf-8")))
    # pprint(r.get("user:1000"))
    # pprint(cipher.decrypt(r.get("user:1000")))
    # pprint(json.loads(cipher.decrypt(r.get("user:1000"))))

    #blob = "i have a lot to talk about" * 10000
    # len(blob.encode("utf-8"))  # 260000
    #r.set("msg:500", bz2.compress(blob.encode("utf-8")))
    # print(r.get("msg:500"))
    # len(r.get("msg:500"))  # 122
    #rblob = bz2.decompress(r.get("msg:500")).decode("utf-8")
    # print(rblob)
    # rblob == blob # True

    # if HIREDIS_AVAILABLE:
    #     DefaultParser = HiredisParser
    # else:
    #     DefaultParser = PythonParser
    # try:
    #     with r.lock('my-lock-key', blocking_timeout=5) as lock:
    #         # code you want executed only after the lock has been acquired
    #         print(f'ok 1')

    #         try:
    #             with r.lock('my-lock-key', blocking_timeout=5) as lock:
    #                 print(f'ok 2')
    #                 # code you want executed only after the lock has been acquired
    #         except Exception:
    #             print(f'Erro 2')  # the lock wasn't acquired

    # except Exception:  # LockError:
    #     print(f'Erro 1')  # the lock wasn't acquired

    # r.set('bing', 'baz')
    # pipe = r.pipeline()
    # pipe.set('foo', 'bar')
    # pipe.get('bing')
    # print(pipe.execute())
    # pipe.set('foo', 'bar').sadd('faz', 'baz').incr('auto_number').execute()

    # pipe = r.pipeline(transaction=False)

    # with r.pipeline() as pipe:
    #     while True:
    #         try:
    #             # put a WATCH on the key that holds our sequence value
    #             pipe.watch('OUR-SEQUENCE-KEY')
    #             # after WATCHing, the pipeline is put into immediate execution
    #             # mode until we tell it to start buffering commands again.
    #             # this allows us to get the current value of our sequence
    #             current_value = pipe.get('OUR-SEQUENCE-KEY')
    #             next_value = int(current_value) + 1
    #             # now we can put the pipeline back into buffered mode with MULTI
    #             pipe.multi()
    #             pipe.set('OUR-SEQUENCE-KEY', next_value)
    #             # and finally, execute the pipeline (the set command)
    #             pipe.execute()
    #             # if a WatchError wasn't raised during execution, everything
    #             # we just did happened atomically.
    #             break
    #         except Exception:
    #             # another client must have changed 'OUR-SEQUENCE-KEY' between
    #             # the time we started WATCHing it and the pipeline's execution.
    #             # our best bet is to just retry.
    #             continue

    # pipe = r.pipeline()
    # while True:
    #     try:
    #         pipe.watch('foo')
    #         print(pipe.execute())
    #         break
    #     except WatchError:
    #         continue
    #     finally:
    #         pipe.reset()

    # p = r.pubsub()
    # p.subscribe('my-first-channel', 'my-second-channel', ...)
    # p.psubscribe('my-*', ...)
    # p.get_message()
    # r.publish('my-first-channel', 'some data')
    # p.get_message()
    # p.unsubscribe()
    # p.punsubscribe('my-*')
    # p.get_message()

    # def my_handler(message):
    #     print('MY HANDLER: ', message['data'])
    # p.subscribe(**{'my-channel': my_handler})
    # p.get_message()
    # r.publish('my-channel', 'awesome data')
    # message = p.get_message()
    # print(message)

    # p = r.pubsub(ignore_subscribe_messages=True)
    # p.subscribe('my-channel')
    # p.get_message()  # hides the subscribe message and returns None
    # r.publish('my-channel', 'my data')
    # p.get_message()

    # while True:
    #     message = p.get_message()
    #     if message:
    #         pass  # do something with the message
    #     time.sleep(0.001)  # be nice to the system :),

    # for message in p.listen():
    #     pass  # do something with the message

    # p = r.pubsub()
    # p.close()

    # r.pubsub_channels()
    # #[b'foo', b'bar']
    # r.pubsub_numsub('foo', 'bar')
    # #[(b'foo', 9001), (b'bar', 42)]
    # r.pubsub_numsub('baz')
    # # [(b'baz', 0)]
    # r.pubsub_numpat()
    # # 1204

    # with r.monitor() as m:
    #     for command in m.listen():
    #         print(command)

    # lua = """
    #  local value = redis.call('GET', KEYS[1])
    #  value = tonumber(value)
    #  return value * ARGV[1]"""
    # multiply = r.register_script(lua)
    # print(multiply)

    # r.set('foo', 2)
    # multiply(keys=['foo'], args=[5])
    # print(multiply)

    # r2.set('foo2', 3)
    # multiply(keys=['foo2'], args=[5], client=r2)

    # for i in range(10):
    #     #r.hset('name', i, i)
    #     r.set('name:' + str(i), i, ex=time_to_expire_s)
    # print(r.hgetall('name'))

    # ttl = datetime.today() + timedelta(seconds=10)
    # r.hset(name=name, key=hash_key, value=hash_data)
    # r.expire(name=hash_name, time=ttl)

    r.set("foo", "bar")
    r.expire(name='foo', time=3)
    # while r.ttl("foo") > 0:
    print(r.ttl("foo"))
    print(r.pttl("foo"))
    time.sleep(4)
    print(r.ttl("foo"))  # segundos
    print(r.pttl("foo"))  # milissegundos


if __name__ == "__main__":
    main()

# pip install redis
# python -m pip install cryptography
# python -m pip install hiredis

import json
import redis

# redis_instance = redis.Redis(host='localhost', port=6379, db=0, password='123', charset='utf-8', decode_responses=True)
redis_instance = redis.Redis(host='localhost', port=6379, charset='utf-8', decode_responses=True)


def get():
    res_cache = redis_instance.get('test_key')
    if (res_cache != None):
        result = json.loads(res_cache)
    else:
        result = {'msg':'Nothing on Cache'}    
    return result 


def post(body):
    try:
        redis_instance.set('test_key', json.dumps(body)) 
        return body          
    except Exception as e:
        print(e)
        return {'msg':'Bad Request!', 'error': str(e)}


def delete(cache_key):
    redis_instance.delete(cache_key)
    return {'msg':'Success!'}

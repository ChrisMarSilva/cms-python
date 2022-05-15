from flask_redis import FlaskRedis


redis_client = FlaskRedis(config_prefix="redis://:123@localhost:6379/0")

import redis
from config.config import config

host = config['REDIS']['host']
port = config['REDIS']['port']
db = config['REDIS']['db']


def get_redis_conn():
    try:
        redis_conn = redis.Redis(host=host,
                                 port=port,
                                 db=db)
        return redis_conn
    except Exception as exc:
        _msg = 'Error on redis connection: %s' % exc.args
        print(_msg)
        raise Exception(exc)

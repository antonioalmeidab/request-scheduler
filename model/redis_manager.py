from connection.redis import get_redis_conn

redis_conn = get_redis_conn()


def register_task(_profile, _tag, _data):
    try:
        redis_conn.hset(_profile, _tag, _data)
    except Exception as exc:
        raise exc


def remove_task(_profile, _tag):
    try:
        redis_conn.hdel(_profile, _tag)
    except Exception as exc:
        raise exc


def get_tasks(_profile):
    _tasks = redis_conn.hgetall(_profile)
    _proper_tasks = {}
    for _key in _tasks:
        _task = _tasks[_key].decode("utf-8")
        _key.decode("utf-8")
        _task = eval(_task)
        _proper_tasks[_key.decode('utf-8')] = _task
    return _proper_tasks


def get_task(_profile, _tag):
    _task = redis_conn.hget(_profile, _tag)
    _task = eval(_task.decode('utf-8'))

    return _task


def get_keys():
    return redis_conn.keys()
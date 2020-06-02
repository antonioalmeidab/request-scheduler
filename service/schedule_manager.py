import datetime
import random
import string
import schedule
import json
from crontab import CronTab
from config.config import config
from model import redis_manager

cron = CronTab(user=config['INSTANCE']['user'])
project_path = config['INSTANCE']['schedule_path']
sched_command = config['INSTANCE']['schedule_command']
env_path = config['INSTANCE']['env_path']


def schedule_task(req, _tag=None):
    res_data = {
        'content': '',
        'status': ''
    }
    try:
        interval = req['schedule']['interval']
        time_unit = req['schedule']['time_unit']
        time = req['schedule']['time']

        try:
            _profile = req['profile']
        except KeyError:
            _profile = 'default'

        if not _tag:
            _tag = _gen_unique_task_tag()

        command = sched_command.format(project_path, env_path,
                                         _profile, _tag)
        job = cron.new(command=command,
                         comment=_profile + ' ' + _tag)
        print("Task tag generated - {}".format(_tag))

        if time_unit == 'day_month':
            time = time.split(':')
            minutes = int(time[1])
            hours = int(time[0])
            cron_string = '{} {} {} * *'.format(minutes, hours, interval)
            job.setall(cron_string)

        if time_unit == 'days':
            time = time.split(':')
            job.dom.every(interval)
            job.minute.on(time[1])
            job.hour.on(time[0])

        if time_unit == 'hours':
            job.hour.every(interval)

        if time_unit == 'minutes':
            job.minute.every(interval)

        cron.write()
        print("Service scheduled")

        req['tag_id'] = _tag
        redis_manager.register_task(_profile, _tag, json.dumps(req))
        print("Registered on redis")

        res_data['content'] = "Task - %s - created" % _tag
        res_data['status'] = 200

    except Exception as exc:
        res_data['content'] = json.dumps(exc.args)
        res_data['status'] = 500
    finally:
        return res_data


def remove_task(req):
    res_data = {}
    try:
        _tag = req['tag_id']
        _profile = req['profile']

        _iter = cron.find_comment(_profile + ' ' + _tag)
        for job in _iter:
            continue
        cron.remove(job)
        cron.write()
        redis_manager.remove_task(_profile, _tag)
        res_data['content'] = "Task - %s - stopped" % _tag
        res_data['status'] = 200
    except NameError:
        res_data['content'] = "Task - %s - is not scheduled" % _tag
        res_data['status'] = 200
    except KeyError:
        res_data['content'] = 'Bad request format - no Tag ID or profile'
        res_data['status'] = 400
    except Exception as exc:
        res_data['content'] = json.dumps(exc.args)
        res_data['status'] = 500
    finally:
        return res_data


def list_tasks(req):
    res_data = {
        "content": '',
        "status": ''
    }
    _profile = req['request_params'].get('profile')

    del(req['request_params'])

    try:
        _backup_tasks = redis_manager.get_tasks(_profile)

        res_data['content'] = json.dumps(_proper_jobs)
        res_data['status'] = 200
    except Exception as exc:
        res_data['content'] = json.dumps(exc.args)
        res_data['status'] = 200
    finally:
        return res_data


def _gen_unique_task_tag():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(5)) + \
           '-' +  \
           datetime.datetime.strftime(datetime.datetime.now(), '%d%m%y%H%M%S')
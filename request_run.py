import datetime
import sys
import requests
import json
from model import redis_manager

_profile = sys.argv[1]
_tag = sys.argv[2]

_data = redis_manager.get_task(_profile, _tag)
del(_data['schedule'])


requests.post('URL', json.dumps(_data['req_body']))

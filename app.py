from flask import Flask, request
from werkzeug.exceptions import BadRequest
from service.schedule_manager import (list_tasks,
                                      schedule_task, remove_task)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/schedule', methods=['POST', 'GET', 'DELETE'])
def schedule_service():
    _data = _get_request_data()

    request_router = {
        'GET': list_tasks,
        'POST': schedule_task,
        'DELETE': remove_task
    }

    _res = request_router[request.method](_data)

    return (_res['content'], _res['status'])


def _get_request_data():
    try:
        _data = request.get_json(force=True)
    except BadRequest as exc:
        _msg = 'Error on get_request_data: BadRequest probably GET'
        print(_msg)
        try:
            _data = {}
            if request.method == 'GET':
                _data['request_params'] = request.args
        except Exception as gerr:
            _msg = 'Error on get_request_data: %s' % exc.args
            print(_msg)
            raise gerr

    return _data


if __name__ == '__main__':
    app.run(debug=True)

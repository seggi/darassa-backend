import json
import time

from flask import jsonify


def stringify_objectid(data):
    str_data = json.dumps(data, default=str)
    return json.loads(str_data)


def response(status, message, data, status_code=200):
    if data:
        data = stringify_objectid(data)
    res = {'status': status, 'message': message,
           'data': data, 'timestamp': timestamp()}
    return jsonify(res), status_code


def error_response(message, status='error', code='R0', status_code=400):
    res = {'message': message, 'status': status, 'code': code}
    return jsonify(res), status_code


def timestamp():
    return time.time()

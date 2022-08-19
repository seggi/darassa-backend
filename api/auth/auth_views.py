from flask import Blueprint
from flask import request, jsonify

from api.utils.responses import response_with
from api.utils import responses as resp

auth = Blueprint("auth", __name__, url_prefix="/api/user")


@auth.get('/login')
def login():
    try:
        return jsonify(data="Welcome to darassa")
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)

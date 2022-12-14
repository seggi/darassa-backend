from flask import make_response, jsonify

# Deffirent responses

INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "code": "invalidField",
    "message": "Invalid fields found"
}

INVALID_INPUT_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Invalid input"
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameter",
    "message": "Missing parameters."
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}

SERVER_ERROR_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Resource not found"
}

UNAUTHORIZED_403 = {
    "http_code": 403,
    "code": "notAuthorized",
    "message": "You are not authorised to execute this."
}

SUCCESS_200 = {
    "http_code": 200,
    "code": "success",
    "message": "Please Verify your email"
}

SUCCESS_201 = {
    "http_code": 201,
    "code": "success",
    "message": "User already exist."
}

SUCCESS_204 = {
    "http_code": 204,
    "code": "success",
}


# Manage all above responses

def response_with(response, value=None, message=None, error=None, headers={}, pagination=None):
    result = {}
    if value is not None:
        result.update(value)

    if response.get('message', None) is not None:
        result.update({'message': response['message']})

    result.update({'code': response['code']})

    if error is not None:
        result.update({'errors': error})

    if pagination is not None:
        result.update({'pagination': pagination})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Flask REST API'})

    return make_response(jsonify(result), response['http_code'], headers)


class Response():
    @staticmethod
    def created(message=None, data=None):
        resp = jsonify({"message": message})
        resp.status_code = 201
        return resp

    def success(message=None, data=None):
        resp = jsonify({"message": message, "data": data})
        resp.status_code = 200
        return resp

    def failed(message=None):
        resp = jsonify({"message": message, })
        resp.status_code = 400
        return resp

    def page_not_found(message=None):
        resp = jsonify({"message": message})
        resp.status_code = 404
        return resp

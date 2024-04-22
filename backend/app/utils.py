# backend/app/utils.py
from functools import wraps
from flask import request, jsonify

def validate_json(*expected_args):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            json_object = request.get_json()
            for expected_arg in expected_args:
                if expected_arg not in json_object:
                    return jsonify(error=f"{expected_arg} is required"), 400
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

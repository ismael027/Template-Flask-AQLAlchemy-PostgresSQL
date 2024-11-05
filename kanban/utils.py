from functools import wraps
from flask import jsonify, request

def required_fields(*fields):
    def decorator(function):
        @wraps(function)
        def inner( *args, **kwargs):
            for field in fields:
                if request.json.get(field) is None:
                    return jsonify({'error': f'required field "{field}"'}), 400
            return function(*args, **kwargs)

        return inner

    return decorator
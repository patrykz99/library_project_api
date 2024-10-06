from flask import request
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps

def validate_content_type_json(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        data = request.get_json()
        if data is None:
            raise UnsupportedMediaType('Content-Type must be applications/json')
        return func(*args,**kwargs)
    return wrapper
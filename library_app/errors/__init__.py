from flask import Blueprint

errors_blueprint = Blueprint('errors',__name__)

from library_app.errors import errors
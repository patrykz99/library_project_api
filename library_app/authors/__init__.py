from flask import Blueprint

authors_blueprint = Blueprint('authors',__name__)

from library_app.authors import authors
from flask import Blueprint

books_blueprint = Blueprint('books',__name__)

from library_app.books import books
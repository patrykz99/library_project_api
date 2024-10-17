from library_app import db
from flask import jsonify,request
from library_app.models import Book,Book_Schema,book_schema
from webargs.flaskparser import use_args
from library_app.utils import validate_content_type_json,get_schema_params,sort_data,filter_data,make_pagination
from library_app.books import books_blueprint

@books_blueprint.route('/books')
def get_books():
    books = sort_data(Book,Book.query)
    books = filter_data(Book,books) 
    schema_params = get_schema_params(Book)
    items_page, pagination = make_pagination(books,'books.get_books')
    #authors = author.all() -> items variable
    author_schema_list = Book_Schema(**schema_params)
    return jsonify({
        'success':True,
        'data': author_schema_list.dump(items_page),
        'amount':len(items_page),
        'pagination': pagination
    })
    
@books_blueprint.route('/books/<int:book_id>',methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id,description=f'No book with id {book_id} in the database')
    return jsonify({
        'success':True,
        'data': book_schema.dump(book)
    })
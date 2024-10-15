from library_app import db
from library_app.models import Author,Book
from sqlalchemy import text
from pathlib import Path
from datetime import datetime
import json
from library_app.commands import db_commands_blueprint


def load_json():
    json_path_authors = Path(__file__).parent.parent /'data'/'authors.json'
    json_path_books = Path(__file__).parent.parent / 'data'/'books.json'
    with open(json_path_authors) as file:
        data_authors = json.load(file)
    with open(json_path_books) as file:
        data_books = json.load(file)
    return (data_authors,data_books)
            
@db_commands_blueprint.cli.group()
def db_commands():
    '''Commands to manipulate database'''
    pass

@db_commands.command()
def add_data():
    '''Add all data from file (JSON) to the table'''
    try:
        data = load_json()   
        for e in data[0]:
            e['date_of_birth'] = datetime.strptime(e['date_of_birth'],"%d-%m-%Y").date()
            author = Author(**e)
            db.session.add(author)
        for e in data[1]:
            book = Book(**e)
            db.session.add(book)
        db.session.commit() 
        print('Data has been added succesfully')  
    except Exception as err:
        print(f'Got an unexpected error: {err}')       

@db_commands.command()
def remove_data():
    '''Remove all data from the table'''
    try:
        db.session.execute(text(f'DELETE FROM {Book.__tablename__};'))
        db.session.execute(text(f'ALTER SEQUENCE {Book.__tablename__}_id_seq RESTART WITH 1;'))
        db.session.execute(text(f'DELETE FROM {Author.__tablename__};'))
        db.session.execute(text(f'ALTER SEQUENCE {Author.__tablename__}_id_seq RESTART WITH 1;'))
        db.session.commit()
        print('Data has been removed succesfully') 
    except Exception as err:
        print(f'Got an unexpected error: {err}')
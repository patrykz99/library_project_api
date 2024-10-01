from library_app import app,db
from library_app.models import Author
from pathlib import Path
from datetime import datetime
import json


@app.cli.group()
def db_commands():
    '''Commands to manipulate database'''
    pass

@db_commands.command()
def add_data():
    '''Add data to the database'''
    try:
        json_path = Path(__file__).parent /'data'/'authors.json'
        with open(json_path) as file:
            data = json.load(file)
        for e in data:
            e['date_of_birth'] = datetime.strptime(e['date_of_birth'],"%d-%m-%Y").date()
            author = Author(**e)
            db.session.add(author)
        db.session.commit() 
        print('Data has been added succesfully')  
    except Exception as err:
        print(f'Got an unexpected error: {err}')       

@db_commands.command()
def remove_data():
    '''Remove data from the database'''
    pass
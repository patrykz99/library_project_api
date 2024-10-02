from library_app import db
from marshmallow import Schema, fields

class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    date_of_birth = db.Column(db.Date,nullable=False)
    
    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}>: {self.first_name} {self.last_name}'

class Author_Schema(Schema):
    id = fields.Int()
    first_name = fields.String()
    last_name = fields.String()
    date_of_birth = fields.Date('%d-%m-%Y')
    
author_schema = Author_Schema()
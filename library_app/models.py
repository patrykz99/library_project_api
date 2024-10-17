from library_app import db
from marshmallow import Schema, fields,validate,validates,ValidationError
from flask_sqlalchemy import query
from flask import request
from datetime import datetime

class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    date_of_birth = db.Column(db.Date,nullable=False)
    books = db.relationship('Book',back_populates='author',cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}>: {self.first_name} {self.last_name}'
    
    @staticmethod
    def has_date_of_birth(key,value):
        if key == 'date_of_birth':
            try:
                value = datetime.strptime(value,'%d-%m-%Y').date()
                return value
            except ValueError:
                return False   
                     
 
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable=False)
    isbn = db.Column(db.BigInteger,nullable=False,unique=True)
    number_of_pages = db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(250))
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'),nullable=False)
    author = db.relationship('Author',back_populates='books')
    
    def __repr__(self):
        return f' {self.title} - {self.author.first_name} {self.author.last_name}'
    
    @staticmethod
    def has_date_of_birth(key,value):
        return value  
         
class Author_Schema(Schema):
    id = fields.Int(dump_only = True)
    first_name = fields.String(required=True,validate=validate.Length(max=50))
    last_name = fields.String(required=True,validate=validate.Length(max=50))
    date_of_birth = fields.Date('%d-%m-%Y',required=True)
    books = fields.List(fields.Nested(lambda: Author_Schema(exclude=['author'])))
    
    @validates('date_of_birth')
    def validate_date_of_birth(self,value):
        if value > datetime.now().date():
            raise ValidationError (f'Date of bierth must be lower than {datetime.now().date()}')


class Book_Schema(Schema):
    id = fields.Int(dump_only = True)
    title = fields.String(required=True,validate=validate.Length(max=100))
    isbn = fields.Integer(required=True)
    number_of_pages = fields.Integer(required=True)  
    description = fields.String(validate=validate.Length(max=250))
    author_id = fields.Integer(load_only=True)  
    author = fields.Nested(lambda: Author_Schema(only=['id','first_name','last_name']))   
    
    @validates('isbn')
    def validate_isbn(self,value):
        if value:
            if len(str(value)) != 13:
                raise ValidationError('ISBN field must contains 13 digits.')
                
        
author_schema = Author_Schema()
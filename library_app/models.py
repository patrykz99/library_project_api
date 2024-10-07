from library_app import db
from marshmallow import Schema, fields,validate,validates,ValidationError
from datetime import datetime
from werkzeug.exceptions import BadRequest
from flask_sqlalchemy import query

class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    date_of_birth = db.Column(db.Date,nullable=False)
    
    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}>: {self.first_name} {self.last_name}'
    
    @staticmethod
    def get_schema_params(field: str):
        schema_params = {
            'many':True
        }
        if field:
            print(field.split(','))
            if all(field in Author.__table__.columns.keys() for field in field.split(',')):    
                schema_params['only']= [p for p in field.split(',') if p in Author.__table__.columns]
            else:
                raise BadRequest(description=f'Invalid value in fields: {",".join(field.split(","))}')
            
        return schema_params
    @staticmethod
    def sort_data(qry: query,sort_keys= None):
        if sort_keys:
            for key in sort_keys.split(','):
                desc = False
                if key.startswith('-'):
                    key = key[1:]
                    desc = True
                column_attr = getattr(Author,key,None)
                if column_attr is not None:
                    qry = qry.order_by(column_attr.desc() if desc else qry.order_by(column_attr))
            return qry
        else:
            return Author.query
            
        
        
class Author_Schema(Schema):
    id = fields.Int(dump_only = True)
    first_name = fields.String(required=True,validate=validate.Length(max=50))
    last_name = fields.String(required=True,validate=validate.Length(max=50))
    date_of_birth = fields.Date('%d-%m-%Y',required=True)
    
    @validates('date_of_birth')
    def validate_date_of_birth(self,value):
        if value > datetime.now().date():
            raise ValidationError (f'Date of bierth must be lower than {datetime.now().date()}')
        
    
author_schema = Author_Schema()
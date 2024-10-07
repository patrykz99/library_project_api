from library_app import db
from marshmallow import Schema, fields,validate,validates,ValidationError
from datetime import datetime
from werkzeug.exceptions import BadRequest

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
            if field.split(',') not in  list(Author.__table__.columns.keys()):
                raise BadRequest(description=f'Invalid value in fields: {",".join(field.split(","))}')
            schema_params['only']= [p for p in field.split(',') if p in Author.__table__.columns]
            
        return schema_params
        
        

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
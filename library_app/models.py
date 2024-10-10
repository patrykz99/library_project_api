from library_app import db
from marshmallow import Schema, fields,validate,validates,ValidationError
from datetime import datetime
from werkzeug.exceptions import BadRequest
from flask_sqlalchemy import query
from flask import request,url_for
from config import Config
from typing import Tuple

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
    @staticmethod
    def filter_data(qry:query, params):
        for key, value in params.items():
            if key not in ('key','fields','page','limit'):
                column = getattr(Author,key,None)
                if column is not None:
                    if key == 'date_of_birth':
                        try:
                            value = datetime.strptime(value,'%d-%m-%Y').date()
                        except ValueError:
                            continue                       
                    qry = qry.filter(column == value)   
        return qry           
    @staticmethod
    def make_pagination(qry:query) -> Tuple[list,dict]:
        page = request.args.get('page',1,type=int)  
        limit = request.args.get('limit',Config.PAGE_LIMIT_DEFAULT,type=int)  
        params = {key:value for key, value in request.args.items() if key != 'page'}
        paginate_obj = qry.paginate(page = page, per_page = limit)
        pagination={
            'total_pages':paginate_obj.pages,
            'total_records':paginate_obj.total,
            'current_page':url_for('authors.get_authors',page=page, **params),
        }
        
        if paginate_obj.has_prev:
            pagination['prev_page'] = url_for('authors.get_authors',page=page-1, **params)
        if paginate_obj.has_next:
            pagination['next_page'] = url_for('authors.get_authors',page=page+1, **params)
            
        return paginate_obj.items,pagination
        
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
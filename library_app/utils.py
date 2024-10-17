from flask import request,url_for,current_app
from flask_sqlalchemy import query
from flask_sqlalchemy.model import DefaultMeta
from werkzeug.exceptions import UnsupportedMediaType,BadRequest
from functools import wraps
from config import Config
from typing import Tuple
from library_app.models import Author


def get_schema_params(model:DefaultMeta):
    schema_params = {
        'many':True
    }
    fields = 'fields'
    if request.args.get(fields):
        if all(field in model.__table__.columns.keys() for field in request.args.get(fields).split(',')):    
            schema_params['only']= [p for p in request.args.get(fields).split(',') if p in model.__table__.columns]
        else:
            raise BadRequest(description=f'Invalid value in fields: {",".join(request.args.get(fields).split(","))}')
        
    return schema_params


def sort_data(model:DefaultMeta, qry: query):
    if request.args.get('sort'):
        for key in request.args.get('sort').split(','):
            desc = False
            if key.startswith('-'):
                key = key[1:]
                desc = True
            column_attr = getattr(model,key,None)
            if column_attr is not None:
                qry = qry.order_by(column_attr.desc() if desc else qry.order_by(column_attr))
        return qry
    else:
        return model.query



def filter_data(model:DefaultMeta, qry:query):
    for key, value in request.args.items():
        if key not in ('key','fields','page','limit'):
            column = getattr(model,key,None)
            if column is not None:
                if model.has_date_of_birth(key,value):
                    value = model.has_date_of_birth(key,value)                     
                qry = qry.filter(column == value)   
    return qry 


def make_pagination(qry:query,fcn_name:str) -> Tuple[list,dict]:
    page = request.args.get('page',1,type=int)  
    limit = request.args.get('limit',current_app.config.get('PAGE_LIMIT_DEFAULT',10),type=int)  
    params = {key:value for key, value in request.args.items() if key != 'page'}
    paginate_obj = qry.paginate(page = page, per_page = limit)
    pagination={
        'total_pages':paginate_obj.pages,
        'total_records':paginate_obj.total,
        'current_page':url_for(fcn_name,page=page, **params),
    }
    
    if paginate_obj.has_prev:
        pagination['prev_page'] = url_for('authors.get_authors',page=page-1, **params)
    if paginate_obj.has_next:
        pagination['next_page'] = url_for('authors.get_authors',page=page+1, **params)
        
    return paginate_obj.items,pagination

def validate_content_type_json(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        data = request.get_json()
        if data is None:
            raise UnsupportedMediaType('Content-Type must be applications/json')
        return func(*args,**kwargs)
    return wrapper


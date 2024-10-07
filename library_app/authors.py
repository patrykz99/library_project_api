from library_app import app,db
from flask import jsonify,request
from library_app.models import Author,Author_Schema,author_schema
from webargs.flaskparser import use_args
from library_app.utils import validate_content_type_json



@app.route('/api/ver1/authors')
def get_authors():
    author = Author.query.all()
    schema_params = Author.get_schema_params(request.args.get('fields'))
    author_schema_list = Author_Schema(**schema_params)
    return jsonify({
        'success':True,
        'data': author_schema_list.dump(author),
        'amount':len(author)
    })
    
@app.route('/api/ver1/authors/<int:author_id>')
def get_author(author_id):
    author = Author.query.get_or_404(author_id,description=f'No author with id {author_id} in the database')
    return jsonify({
        'success':True, 
        'data': author_schema.dump(author)
    })
    
@app.route('/api/ver1/authors',methods=['POST'])
@validate_content_type_json
@use_args(author_schema,error_status_code=400)
def add_author(args:dict): 
    author = Author(**args)
    db.session.add(author)
    db.session.commit()
    
    return jsonify({
        'success':True,
        'data': args
    }),201
    
@app.route('/api/ver1/authors/<int:author_id>',methods=['PUT'])
@validate_content_type_json
@use_args(author_schema,error_status_code=400)
def update_author(args: dict, author_id: int):
    author = Author.query.get_or_404(author_id,description=f'No author with id {author_id} in the database')
    author.first_name = args['first_name']
    author.first_name = args['last_name']
    author.first_name = args['date_of_birth']
    
    db.session.commit()
    return jsonify({
        'success':True,
        'data': author_schema.dump(author)
    }),200
    
@app.route('/api/ver1/authors/<int:author_id>',methods=['DELETE'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id,description=f'No author with id {author_id} in the database') 
    db.session.delete(author)
    db.session.commit()
    return jsonify({
        'success':True,
        'data': f'Author with id {author_id} was deleted from the database'
    })
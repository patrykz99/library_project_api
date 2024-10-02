from library_app import app
from flask import jsonify
from library_app.models import Author,Author_Schema,author_schema




@app.route('/api/ver1/authors')
def get_authors():
    author = Author.query.all()
    author_schema_list = Author_Schema(many=True)
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
def add_author():
    
    return jsonify({
        'success':True,
        'data': '"testing" ADDED NEW AUTHOR'
    }),201
    
@app.route('/api/ver1/authors/<int:author_id>',methods=['PUT'])
def update_author(author_id):
    
    return jsonify({
        'success':True,
        'data': f'"testing" UPDATED DATA OF AUTHOR {author_id}'
    })
    
@app.route('/api/ver1/authors/<int:author_id>',methods=['DELETE'])
def delete_author(author_id):
     
    return jsonify({
        'success':True,
        'data': f'"testing" DELETED DATA OF AUTHOR {author_id}'
    })
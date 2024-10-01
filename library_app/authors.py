from library_app import app
from flask import jsonify,request



@app.route('/api/ver1/authors')
def get_authors():
    return jsonify({
        'success':True,
        'data': '"testing" GET DATA OF AUTHORS'
    })
    
@app.route('/api/ver1/authors/<int:author_id>')
def get_author(author_id):
    
    # if data[author_id] == author_id:
    return jsonify({
        'success':True,
        'data': f'"testing" GET DATA OF AUTHOR {author_id}'
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
from library_app import app,db
from flask import jsonify



class ErrorResponse:
    def __init__(self,mess: str, http_status: int):
        self.payload = {
            'success': False,
            'response_message': mess
        }
        self.http_status = http_status
    def to_response(self):
        response = jsonify(self.payload)
        response.status_code = self.http_status
        return response
    
@app.errorhandler(404)
def error_not_found(e):
    return ErrorResponse(e.description,404).to_response()

@app.errorhandler(400)
def error_bad_request(e):
    if 'fields' in e.description:
        return ErrorResponse(e.description,400).to_response() 
    print(e)    
    error_message = e.data.get('messages',{}).get('json',{})
    return ErrorResponse(error_message,400).to_response()

@app.errorhandler(415)
def error_unsupported_media_type(e):
    return ErrorResponse(e.description,415).to_response()

@app.errorhandler(500)
def error_internal_server(e):
    #Reset session db
    db.session.rollback()
    return ErrorResponse(e.description,500).to_response()
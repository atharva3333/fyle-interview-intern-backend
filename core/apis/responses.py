from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))
    
    @classmethod
    def respond_error(cls, message, status_code):
        error_data = {'error': message}
        return make_response(jsonify(error_data), status_code)
    
    @classmethod
    def respond_status_code(cls, status_code):
        return make_response('', status_code)

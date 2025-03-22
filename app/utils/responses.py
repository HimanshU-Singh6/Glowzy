from flask import jsonify

def success_response(message, data=None, status_code=200):
    resp = {"message": message}
    if data is not None:
        resp['data'] = data
    return jsonify(resp), status_code

def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code
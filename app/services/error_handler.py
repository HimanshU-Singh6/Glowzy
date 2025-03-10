from flask import jsonify

def handle_validation_error(err):
    return jsonify({"error": err.messages}), 400

def handle_server_error(err):
    return jsonify({"error": str(err)}), 500
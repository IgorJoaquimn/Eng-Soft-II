import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import process_request, UPLOAD_FOLDER
import traceback

app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/submit', methods=['POST'])
def submit_data():
        response = process_request(request)
        print(response)
        return response

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": error.description}), 400

@app.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

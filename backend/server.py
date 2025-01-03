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
    try:
        return process_request(request) 

    except Exception as e:
        print(traceback.format_exc())
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from extractInfo import getInfosFromText
from utils import process_file, UPLOAD_FOLDER

app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/submit', methods=['POST'])
def submit_data():
    try:
        if request.is_json:
            data = request.get_json()
            text = data.get('text', "")
            return jsonify(getInfosFromText(text))
        
        # Check if it's a multipart form data request (file upload)
        if request.files:
            return jsonify(getInfosFromText(process_file(request)))
        
        # If neither JSON nor file
        return jsonify({"error": "Invalid request format"}), 400
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

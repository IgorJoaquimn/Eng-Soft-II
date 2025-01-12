import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import process_request, UPLOAD_FOLDER
import traceback
from GeminiGenerator import GeminiGenerator

app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check if upload directory exists and is writable
        if not os.path.exists(UPLOAD_FOLDER):
            return jsonify({
                "status": "error",
                "message": "Upload directory not found",
                "checks": {
                    "upload_directory": False,
                    "gemini_api": None
                }
            }), 500
            
        if not os.access(UPLOAD_FOLDER, os.W_OK):
            return jsonify({
                "status": "error",
                "message": "Upload directory not writable",
                "checks": {
                    "upload_directory": False,
                    "gemini_api": None
                }
            }), 500

        # Test Gemini API connection
        llm = GeminiGenerator()
        test_prompt = "Test connection"
        try:
            llm.generate(test_prompt)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gemini API connection failed",
                "checks": {
                    "upload_directory": True,
                    "gemini_api": False
                }
            }), 500

        # All checks passed
        return jsonify({
            "status": "healthy",
            "message": "All systems operational",
            "checks": {
                "upload_directory": True,
                "gemini_api": True
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Health check failed: {str(e)}",
            "checks": {
                "upload_directory": None,
                "gemini_api": None
            }
        }), 500

@app.route('/api/submit', methods=['POST'])
def submit_data():
        response = process_request(request)
        return response

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": error.description}), 400

@app.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

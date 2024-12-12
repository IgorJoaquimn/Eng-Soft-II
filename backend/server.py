import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from extractInfo import getInfosFromText

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/submit', methods=['POST'])
def submit_data():
    try:
        if request.is_json:
            data = request.get_json()
            text = data.get('text', "")

            return jsonify(getInfosFromText(text))
        
        # Check if it's a multipart form data request (file upload)
        elif request.files:
            # Get the file
            file = request.files.get('file')
            
            if file:
                # Save the file
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                
                print(f"Received File:")
                print(f"Filename: {file.filename}")
                print(f"Filepath: {filepath}")
                
                # Read file content
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("File Content:")
                    print(content)
                
                # Example mock response for file upload
                return jsonify([
                    {"id": 1, "filename": file.filename, "file_size": len(content)},
                    {"id": 2, "name": "File Processing", "details": "File processed successfully"}
                ])
            else:
                return jsonify({"error": "No file received"}), 400
        
        # If neither JSON nor file
        else:
            return jsonify({"error": "Invalid request format"}), 400
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
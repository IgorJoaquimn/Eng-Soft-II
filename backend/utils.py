import os
from flask import jsonify

UPLOAD_FOLDER = 'uploads'

def process_file(request):
    # Get the file
    file = request.files.get('file')

    if not file: return jsonify({"error": "No file received"}), 400

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

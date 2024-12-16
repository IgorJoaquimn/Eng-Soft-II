import os
from flask import jsonify

UPLOAD_FOLDER = 'uploads'

def process_file(request):

    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file received"}), 400
    
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    allowed_extensions = {'txt', 'pdf', 'docx', 'doc'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({"error": "Unsupported file type"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath, 'r', encoding='UTF-8') as f:
        content = f.read(1024 * 1024)

        return content
import os
from flask import jsonify
from extractInfo import getInfosFromText

UPLOAD_FOLDER = 'uploads'

def process_request(request):
    if request.is_json:
        data = request.get_json()
        text = data.get('text', "")
        return jsonify(getInfosFromText(text))

    # Check if it's a multipart form data request (file upload)
    if request.files:
        error_message = validate_file_input(request)
        if error_message != "":
            return jsonify({"error": error_message}), 400

        text = process_file(request)
        return jsonify(getInfosFromText(text))

    return jsonify({"error": "Invalid request format"}), 400

def process_file(request):

    file = request.files.get('file')

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath, 'r', encoding='UTF-8') as f:
        content = f.read(1024 * 1024)

        return content

def validate_file_input(request):

    file = request.files.get('file')
    if not file:
        return "No file received"

    if not file.filename:
        return "Empty filename"

    allowed_extensions = {'txt', 'pdf', 'docx', 'doc'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return "Unsupported file type"

    return ""

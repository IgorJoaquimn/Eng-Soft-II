import os
from flask import jsonify, abort
from extractInfo import getInfosFromText
import pdfplumber

UPLOAD_FOLDER = 'uploads'

def process_request(request):
    # Check if it's a multipart form data request (file upload)
    if request.files:
        error_message = validate_file_input(request)
        if error_message != "":
            abort(400, description=error_message)

        text = process_file(request)
        return jsonify(getInfosFromText(text))

    if request.is_json:
        data = request.get_json()
        text = data.get('text', "")
        return jsonify(getInfosFromText(text))

    abort(400, description="Invalid request format")

def process_file(request):
    file = request.files.get('file')
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    if file.filename.lower().endswith('.pdf'):
        with pdfplumber.open(filepath) as pdf:
            content = ""
            for page in pdf.pages:
                content += page.extract_text() + "\n"
    else:
        with open(filepath, 'r', encoding='UTF-8', errors="ignore") as f:
            content = f.read(1024 * 1024)
    
    return content

def validate_file_input(request):

    file = request.files.get('file')
    if not file:
        abort(400, description="No file received")

    if not file.filename:
        abort(400, description="Empty filename")

    allowed_extensions = {'txt', 'pdf', 'docx', 'doc'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        abort(400, description="Unsupported file type")

    return ""

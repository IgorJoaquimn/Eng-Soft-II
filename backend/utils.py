import os
from flask import jsonify

UPLOAD_FOLDER = 'uploads'

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
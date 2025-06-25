import os
from werkzeug.utils import secure_filename
from pathlib import Path




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def remove_files(folder):
    for file in folder.iterdir():
        if file.is_file():
            file.unlink()

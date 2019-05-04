#!/usr/bin/env python3

__author__ = "Aurryon SCHWARTZ"
__copyright__ = "Copyright (C) 2019 StarAurryon"
__license__ = "MIT"
__version__ = "1.0"

from flask import Flask, request, render_template, send_from_directory, url_for
from werkzeug.utils import secure_filename
import filetype, os, stat as st, uuid

ALLOWED_EXTENSIONS = set(['flac', 'mp3', 'ogg', 'wav'])
IN_PATH = 'data/in/'
OUT_PATH = 'data/out/'

app = Flask(__name__)

@app.route("/check/<string:filename>", methods=["GET"])
def check_page(filename):
    filename = secure_filename(filename)

    in_files = [f for f in os.listdir(IN_PATH)
        if os.path.isfile(os.path.join(IN_PATH, f))]
    if not filename in in_files:
        return render_template('error.html')

    out_files = [f for f in os.listdir(OUT_PATH)
        if os.path.isfile(os.path.join(OUT_PATH, f))]
    if not filename in out_files:
        return render_template('inprogress.html')

    return render_template('done.html', link = url_for("download", filename = filename))

@app.route("/download/<string:filename>", methods=["GET"])
def download(filename):
    filename = secure_filename(filename)
    out_files = [f for f in os.listdir(OUT_PATH) if os.path.isfile(os.path.join(OUT_PATH, f))]
    if filename in out_files:
        result = send_from_directory(OUT_PATH, out_files[0], as_attachment=True)
        return result
    return render_template('error.html')

@app.route("/", methods=["GET"])
def upload_page():
    return render_template('upload.html')

@app.route("/", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return 'ERROR: No file part'

    file = request.files['file']

    if file.filename == '':
        return 'ERROR: No selected file'

    if not filetype.audio(file.read()):
        return 'ERROR: Not audio file'

    filename = secure_filename(file.filename)
    _, file_ext = os.path.splitext(filename)

    filename = str(uuid.uuid4()) + file_ext
    file.save(IN_PATH + filename)
    return "OK"

if __name__ == '__main__':
    app.run()

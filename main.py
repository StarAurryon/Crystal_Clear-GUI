#!/usr/bin/env python3

__author__ = "Aurryon SCHWARTZ"
__copyright__ = "Copyright (C) 2019 StarAurryon"
__license__ = "MIT"
__version__ = "1.0"

from flask import Flask, request, redirect, render_template, send_from_directory, url_for, make_response
from werkzeug.utils import secure_filename
import filetype, os, stat as st, uuid


ALLOWED_EXTENSIONS = set(['.flac', '.mp3', '.ogg', '.wav'])
IN_PATH = 'data/in/'
OUT_PATH = 'data/out/'
SAMPLES_PATH = 'data/samples/'

app = Flask(__name__)

@app.route("/check/<string:filename>", methods=["GET"])
def check(filename):
    if request.method == 'GET':
        filename = secure_filename(filename)
        in_files = [f for f in os.listdir(IN_PATH)
            if os.path.isfile(os.path.join(IN_PATH, f))]
        if not filename in in_files:
            response = make_response(render_template('error.html'))
            response.delete_cookie('filename')
            return response
        out_files = [f for f in os.listdir(OUT_PATH)
            if os.path.isfile(os.path.join(OUT_PATH, f))]
        if not filename in out_files:
            return render_template('inprogress.html')

        return render_template('done.html',
                               link = url_for("download", filename = filename),
                               link_upload = url_for("upload_page"))
    if request.method == 'POST':
        pass


@app.route("/download/<string:filename>", methods=["GET"])
def download(filename):
    filename = secure_filename(filename)
    out_files = [f for f in os.listdir(OUT_PATH) if os.path.isfile(os.path.join(OUT_PATH, f))]
    if filename in out_files:
        result = send_from_directory(OUT_PATH, filename, as_attachment=True)
        return result
    return render_template('error.html')

@app.route("/samples", methods = ["GET"])
def show_samples():
    return render_template('samples.html')

@app.route("/samples/original/<string:filename>", methods=["GET"])
def get_original_sample(filename):
    filename = secure_filename(filename)
    path = f'{SAMPLES_PATH}original/'
    samples_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    if filename in samples_files:
        result = send_from_directory(path, filename, as_attachment=True)
        return result
    return render_template('error.html')

@app.route("/samples/reconstructed/<string:filename>", methods=["GET"])
def get_reconstructed_sample(filename):
    filename = secure_filename(filename)
    path = f'{SAMPLES_PATH}reconstructed/'
    samples_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    if filename in samples_files:
        result = send_from_directory(path, filename, as_attachment=True)
        return result
    return render_template('error.html')

@app.route("/", methods=["GET"])
def upload_page():
    try:
        filename = request.cookies['filename']
        return redirect(url_for("check", filename=filename))
    except KeyError:
        return render_template('upload.html')

@app.route("/", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return render_template('error.html')

    file = request.files['file']

    if file.filename == '':
        return render_template('error.html')

    filename = secure_filename(file.filename)
    _, file_ext = os.path.splitext(filename)

    if not file_ext in ALLOWED_EXTENSIONS:
        return render_template('error.html')

    if not filetype.audio(file.read()):
        return render_template('error.html')

    file.seek(0)
    filename = str(uuid.uuid4()) + file_ext
    file.save(IN_PATH + filename)
    response = make_response(redirect(url_for("check", filename = filename)))
    response.set_cookie('filename', filename, max_age=3600)
    return response

@app.route("/about", methods=["GET"])
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()

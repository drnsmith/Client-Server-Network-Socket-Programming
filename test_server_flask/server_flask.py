from flask import send_from_directory
import os
import tempfile

import pprint
import click
import json
import xml.etree.ElementTree as ET


from flask import Flask, flash, request, redirect, url_for
from flask import Blueprint
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet

from os import listdir
from os.path import isfile, join

UPLOAD_FOLDER = './uploads'
TEMP_FOLDER = './temp'

ALLOWED_EXTENSIONS = {'txt'}

pp = pprint.PrettyPrinter(indent=2)


def echo_file(file):
    print()
    print(file.read())
    print()


def echo_data(data, content_type):

    assert content_type.lower() in ['application/json', 'application/xml',
                                    'application/octet-stream'], f"Invalid content_type found: {content_type}"

    print()
    print(f"Echoing data upload, content type: {content_type}")

    if (content_type == "application/json"):
        parsed = json.loads(data)
        data = json.dumps(parsed, indent=2)

    if (content_type == "application/xml"):
        parsed = ET.fromstring(data)
        data = ET.tostring(parsed, encoding='unicode')

    print(data)
    print()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


@click.command("run")
@click.option('--key', default="testing_key", help="The encryption string")
@click.option('--echo', is_flag=True, show_default=True,
              default=False, help="Echo the contents")
def run(key, echo):
    app.debug = True
    app.secret_key = b'_5#y2L"fdfsef44$2llm]/'
    app.config['key'] = key
    app.config['echo'] = echo
    print(" * Encryption key:", key)
    print(" * Will echo contents: ", echo)
    app.run()


app.add_url_rule(
    "/files/<name>", endpoint="download_file", build_only=True
)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/dictionaries', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        print(request.headers['Content-Type'])
        if (app.config['echo']):
            echo_data(request.data, request.headers['Content-Type'])

        temp_name = next(tempfile._get_candidate_names())
        with open(os.path.join(UPLOAD_FOLDER, temp_name), 'wb') as f:
            print("wrting file ", f, request.data)
            print(
                "location ",
                UPLOAD_FOLDER,
                temp_name,
                os.path.join(
                    UPLOAD_FOLDER,
                    temp_name))
            f.write(request.data)

    return ''


@app.route('/files/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


@app.route('/files', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # print(file)
        # print(request)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if (app.config['echo']):
                echo_file(file)

            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return "OK"
        else:
            print(
                "not a valid file",
                file,
                file.filename,
                allowed_file(
                    file.filename))
            return "opps", 400

    if request.method == 'GET':
        uploads = []
        for f in listdir(UPLOAD_FOLDER):
            if isfile(join(UPLOAD_FOLDER, f)) and f.endswith('.txt'):
                uploads.append(f)

        return uploads


if __name__ == '__main__':
    run()
# @click.group()
# @click.option('--key', default="testing_key", help="The encryption string")
# @click.option('--echo', is_flag=True, show_default=True, default=False, help="Echo the contents")

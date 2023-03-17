import requests
import click # https://dbader.org/blog/python-commandline-tools-with-click
import pprint
import tempfile
import json

from os.path import exists
from cryptography.fernet import Fernet
from dicttoxml import dicttoxml

key = Fernet.generate_key()
fernet = Fernet(key)

pp = pprint.PrettyPrinter(indent=2)

SERVER = "http://127.0.0.1"
# SERVER = "localhost"
PORT = "5000"
FILE_UPLOAD_PATH = "/files"
DICT_UPLOAD_PATH = "/dictionaries"


def encrypt(contents):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(contents)
    return encrypted


def send_file(session, file, url):
    try:
        print('sending file', file)
        f = open(file, 'rb')
        files = {"file": (file, f)}
        r = session.post(url, files=files)
        assert r.status_code == 200, f"status code not 200, got: {r.status_code}"
        print("File uploaded")
    finally:
        f.close()


def send_dict(session, dict, url, format, _encrypt):
    format = format.lower()
    assert format in [
        'json', 'xml', 'binary'], "Invalid format, must be one of [binary|JSON|XML]"

    content_types = {
        'json': "application/json",
        'xml': 'application/xml',
        'binary': 'application/octet-stream'
    }

    headers = {'Content-type': content_types[format.lower()]}
    r = requests.get(url, headers=headers)

    if (format == "json"):
        data = json.dumps(dict)
        print('sending json', data)

    if (format == "xml"):
        # data = xml = dicttoxml(data, custom_root='test', attr_type=False)
        data = xml = dicttoxml(dict)
        print('sending xml', data)

    if (format == "binary"):
        data = json.dumps(dict).encode('utf-8')
        print('sending binary', data)

    if (_encrypt):
        data = encrypt(data)

    r = session.post(url, data=data, headers=headers)
    assert r.status_code == 200, f"status code not 200, got: {r.status_code}"
    print("dict uploaded")


def get_dict():
    # could use the below to capture a dict via user input (UNTESTED)
    # while (True):
    #     d = dict()
    #     entry = click.prompt("key, value", type=str, default="key,value")
    #     key = entry.split(',')[0]
    #     value = entry.split(',')[1]
    #     d[key] = value
    #     more = click.prompt("continue Y,n", type=str, default="n")
    #     if (more.lower() == "n"):
    #         break

    d = {
        'key1': 1,
        'key2': 2,
        'key3': 3,
        'key4': 4,
    }
    return d


def validate_argument(ctx, param, value):
    if value.lower() in ['file', 'dict']:
        return (value)
    else:
        raise click.BadParameter(
            'Invalid argument, must be one of [file|dict]')


def validate_pickle_format(ctx, param, value):
    if value.lower() in ['json', 'xml', 'binary']:
        return (value)
    else:
        raise click.BadParameter(
            'Invalid format, must be one of [binary|JSON|XML]')


# @click.group()
# @click.option('--base_url',
#               default='%s:%s' % (SERVER,
#                                  PORT),
#               show_default=True,
#               prompt="The base url (scheme://host:port)",
#               help="The base url (scheme://host:port)")
# @click.option('--key', default="testing_key", help="The encryption string")
# @click.option('--encrypt', is_flag=True, show_default=True,
#               default=False, help="Encrypt the contents")
# @click.pass_context
def run(ctx, base_url, key, encrypt):
    print()
    print("Client configuration:")
    print(f"base_url: {base_url}")
    print(f"Encrypt: {encrypt}")
    print(f"Encryption key: {key}")
    print()

    ctx.obj['base_url'] = base_url
    ctx.obj['encrypt'] = encrypt
    ctx.obj['key'] = key

    # print(base_url, key, encrypt, file)

    # print("connecting to", url)
    session = requests.Session()
    options = session.options(base_url)

    assert options.status_code == 200, f"status code not 200, got: {options.status_code}"

    ctx.obj['session'] = session
    print("connection successful")


# @run.command()
# @click.pass_context
# @click.option('--file',
#               default="temp.txt",
#               help="The path to the file to send",
#               type=click.Path(exists=True))
def file(ctx, file):
    url = ctx.obj['base_url'] + FILE_UPLOAD_PATH
    print('file', file, ctx.obj, url)

    if (ctx.obj['encrypt']):
        with open(file, 'rb') as f:
            temp = tempfile.NamedTemporaryFile(suffix=".txt")
            try:
                temp.write(encrypt(f.read()))
                temp.seek(0)
                send_file(ctx.obj['session'], temp.name, url)
            finally:
                temp.close()

    else:
        send_file(ctx.obj['session'], file, url)

    # try:
    #     temp.write(encrypted)
    #     temp.seek(0)

    #     print("==========\n",temp.read())
    #     send_file(ctx.obj['session'], temp, url)
    # finally:
    #     temp.close()


# @run.command()
# @click.pass_context
# @click.option('--format',
#               default="JSON",
#               prompt="Choose your serialisation format [binary|JSON|XML]",
#               help="If sending a dict, choose your pickling format [binary|JSON|XML]",
#               callback=validate_pickle_format)
def dict(ctx, format):
    url = ctx.obj['base_url'] + DICT_UPLOAD_PATH
    print('dict', format, url)
    data = get_dict()

    send_dict(ctx.obj['session'], data, url, format, ctx.obj['encrypt'])


if __name__ == "__main__":
    run(obj={})


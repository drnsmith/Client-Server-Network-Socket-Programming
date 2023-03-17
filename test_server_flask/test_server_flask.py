import pytest
import os

from io import BytesIO as BytesIO

from server import app as flask_app
from server import UPLOAD_FOLDER as UPLOAD_FOLDER


def setup():
    with open(os.path.join(UPLOAD_FOLDER, "uploaded-file.txt"), 'w') as f:
        f.write("some data")

    with open("file.txt", 'w') as f:
        f.write("some data")


def tear_down():
    files = os.listdir(UPLOAD_FOLDER)
    for f in files:
        if f.endswith(".txt"):
            os.remove(os.path.join(UPLOAD_FOLDER, f))

    os.remove("file.txt")


@pytest.fixture
def app():
    setup()
    flask_app.config['echo'] = True
    yield flask_app
    tear_down()


@pytest.fixture
def client(app):

    return app.test_client()


def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200


def test_get_files(client):
    response = client.get("/files")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_post_file(client):

    response = client.get("/files")
    assert response.status_code == 200
    assert len(response.json) == 1

    try:
        file = "file.txt"
        f = open(file, 'rb')
        # (io.BytesIO(b"abcdef"), 'test.jpg')
        data = dict(
            file=(BytesIO(f.read()), file),
        )
        # data = {"file": (file, f)}
        response = client.post(
            "/files",
            data=data,
            follow_redirects=True,
            content_type='multipart/form-data')
        assert response.status_code == 200
        assert response.text == 'OK'

    finally:
        f.close()

    response = client.get("/files")
    assert response.status_code == 200
    assert len(response.json) == 2


def test_post_nontxt_file(client):

    with open("file.nontxt", 'w') as f:
        f.write("some data")

    try:
        file = "file.nontxt"
        f = open(file, 'rb')
        data = dict(
            file=(BytesIO(f.read()), file),
        )
        # data = {"file": (file, f)}
        response = client.post(
            "/files",
            data=data,
            follow_redirects=True,
            content_type='multipart/form-data')
        assert response.status_code != 200

    finally:
        f.close()
        os.remove("file.nontxt")

    response = client.get("/files")
    assert response.status_code == 200
    assert len(response.json) == 1

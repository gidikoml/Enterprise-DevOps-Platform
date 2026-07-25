import os
import sys
import pytest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app
from database import db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
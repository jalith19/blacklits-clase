import os
import pytest
from flask import Flask
from flask_cors import CORS

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["BEARER_TOKEN"] = "test-bearer-token"

from src.db.database import db, create_tables
from src.routes.blacklist_router import blacklist_bp


@pytest.fixture
def app():
    """Create and configure a fresh Flask app for testing."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    db.init_app(app)
    app.register_blueprint(blacklist_bp)

    with app.app_context():
        create_tables(app)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Default authorization headers for protected endpoints."""
    return {"Authorization": "Bearer test-bearer-token"}

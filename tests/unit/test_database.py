import pytest
from flask import Flask

from src.db.database import init_db, create_tables, db
from src.db.models import Blacklist


def test_init_db_with_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    app = Flask(__name__)
    result = init_db(app)
    assert result is db
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False


def test_init_db_without_url_raises(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    app = Flask(__name__)
    with pytest.raises(ValueError):
        init_db(app)


def test_create_tables(app):
    create_tables(app)
    with app.app_context():
        # table exists and is usable
        entry = Blacklist(
            id="x",
            email="a@b.com",
            app_uuid="123e4567-e89b-12d3-a456-426614174000",
            blocked_reason=None,
            ip_address="10.0.0.1",
        )
        db.session.add(entry)
        db.session.commit()
        found = db.session.query(Blacklist).filter_by(email="a@b.com").first()
        assert found is not None
        assert found.id == "x"

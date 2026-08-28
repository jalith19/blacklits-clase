import pytest
from sqlalchemy.exc import IntegrityError

from src.repositories.blacklist_repository import BlacklistRepository
from src.db.database import db
from src.db.models import Blacklist
from src.models.errors import ConflictError


@pytest.fixture
def repo(app):
    return BlacklistRepository()


def default_data(**overrides):
    data = {
        "id": "id-1",
        "email": "user@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "spam",
        "ip_address": "10.0.0.1",
    }
    data.update(overrides)
    return data


def test_create_success(repo, app):
    entry = repo.create(default_data())
    assert entry.email == "user@example.com"
    assert entry.id == "id-1"


def test_create_duplicate_raises_conflict(repo, app):
    repo.create(default_data())
    with pytest.raises(ConflictError):
        repo.create(default_data(email="user@example.com", id="id-2"))


def test_create_integrity_error_rethrows(repo, app):
    # Missing required field (ip_address) triggers IntegrityError that is not a unique violation
    with pytest.raises(IntegrityError):
        repo.create(default_data(ip_address=None, email="other@example.com", id="id-x"))


def test_get_by_email_found(repo, app):
    repo.create(default_data())
    entry = repo.get_by_email("user@example.com")
    assert entry is not None
    assert entry.email == "user@example.com"


def test_get_by_email_not_found(repo, app):
    entry = repo.get_by_email("missing@example.com")
    assert entry is None


def test_exists_by_email_true(repo, app):
    repo.create(default_data())
    assert repo.exists_by_email("user@example.com") is True


def test_exists_by_email_false(repo, app):
    assert repo.exists_by_email("missing@example.com") is False

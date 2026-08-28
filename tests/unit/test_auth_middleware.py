import os
from flask import jsonify
from src.middleware.auth_middleware import require_bearer_token


def test_require_token_missing_header(app):
    client = app.test_client()
    resp = client.post(
        "/blacklists",
        json={"email": "a@b.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"},
    )
    assert resp.status_code == 401
    body = resp.get_json()
    assert body["error"] == "Unauthorized"
    assert "missing" in body["message"].lower()


def test_require_token_invalid_format(app):
    client = app.test_client()
    resp = client.post(
        "/blacklists",
        headers={"Authorization": "Basic abc123"},
        json={"email": "a@b.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"},
    )
    assert resp.status_code == 401


def test_require_token_wrong_token(app):
    client = app.test_client()
    resp = client.post(
        "/blacklists",
        headers={"Authorization": "Bearer wrong-token"},
        json={"email": "a@b.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"},
    )
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Unauthorized"


def test_require_token_correct_token(app):
    client = app.test_client()
    resp = client.post(
        "/blacklists",
        headers={"Authorization": "Bearer test-bearer-token"},
        json={"email": "a@b.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"},
    )
    # Should pass auth and reach the handler (201 for valid data)
    assert resp.status_code == 201


def test_require_token_no_env_var(monkeypatch, app):
    monkeypatch.delenv("BEARER_TOKEN", raising=False)
    client = app.test_client()
    resp = client.post(
        "/blacklists",
        headers={"Authorization": "Bearer test-bearer-token"},
        json={"email": "a@b.com", "app_uuid": "123e4567-e89b-12d3-a456-426614174000"},
    )
    assert resp.status_code == 500


def test_require_token_decorator_function(app):
    @require_bearer_token
    def protected():
        return jsonify({"ok": True}), 200

    app.add_url_rule("/protected", "protected", protected)
    client = app.test_client()
    resp = client.get("/protected", headers={"Authorization": "Bearer test-bearer-token"})
    assert resp.status_code == 200

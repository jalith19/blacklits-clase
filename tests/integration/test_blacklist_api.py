VALID_UUID = "123e4567-e89b-12d3-a456-426614174000"


def create_entry(client, auth_headers, email="user@example.com", app_uuid=VALID_UUID,
                 blocked_reason="spam", **extra_headers):
    return client.post(
        "/blacklists",
        headers={**auth_headers, **extra_headers},
        json={
            "email": email,
            "app_uuid": app_uuid,
            "blocked_reason": blocked_reason,
        },
    )


def test_create_success(client, auth_headers):
    resp = create_entry(client, auth_headers)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["email"] == "user@example.com"
    assert "added to blacklist" in body["message"]
    assert body["id"]
    assert body["created_at"]


def test_create_without_reason(client, auth_headers):
    resp = client.post(
        "/blacklists",
        headers=auth_headers,
        json={"email": "no-reason@example.com", "app_uuid": VALID_UUID},
    )
    assert resp.status_code == 201


def test_create_missing_body(client, auth_headers):
    resp = client.post("/blacklists", headers=auth_headers)
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Bad Request"


def test_create_invalid_email(client, auth_headers):
    resp = client.post(
        "/blacklists",
        headers=auth_headers,
        json={"email": "not-an-email", "app_uuid": VALID_UUID},
    )
    assert resp.status_code == 400


def test_create_missing_uuid(client, auth_headers):
    resp = client.post(
        "/blacklists",
        headers=auth_headers,
        json={"email": "user@example.com"},
    )
    assert resp.status_code == 400


def test_create_invalid_uuid(client, auth_headers):
    resp = client.post(
        "/blacklists",
        headers=auth_headers,
        json={"email": "user@example.com", "app_uuid": "bad-uuid"},
    )
    assert resp.status_code == 400


def test_create_duplicate_conflict(client, auth_headers):
    create_entry(client, auth_headers, email="dup@example.com")
    resp = create_entry(client, auth_headers, email="dup@example.com")
    assert resp.status_code == 409
    assert resp.get_json()["error"] == "Conflict"


def test_create_stores_ip_from_forwarded_for(client, auth_headers):
    resp = create_entry(client, auth_headers, email="ip@example.com",
                        **{"X-Forwarded-For": "203.0.113.9, 10.0.0.1"})
    assert resp.status_code == 201


def test_check_blacklisted(client, auth_headers):
    create_entry(client, auth_headers, email="check@example.com", blocked_reason="fraud")
    resp = client.get(
        "/blacklists/check@example.com",
        headers=auth_headers,
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["is_blacklisted"] is True
    assert body["email"] == "check@example.com"
    assert body["blocked_reason"] == "fraud"


def test_check_not_blacklisted(client, auth_headers):
    resp = client.get(
        "/blacklists/unknown@example.com",
        headers=auth_headers,
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["is_blacklisted"] is False
    assert body["blocked_reason"] is None


def test_ping(client):
    resp = client.get("/blacklists/ping")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "pong"


def test_404_unknown_route(client, auth_headers):
    resp = client.get("/non-existent-route", headers=auth_headers)
    assert resp.status_code == 404

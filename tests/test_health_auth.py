import pytest

import config


@pytest.mark.smoke
@pytest.mark.regression
def test_ping_returns_201(client):
    response = client.ping()
    assert response.status_code == 201


@pytest.mark.regression
def test_ping_responds_quickly(client):
    response = client.ping()
    assert response.elapsed.total_seconds() < config.MAX_RESPONSE_SECONDS


@pytest.mark.smoke
@pytest.mark.regression
def test_valid_credentials_return_token(client):
    response = client.create_token(config.USERNAME, config.PASSWORD)
    assert response.status_code == 200
    assert response.json().get("token")


@pytest.mark.regression
def test_invalid_credentials_return_no_token(client):
    response = client.create_token(config.USERNAME, "wrong_password")
    body = response.json()
    assert "token" not in body
    assert "reason" in body

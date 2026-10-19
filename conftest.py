import pytest

import config
from api.client import BookerClient
from api.payloads import new_booking


@pytest.fixture
def client():
    return BookerClient()


@pytest.fixture(scope="session")
def token():
    """Auth token, requested once per run."""
    response = BookerClient().create_token(config.USERNAME, config.PASSWORD)
    assert response.status_code == 200, response.text
    value = response.json().get("token")
    assert value, f"No token in response: {response.text}"
    return value


@pytest.fixture
def booking(client, token):
    """A booking created for one test and deleted afterward, so tests stay independent."""
    payload = new_booking()
    response = client.create_booking(payload)
    assert response.status_code == 200, response.text
    booking_id = response.json()["bookingid"]
    yield {"id": booking_id, "payload": payload}
    client.delete_booking(booking_id, token=token)  # already-deleted bookings are fine

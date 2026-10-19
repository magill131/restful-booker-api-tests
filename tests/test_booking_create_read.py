import pytest
from jsonschema import validate

from api.payloads import new_booking
from api.schemas import BOOKING_SCHEMA, CREATE_RESPONSE_SCHEMA


@pytest.mark.smoke
@pytest.mark.regression
def test_create_booking_returns_id_and_echoes_data(client, token):
    payload = new_booking()
    response = client.create_booking(payload)
    try:
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body["bookingid"], int)
        assert body["booking"] == payload
    finally:
        if response.ok:
            client.delete_booking(response.json()["bookingid"], token=token)


@pytest.mark.regression
def test_create_booking_response_matches_schema(client, token):
    response = client.create_booking(new_booking())
    try:
        assert response.status_code == 200
        validate(instance=response.json(), schema=CREATE_RESPONSE_SCHEMA)
    finally:
        if response.ok:
            client.delete_booking(response.json()["bookingid"], token=token)


@pytest.mark.smoke
@pytest.mark.regression
def test_get_booking_returns_created_data(client, booking):
    response = client.get_booking(booking["id"])
    assert response.status_code == 200
    assert response.json() == booking["payload"]


@pytest.mark.regression
def test_get_booking_matches_schema(client, booking):
    response = client.get_booking(booking["id"])
    assert response.status_code == 200
    validate(instance=response.json(), schema=BOOKING_SCHEMA)


@pytest.mark.regression
def test_get_booking_returns_json_content_type(client, booking):
    response = client.get_booking(booking["id"])
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.regression
def test_list_bookings_contains_created_id(client, booking):
    response = client.list_bookings()
    assert response.status_code == 200
    ids = [item["bookingid"] for item in response.json()]
    assert booking["id"] in ids


@pytest.mark.regression
def test_list_bookings_items_have_integer_ids(client):
    response = client.list_bookings()
    assert response.status_code == 200
    items = response.json()
    assert len(items) > 0
    assert all(isinstance(item["bookingid"], int) for item in items)


@pytest.mark.regression
def test_filter_by_firstname_finds_booking(client, booking):
    response = client.list_bookings(firstname=booking["payload"]["firstname"])
    assert response.status_code == 200
    ids = [item["bookingid"] for item in response.json()]
    assert booking["id"] in ids

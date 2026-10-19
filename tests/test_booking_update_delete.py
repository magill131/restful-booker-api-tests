import pytest

from api.client import BookerClient
from api.payloads import new_booking


@pytest.mark.smoke
@pytest.mark.regression
def test_full_update_changes_all_fields(client, booking, token):
    updated = new_booking(lastname="Updated", totalprice=999, depositpaid=False)
    response = client.update_booking(booking["id"], updated, token=token)
    assert response.status_code == 200
    assert response.json() == updated
    assert client.get_booking(booking["id"]).json() == updated


@pytest.mark.regression
def test_update_with_basic_auth_header(client, booking):
    updated = new_booking(lastname="BasicAuth")
    response = client.update_booking(
        booking["id"], updated, headers=BookerClient.basic_auth_header()
    )
    assert response.status_code == 200
    assert response.json()["lastname"] == "BasicAuth"


@pytest.mark.regression
def test_update_without_auth_is_forbidden(client, booking):
    response = client.update_booking(booking["id"], new_booking(lastname="NoAuth"))
    assert response.status_code == 403
    assert client.get_booking(booking["id"]).json() == booking["payload"]


@pytest.mark.regression
def test_partial_update_changes_only_given_fields(client, booking, token):
    response = client.partial_update_booking(
        booking["id"], {"firstname": "Patched"}, token=token
    )
    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == "Patched"
    assert body["lastname"] == booking["payload"]["lastname"]
    assert body["totalprice"] == booking["payload"]["totalprice"]


@pytest.mark.regression
def test_partial_update_without_auth_is_forbidden(client, booking):
    response = client.partial_update_booking(booking["id"], {"firstname": "Nope"})
    assert response.status_code == 403


@pytest.mark.smoke
@pytest.mark.regression
def test_delete_booking_returns_201(client, booking, token):
    response = client.delete_booking(booking["id"], token=token)
    assert response.status_code == 201


@pytest.mark.regression
def test_deleted_booking_returns_404(client, booking, token):
    client.delete_booking(booking["id"], token=token)
    response = client.get_booking(booking["id"])
    assert response.status_code == 404


@pytest.mark.regression
def test_delete_without_auth_is_forbidden(client, booking):
    response = client.delete_booking(booking["id"])
    assert response.status_code == 403
    assert client.get_booking(booking["id"]).status_code == 200

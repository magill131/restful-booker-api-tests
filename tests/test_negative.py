import pytest


@pytest.mark.regression
def test_get_nonexistent_booking_returns_404(client):
    response = client.get_booking(99999999)
    assert response.status_code == 404


@pytest.mark.regression
def test_create_booking_with_missing_fields_is_rejected(client):
    response = client.create_booking({"firstname": "OnlyAName"})
    assert response.status_code in (400, 500)

import uuid


def new_booking(**overrides):
    """A valid booking body. The first name is unique so tests can find their own booking."""
    booking = {
        "firstname": f"Test{uuid.uuid4().hex[:8]}",
        "lastname": "Magill",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
        "additionalneeds": "Breakfast",
    }
    booking.update(overrides)
    return booking

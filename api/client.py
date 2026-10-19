import base64

import requests

import config


class BookerClient:
    """Thin wrapper around the Restful-Booker endpoints so tests read like steps."""

    def __init__(self, base_url=config.BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    # -- helpers -----------------------------------------------------------
    def _url(self, path):
        return f"{self.base_url}{path}"

    @staticmethod
    def _auth_headers(token=None, headers=None):
        merged = dict(headers or {})
        if token:
            merged["Cookie"] = f"token={token}"
        return merged

    @staticmethod
    def basic_auth_header(username=config.USERNAME, password=config.PASSWORD):
        encoded = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    # -- endpoints ---------------------------------------------------------
    def ping(self):
        return self.session.get(self._url("/ping"), timeout=config.TIMEOUT)

    def create_token(self, username, password):
        return self.session.post(
            self._url("/auth"),
            json={"username": username, "password": password},
            timeout=config.TIMEOUT,
        )

    def list_bookings(self, **filters):
        return self.session.get(
            self._url("/booking"), params=filters or None, timeout=config.TIMEOUT
        )

    def get_booking(self, booking_id):
        return self.session.get(self._url(f"/booking/{booking_id}"), timeout=config.TIMEOUT)

    def create_booking(self, payload):
        return self.session.post(self._url("/booking"), json=payload, timeout=config.TIMEOUT)

    def update_booking(self, booking_id, payload, token=None, headers=None):
        return self.session.put(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            headers=self._auth_headers(token, headers),
            timeout=config.TIMEOUT,
        )

    def partial_update_booking(self, booking_id, payload, token=None, headers=None):
        return self.session.patch(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            headers=self._auth_headers(token, headers),
            timeout=config.TIMEOUT,
        )

    def delete_booking(self, booking_id, token=None, headers=None):
        return self.session.delete(
            self._url(f"/booking/{booking_id}"),
            headers=self._auth_headers(token, headers),
            timeout=config.TIMEOUT,
        )

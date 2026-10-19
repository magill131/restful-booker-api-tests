"""Test configuration. The admin credentials are the demo ones published for Restful-Booker."""

import os

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")

USERNAME = "admin"
PASSWORD = "password123"

TIMEOUT = 30                 # seconds to wait for any single request
MAX_RESPONSE_SECONDS = 10    # generous: the public demo server can be slow to wake up

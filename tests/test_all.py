from fastapi.testclient import TestClient
from run import app
# from utils.db import fetch, execute
import asyncio

client = TestClient(app)
loop = asyncio.get_event_loop()


def get_auth_header():
    response = client.post("/token", dict(username="jbsg", password="1793"))
    jwt_token = response.json()["access_token"]

    auth_header = {"Authorization": f"Bearer {jwt_token}"}
    return auth_header


def test_get_user():
    auth_header = get_auth_header()
    response = client.get("/v1/user/jbsg", headers=auth_header)

    assert response.status_code == 200
    assert "access_token" in response.json()

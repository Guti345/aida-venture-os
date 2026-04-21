import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "postgresql://postgres:AIDAvc2026!@localhost:5432/aida_venture_os")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def auth_headers(client):
    resp = client.post("/auth/login", json={"email": "admin@aidaventures.co", "password": "AidaVC2025!"})
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

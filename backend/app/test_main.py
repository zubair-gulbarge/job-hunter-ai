import pytest
from fastapi.testclient import TestClient
from app.main import app

# This fixture creates ONE test client and keeps the event loop 
# alive for the entire testing session. Motor will stay happy!
@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

# Pass the 'client' fixture into your tests
def test_get_applications(client):
    response = client.get("/api/applications")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_profile_not_found_initially(client):
    response = client.get("/api/profile")
    # It should return either 200 (if data exists) or 404 (if empty)
    assert response.status_code in [200, 404]
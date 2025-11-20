import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json()["message"]
    # Unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert "Unregistered" in unregister_resp.json()["message"]
    # Unregister again should fail
    unregister_resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp2.status_code == 400
    assert "not registered" in unregister_resp2.json()["detail"]


def test_signup_duplicate():
    activity = "Chess Club"
    email = "daniel@mergington.edu"  # Already signed up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]


def test_activity_not_found():
    resp = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]

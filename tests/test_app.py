import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    # Arrange: No special setup needed

    # Act: Make GET request to root
    response = client.get("/", follow_redirects=False)

    # Assert: Check for redirect status and location
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    # Arrange: No special setup needed

    # Act: Make GET request to activities
    response = client.get("/activities")

    # Assert: Check status and response structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange: Use an activity that exists

    # Act: Attempt to sign up a new student
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

def test_signup_duplicate():
    # Arrange: Sign up first
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    # Act: Try to sign up again
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    # Assert: Check for error
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    # Arrange: Use a non-existent activity

    # Act: Attempt to sign up
    response = client.post("/activities/Invalid/signup?email=test@mergington.edu")

    # Assert: Check for not found error
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_remove_participant_success():
    # Arrange: Sign up a participant first
    client.post("/activities/Chess%20Club/signup?email=remove@mergington.edu")

    # Act: Remove the participant
    response = client.delete("/activities/Chess%20Club/participants/remove@mergington.edu")

    # Assert: Check success
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]

def test_remove_participant_not_found():
    # Arrange: Use a non-existent participant

    # Act: Attempt to remove
    response = client.delete("/activities/Chess%20Club/participants/nonexistent@mergington.edu")

    # Assert: Check for error
    assert response.status_code == 400
    data = response.json()
    assert "Participant not found" in data["detail"]

def test_remove_invalid_activity():
    # Arrange: Use a non-existent activity

    # Act: Attempt to remove participant
    response = client.delete("/activities/Invalid/participants/test@mergington.edu")

    # Assert: Check for not found error
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]
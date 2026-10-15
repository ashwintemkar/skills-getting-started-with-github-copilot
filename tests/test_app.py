"""Backend tests for Mergington High School activities API (AAA pattern)."""

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    # Arrange / Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]


def test_signup_for_activity():
    # Arrange
    activity = "Art Club"
    email = "newstudent@mergington.edu"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_prevent_duplicate_signup():
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400


def test_unregister_from_activity():
    # Arrange
    activity = "Drama Club"
    email = "temp@mergington.edu"
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

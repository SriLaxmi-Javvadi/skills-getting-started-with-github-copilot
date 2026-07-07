from fastapi.testclient import TestClient

from src import app as app_module


def test_remove_participant_from_activity():
    client = TestClient(app_module.app)
    activity = app_module.activities["Basketball Team"]
    original_participants = list(activity["participants"])

    try:
        response = client.delete("/activities/Basketball Team/participants/alex@mergington.edu")

        assert response.status_code == 200
        assert "alex@mergington.edu" not in activity["participants"]
        assert response.json()["message"] == "Removed alex@mergington.edu from Basketball Team"
    finally:
        activity["participants"] = original_participants


def test_activities_response_is_not_cached():
    client = TestClient(app_module.app)

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"].startswith("no-store")

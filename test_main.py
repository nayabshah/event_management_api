import pytest
from fastapi.testclient import TestClient
from main import app,Base
from datetime import datetime, timedelta
from database import engine,get_db,SessionLocal

DATABASE_URL = "sqlite:///./test.db" 
@pytest.fixture(scope='module',autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


# Sample data for testing
event_data = {
    "event_id": 1,
    "name": "Sample Event",
    "description": "This is a sample event.",
    "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
    "end_time": (datetime.now() + timedelta(days=2)).isoformat(),
    "location": "Sample Location",
    "max_attendees": 2,
    "status": "scheduled"
}

attendee_data_1 = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone_number": "1234567890",
    "event_id": 1
}

attendee_data_2 = {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "phone_number": "0987654321",
    "event_id": 1
}

attendee_data_3 = {
    "first_name": "Jim",
    "last_name": "Beam",
    "email": "jim.beam@example.com",
    "phone_number": "1122334455",
    "event_id": 1
}

# Test case for creating an event
def test_create_event(client):
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200
    assert response.json()["event_id"] == event_data["event_id"]

# Test case for registering attendees within limits
def test_register_attendees_within_limit(client):
    client.post("/events/", json=event_data)  # Create the event

    response_1 = client.post("/attendees/", json=attendee_data_1)
    assert response_1.status_code == 200

    response_2 = client.post("/attendees/", json=attendee_data_2)
    assert response_2.status_code == 200

# Test case for exceeding registration limits
def test_register_attendee_exceeding_limit(client):
    response = client.post("/attendees/", json=attendee_data_3)
    assert response.status_code == 400
    assert response.json()["detail"] == "Max attendees limit reached"

# Test case for checking in an attendee
def test_check_in_attendee(client):
    response = client.put("/attendees/checkin/", json={"attendee_id": 1})
    assert response.status_code == 200
    assert response.json()["check_in_status"] is True

# Test case for automatic status update
'''def test_automatic_status_update(client):
    #Create an event that has already ended
    past_event_data = {
        "event_id": 3,
        "name": "Past Event",
        "description": "This event has already ended.",
        "start_time": (datetime.now() - timedelta(days=2)).isoformat(),
        "end_time": (datetime.now() - timedelta(days=1)).isoformat(),
        "location": "Past Location",
        "max_attendees": 5,
        "status": "scheduled"
    }
    #client.post("/events/", json=past_event_data)

    # Fetch the event to check its status
    response = client.get("/events/3")
    assert response.status_code == 200
    assert response.json()["status"] == "completed" '''

# Run the test
if __name__ == "__main__":
    pytest.main()
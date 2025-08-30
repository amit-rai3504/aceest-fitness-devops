import pytest
from aceest_fitness import app, DB

@pytest.fixture(autouse=True)
def clear_db():
    # Reset in-memory DB before each test
    DB["workouts"].clear()
    yield

def test_health():
    client = app.test_client()
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.data.decode().strip() == "ok"

def test_index():
    client = app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["app"] == "ACEest Fitness & Gym"
    assert "Welcome" in data["message"]

def test_add_and_list_workouts_happy_path():
    client = app.test_client()

    # add one
    rv = client.post("/workouts", json={"workout": "Pushups", "duration": 15})
    assert rv.status_code == 201
    created = rv.get_json()
    assert created == {"workout": "Pushups", "duration": 15}

    # list
    rv = client.get("/workouts")
    assert rv.status_code == 200
    workouts = rv.get_json()
    assert workouts == [{"workout": "Pushups", "duration": 15}]

@pytest.mark.parametrize(
    "payload",
    [
        {},                                                # nothing
        {"workout": "Pushups", "duration": 0},            # zero duration
        {"workout": "Pushups", "duration": -5},           # negative duration
        {"workout": "Run", "duration": "fifteen"},        # non-integer duration
        {"workout": "   ", "duration": 10},               # whitespace name
        {"duration": 10},                                  # missing workout
        {"workout": "Squats"},                             # missing duration
    ],
)
def test_add_workout_validation_errors(payload):
    client = app.test_client()
    rv = client.post("/workouts", json=payload)
    assert rv.status_code == 400
    data = rv.get_json()
    assert "errors" in data and isinstance(data["errors"], list) and data["errors"]

def test_add_workout_with_non_json_body():
    client = app.test_client()
    rv = client.post("/workouts", data="not json", content_type="text/plain")
    assert rv.status_code == 400
    data = rv.get_json()
    assert "errors" in data and data["errors"]

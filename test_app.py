import pytest
from app import app, tasks


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        tasks.clear()   # clear memory before each test
        yield client


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Task"
    assert data["status"] == "pending"


def test_missing_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_update_status(client):
    response = client.post("/tasks", json={"title": "Task"})
    task_id = response.get_json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"status": "completed"})
    assert response.status_code == 200
    assert response.get_json()["status"] == "completed"


def test_filter_status(client):
    client.post("/tasks", json={"title": "Task 1"})
    response = client.get("/tasks?status=pending")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_delete_task(client):
    response = client.post("/tasks", json={"title": "Task"})
    task_id = response.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200


def test_invalid_status(client):
    response = client.post("/tasks", json={"title": "Task"})
    task_id = response.get_json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"status": "wrong"})
    assert response.status_code == 400


def test_non_existent_id(client):
    response = client.put("/tasks/invalid-id", json={"status": "completed"})
    assert response.status_code == 404

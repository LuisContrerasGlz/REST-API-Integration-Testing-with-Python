import uuid

import pytest
import requests

ENDPOINT = "https://todo.pixegami.io/"

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print(data)

    task_id = data["task"]["task_id"]
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

def test_can_update_task():
    # Create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # Update the task
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # Get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]

def test_can_list_tasks():
    # Create N tasks
    n = 3
    user_id = f"test_user_{uuid.uuid4().hex}"
    for _ in range(n):
        payload = new_task_payload(user_id=user_id)
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # List tasks and check that there are N items
    list_tasks_response = list_tasks(user_id)
    assert list_tasks_response.status_code == 200

    data = list_tasks_response.json()
    print(data)

    tasks = data["tasks"]
    assert len(tasks) == n

def test_can_delete_task():
    # Create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # Delete the task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    # Get the task and check that it is not found
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404

# Helper functions 

def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)
    
def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def new_task_payload(user_id=None):
    if user_id is None:
        user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

import pytest
import requests

ENDPOINT = "https://todo.pixegami.io/"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_tasl():
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
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # update the task
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]


def test_can_list_tasks():
    # Create N tasks
    n = 3
    for _ in range(n):
        payload = new_task_payload()
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # List tasks, and check that htere are N items
    list_tasks_response = list_tasks("test_user")
    assert list_tasks_response.status_code == 200

    data = list_tasks_response.json()
    print(data)

    tasks = data["tasks"]
    assert len(tasks) == n





def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)


def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)
    
def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def new_task_payload():
    return {
        "content": "my test content",
        "user_id": "test_user",
        "is_done": False
    }


def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


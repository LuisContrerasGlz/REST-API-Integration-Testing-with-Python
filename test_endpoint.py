import pytest
import requests

ENDPOINT = "https://todo.pixegami.io/"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_tasl():
    payload = {
        "content": "my test content",
        "user_id": "test_user",
        "is_done": False
    }
    response = requests.put(ENDPOINT + "/create-task", json=payload)
    assert response.status_code == 200


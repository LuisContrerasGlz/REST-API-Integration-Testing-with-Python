import pytest
import requests

ENDPOINT = "https://todo.pixegami.io/"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


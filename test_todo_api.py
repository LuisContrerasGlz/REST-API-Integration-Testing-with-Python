import requests

ENDPOINT = "https://todo.pixegami.io/"

response = requests.get(ENDPOINT)
print(response)
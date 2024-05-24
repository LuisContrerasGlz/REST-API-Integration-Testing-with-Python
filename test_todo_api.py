import requests

ENDPOINT = "https://todo.pixegami.io/"

response = requests.get(ENDPOINT)
print(response) 

data = response.json()
print(data)

status_code = response.status_code
print(status_code)
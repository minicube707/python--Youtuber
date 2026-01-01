
import requests

url = "https://jsonplaceholder.typicode.com/posts"

payload = {
    "title": "Hello from Python",
    "body": "This is a test post",
    "userID": 1
}

#Post Request
reponse = requests.post(url=url, json=payload)

print("Status code:", reponse.status_code)
data = reponse.json()
print(data)
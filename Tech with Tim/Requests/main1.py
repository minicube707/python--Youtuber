
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

#Get Request
reponse = requests.get(url)

print("Status code:", reponse.status_code)
print("Content-Type:", reponse.headers.get("Content-Type"))

data = reponse.json() #parse JSON into Python dict
print("Post title: ", data["title"])
print("Data: ", data)
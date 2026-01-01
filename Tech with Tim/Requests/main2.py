
import requests

url = "https://reqres.in/api/users"
params = {"page": 2}

#Get Request with multiple parameters
reponse = requests.get(url, params=params)
print("Final URL: ", reponse.url) #shows ?page=2

reponse.raise_for_status() #raise for error 4xx/5xx

data = reponse.json()
print("Page: ", data["page"])
for user in data["data"]:
    print(user["email"])
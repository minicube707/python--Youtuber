
import requests
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

#Get Requests
print("\nGet Request")
reponse = requests.get("https://httpbin.org/get")
print(reponse.text)


#Query Parameters
print("\nQuery Parameters")
params = {
    "name": "Mike",
    "age": 25
}

reponse = requests.get("https://httpbin.org/get", params=params)
print(reponse.url)
print(reponse.text)


#Post Requests
print("\nPost Requests")
payload = {
    "name": "Mike",
    "age": 25
}

reponse = requests.post("https://httpbin.org/post", data=payload)
print(reponse.url)


#Status Codes
print("\nStatus Codes")
reponse = requests.get("https://httpbin.org/status/200")
print(reponse.status_code)
reponse = requests.get("https://httpbin.org/status/404")
print(reponse.status_code)


#User-Agent
print("\nUser-Agent")
headers = {
    "User-Agent" : "Hello Wolrd/1.1"
}
reponse = requests.get("https://httpbin.org/user-agent")
print(reponse.text)
reponse = requests.get("https://httpbin.org/user-agent", headers=headers)
print(reponse.text)


#Images & File Types
print("\nImages & File Types")
headers = {
    "Accept" : "image/png"
}
reponse = requests.get("https://httpbin.org/image", headers=headers)
print(reponse.content)

#with open("myimage.png", "wb") as f:
#    f.write(reponse.content)

headers = {
    "Accept" : "image/jpeg"
}
reponse = requests.get("https://httpbin.org/image", headers=headers)
print(reponse.content)

#with open("myimage.jpeg", "wb") as f:
#    f.write(reponse.content)

#Requests Timeout
print("\nRequests Timeout")
for i in [1, 2, 3, 4, 5]:
    try:
        url = f"https://httpbin.org/delay/{i}"
        reponse = requests.get(url, timeout=3)
        print("Get reponse from ", url)
    except:
        print("Timeout from ", url)
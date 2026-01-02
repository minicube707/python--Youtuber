
import requests

#Get requests with authorization
r = requests.get("https://httpbin.org/basic-auth/corey/testing", auth=("corey", "testing"))
print("\nCorrect user")
print(r)
print(r.text)

#Wrong user
r = requests.get("https://httpbin.org/basic-auth/corey/testing", auth=("coreys", "testing"))
print("\nWrong user")
print(r)
print(r.text)


#Timeout
r = requests.get("https://httpbin.org/delay/1", timeout=3)
print("\nGet reponse: ", r)

r = requests.get("https://httpbin.org/delay/5", timeout=3)
print("\nGet no reponse: ", r)

import requests

payload = {
    "page": 2,
    "count": 25
}

#Get requests
r = requests.get("https://httpbin.org/get", params=payload)

print("\nText: ", r.text)

print("\nUrl", r.url)
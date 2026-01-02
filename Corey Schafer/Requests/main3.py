
import requests

payload = {
    "username": "corey",
    "password": "testing"
}

#Post requests
r = requests.post("https://httpbin.org/post", data=payload)

print("\nText: ", r.text)

print("\nUrl", r.url)

r_dict = r.json()
print("\nJson: ", r_dict)

print("\n'form': ", r_dict["form"])
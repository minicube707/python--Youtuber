import requests

# Proxy configuration (disabled for now - uncomment to route traffic through a proxy server)
proxies = {
    'https': 'https://154.64.231.208:8081'  # Proxy address and port
}

# Fetch IP information using proxy (disabled)
response = requests.get("https://ipinfo.io/json", proxies=proxies)

# Send a GET request to ipinfo.io to retrieve public IP information (no proxy)
# response = requests.get("https://ipinfo.io/json")

# Iterate over the JSON response and print each key-value pair
for key, value in response.json().items():
    print(f"{key} : {value}")
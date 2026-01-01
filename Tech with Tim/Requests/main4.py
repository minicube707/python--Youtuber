
import requests

#Error han  dling
try:
    #httpbin//delay/3 waits seconds before reponsding
    reponse = requests.get(url="https://httpbin.org/delay/3", timeout=1)
    reponse.raise_for_status()
    print("Success: ", reponse.json())
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e    :
    print("Request failed: ", e)
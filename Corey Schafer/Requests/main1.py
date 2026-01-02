
import requests
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

r = requests.get("https://xkcd.com/353/")

#print(dir(r))  All function we can call
#print(help(r)) If we need help

#Dispaly the html code
print(r.text)

r = requests.get("https://imgs.xkcd.com/comics/python.png")

#Display a picture
print(r.content)

#with open("comic.png", "wb") as f:
#    f.write(r.content)

#Get status of the reponse
print("\nStatus: ", r.status_code)

#Return true if the reponse is below 400
print("\nOk: ", r.ok)

# key-value pairs sent from the client to the server to provide context about the request
print("\nHeaders: ", r.headers)



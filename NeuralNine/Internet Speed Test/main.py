import speedtest 
import json

test = speedtest.Speedtest()


print("Loading server list...")
test.get_servers() # -> get list of servers
print("Choose best server...")
best = test.get_best_server() # -> choose best server


print(f"\nFound: {best['host']} located in {best['country']}")
print(json.dumps(best, indent=4))


print("\nPerforming  download test...")
download_result = test.download()
print("Performing  upload test...")
upload_result = test.upload()
ping_result = test.results.ping

print(f"Download speed: {download_result / 1024 / 1024:.2f} Mbit/s")
print(f"Upload speed: {upload_result / 1024 / 1024:.2f} Mbit/s")
print(f"Ping: {ping_result:.2f} ms")

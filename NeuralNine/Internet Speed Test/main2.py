
import requests
import time
import json

DOWNLOAD_SIZE = 25_000_000
UPLOAD_SIZE = 10_000_000

DOWNLOAD_URL = f"https://speed.cloudflare.com/__down?bytes={DOWNLOAD_SIZE}"
UPLOAD_URL = "https://speed.cloudflare.com/__up"


def test_ping():
    times = []

    for _ in range(5):
        start = time.perf_counter()

        response = requests.get(
            "https://speed.cloudflare.com/",
            timeout=10
        )

        response.raise_for_status()

        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)

    return sum(times) / len(times)


def test_download():
    start = time.perf_counter()

    response = requests.get(
        DOWNLOAD_URL,
        timeout=60
    )

    response.raise_for_status()

    elapsed = time.perf_counter() - start
    size = len(response.content)

    return (size * 8) / elapsed / 1_000_000


def test_upload():
    data = b"0" * UPLOAD_SIZE

    start = time.perf_counter()

    response = requests.post(
        UPLOAD_URL,
        data=data,
        headers={"Content-Type": "application/octet-stream"},
        timeout=60
    )

    response.raise_for_status()

    elapsed = time.perf_counter() - start

    return (len(data) * 8) / elapsed / 1_000_000


def main():
    print("=" * 40)
    print("          INTERNET SPEEDTEST")
    print("=" * 40)

    try:
        print("\nTesting ping...")
        ping = test_ping()

        print("Testing download...")
        download = test_download()

        print("Testing upload...")
        upload = test_upload()

        results = {
            "ping_ms": round(ping, 2),
            "download_mbps": round(download, 2),
            "upload_mbps": round(upload, 2)
        }

        print("\n========== RESULTS ==========")
        print(f"Ping     : {ping:.2f} ms")
        print(f"Download : {download:.2f} Mbps")
        print(f"Upload   : {upload:.2f} Mbps")
        print("=============================")

        # Save results to JSON
        with open("results.json", "w") as file:
            json.dump(results, file, indent=4)

        print("\nResults saved to results.json")

    except requests.RequestException as error:
        print(f"Network error: {error}")

    except KeyboardInterrupt:
        print("\nTest interrupted.")


if __name__ == "__main__":
    main()

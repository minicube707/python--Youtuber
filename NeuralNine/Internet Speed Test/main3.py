
import socket
import ssl
import time
import json


HOST = "speed.cloudflare.com"
PORT = 443

DOWNLOAD_SIZE = 25_000_000
UPLOAD_SIZE = 10_000_000


def create_connection():
    # Create a TCP connection and wrap it with TLS
    raw_socket = socket.create_connection((HOST, PORT), timeout=30)

    context = ssl.create_default_context()
    client = context.wrap_socket(raw_socket, server_hostname=HOST)

    return client


def read_headers(client):
    # Read HTTP headers until the end of the header section
    buffer = b""

    while b"\r\n\r\n" not in buffer:
        data = client.recv(4096)

        if not data:
            raise ConnectionError("Incomplete HTTP response")

        buffer += data

    headers, body = buffer.split(b"\r\n\r\n", 1)

    return headers, body


def test_ping():
    times = []

    for _ in range(5):
        start = time.perf_counter()

        client = create_connection()
        client.close()

        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)

    return sum(times) / len(times)


def test_download():
    client = create_connection()

    try:
        request = (
            f"GET /__down?bytes={DOWNLOAD_SIZE} HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        start = time.perf_counter()

        # Send HTTP download request
        client.sendall(request.encode())

        # Read HTTP response headers
        headers, body = read_headers(client)

        if b" 200 " not in headers:
            raise RuntimeError("Download request failed")

        total_bytes = len(body)

        # Receive remaining download data
        while True:
            data = client.recv(65536)

            if not data:
                break

            total_bytes += len(data)

        elapsed = time.perf_counter() - start

        # Calculate download speed
        mbps = (total_bytes * 8) / elapsed / 1_000_000

        return mbps

    finally:
        client.close()


def test_upload():
    client = create_connection()

    try:
        data = b"0" * UPLOAD_SIZE

        request = (
            f"POST /__up HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            "Content-Type: application/octet-stream\r\n"
            f"Content-Length: {len(data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode()

        start = time.perf_counter()

        # Send HTTP headers and upload data
        client.sendall(request)
        client.sendall(data)

        # Wait for the server response
        headers, body = read_headers(client)

        if b" 200 " not in headers:
            raise RuntimeError("Upload request failed")

        while client.recv(4096):
            pass

        elapsed = time.perf_counter() - start

        # Calculate upload speed
        mbps = (len(data) * 8) / elapsed / 1_000_000

        return mbps

    finally:
        client.close()


def main():
    print("=" * 45)
    print("             SOCKET SPEEDTEST")
    print("=" * 45)

    try:
        print("\nTesting TCP ping...")
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

        print("\n" + "=" * 45)
        print("                  RESULTS")
        print("=" * 45)

        print(f"Ping     : {ping:.2f} ms")
        print(f"Download : {download:.2f} Mbps")
        print(f"Upload   : {upload:.2f} Mbps")

        print("=" * 45)

        # Save results to JSON
        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)

        print("\nResults saved to results.json")

    except (OSError, ssl.SSLError, ConnectionError) as error:
        print(f"\nNetwork error: {error}")

    except KeyboardInterrupt:
        print("\nTest interrupted by user.")


if __name__ == "__main__":
    main()

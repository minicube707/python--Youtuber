
import requests

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

"""
RDAP (Registration Data Access Protocol)
----------------------------------------

RDAP is a modern protocol designed to replace the traditional WHOIS
protocol. It allows users to retrieve registration information about
domain names, IP addresses, and autonomous system numbers.

Unlike traditional WHOIS, which returns information as plain text
over TCP port 43, RDAP uses HTTP/HTTPS and provides structured data
in JSON format.

This makes RDAP easier to use with Python libraries such as requests,
as the returned JSON data can be directly converted into Python
dictionaries.

RDAP can provide information such as:
    - Domain registration and expiration dates
    - Registrar information
    - Domain status
    - Nameservers
    - IP address ranges
    - Contact information (when publicly available)

RDAP is standardized by the IETF and is progressively replacing
traditional WHOIS services.

Official documentation:
https://www.icann.org/rdap
"""

BASE_URL = "https://rdap.org/domain/"


# --------------------------------------------------
# 2. WHOIS lookup function
# --------------------------------------------------

def whois(domain):
    """
    Retrieve registration information for a domain.
    """

    url = BASE_URL + domain

    # Send an HTTP GET request
    response = requests.get(url, timeout=10)

    # Raise an exception if the request failed
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary
    return response.json()


# --------------------------------------------------
# 3. Retrieve information for one domain
# --------------------------------------------------

res = whois("spotify.com")

print("\n========== SPOTIFY ==========")

print(f"\nDomain: {res.get('ldhName')}")

# Extract organization information
for entity in res.get("entities", []):
    print(f"Entity: {entity.get('handle')}")


# --------------------------------------------------
# 4. Retrieve information for multiple domains
# --------------------------------------------------

sites = [
    "facebook.com",
    "spotify.com",
    "instagram.com",
    "meta.com"
]

# Retrieve information for all domains
results = {
    site: whois(site)
    for site in sites
}

print("\n========== DOMAIN INFORMATION ==========")

for site, data in results.items():

    print(f"\nDomain: {site}")

    # Display registration events
    for event in data.get("events", []):
        if event.get("eventAction") == "registration":
            print(f"Creation date: {event.get('eventDate')}")


# --------------------------------------------------
# 5. Find the oldest domain
# --------------------------------------------------

creation_dates = {}

for site, data in results.items():

    for event in data.get("events", []):

        if event.get("eventAction") == "registration":
            creation_dates[site] = event.get("eventDate")
            break


if creation_dates:
    oldest_domain = min(
        creation_dates,
        key=creation_dates.get
    )

    print("\n========== OLDEST DOMAIN ==========")
    print(f"Domain: {oldest_domain}")
    print(f"Creation date: {creation_dates[oldest_domain]}")


# --------------------------------------------------
# 6. Extract email addresses
# --------------------------------------------------

print("\n========== EMAIL ADDRESSES ==========")

for site, data in results.items():

    emails = []

    # Extract email addresses from RDAP entities
    for entity in data.get("entities", []):

        for item in entity.get("vcardArray", [None, []])[1]:

            if item[0] == "email":
                emails.append(item[3])

    print(f"\n{site}:")
    print(emails if emails else "No email available")


# --------------------------------------------------
# 6. Perform a RDAP  lookup using an IP address
# --------------------------------------------------

# Retrieve registration information for an IP address
ip_address = "81.19.159.28"

url = f"https://rdap.org/ip/{ip_address}"

response = requests.get(url, timeout=10)

data = response.json()

print("\n========== IP INFORMATION ==========")

print(f"IP range: {data.get('startAddress')} - {data.get('endAddress')}")
print(f"Network name: {data.get('name')}")
print(f"Country: {data.get('country')}")

import whois

# List of domain names to investigate
sites = [
    'facebook.com',
    'spotify.com',
    'instagram.com',
    'meta.com'
]


# --------------------------------------------------
# 1. Retrieve WHOIS information for a single domain
# --------------------------------------------------

# Perform a WHOIS lookup for Spotify
res = whois.whois('spotify.com')

# Display the complete WHOIS record
print("\n========== SPOTIFY WHOIS ==========")
print(res)

# Display specific information
print(f"\nOrganization : {res.org}")
print(f"Creation date: {res.creation_date}")


# --------------------------------------------------
# 2. Retrieve WHOIS information for multiple domains
# --------------------------------------------------

# Perform one WHOIS lookup per domain
whois_data = {
    site: whois.whois(site)
    for site in sites
}

# Extract organizations and creation dates
companies = [whois_data[s].org for s in sites]
creation_dates = [whois_data[s].creation_date for s in sites]

print("\n========== DOMAIN INFORMATION ==========")

# Display information for each domain
for site in sites:
    data = whois_data[site]

    print(f"\nDomain       : {site}")
    print(f"Organization : {data.org}")
    print(f"Creation date: {data.creation_date}")


# --------------------------------------------------
# 3. Find the oldest registered domain
# --------------------------------------------------

# Convert creation dates to comparable values
# Some WHOIS records may contain a list of dates
def get_first_date(date):
    if isinstance(date, list):
        date = min(d for d in date if d is not None)
    return date


valid_dates = {
    site: get_first_date(whois_data[site].creation_date)
    for site in sites
    if whois_data[site].creation_date is not None
}

# Find the domain with the earliest creation date
oldest_domain = min(valid_dates, key=valid_dates.get)

print("\n========== OLDEST DOMAIN ==========")
print(f"Domain: {oldest_domain}")
print(f"Creation date: {valid_dates[oldest_domain]}")


# --------------------------------------------------
# 4. Extract contact email addresses
# --------------------------------------------------

print("\n========== CONTACT EMAILS ==========")

# Retrieve and display email addresses for each domain
for site in sites:
    emails = whois_data[site].emails

    print(f"\n{site}:")
    print(emails if emails else "No email available")


# --------------------------------------------------
# 5. Perform a WHOIS lookup using an IP address
# --------------------------------------------------

# WHOIS can also be used to retrieve information about IP addresses
ip_address = "81.19.159.28"

ip_info = whois.whois(ip_address)

print("\n========== IP ADDRESS WHOIS ==========")
print(ip_info)

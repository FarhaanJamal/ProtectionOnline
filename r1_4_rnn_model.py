import socket
import requests
import whois
from tld import get_tld
from urllib.parse import urlparse
import geoip2.database
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd


import requests
import re


def calculate_obfuscated_js_length(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Extract JavaScript code from the HTML content
        js_code = re.findall(r"<script[^>]*>(.*?)</script>", response.text, re.DOTALL)

        # Define regular expressions to match common obfuscation patterns
        patterns = [
            r"eval\s*\(\s*function\s*\(\s*\w+\s*\)\s*\{.*?\.join\(\s*\"\s*\"\s*\)",
            r"eval\s*\(\s*function\s*\(\s*\w+\s*\)\s*\{.*?\.split\(\s*\"\s*\"\s*\)",
            r"eval\s*\(\s*function\s*\(\s*\w+\s*\)\s*\{.*?\.replace\(\s*\"\s*\"\s*\,\s*\"\s*\"\s*\)",
            r"eval\s*\(\s*function\s*\(\s*\w+\s*\)\s*\{.*?\)\s*;\s*\}",
            r"function\s*\(\s*\w+\s*\)\s*\{.*?\.split\(\s*\"\s*\"\s*\)",
            r"function\s*\(\s*\w+\s*\)\s*\{.*?\.join\(\s*\"\s*\"\s*\)",
            r"function\s*\(\s*\w+\s*\)\s*\{.*?\.replace\(\s*\"\s*\"\s*\,\s*\"\s*\"\s*\)",
        ]

        # Compile regular expressions
        compiled_patterns = [re.compile(pattern, re.DOTALL) for pattern in patterns]

        # Calculate total length of obfuscated JavaScript code
        total_length = 0
        for code in js_code:
            for pattern in compiled_patterns:
                matches = pattern.findall(code)
                if matches:
                    for match in matches:
                        total_length += len(match)

        return total_length

    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)
        return 0


def extract_info(url):
    # 1. Extract URL, URL's length, and HTTPS status.
    url_length = len(url)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    https = 1 if parsed_url.scheme == "https" else 0

    # 2. Extract the top-level domain (TLD).
    tld = get_tld(url, as_object=True).fld
    tld = tld.split(".")[-1]

    # 3. Compute the geographic location.
    ip_address = socket.gethostbyname(domain)
    reader = geoip2.database.Reader("model/GeoLite2-Country.mmdb")
    try:
        response = reader.country(ip_address)
        geo_location = response.country.iso_code
    except geoip2.errors.AddressNotFoundError:
        geo_location = 0

    # 4. Fetch WHOIS information.
    whois_info = whois.whois(domain)
    if len(whois_info)>0:
        whois_info = 1.0
    else:
        whois_info = 0.0

    # 5. Extract JavaScript content from the webpage.
    response = requests.get(url)
    javascript_content = response.text  # Assuming JavaScript is embedded in the HTML
    javascript_content_length = len(javascript_content)



    data = [url_length, float(whois_info), float(https), float(javascript_content_length), float(calculate_obfuscated_js_length(url))]

    return data
    


"""# Example usage:
url = "https://google.com"
info = extract_info(url)
print(info)"""

import requests
import socket
import urllib.parse
import whois
import re
from bs4 import BeautifulSoup


def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.gaierror:
        return None


def get_geo_location(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        return data["countryCode"]
    except:
        return None


def get_url_length(url):
    return len(url)


def get_javascript_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        scripts = soup.find_all("script")
        js_content = "".join([script.text for script in scripts])
        return js_content, len(js_content), len(re.sub(r"\s", "", js_content))
    except:
        return None, None, None


def get_top_level_domain(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc.split(".")[-1]


def get_whois_info(url):
    try:
        domain = whois.whois(url)
        return domain.text
    except:
        return None


def get_https_status(url):
    if url.startswith("https"):
        return 1
    else:
        return 0


def main(url):
    ip_address = get_ip_address(url)
    geo_location = get_geo_location(ip_address) if ip_address else None
    url_length = get_url_length(url)
    javascript_content, js_content_length, js_obfuscated_content_length = (
        get_javascript_content(url)
    )
    top_level_domain = get_top_level_domain(url)
    whois_info = get_whois_info(url)
    https_status = get_https_status(url)

    return [
        url,
        ip_address,
        geo_location,
        url_length,
        js_content_length,
        js_obfuscated_content_length,
        top_level_domain,
        whois_info,
        https_status,
        javascript_content,
    ]


# Example usage:
url = "www.google.com"
output = main(url)
print(output)

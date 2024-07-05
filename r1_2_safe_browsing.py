""""
filename : _1_2_safe_browsing.py
Google Safe Browsing API
Date Created : Feb 8, 2024 | Last Updated : Feb 9, 2024
Language: Python | Version : 3.10.13
"""

# Required imports
import requests
import json
import os
from dotenv import load_dotenv

# Load ENV variables
load_dotenv()
GOOGLE_SAFE_BROWSING = os.getenv("GOOGLE_SAFE_BROWSING")
url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"


# Function to check
def CheckUrl(checkingurl):
    payload = {
        "client": {
            "clientId": "rockstars",
            "clientVersion": "1.0",
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
                "THREAT_TYPE_UNSPECIFIED",
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": checkingurl}],
        },
    }

    headers = {"Content-Type": "application/json"}
    params = {"key": GOOGLE_SAFE_BROWSING}

    response = requests.post(url, params=params, headers=headers, json=payload)

    if response.status_code == 200:
        results = response.json()
        matches = results.get("matches", [])
        res = ""
        if matches:
            res += "UNSAFE URL,"
            res += f"Threat type: {matches[0]['threatType']},"
            res += f"Platform type: {matches[0]['platformType']},"
        else:
            res += "SAFE URL"

        return res
    else:
        return f"ERROR : {response.text}"


# Main
"""
result = CheckUrl("https://testsafebrowsing.appspot.com/s/phishing.html")
result = result.split(",")
for i in result:
    print(i)
"""

""""
filename : _1_1_ssl.py
SSL Certificate Verification
Date Created : Feb 9, 2024 | Last Updated : Feb 9, 2024
Language: Python | Version : 3.10.13
"""

# Required imports
import ssl
import socket
import http.client
from urllib.parse import urlparse


# Validation of SSL
def ValidateSsl(url):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 443

        # Establish connection with the server
        context = ssl.create_default_context()
        res = ""

        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Certificate details
                cert = ssock.getpeercert()

                print("Certificate Subject:", cert["subject"])
                print("Certificate Issuer:", cert["issuer"])
                print("Certificate Expiry Date:", cert["notAfter"])
                print("Certificate Version:", cert["version"])

                # Check certificate validation
    
                if cert["subject"] == cert["issuer"]:
                    res += "Self-signed certificate detected!,"
                else:
                    res += "Certificate is issued by a trusted CA.,"
                

                # Check if connection is using HTTPS
                if parsed_url.scheme == "https":
                    res += "Secure Connection, "
                else:
                    res += "InSecure Connection, "

                # Get cookie expiry date if available
                conn = http.client.HTTPSConnection(hostname)
                conn.request("GET", parsed_url.path)
                response = conn.getresponse()
                cookie_header = response.getheader("Set-Cookie")
                #print(cookie_header)
                #print("\n\n\n0"+type(cookie_header))
                #print("\n\n\n0"+type(cookie_header))
                if cookie_header:
                    # print(cookie_header)
                    print("\n\n\n1"+type(cookie_header))
                    cookie_expires = cookie_header.split(";")
                    """cookie_expires = cookie_header.split(";")[1].strip().split("=")[1]
                    cookie_expires = cookie_expires.split(",")[1]
                    temp = cookie_expires + ","
                    res += temp"""
                    print("\n\n"+cookie_expires+"\n\n")
                else:
                    res += "No cookies set in the response.,"
                res += "Validated"

                return res
    except Exception as e:
        return "Secure Connection, 17-02-2025"


"""
    # Main
    result = ValidateSsl("https://infograph.venngage.com/")

    result = result.split(",")
    print(result)
    for i in result:
        print(i)
"""

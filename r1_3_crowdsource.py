""""
filename : _1_3_crowdsource.py
Blacklisting and White listing
Date Created : Feb 9, 2024 | Last Updated : Feb 9, 2024
Language: Python | Version : 3.10.13
"""

# Required imports
import json


def RetrieveData():
    with open("data.json", "r") as file:
        return json.load(file)


def SaveJson(data):
    with open("data.json", "w") as file:
        return json.dump(data, file)


def SearchUrl(url):
    data = RetrieveData()
    return data[url]


def UpdateUrl(url, category):
    data = RetrieveData()
    if url not in data:
        data[url] = [0, 0]

    temp_value = data[url]

    if category == 0:
        data[url] = [temp_value[0] + 1, temp_value[1]]
    else:
        data[url] = [temp_value[0], temp_value[1] + 1]

    SaveJson(data)


# Main
"""
print(SearchUrl("google.com"))
UpdateUrl("micro.com", 0)
print(RetrieveData())
"""

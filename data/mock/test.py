import requests
import json

url = "https://anapioficeandfire.com/api/characters"

payload = ""
headers = {}

all_chars = []

counter = 1
while True:
    querystring = {"page": str(counter), "pageSize": "50"}
    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring)
    data = response.json()

    l = len(data)

    print(l, counter)

    if not isinstance(data, list) or l == 0:
        break

    with open('chars/data' + str(counter) + '.json', 'w') as outfile:
        for c in data:
            json.dump(c, outfile)
            print(', ', file=outfile)

    counter += 1

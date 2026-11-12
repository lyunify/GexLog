import json

import requests

BASE_URL = "https://lab.flashalpha.com"
SYMBOL = "spy"

response = requests.get(
    f"{BASE_URL}/v1/stock/{SYMBOL}/summary",
    timeout=10,
)

print("Status:", response.status_code)

if response.status_code != 200:
    print("Request failed:", response.text)
    raise SystemExit(1)

data = response.json()
print(json.dumps(data, indent=2))

with open("sample_response.json", "w") as f:
    json.dump(data, f, indent=2)
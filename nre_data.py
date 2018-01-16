import requests
import json


url = 'https://hsp-prod.rockshore.net/api/v1/serviceMetrics'

# create request form
body = {
    "from_loc":"PMT",
    "to_loc":"GLQ",
    "from_time":"0700",
    "to_time":"0900",
    "from_date":"2018-01-15",
    "to_date":"2018-01-16",
    "days":"WEEKDAY"
}
# no auth= parameter - uses .netrc
r = requests.post(url, json=body)
print(r.url)
print(r.status_code)
print(r.json())
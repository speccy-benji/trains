import requests
import json

def get_serviceMetrics():

  url = 'https://hsp-prod.rockshore.net/api/v1/serviceMetrics'

  # create request form
  body = {
      "from_loc":"GLQ",
      "to_loc":"PMT",
      "from_time":"1730",
      "to_time":"1800",
      "from_date":"2018-01-15",
      "to_date":"2018-01-18",
      "days":"WEEKDAY"
  }
  # no auth= parameter - uses .netrc
  r = requests.post(url, json=body)
  print(r.url)
  print(r.status_code)
  if r.status_code == requests.codes.ok :
    serviceMetrics = r.json()
    with open('serviceMetrics.json', 'w') as outfile :
      json.dump(serviceMetrics, outfile)
    return serviceMetrics
  else :
    r.raise_for_status()
  
if __name__ == "__main__" :
  try:
    with open('serviceMetrics.json', 'r') as infile:
      print("File found")
      serviceMetrics = json.load(infile)
  except OSError:
    print("File not found")
    serviceMetrics = get_serviceMetrics()
  print(json.dumps(serviceMetrics, indent=4))
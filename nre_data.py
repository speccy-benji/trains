import requests
import json

def get_serviceMetrics():
  try:
    with open('serviceMetrics.json', 'r') as infile:
      print("File found")
      serviceMetrics = json.load(infile)
      return serviceMetrics
  except OSError:
    print("File not found")
 
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
    #print(r.url)
    # print(r.status_code)
    if r.status_code == requests.codes.ok :
      serviceMetrics = r.json()
      with open('serviceMetrics.json', 'w') as outfile :
        json.dump(serviceMetrics, outfile)
      return serviceMetrics
    else :
      r.raise_for_status()
      
def get_serviceDetails(rid):
  url = 'https://hsp-prod.rockshore.net/api/v1/serviceDetails'
  body = {
           "rid": rid
         }
  r = requests.post(url, json=body)
  if r.status_code == requests.codes.ok:
    return r.json()
  else:
    r.raise_for_status()
  
def main():
  serviceMetrics= get_serviceMetrics()
  print(json.dumps(serviceMetrics, indent=4))
  for service in serviceMetrics['Services']:
    print(service['Metrics'][0]['num_tolerance'])
    for rid in service['serviceAttributesMetrics']['rids']:
      print(rid)
      serviceDetails = get_serviceDetails(rid)
      print(json.dumps(serviceDetails, indent=4))

if __name__ == "__main__":
  main()
 
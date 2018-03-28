import requests
import json
import os

def get_serviceMetrics(from_loc,
                       to_loc,
                       from_time,
                       to_time,
                       from_date,
                       to_date,
                       days,
                       force=False
                      ):
  service_file = ''.join((from_loc,
                 to_loc,
                 from_time,
                 to_time,
                 from_date,
                 to_date,
                 days,
                 ".json"))
  full_filename = os.path.join('data', 'serviceMetrics', service_file)
  if force or not os.path.exists(full_filename):
    print('calling serviceMetrics api ...')
    url = 'https://hsp-prod.rockshore.net/api/v1/serviceMetrics'

    # create request form
    body = {
        "from_loc": from_loc,
        "to_loc": to_loc,
        "from_time": from_time,
        "to_time": to_time,
        "from_date": from_date,
        "to_date": to_date,
        "days": days
    }
    # no auth= parameter - uses .netrc
    r = requests.post(url, json=body)
    
    if r.status_code == requests.codes.ok :
      serviceMetrics = r.json()
      with open(full_filename, 'w') as outfile :
        json.dump(serviceMetrics, outfile)
      return serviceMetrics
    else :
      r.raise_for_status()
      
  else:
    print('reading serviceMetrics from file')
    with open(full_filename, 'r') as infile:

      serviceMetrics = json.load(infile)
      return serviceMetrics

      
def get_serviceDetails(rid, force=False):
  rid_file = os.path.join('data', 'rids', rid + '.json')
  print(rid)
  if force or not os.path.exists(rid_file):
    print('calling getServiceDetails api for rid')
    
    url = 'https://hsp-prod.rockshore.net/api/v1/serviceDetails'
    body = {
             "rid": rid
           }
    r = requests.post(url, json=body)
    if r.status_code == requests.codes.ok:
      service_details = r.json()
      with open(rid_file, 'w') as outfile:
        json.dump(service_details, outfile)
    else:
      r.raise_for_status()
  else:
    print('reading rid from file')
    with open(rid_file, 'r') as infile:
      service_details = json.load(infile)
  return service_details
  
def main():
  from_loc = 'PMT'
  to_loc = 'GLQ'
  from_time = '0756'
  to_time = '0915'
  from_date = '2018-01-27'
  to_date = '2018-03-26'
  days = 'WEEKDAY'
  serviceMetrics = get_serviceMetrics(from_loc,
                                      to_loc,
                                      from_time,
                                      to_time,
                                      from_date,
                                      to_date,
                                      days)
  rid_count = 0
  service_file = ''.join((from_loc,
                 to_loc,
                 from_time,
                 to_time,
                 from_date,
                 to_date,
                 days,
                 ".json"))
  qualified_file = os.path.join('data', 'aggregated', service_file)
  with open(qualified_file, 'w') as outfile:
    for service in serviceMetrics['Services']:
    #print(service['Metrics'][0]['num_tolerance'])
      for rid in service['serviceAttributesMetrics']['rids']:
        rid_count += 1
        serviceDetails = get_serviceDetails(rid)
        json.dump(serviceDetails, outfile)
        outfile.write("\n")
  print('total rids ', rid_count) 

if __name__ == "__main__":
  main()
 
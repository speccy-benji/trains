import matplotlib
matplotlib.use('Agg')
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
  from_loc = 'PMT'
  to_loc = 'GLQ'
  from_time = '0756'
  to_time = '0915'
  from_date = '2018-01-27'
  to_date = '2018-03-26'
  days = 'WEEKDAY'
  service_file = ''.join((from_loc,
                 to_loc,
                 from_time,
                 to_time,
                 from_date,
                 to_date,
                 days,
                 ".json"))
  qualified_file = os.path.join('data', 'aggregated', service_file)
  full_df = pd.DataFrame([])
  with open(qualified_file, 'r') as infile:
    for in_line in infile:
      #need to use loads rather than load - might be because of \n?
      serviceDetails = json.loads(in_line)
      df = pd.io.json.json_normalize(serviceDetails['serviceAttributesDetails']['locations'])
      df['rid'] = serviceDetails['serviceAttributesDetails']['rid']
      df['date_of_service'] = serviceDetails['serviceAttributesDetails']['date_of_service']
      full_df = full_df.append(df)
  full_df = full_df.reset_index(drop=True)
  #convert hhmm times to datetimes setting to NaT where no time
  full_df['actual_ta'] = pd.to_datetime(np.where(full_df['actual_ta']=="", None,
            full_df[['date_of_service', 'actual_ta']].astype(str).apply(' '.join, 1)))
  full_df['actual_td'] = pd.to_datetime(np.where(full_df['actual_td']=="", None,
            full_df[['date_of_service', 'actual_td']].astype(str).apply(' '.join, 1)))
  full_df['gbtt_pta'] = pd.to_datetime(np.where(full_df['gbtt_pta']=="", None,
            full_df[['date_of_service', 'gbtt_pta']].astype(str).apply(' '.join, 1)))
  full_df['gbtt_ptd'] = pd.to_datetime(np.where(full_df['gbtt_ptd']=="", None,
            full_df[['date_of_service', 'gbtt_ptd']].astype(str).apply(' '.join, 1)))
  # calculate time difference in minutes
  full_df['ta_diff'] = (full_df['actual_ta'] - full_df['gbtt_pta']).astype('timedelta64[m]')
  full_df['td_diff'] = (full_df['actual_td'] - full_df['gbtt_ptd']).astype('timedelta64[m]')
  full_df['actual_lay'] = (full_df['actual_td'] - full_df['actual_ta']).astype('timedelta64[m]')
  full_df['gbtt_lay'] = (full_df['gbtt_ptd'] - full_df['gbtt_pta']).astype('timedelta64[m]')
  # write out as csv for future use
  full_df.to_csv("train_times.csv")
  # print and describe resulting df
  #print(full_df.describe())
  #print(full_df.head())
  # create pivot of arrival times by station
  pvt = full_df.pivot_table('ta_diff',rows='rid', cols='location')
  pvt = pvt.drop(['EDB'], axis=1)

  print(pvt)
  plt.figure()
  pvt.hist(stacked=True)
  plt.savefig('hist2.png')


if __name__ == '__main__':
  main()
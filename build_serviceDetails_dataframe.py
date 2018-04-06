import matplotlib
matplotlib.use('Agg')

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
  full_df = pd.DataFrame([])
  with open('serviceDetails.json', 'r') as infile:
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
  # print and describe resulting df
  #print(full_df.describe())
  #print(full_df.head())
  # create pivot of arrival times by station
  pvt = full_df.pivot_table('ta_diff',rows='rid', cols='location')
  pvt = pvt.drop(['GLQ'], axis=1)

  print(pvt)
  plt.figure()
  pvt.hist(stacked=True)
  plt.savefig('hist.png')


if __name__ == '__main__':
  main()
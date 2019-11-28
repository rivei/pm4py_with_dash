# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:55:51 2019

@author: Wei
"""

import os
from pm4py.objects.log.importer.xes import factory as xes_importer

log = xes_importer.apply("..\\data\\financial_log.xes")

from pm4py.objects.log.util import interval_lifecycle

enriched_log = interval_lifecycle.assign_lead_cycle_time(log)
#print(enriched_log[0][0])

import pandas as pd
#print(pd.DataFrame.from_dict(enriched_log[0][0]))

df = pd.DataFrame()
for case in enriched_log:
    #print(case)
    df = df.append(pd.DataFrame.from_dict(case), ignore_index=True)
    #for event in case:
        #print(event)
        #df = df.append(pd.DataFrame.from_dict(event).transpose(), ignore_index=True)
        
#print(df.head())
print(df.columns)
#df.groupby('org:group')['time:timestamp'].count()
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 22:17:20 2019

@author: Wei
"""

import pathlib
import pandas as pd
import numpy as np
#import pytz
from datetime import datetime, tzinfo,timedelta

from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.util import interval_lifecycle
from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
log = xes_importer.apply(str(DATA_PATH.joinpath("receipt.xes")))
# =============================================================================
#enriched_log = interval_lifecycle.assign_lead_cycle_time(log)
#endf['ts_utc'] = endf['time:timestamp'].apply(lambda i: i.tz_convert('UTC'))
# enriched_log does not help much
# 0	0.0	0.0	0.0	0.0	0.0	1.0	task-42933	Confirmation of receipt	Group 1	Resource21	2011-10-11 13:45:40.276000+02:00	2011-10-11 13:45:40.276000+02:00
# 1	16800.0	0.0	16800.0	16800.0	0.0	0.0	task-42935	T02 Check confirmation of receipt	Group 4	Resource10	2011-10-12 08:26:25.398000+02:00	2011-10-12 08:26:25.398000+02:00
# 2	1158600.0	0.0	1158600.0	1141800.0	0.0	0.0	task-42957	T03 Adjust confirmation of receipt	Group 1	Resource21	2011-11-24 15:36:51.302000+01:00	2011-11-24 15:36:51.302000+01:00
# 3	1158600.0	0.0	1158600.0	0.0	0.0	0.0	task-47958	T02 Check confirmation of receipt	Group 4	Resource21	2011-11-24 15:37:16.553000+01:00	2011-11-24 15:37:16.553000+01:00
# 4	0.0	0.0	0.0	0.0	0.0	1.0	task-43021	Confirmation of receipt	EMPTY	Resource30	2011-10-18 13:46:39.679000+02:00	2011-10-18 13:46:39.679000+02:00
# 5	0.0	0.0	0.0	0.0	0.0	1.0	task-43672	T06 Determine necessity of stop advice	Group 1	Resource30	2011-10-18 13:47:06.950000+02:00	2011-10-18 13:47:06.950000+02:00
# 6	0.0	0.0	0.0	0.0	0.0	1.0	task-43671	T02 Check confirmation of receipt	Group 4	Resource30	2011-10-18 13:47:26.235000+02:00	2011-10-18 13:47:26.235000+02:00
# 7	0.0	0.0	0.0	0.0	0.0	1.0	task-43674	T03 Adjust confirmation of receipt	Group 1	Resource30	2011-10-18 13:47:41.811000+02:00	2011-10-18 13:47:41.811000+02:00
# 8	0.0	0.0	0.0	0.0	0.0	1.0	task-43675	T02 Check confirmation of receipt	Group 4	Resource30	2011-10-18 13:47:57.979000+02:00	2011-10-18 13:47:57.979000+02:00
# 9	0.0	0.0	0.0	0.0	0.0	1.0	task-43673	T10 Determine necessity to stop indication	Group 1	Resource30	2011-10-18 13:48:15.357000+02:00	2011-10-18 13:48:15.357000+02:00
# 10	0.0	0.0	0.0	0.0	0.0	1.0	task-43676	T03 Adjust confirmation of receipt	Group 1	Resource30	2011-10-18 13:48:30.632000+02:00	2011-10-18 13:48:30.632000+02:00
# 
# =============================================================================



#endf = pd.DataFrame(columns=['caseid','actid','resid','ts'])#,'dur'])#,'partcycleT','partleadT','wasteT','thisWT','rclt'])

n_cases = 0
n_events = 0

caseid = []
actid = []
actseq = []
resid = []
ts = []
startTime = []
for case in log:
    actidx = 0
    startT = case[0]['time:timestamp'].timestamp()
    for event in case:
        #endf = endf.append(dict(event), ignore_index = True) #this takes too long time 
#        endf = endf.append({
#                'caseid': n_cases,
#                'actid':event['concept:name'],
#                'resid':event['org:resource'],
#                'ts':event['time:timestamp'].timestamp()
#                }, ignore_index = True)
        
        caseid.append(n_cases)
        actid.append(event['concept:name'])
        actseq.append(actidx)
        resid.append(event['org:resource'])
        ts.append(event['time:timestamp'].timestamp())
        startTime.append(event['time:timestamp'].timestamp() - startT)
        actidx = actidx + 1
        n_events = n_events + 1
    n_cases = n_cases + 1
            
df = pd.DataFrame({'caseid': caseid, 
                   'actid':actid, 
                   'actseq':actseq, 
                   'resid':resid, 
                   'ts':ts, 
                   'sT': startTime})        

df['preid'] = df['actid'].shift(1)
df['preid'] = df.apply(lambda row: row['preid'] if row['actseq']!=0 else 'START', axis = 1)

df['dur'] = 0
dur = list(df['dur'])

evS = 0
evE = -1
for i in range(0, len(df)):
    if df['actseq'][i] == 0:
        evS = i
    if i < len(df) - 1:
        if df['actseq'][i + 1] == 0:
            evE = i
    else:
        evE = i
        
    if evE >= evS:
        #df['dur'][evS:evE] = df['sT'][evE]
        for j in range(evS, evE+1):
            #print(df['sT'][evE])
            dur[j] = df['sT'][evE-1]
df['dur'] = dur


sort_df = df.sort_values(by=['dur','caseid', 'actseq'], ascending = [0,1,1])
sortid = 0
#sort_df['sid'] = 0
sid = np.zeros(len(sort_df))
for i in range(1, len(sort_df)):
    if i < len(sort_df) - 1:
        if sort_df.iloc[i,:]['caseid'] != sort_df.iloc[i-1,:]['caseid']:
            sortid = sortid + 1

    sid[i] = sortid
    
sort_df['sid'] = sid

activities = log_attributes_filter.get_attribute_values(log, "concept:name")
actid = []
cnt = []
for act0 in activities.items():
    actid.append(act0[0])
    cnt.append(act0[1])

act_df = pd.DataFrame({'id':actid, 'cnt':cnt})

n_activities = len(act_df)

from pm4py.statistics.traces.log import case_statistics
traces = case_statistics.get_variant_statistics(log)#, parameters={"max_variants_to_return": 5})

#acts = []
#cnt = []
#tid = []
#idx = 0
#for trace in traces:
#    tid.append(idx)
#    acts.append(trace['variant'])
#    cnt.append(trace['count'])
#    idx = idx + 1
#    
#trace_df = pd.DataFrame({'id': tid, 'acts': acts, 'cnt':cnt})
#n_traces = len(trace_df)

tid = []
actid = []
actseq = []
cnt = []
n_traces = 0
for trace in traces:
    actidx = 0
    acts = trace['variant']
    for s in acts.split(','):
        tid.append(n_traces)
        actid.append(s)
        actseq.append(actidx)
        cnt.append(trace['count'])
        actidx = actidx+1
    n_traces = n_traces + 1
    
trace_df = pd.DataFrame({'id': tid, 'actid': actid, 'actseq':actseq, 'cnt':cnt})
trace_df['preid'] = trace_df['actid'].shift(1)
trace_df['preid'] = trace_df.apply(lambda row: row['preid'] if row['actseq']!=0 else 'START', axis = 1)
#trace_df['postid'] = trace_df['actid'].shift(1)
#trace_df['postid'] = trace_df.apply(lambda row: row['preid'] if row['actseq']!=0 else 'START', axis = 1)

trace_df['pre_post'] = trace_df.apply(lambda row: row['preid']+"-"+row['actid'], axis = 1)

def actid2num(sactid, df):
    nactid = -1
    for i in range(0, len(df)):
        if df['id'][i] == sactid:
            nactid = i/len(df)
    return nactid

#actid2num("Confirmation of receipt", act_df)

trace_df['nactid'] = trace_df['actid'].apply(lambda i:actid2num(i, act_df))

# matrix
df['pre_post'] = df.apply(lambda row: row['preid']+"-"+row['actid'], axis = 1)
#mtxdf1 = pd.DataFrame({'ant':df['preid'],'con':df})
mtxdf1 = df[df['preid']!='START'].groupby('pre_post')['caseid'].count() #agg(['sum','count','mean'])
#mtxdf1['abs'] = mtxdf1['sum']/mtxdf1['count']
mtxdf= pd.DataFrame({'pre_post':mtxdf1.index, 'cnt': list(mtxdf1)})

#roles Detection: related to resource vs activity?
#from pm4py.algo.enhancement.roles import factory as roles_factory
#roles = roles_factory.apply(log)
aaa

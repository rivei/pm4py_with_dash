# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 22:17:20 2019

@author: Wei
"""

#from dash_app import default_log as log
import pandas as pd
import numpy as np
#import pytz
from datetime import datetime, tzinfo,timedelta

from pm4py.statistics.traces.log import case_statistics
from pm4py.algo.filtering.log.attributes import attributes_filter

MAX_TRACES = 9999

def filtered_log_df(log, top_trace_n = MAX_TRACES):
#    if top_trace_n == MAX_TRACES:
#        traces_with_count = case_statistics.get_variant_statistics(log) #parameters=("max_variants_to_return":5)
#        #df = pd.DataFrame.from_dict([dict(x) for x in traces_with_count])
#        df = pd.DataFrame()
#        df.columns = ['caseid','actid','actseq','resid','ts','sT']
#    else:
    n_cases = 0
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
            caseid.append(n_cases)
            actid.append(event['concept:name'])
            actseq.append(actidx)
            resid.append(event['org:resource'])
            ts.append(event['time:timestamp'].timestamp())
            startTime.append(event['time:timestamp'].timestamp() - startT)
            actidx = actidx + 1
        n_cases = n_cases + 1
    df = pd.DataFrame({'caseid': caseid, 
                           'actid':actid, 
                           'actseq':actseq, 
                           'resid':resid, 
                           'ts':ts, 
                           'sT': startTime})        
    df['preid'] = df['actid'].shift(1)
    df['preid'] = df.apply(lambda row: row['preid'] if row['actseq']!=0 else 'START', axis = 1)

    return df

def n_cases(log, top_trace_n = MAX_TRACES):
    if top_trace_n == MAX_TRACES:
        df = filtered_log_df(log)
    else:
        df = filtered_log_df(log, top_trace_n)
    return len(df['caseid'].unique())
    

def n_events(log):
    df = filtered_log_df(log)
    return len(df)
    
def n_activities(log):
    df = filtered_log_df(log)
    return len(df['actid'].unique())

def n_resources(log):
    df = filtered_log_df(log)
    return len(df['resid'].unique())

def n_traces(log, top_trace_n = MAX_TRACES):
    if top_trace_n == MAX_TRACES:
        traces_with_count = case_statistics.get_variant_statistics(log) #parameters=("max_variants_to_return":5)
    else:
        traces_with_count = case_statistics.get_variant_statistics(log, parameters={"max_variants_to_return":top_trace_n})
    
    df = pd.DataFrame.from_dict([dict(x) for x in traces_with_count])
    return len(df)

def acts_df(log):
    activities = attributes_filter.get_attribute_values(log, "concept:name")
    actid = []
    cnt = []
    for act0 in activities.items():
        actid.append(act0[0])
        cnt.append(act0[1])    
    return pd.DataFrame({'id':actid, 'cnt':cnt})

def traces_df(log):
    traces = case_statistics.get_variant_statistics(log)    
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
    trace_df['pre_post'] = trace_df.apply(lambda row: row['preid']+"@@"+row['actid'], axis = 1)
    
#    def actid2num(sactid, df):
#        nactid = -1
#        for i in range(0, len(df)):
#            if df['id'][i] == sactid:
#                nactid = i/len(df)
#        return nactid
#    
#    act_df = acts_df(log)
#    trace_df['nactid'] = trace_df['actid'].apply(lambda i:actid2num(i, act_df))
    return trace_df
    
    
def sort_df(log):
    df = filtered_log_df(log) 
    dur = np.zeros(len(df))
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
            for j in range(evS, evE+1):
                dur[j] = df['sT'][evE-1]

    df['dur'] = dur
    
    sort_df = df.sort_values(by=['dur','caseid', 'actseq'], ascending = [0,1,1])
 
    sortid = 0
    sid = np.zeros(len(sort_df))
    for i in range(1, len(sort_df)):
        if i < len(sort_df) - 1:
            if sort_df.iloc[i,:]['caseid'] != sort_df.iloc[i-1,:]['caseid']:
                sortid = sortid + 1
    
        sid[i] = sortid
        
    sort_df['sid'] = sid
    return sort_df

def mtx_df(log):
    df = traces_df(log)
    prelist = (df['preid'].unique())
    actlist = (df['actid'].unique())
    dff = pd.DataFrame(columns=prelist,index = actlist)
#    dff.columns = actlist
#    dff.index = prelist

    mtxdf1 = df.groupby('pre_post')['cnt'].sum() #agg(['sum','count','mean'])
    #mtxdf1['abs'] = mtxdf1['sum']/mtxdf1['count']
#    mtxdf= pd.DataFrame({'pre_post':mtxdf1.index, 'cnt': list(mtxdf1)})
    
    for s in mtxdf1.index:
        a = s.split("@@")
        if len(a) != 2:
            print(a[0], a[1])
        else:
            dff[a[0]][a[1]] = mtxdf1[s]

    return dff
    
#
#activities = log_attributes_filter.get_attribute_values(log, "concept:name")
#actid = []
#cnt = []
#for act0 in activities.items():
#    actid.append(act0[0])
#    cnt.append(act0[1])
#
#act_df = pd.DataFrame({'id':actid, 'cnt':cnt})
#
#n_activities = len(act_df)
#
#from pm4py.statistics.traces.log import case_statistics
#traces = case_statistics.get_variant_statistics(log)#, parameters={"max_variants_to_return": 5})
#
##acts = []
##cnt = []
##tid = []
##idx = 0
##for trace in traces:
##    tid.append(idx)
##    acts.append(trace['variant'])
##    cnt.append(trace['count'])
##    idx = idx + 1
##    
##trace_df = pd.DataFrame({'id': tid, 'acts': acts, 'cnt':cnt})
##n_traces = len(trace_df)
#
#tid = []
#actid = []
#actseq = []
#cnt = []
#n_traces = 0
#for trace in traces:
#    actidx = 0
#    acts = trace['variant']
#    for s in acts.split(','):
#        tid.append(n_traces)
#        actid.append(s)
#        actseq.append(actidx)
#        cnt.append(trace['count'])
#        actidx = actidx+1
#    n_traces = n_traces + 1
#    
#trace_df = pd.DataFrame({'id': tid, 'actid': actid, 'actseq':actseq, 'cnt':cnt})
#trace_df['preid'] = trace_df['actid'].shift(1)
#trace_df['preid'] = trace_df.apply(lambda row: row['preid'] if row['actseq']!=0 else 'START', axis = 1)
##trace_df['postid'] = trace_df['actid'].shift(1)
##trace_df['postid'] = trace_df.apply(lambda row: row['preid'] if row['actseq']!=0 else 'START', axis = 1)
#
#trace_df['pre_post'] = trace_df.apply(lambda row: row['preid']+"-"+row['actid'], axis = 1)
#
#def actid2num(sactid, df):
#    nactid = -1
#    for i in range(0, len(df)):
#        if df['id'][i] == sactid:
#            nactid = i/len(df)
#    return nactid
#
##actid2num("Confirmation of receipt", act_df)
#
#trace_df['nactid'] = trace_df['actid'].apply(lambda i:actid2num(i, act_df))
#
## matrix
#df['pre_post'] = df.apply(lambda row: row['preid']+"-"+row['actid'], axis = 1)
##mtxdf1 = pd.DataFrame({'ant':df['preid'],'con':df})
#mtxdf1 = df[df['preid']!='START'].groupby('pre_post')['caseid'].count() #agg(['sum','count','mean'])
##mtxdf1['abs'] = mtxdf1['sum']/mtxdf1['count']
#mtxdf= pd.DataFrame({'pre_post':mtxdf1.index, 'cnt': list(mtxdf1)})
#
##roles Detection: related to resource vs activity?
##from pm4py.algo.enhancement.roles import factory as roles_factory
##roles = roles_factory.apply(log)
#aaa

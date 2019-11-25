# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:55:51 2019

@author: Wei
"""

import os
import time

from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.discovery.inductive import factory as inductive_factory
from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.algo.filtering.pandas.cases import case_filter
from pm4py.algo.filtering.pandas.end_activities import end_activities_filter
from pm4py.algo.filtering.pandas.start_activities import start_activities_filter
from pm4py.objects.log.adapters.pandas import csv_import_adapter as csv_import_adapter
from pm4py.statistics.traces.pandas import case_statistics
from pm4py.util import constants
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.visualization.petrinet.util import vis_trans_shortest_paths


MAX_NO_ACTIVITIES = 25
GENERATED_IMAGES = []
REMOVE_GENERATED_IMAGES = True

inputLog = os.path.join("..", "tests", "input_data", "running-example.csv")
CASEID_GLUE = "case:concept:name"
ACTIVITY_KEY = "concept:name"
TIMEST_KEY = "time:timestamp"
TIMEST_COLUMNS = ["time:timestamp"]
TIMEST_FORMAT = None
ENABLE_ATTRIBUTE_FILTER = True
ATTRIBUTE_TO_FILTER = "concept:name"
ATTRIBUTE_VALUES_TO_FILTER = ["reject request"]
ENABLE_STARTACT_FILTER = True
STARTACT_TO_FILTER = ["register request"]
ENABLE_ENDACT_FILTER = True
ENDACT_TO_FILTER = ["pay compensation"]
DELETE_VARIABLES = False

def calculate_process_schema_from_df(dataframe, path_frequency, path_performance):
    activities_count = attributes_filter.get_attribute_values(dataframe, attribute_key=ACTIVITY_KEY)
    [dfg_frequency, dfg_performance] = df_statistics.get_dfg_graph(dataframe, measure="both",
                                                                   perf_aggregation_key="median",
                                                                   case_id_glue=CASEID_GLUE, activity_key=ACTIVITY_KEY,
                                                                   timestamp_key=TIMEST_KEY, sort_caseid_required=False)
    net, initial_marking, final_marking = inductive_factory.apply_dfg(dfg_frequency)
    spaths = vis_trans_shortest_paths.get_shortest_paths(net)
    aggregated_statistics = vis_trans_shortest_paths.get_decorations_from_dfg_spaths_acticount(net, dfg_frequency,
                                                                                               spaths,
                                                                                               activities_count,
                                                                                               variant="frequency")
    parameters_viz = {"format": "png"}
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking, variant="frequency",
                                aggregated_statistics=aggregated_statistics, parameters=parameters_viz)
    pn_vis_factory.save(gviz, path_frequency)
    aggregated_statistics = vis_trans_shortest_paths.get_decorations_from_dfg_spaths_acticount(net, dfg_performance,
                                                                                               spaths,
                                                                                               activities_count,
                                                                                               variant="performance")
    parameters_viz = {"format": "png"}
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking, variant="performance",
                                aggregated_statistics=aggregated_statistics, parameters=parameters_viz)
    pn_vis_factory.save(gviz, path_performance)

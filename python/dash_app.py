# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 22:49:04 2019

@author: Wei
"""

# -*- coding: utf-8 -*-
#import base64
#import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
#import pathlib

from dash.dependencies import Input, Output, State
from scipy import stats
import pm4pyPlus as ppp

#import process_csv as pscsv

group_colors = {"control": "light blue", "reference": "red"}

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

#PATH = pathlib.Path(__file__).parent
#DATA_PATH = PATH.joinpath("data").resolve()
#default_csv_data = pd.read_csv(DATA_PATH.joinpath("running-example.csv"))
#default_study_data = pd.read_csv(DATA_PATH.joinpath("study.csv"))

#from pm4py.objects.log.importer.xes import factory as xes_importer
#default_log = xes_importer.apply(str(DATA_PATH.joinpath("receipt.xes")))

testdf = ppp.trace_df[ppp.trace_df['id']==0]
#
#ttfig = go.Figure(data=[
#    go.Bar(x=testdf['actseq'], y=testdf['id'],orientation='h')
#])
## Change the bar mode
#ttfig.update_layout(barmode='stack')
#
import plotly.express as px
#ttfig = px.bar(ppp.trace_df, x="actseq", y="id", color='actid', orientation='h',
#             #hover_data=["tip", "size"],
#             height=1000,
#             title='Top Trace')

ttfig = go.Figure(
        data = go.Scatter(y = ppp.trace_df['actseq'],
                                    x= ppp.trace_df['id'],
                                    mode='markers', 
                                    #height=1000,
                                    orientation = 'h',
                                    marker = dict(color= np.random.randn(120),#ppp.trace_df['actid'],
                                                  symbol='square')))
#tips = px.data.tips()
#ttfig = px.bar(tips, x="total_bill", y="sex", color='day', orientation='h',
#             hover_data=["tip", "size"],
#             height=400,
#             title='Restaurant bills')


#time
dtfig = px.scatter(ppp.sort_df, x="sT", y="sid", color="actid")
                 #size='petal_length', hover_data=['petal_width'])

#mtxfig1 = go.Figure(data=go.Heatmap(
#       z=[[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
#       x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
#       y=['Morning', 'Afternoon', 'Evening']))


app.layout = html.Div(
    children=[
        # Error Message
#        html.Div(id="error-message"),
        # Top Banner
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title", children="PM4PY Demo"),
#                html.Div(
#                    className="div-logo",
#                    children=html.Img(
#                        className="logo", src=app.get_asset_url("dash-logo-new.png")
#                    ),
#                ),
                html.H2(className="h2-title-mobile", children="PM4PY Demo"),
            ],
        ),
                
        # settings and key elements
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="user-control two columns",
                    children=[
                        html.H6("Event Log File"),
                        dcc.Upload(
                            id="upload-data",
                            className="upload",
                            children=html.Div(
                                children=[
                                    html.P("Drag and Drop or "),
                                    html.A("Select Files"),
                                ]
                            ),
                            accept=".csv,.xes"
                        ),
                    ],
                ),
                html.Div(
                    id="info-container",
                    className="row container-display",            
                    children=[
                        html.Div(
                            [#html.H6(id="eventText"), 
                                    html.H6(ppp.n_events),
                                    html.P("No. of Events")],
                            id="events",
                            className="mini_container",
                        ),
                        html.Div(
                            [#html.H6(id="caseText"), 
                                    html.H6(ppp.n_cases),
                                    html.P("Cases")],
                            id="cases",
                            className="mini_container",
                        ),
                        html.Div(
                            [#html.H6(id="traceText"), 
                                    html.H6(ppp.n_traces),
                                    html.P("Traces")],
                            id="traces",
                            className="mini_container",
                        ),
                        html.Div(
                            [#html.H6(id="activityText"),
                                    html.H6(ppp.n_activities),
                                    html.P("Activities")],
                            id="acitivities",
                            className="mini_container",
                        ),
                        html.Div(
                            [#html.H6(id="resourceText"), 
                                    html.P("Resources")],
                            id="resources",
                            className="mini_container",
                        ),
                    ],
                ),
            ],
        ),
        # Body of the App
        html.Div(
            id="content_container",
            className="row tabs",
            children=[
                dcc.Tabs(
                    id="content_tabs",
                    value="ttrace",
                    children= [
                        dcc.Tab(
                            label="Map",
                            value="promap",
                            children=[
                                html.H3("Map"),
                            ],
                        ),
                        dcc.Tab(
                            label="Top-Trace",
                            value="ttrace",
                            children=[
                                html.H3("top trace"),
                                dcc.Graph(figure = ttfig),
                            ],
                        ),
                        dcc.Tab(
                            label="Sequence",
                            value="seq",
                            children=[
                                html.H3("Sequence"),
                            ],
                        ),
                        dcc.Tab(
                            label="Time",
                            value="tim",
                            children=[
                                html.H3("Time"),
                                dcc.Graph(figure=dtfig),
                            ],
                        ),
                        dcc.Tab(
                            label="Resources",
                            value="res",
                            children=[
                                html.H3("Resources"),
                            ],
                        ),
                    ]
                ),
            ],
        ),
    ]
)


    

if __name__ == "__main__":
    app.run_server(debug=True) 
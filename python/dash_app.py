# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 22:49:04 2019

@author: Wei
"""

# -*- coding: utf-8 -*-
#import base64
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import pathlib

from dash.dependencies import Input, Output, State
from scipy import stats
import pm4pyPlus as ppd
import goPlots as gpp

group_colors = {"control": "light blue", "reference": "red"}

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

from pm4py.objects.log.importer.xes import factory as xes_importer
default_log = xes_importer.apply(str(DATA_PATH.joinpath("receipt.xes")))


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
                
        html.Div(
            className="app-body",
            children=[
                # settings
                html.Div(
                    className="card user-control two columns bg-white",
                    children=[
                        html.H6("User control"),
#                        dcc.Upload(
#                            id="upload-data",
#                            className="upload",
#                            children=html.Div(
#                                children=[
#                                    html.P("Drag and Drop or "),
#                                    html.A("Select Files"),
#                                ]
#                            ),
#                            accept=".csv,.xes"
#                        ),
                    ],
                ),
                html.Div(
                    id="main-content-container",
                    className="card-left nine columns",            
                    children=[
                        # statistics
						html.Div(
							id="stats-container",
                            className="container-display body",
							children=[
								html.Div(
									id="events",
									className="mini_container",
									children=[
											html.H6(ppd.n_events(default_log)),
											html.P("Events")],
								),
								html.Div(
									id="cases",
									className="mini_container",
									children=[ 
											html.H6(ppd.n_cases(default_log)),
											html.P("Cases")],
								),
								html.Div(
									id="traces",
									className="mini_container",
									children=[ 
											html.H6(ppd.n_traces(default_log)),
											html.P("Traces")],
								),
								html.Div(
									id="acitivities",
									className="mini_container",
									children=[
											html.H6(ppd.n_activities(default_log)),
											html.P("Activities")],
								),
								html.Div(
									id="resources",
									className="mini_container",
									children=[ 
                                            html.H6(ppd.n_traces(default_log)),
											html.P("Resources")],
								),
							],
						),
						# Body of the App
						html.Div(
							id="tabs_container",
							className="tabs body bg-white",
							children=[
								dcc.Tabs(
									id="content_tabs",
									value="seq",
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
				                                #dcc.Graph(figure = gpp.top_trace_plot(default_log)),
											],
										),
										dcc.Tab(
											label="Sequence",
											value="seq",
											children=[
												html.H3("Sequence"),
                                                dcc.Graph(figure = gpp.mtx_chart(default_log)),
											],
										),
										dcc.Tab(
											label="Time",
											value="tim",
											children=[
												html.H3("Time"),
				                                dcc.Graph(figure=gpp.dotted_chart(default_log)),
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
                    ],
                ),
            ],
        ),
    ]
)


    

if __name__ == "__main__":
    app.run_server(debug=True) 
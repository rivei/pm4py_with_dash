# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 07:06:25 2019

@author: Wei
"""

import plotly.express as px
import plotly.graph_objs as go
import pm4pyPlus as ppd

def top_trace_plot(log):
#ttfig = go.Figure(data=[
#    go.Bar(x=testdf['actseq'], y=testdf['id'],orientation='h')
#])
## Change the bar mode
#ttfig.update_layout(barmode='stack')
#
#ttfig = px.bar(ppd.trace_df, x="actseq", y="id", color='actid', orientation='h',
#             #hover_data=["tip", "size"],
#             height=1000,
#             title='Top Trace')
    df = ppd.traces_df(log)
    return go.Figure(
            data = go.Scatter(y = -df['actseq'],
                                x = df['id'],
                                mode='markers',
                                marker = dict(color= df['nactid'],#np.random.randn(120),#ppd.trace_df['actid'],
                                              colorscale = 'rainbow',#'Cividis',#'Viridis',
                                              size = 10,
                                              symbol='square')))

##ttfig.update_layout(
##    autosize=False,
##    width=400,
##    height=1000,
##    margin=go.layout.Margin(
##        l=50,
##        r=50,
##        b=100,
##        t=100,
##        pad=4
##    ),
##    paper_bgcolor="LightSteelBlue",
##)
##tips = px.data.tips()
##ttfig = px.bar(tips, x="total_bill", y="sex", color='day', orientation='h',
##             hover_data=["tip", "size"],
##             height=400,
##             title='Restaurant bills')
#
#
    
def dotted_chart(log):
    df = ppd.sort_df(log)
    return px.scatter(df, x="sT", y="sid", color="actid")
                     #size='petal_length', hover_data=['petal_width'])
#
##mtxfig1 = go.Figure(data=go.Heatmap(
##       z=[[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
##       x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
##       y=['Morning', 'Afternoon', 'Evening']))
#

import plotly.figure_factory as ff
import numpy as np
def mtx_chart(log):
    df = ppd.mtx_df(log)
    df = df.replace(np.nan,0)
    z_text = df.replace(0,"") #  new_items = [x if x % 2 else None for x in items]
    colorscale = [[0, 'white'], [1, 'blue']]
    font_colors =  ['black', 'white']# min max
    fig = ff.create_annotated_heatmap(z=df.values,x=list(df.columns),y=list(df.index),
                                      colorscale = colorscale, font_colors = font_colors,#'brbg',
                                      annotation_text=z_text.values)#, showscale=True)
    
    return fig.update_layout(width = 1000, height = 800 )
    
    
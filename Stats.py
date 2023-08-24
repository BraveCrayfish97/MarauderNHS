import streamlit as sl
from functions import *
import plotly.graph_objects as go

val = 469
fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = val,
    mode = "gauge+number",
    title = {'text': "Total Hours"},
    delta = {'reference': 380},
    gauge = {'axis': {'range': [None, 500], 'tickcolor': "white"},
             'bordercolor': "#EEEEEE",
             'borderwidth': 0.5,
             'steps' : [{'range': [0, 500], 'color': "#EEEEEE"}],
             'bar': {'color': "#CF0A0A", 'thickness': 0.7},
             'threshold' : {'line': {'color': "black", 'width': 3}, 'thickness': 0.75, 'value': 499}}))

sl.plotly_chart(fig)

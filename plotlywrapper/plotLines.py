import logging

import pandas as pd
import numpy as np

import plotly.graph_objects as go

from .shared import saveFigure

def basicLineChart(series, legend, styles=None, batch=True, plotTitle=None, color="Viridis",
                   savePlot=False, height=1000, width=1400, staicFormat="png", filename=None, folder="."):
    """
    Produces a basic plot with mulitple lines

    Args:
      series (list) : List of series to be plotted
      legend (list) : List of Legend items (requeired to be of same length as passed series

      savePlot (bool) : If true the plot will be saved
      height (int) : Image height
      width (int) : Image width
      staicFormat (str) : Choose from: png, jpeg, pdf, svg 
      filename (str) : File name
      folder (str) : Output folder
    """

    if len(series) != len(legend):
        raise RuntimeError("Passed legend and series are not of equal length")

    if styles is not None:
        if not isinstance(styles, list):
            raise TypeError("Object of type %s was passed for styles but has to be list"%(type(styles)))
        if len(styles) != len(legend):
            raise RuntimeError("Passed styles and series/legend are not of equal length")


    fig = go.Figure()
    for i in range(len(series)):
        fig.add_trace(go.Scatter(x=series[i].index,
                                 y=series[i].values,
                                 mode='lines' if styles is None else styles[i],
                                 name=legend[i]))
    
    if not batch:
        fig.show()
    
    if savePlot:
        return saveFigure(fig, height, width, staicFormat, filename, folder)

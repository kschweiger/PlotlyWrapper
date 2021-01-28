import logging

import pandas as pd
import numpy as np

import plotly.graph_objects as go

from .shared import saveFigure

def basicLineChart(series, legend, styles=None, batch=True, plotTitle=None, color="Viridis",
                   xTitle=None, yTitle=None, lineWidth=None, scaleTitles=1, scaleTicks=1,
                   legend_position = (0.01, 0.99),
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
      xTitle (str) : Title of the x Axis
      yTitle (str) : Title of the y Axis
      lineWidth (int, list) : Set the line size of all lines (int) or each line (list)
      scaleTitles (float) : Scaling factor for the x,y and plot title
      scaleTicks (float) : Scaling factor for the x,y axis ticks
      legend_position (tuple) : x and y start postions of the legend
    """

    if len(series) != len(legend):
        raise RuntimeError("Passed legend and series are not of equal length")

    if styles is not None:
        if not isinstance(styles, list):
            raise TypeError("Object of type %s was passed for styles but has to be list"%(type(styles)))
        if len(styles) != len(legend):
            raise RuntimeError("Passed styles and series/legend are not of equal length")

    if lineWidth is None:
        lineWidths = [2 for i in range(len(series))]
    else:
        if isinstance(lineWidth, int):
            lineWidths = [lineWidth for i in range(len(series))]
        elif isinstance(lineWidth, list):
            if len(lineWidth) != len(legend):
                raise RuntimeError("Passed lineWidth and series/legend are not of equal length")
            else:
                lineWidths = lineWidth
        else:
            raise TypeError("Object of type %s was passed for lineWidth but has to be list or int"%(type(styles)))


    if not len(legend_position) == 2:
        raise TypeError("Pass tuple with two elements as legend_position")
    
    leg_x, leg_y = legend_position
    if not (isinstance(leg_x, float) and isinstance(leg_y, float)):
        raise TypeError("Values in the legend postion must be float")

    logging.debug("Legend postions: x = %s | y = %s", leg_x, leg_y)

    fig = go.Figure()
    for i in range(len(series)):
        fig.add_trace(go.Scatter(x=series[i].index,
                                 y=series[i].values,
                                 mode='lines' if styles is None else styles[i],
                                 line=dict(width=lineWidths[i]),
                                 name=legend[i]))

    if plotTitle is not None:
        fig.update_layout(title=plotTitle)
    if xTitle is not None:
        fig.update_layout(xaxis_title=xTitle)
    if yTitle is not None:
        fig.update_layout(yaxis_title=yTitle)

    fig.update_layout(
        title_font_size = 35*scaleTitles,
        xaxis_title_font_size = 30*scaleTitles,
        yaxis_title_font_size = 30*scaleTitles,
        xaxis=dict(
            tickfont=dict(
                size=25*scaleTicks,
            ),
        ),
        yaxis=dict(
            tickfont=dict(
                size=25*scaleTicks,
            ),
        ),
        legend=dict(
            yanchor="top",
            y=leg_y,
            xanchor="left",
            x=leg_x,
            font_size=25*scaleTitles,
        )
    )

        
    if not batch:
        fig.show()
    
    if savePlot:
        return saveFigure(fig, height, width, staicFormat, filename, folder)

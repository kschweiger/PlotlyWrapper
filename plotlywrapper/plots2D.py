import logging
import os
import itertools

import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from .shared import saveFigure

def correlationMatrix(data, annotated=False, batch=True, plotTitle=None, reverseOrder=True, color="Viridis", removeDuplicates=False,
                      savePlot=False, height=1000, width=1400, staicFormat="png", filename=None, folder="."):
    """
    Plots the correlation between all feateres in the dataframe

    Args:
      data (pd.DataFrame) : Dataframe with samples/events in rows and featueres in columns.
                                 Make sure to drop unwanted rows (like the target) before passing 
      annotated (bool) : If True, the cooorealtion values will be shown in the corresponding bins
      batch (bool) : If True, the figure will not be shown but only saved
      plotTitle (str) : Custom plot title
      reverseOrder (bool) : Only has effect if annotated is true. Will reverse to oder of y axis.
      removeDuplicates (bool) : Remove the upper half of the correlation plot
      color (str) : Valid plotly color scale
    
      savePlot (bool) : If true the plot will be saved
      height (int) : Image height
      width (int) : Image width
      staicFormat (str) : Choose from: png, jpeg, pdf, svg 
      filename (str) : File name
      folder (str) : Output folder
    """
    corr = data.corr()
    if removeDuplicates:
        corr_ = data.corr()
        logging.info("Will reomve all elements above diagonal")
        for r in range(len(corr[0])):
            for c in range(r+1, len(corr[0])):
                corr_[c][r] = np.nan
        corr = corr_
    if annotated:
        logging.debug("Will plot annoted heatmap")
        corr_text = np.around(corr.values, decimals=2)
        fig = ff.create_annotated_heatmap(z=corr.values,
                                          annotation_text=corr_text,
                                          hoverinfo='z',
                                          x =[str(c) for c in corr.columns],
                                          y= [str(c) for c in corr.columns],
                                          colorscale=color)
    else:
        logging.debug("Will plot regular heatmap")
        fig = go.Figure(
            data=[
                go.Heatmap(z=corr,
                           x = corr.columns,
                           y= corr.columns,
                           colorscale=color,
                )
            ]
        )
    if plotTitle is None:
        fig.update_layout(title="Feature Correlation")
    else:
        fig.update_layout(title=plotTitle)

    if reverseOrder:
        fig['layout']['yaxis']['autorange'] = "reversed"
    if removeDuplicates:
        fig['layout']['xaxis']['zeroline'] = False
        fig['layout']['yaxis']['zeroline'] = False
        fig['layout']['xaxis']['showgrid'] = False
        fig['layout']['yaxis']['showgrid'] = False
        
    
    if not batch:
        fig.show()

    # Now the ouput stuff
    if savePlot:
        return saveFigure(fig, height, width, staicFormat, filename, folder)
            
    return True


def featureCorrelation(data, nRows, nColumns, batch=True, plotTitle=None, color="Viridis",
                       savePlot=False, height=1000, width=1400, staicFormat="png", filename=None, folder="."):
    """
    Will plot all two variable correlations in the passed data. Mulitple 2D plots will be put one each plot. Set 
    the number ofplots per row and columns with nRows and nColumns.

    TODO: Add title per subplot with correaltion value

    Args:
      data (pd.DataFrame) : Dataframe with samples/events in rows and featueres in columns.
                            Make sure to drop unwanted rows (like the target) before passing 
      
      nRows (int) : Number of plots per rwo
      nColumns (int) : Number of plots per column
      batch (bool) : If True, the figure will not be shown but only saved
      plotTitle (str) : Custom plot title
      color (str) : Valid plotly color scale
    
      savePlot (bool) : If true the plot will be saved
      height (int) : Image height
      width (int) : Image width
      staicFormat (str) : Choose from: png, jpeg, pdf, svg 
      filename (str) : File name
      folder (str) : Output folder
    """
    if not ( isinstance(nRows, int) and isinstance(nColumns, int)):
        raise ValueError("nRows and nColumns need to be int but are: %s / %s"%(nRows, nColumns))

    corr = data.corr()
    figures = []
    figures_titles = []
    figures_corrcoef = []

    for var1, var2 in itertools.combinations(list(data.columns), 2):
        logging.debug("Correlation for %s / %s", var1, var2)
        figures.append(
            go.Histogram2d(
                x = data[var1],
                y = data[var2],
                coloraxis = 'coloraxis1'
            )
        )
        figures_titles.append((var1, var2))
        figures_corrcoef.append(np.corrcoef(data[var1].values, data[var2].values)[0][1])
        
    nSubplotsPerPlot = nRows*nColumns
    nTotal = len(figures_titles)

    logging.debug("nSubplotsPerPlot = %s", nSubplotsPerPlot)
    logging.debug("nTotal = %s", nTotal)
    
    if round(nTotal/nSubplotsPerPlot) < nTotal/nSubplotsPerPlot:
        nPlots = round(nTotal/nSubplotsPerPlot)+1
    else:
        nPlots = round(nTotal/nSubplotsPerPlot)


    logging.info("Will produce %s plots",nPlots)
    iPlotted = 0
    iCorr = 0
    for i in range(nPlots):
        logging.info("Producing plot %s", i)
        
        subplotTitles = []
        for ir in range(nRows):
            for ic in range(nColumns):
                subplotTitles.append(
                    "Correlation: {:.4f}".format(float(figures_corrcoef[iCorr]))
                )
                iCorr += 1
                if iCorr >= nTotal:
                    break
                
        fig = make_subplots(nRows, nColumns, subplot_titles=subplotTitles)
        for ir in range(nRows):
            for ic in range(nColumns):
                logging.debug("Plot %s -- iPlotted = %s / row = %s / column = %s", i, iPlotted, ir+1 ,ic+1)
                fig.add_trace(figures[iPlotted], row=ir+1 , col=ic+1)
                fig.update_xaxes(title_text=figures_titles[iPlotted][0], row=ir+1, col=ic+1)
                fig.update_yaxes(title_text=figures_titles[iPlotted][1], row=ir+1, col=ic+1)
                iPlotted += 1
                if iPlotted >= nTotal:
                    break

        #Shared z axis:
        fig.update_layout(coloraxis1 = {'colorscale':color})
        if plotTitle is None:
            fig.update_layout(title="Feature Correlations")
        else:
            fig.update_layout(title=plotTitle)
            
        if not batch:
            fig.show()

        if savePlot:
            if not saveFigure(fig, height, width, staicFormat, filename+"_"+str(i), folder):
                return False
            
    return True


if __name__ == "__main__":
    testCorrMatrix = False
    testFeaturePlots = True
    log_format = ('[%(asctime)s] %(funcName)-'+str(30)+'s %(levelname)-8s %(message)s')
    logging.basicConfig(
        format=log_format,
        level=logging.DEBUG,
    )
    
    df = pd.DataFrame(np.random.random_sample((100, 5)))

    if testCorrMatrix:
        print("----- Regular ------")
        correlationMatrix(df, batch=False)
        print("----- Regular (reomve upper half)------")
        correlationMatrix(df, batch=False, removeDuplicates=True)
        print("----- Annotated ------")
        correlationMatrix(df, annotated=True, batch=False)
        print("----- Saving -----")
        print("Should give filename Error")
        correlationMatrix(df, batch=True, savePlot=True)
        print("Should give format error")
        correlationMatrix(df, batch=True, savePlot=True, filename="corrMatrix", staicFormat="bogus")
        print("This should work")
        correlationMatrix(df, batch=True, savePlot=True, filename="corrMatrix", folder="test")

    if testFeaturePlots:
        #featureCorrelation(df, 2,3, batch=False)
        featureCorrelation(df, 2,3, batch=True, savePlot=True, filename="featureCorr", folder="test")

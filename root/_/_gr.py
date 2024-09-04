import pandas as pd
import uproot
import numpy as np
from ROOT import TGraph, TGraph2D, TGraphErrors, TGraph2DErrors, TGraphAsymmErrors

def get_dataframe_TGraph(TGraph: TGraph):
    """
    Converts a ROOT TGraph to a pandas DataFrame.
    
    Parameters:
    TGraph: The ROOT TGraph object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraph.
    """

    n_points = TGraph.GetN()
    x = np.zeros(n_points, dtype=np.float64)
    y = np.zeros(n_points, dtype=np.float64)

    for i in range(n_points):
        x[i] = TGraph.GetPointX(i)
        y[i] = TGraph.GetPointY(i)

    return pd.DataFrame({'x': x, 'y': y})

def get_dataframe_TGraphErrors(TGraph: TGraphErrors):
    """
    Converts a ROOT TGraphErrors to a pandas DataFrame.
    
    Parameters:
    TGraph: The ROOT TGraphErrors object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraphErrors.
    """

    n_points = TGraph.GetN()
    x = np.zeros(n_points, dtype=np.float64)
    y = np.zeros(n_points, dtype=np.float64)
    ex = np.zeros(n_points, dtype=np.float64)
    ey = np.zeros(n_points, dtype=np.float64)


    for i in range(n_points):
        x[i] = TGraph.GetPointX(i)
        y[i] = TGraph.GetPointY(i)
        ex[i] = TGraph.GetErrorX(i)
        ey[i] = TGraph.GetErrorY(i)

    
    return pd.DataFrame({'x': x, 'y': y, 'dx': ex, 'dy': ey})


def get_dataframe_TGraphAsymmErrors(TGraph: TGraphAsymmErrors):
    """
    Converts a ROOT TGraphAsymmErrors to a pandas DataFrame.
    
    Parameters:
    TGraph: The ROOT TGraphAsymmErrors object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraphAsymmErrors.
    """

    n_points = TGraph.GetN()
    x = np.zeros(n_points, dtype=np.float64)
    y = np.zeros(n_points, dtype=np.float64)
    ex_low  = np.zeros(n_points, dtype=np.float64)
    ex_high = np.zeros(n_points, dtype=np.float64)
    ey_low  = np.zeros(n_points, dtype=np.float64)
    ey_high = np.zeros(n_points, dtype=np.float64)


    for i in range(n_points):
        x[i] = TGraph.GetPointX(i)
        y[i] = TGraph.GetPointY(i)
        ex_low[i]  = TGraph.GetErrorXlow(i)
        ex_high[i] = TGraph.GetErrorXhigh(i)
        ey_low[i]  = TGraph.GetErrorYlow(i)
        ey_high[i] = TGraph.GetErrorYhigh(i)

    
    return pd.DataFrame({
        'x': x, 'y': y, 'dx_low': ex_low, 'dx_high': ex_high, 'dy_low': ey_low, 'dy_high': ey_high
    })


def get_dataframe_TGraph2D(TGraph: TGraph2D):
    """
    Converts a ROOT TGraph2D to a pandas DataFrame.
    
    Parameters:
    TGraph: The ROOT TGraph2D object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraph2D.
    """

    n_points = TGraph.GetN()
    x = np.zeros(n_points, dtype=np.float64)
    y = np.zeros(n_points, dtype=np.float64)
    z = np.zeros(n_points, dtype=np.float64)

    for i in range(n_points):
        x[i] = TGraph.GetPointX(i)
        y[i] = TGraph.GetPointY(i)
        z[i] = TGraph.GetPointZ(i)

    return pd.DataFrame({'x': x, 'y': y, 'z': z})
    

def get_dataframe_TGraph2DErrors(TGraph: TGraph2DErrors):
    """
    Converts a ROOT TGraph2DErrors to a pandas DataFrame.
    
    Parameters:
    TGraph: The ROOT TGraph2DErrors to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraph2DErrors.
    """

    n_points = TGraph.GetN()
    x = np.zeros(n_points, dtype=np.float64)
    y = np.zeros(n_points, dtype=np.float64)
    z = np.zeros(n_points, dtype=np.float64)
    ex = np.zeros(n_points, dtype=np.float64)
    ey = np.zeros(n_points, dtype=np.float64)
    ez = np.zeros(n_points, dtype=np.float64)

    for i in range(n_points):
        x[i]  = TGraph.GetPointX(i)
        y[i]  = TGraph.GetPointY(i)
        z[i]  = TGraph.GetPointZ(i)
        ex[i] = TGraph.GetErrorX(i)
        ey[i] = TGraph.GetErrorY(i)
        ez[i] = TGraph.GetErrorZ(i)


    return pd.DataFrame({'x': x, 'y': y, 'z': z, 'dx': ex, 'dy': ey, 'dz': ez})
import pandas as pd
import uproot
import numpy as np
from ROOT import TGraph, TGraph2D, TGraphErrors, TGraph2DErrors, TGraphAsymmErrors

def _get_dataframe_TGraph(tgraph: TGraph):
    """
    Converts a ROOT TGraph to a pandas DataFrame.
    
    Parameters:
    tgraph: The ROOT TGraph object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraph.
    """

    n_points = tgraph.GetN()
    x = np.zeros(n_points, dtype=np.float64)
    y = np.zeros(n_points, dtype=np.float64)

    for i in range(n_points):
        x[i] = tgraph.GetPointX(i)
        y[i] = tgraph.GetPointY(i)

    return pd.DataFrame({'x': x, 'y': y})


def _get_dataframe_TH1_uproot(hist):
    """
    Converts an uproot TH1 or TProfile object to a pandas DataFrame.
    
    Parameters:
    hist: The uproot TH1 or TProfile object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TH1F.
    """
    if not uproot.Model.is_instance(hist, "TH1"): raise ValueError(f"{type(hist)} is not an uproot TH1 object!")

    return pd.DataFrame({
        'x':  np.array(hist.axis().centers(), dtype=np.float64),
        'y':  np.array(hist.values(),         dtype=np.float64),
        'ex': np.array((hist.axis().edges()[1:] - hist.axis().edges()[:-1])/2,
                                              dtype=np.float64),
        'ey': np.array(hist.errors(),         dtype=np.float64)
    })


def _get_dataframe_TGraphErrors(tgraph: TGraphErrors):
    """
    Converts a ROOT TGraphErrors to a pandas DataFrame.
    
    Parameters:
    tgraph: The ROOT TGraphErrors object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraphErrors.
    """
    if not uproot.Model.is_instance(tgraph, "TGraph"): raise ValueError(f"{type(tgraph)} is not an uproot TGraphErrors object!")

    n_points = tgraph.GetN()
    x  = np.zeros(n_points, dtype=np.float64)
    y  = np.zeros(n_points, dtype=np.float64)
    ex = np.zeros(n_points, dtype=np.float64)
    ey = np.zeros(n_points, dtype=np.float64)


    for i in range(n_points):
        x[i]  = tgraph.GetPointX(i)
        y[i]  = tgraph.GetPointY(i)
        ex[i] = tgraph.GetErrorX(i)
        ey[i] = tgraph.GetErrorY(i)

    
    return pd.DataFrame({'x': x, 'y': y, 'ex': ex, 'ey': ey})




def _get_dataframe_TGraphAsymmErrors_uproot(tgraph: uproot.models.TGraph.Model_TGraphAsymmErrors_v3):
    """
    Converts an uproot TGraphAsymmErrors to a pandas DataFrame.
    
    Parameters:
    TGraph: The uproot TGraphAsymmErrors object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraphAsymmErrors.
    """
    if not uproot.Model.is_instance(tgraph, "TGraphErrors"):
        raise ValueError(f"{type(tgraph)} is not an uproot TGraphErrors object!")

    return pd.DataFrame({
        'x':   np.array(tgraph.member("fX"),      dtype=np.float64),
        'y':   np.array(tgraph.member("fY"),      dtype=np.float64),
        'exl': np.array(tgraph.member("fEXlow"),  dtype=np.float64),
        'exh': np.array(tgraph.member("fEXhigh"), dtype=np.float64),
        'eyl': np.array(tgraph.member("fEYlow"),  dtype=np.float64),
        'eyh': np.array(tgraph.member("fEYhigh"), dtype=np.float64)
    })


def _get_dataframe_TGraphAsymmErrors(tgraph: TGraphAsymmErrors):
    """
    Converts a ROOT TGraphAsymmErrors to a pandas DataFrame.
    
    Parameters:
    tgraph: The ROOT TGraphAsymmErrors object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraphAsymmErrors.
    """
    if not uproot.Model.is_instance(tgraph, "TGraphAsymmErrors"):
        raise ValueError(f"{type(tgraph)} is not an uproot TGraphAsymmErrors object!")

    n_points = tgraph.GetN()
    x       = np.zeros(n_points, dtype=np.float64)
    y       = np.zeros(n_points, dtype=np.float64)
    ex_low  = np.zeros(n_points, dtype=np.float64)
    ex_high = np.zeros(n_points, dtype=np.float64)
    ey_low  = np.zeros(n_points, dtype=np.float64)
    ey_high = np.zeros(n_points, dtype=np.float64)


    for i in range(n_points):
        x[i]       = tgraph.GetPointX(i)
        y[i]       = tgraph.GetPointY(i)
        ex_low[i]  = tgraph.GetErrorXlow(i)
        ex_high[i] = tgraph.GetErrorXhigh(i)
        ey_low[i]  = tgraph.GetErrorYlow(i)
        ey_high[i] = tgraph.GetErrorYhigh(i)

    
    return pd.DataFrame({
        'x': x, 'y': y, 'exl': ex_low, 'exh': ex_high, 'eyl': ey_low, 'eyh': ey_high
    })



def _get_dataframe_TGraph2D(tgraph: TGraph2D):
    """
    Converts a ROOT TGraph2D to a pandas DataFrame.
    
    Parameters:
    tgraph: The ROOT TGraph2D object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraph2D.
    """
    
    if not uproot.Model.is_instance(tgraph, "TGraph2D"): raise ValueError(f"{type(tgraph)} is not an uproot TGraph2D object!")

    n_points = tgraph.GetN()
    x = np.zeros(n_points, dtype=np.float64)
    y = np.zeros(n_points, dtype=np.float64)
    z = np.zeros(n_points, dtype=np.float64)

    for i in range(n_points):
        x[i] = tgraph.GetPointX(i)
        y[i] = tgraph.GetPointY(i)
        z[i] = tgraph.GetPointZ(i)

    return pd.DataFrame({'x': x, 'y': y, 'z': z})
    

def _get_dataframe_TGraph2DErrors(tgraph: TGraph2DErrors):
    """
    Converts a ROOT TGraph2DErrors to a pandas DataFrame.
    
    Parameters:
    tgraph: The ROOT TGraph2DErrors to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraph2DErrors.
    """
    if not uproot.Model.is_instance(tgraph, "TGraph2DErrors"): raise ValueError(f"{type(tgraph)} is not an uproot TGraph2DErrors object!")

    n_points = tgraph.GetN()
    x = np.zeros(n_points,  dtype=np.float64)
    y = np.zeros(n_points,  dtype=np.float64)
    z = np.zeros(n_points,  dtype=np.float64)
    ex = np.zeros(n_points, dtype=np.float64)
    ey = np.zeros(n_points, dtype=np.float64)
    ez = np.zeros(n_points, dtype=np.float64)

    for i in range(n_points):
        x[i]  = tgraph.GetPointX(i)
        y[i]  = tgraph.GetPointY(i)
        z[i]  = tgraph.GetPointZ(i)
        ex[i] = tgraph.GetErrorX(i)
        ey[i] = tgraph.GetErrorY(i)
        ez[i] = tgraph.GetErrorZ(i)
    return pd.DataFrame({'x': x, 'y': y, 'z': z, 'ex': ex, 'ey': ey, 'ez': ez})
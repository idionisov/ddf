import ROOT
import numpy as np
import pandas as pd


def getPandasFromTGraph(tgraph: ROOT.TGraph):
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



def getPandasFromTGraphErrors(tgraph: ROOT.TGraphErrors):
    """
    Converts a ROOT TGraphErrors to a pandas DataFrame.

    Parameters:
    tgraph: The ROOT TGraphErrors object to be converted.

    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraphErrors.
    """

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



def getPandasFromTGraphAsymmErrors(tgraph: ROOT.TGraphAsymmErrors):
    """
    Converts a ROOT TGraphAsymmErrors to a pandas DataFrame.

    Parameters:
    tgraph: The ROOT TGraphAsymmErrors object to be converted.

    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraphAsymmErrors.
    """

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



def getPandasFromTGraph2D(tgraph: ROOT.TGraph2D):
    """
    Converts a ROOT TGraph2D to a pandas DataFrame.

    Parameters:
    tgraph: The ROOT TGraph2D object to be converted.

    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraph2D.
    """

    n_points = tgraph.GetN()
    x = np.zeros(n_points, dtype=np.float64)
    y = np.zeros(n_points, dtype=np.float64)
    z = np.zeros(n_points, dtype=np.float64)

    for i in range(n_points):
        x[i] = tgraph.GetPointX(i)
        y[i] = tgraph.GetPointY(i)
        z[i] = tgraph.GetPointZ(i)

    return pd.DataFrame({'x': x, 'y': y, 'z': z})




def getPandasFromUprootTGraphAsymmErrors(tgraph):
    """
    Converts an uproot TGraphAsymmErrors to a pandas DataFrame.

    Parameters:
    TGraph: The uproot TGraphAsymmErrors object to be converted.

    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TGraphAsymmErrors.
    """
    if not uproot.Model.is_instance(tgraph, "TGraphAsymmErrors"):
        raise ValueError(f"{type(tgraph)} is not an uproot TGraphAsymmErrors object!")

    return pd.DataFrame({
        'x':   np.array(tgraph.member("fX"),      dtype=np.float64),
        'y':   np.array(tgraph.member("fY"),      dtype=np.float64),
        'exl': np.array(tgraph.member("fEXlow"),  dtype=np.float64),
        'exh': np.array(tgraph.member("fEXhigh"), dtype=np.float64),
        'eyl': np.array(tgraph.member("fEYlow"),  dtype=np.float64),
        'eyh': np.array(tgraph.member("fEYhigh"), dtype=np.float64)
    })

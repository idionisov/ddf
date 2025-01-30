from typing import Union
from ROOT import TH1, TH2, TH3
import numpy as np
import pandas as pd
import uproot

def isTH1(obj):
    if isinstance(obj, TH1) and not isinstance(obj, (TH2, TH3)):
        return True
    else:
        return False


def isTH2(obj):
    if isinstance(obj, TH2) and not isinstance(obj, TH3):
        return True
    else:
        return False


def getNumpyFromTH2(
    hist: TH2,
    xmin: Union[float, None] = None,
    xmax: Union[float, None] = None,
    ymin: Union[float, None] = None,
    ymax: Union[float, None] = None
) -> tuple:
    xBinEdges = []
    yBinEdges = []

    filteredBins = []
    filteredBinsErrLow = []
    filteredBinsErrUp = []


    for yBin in range(1, hist.GetYaxis().GetNbins() + 1):
        yLow = hist.GetYaxis().GetBinLowEdge(yBin)
        yUp  = hist.GetYaxis().GetBinUpEdge(yBin)

        if (ymin is not None and yLow < ymin) or (ymax is not None and yUp > ymax):
            continue

        if yBinEdges == []:
            yBinEdges.append(yLow)
        yBinEdges.append(yUp)


    for xBin in range(1, hist.GetXaxis().GetNbins() + 1):
        xLow = hist.GetXaxis().GetBinLowEdge(xBin)
        xUp  = hist.GetXaxis().GetBinUpEdge(xBin)

        if (xmin is not None and xLow < xmin) or (xmax is not None and xUp > xmax):
            continue

        if xBinEdges == []:
            xBinEdges.append(xLow)
        xBinEdges.append(xUp)

        yRow = []
        yRowErrLow = []
        yRowErrUp = []

        for yBin in range(1, hist.GetYaxis().GetNbins() + 1):
            yLow = hist.GetYaxis().GetBinLowEdge(yBin)
            yUp  = hist.GetYaxis().GetBinUpEdge(yBin)

            if (ymin is not None and yLow < ymin) or (ymax is not None and yUp > ymax):
                continue


            yRow.insert(0, hist.GetBinContent(xBin, yBin))
            yRowErrLow.insert(0, hist.GetBinErrorLow(xBin, yBin))
            yRowErrUp.insert(0, hist.GetBinErrorUp(xBin, yBin))

        if yRow:
            filteredBins.append(yRow)
            filteredBinsErrLow.append(yRowErrLow)
            filteredBinsErrUp.append(yRowErrUp)



    xBinEdges = np.array(xBinEdges, dtype=np.float64)
    yBinEdges = np.array(yBinEdges, dtype=np.float64)
    hArr = np.array(filteredBins, dtype=np.float64).T
    hArrErrLow = np.array(filteredBinsErrLow, dtype=np.float64).T
    hArrErrUp = np.array(filteredBinsErrUp, dtype=np.float64).T

    return hArr, hArrErrLow, hArrErrUp, xBinEdges, yBinEdges


def getNumpyFromUprootTH2(hist,
    xmin: Union[float, None] = None,
    xmax: Union[float, None] = None,
    ymin: Union[float, None] = None,
    ymax: Union[float, None] = None
) -> tuple:
    """
    Takes an uproot TH2 histogram and optional axis ranges.
    Returns a numpy array of the bin contents within selected ranges and arrays of bin edges.

    Parameters:
    - hist (uproot.behaviors.TH2.TH2): The uproot 2D histogram.
    - xmin (float, optional): Minimum x-axis value.
    - xmax (float, optional): Maximum x-axis value.
    - ymin (float, optional): Minimum y-axis value.
    - ymax (float, optional): Maximum y-axis value.

    Returns:
    - numpy.array: A 2D array of the bin contents.
    - numpy.array: A 1D array of the x-axis bin edges.
    - numpy.array: A 1D array of the y-axis bin edges.
    """

    # Get the bin edges (CALL the edges method, do not access as an attribute)
    x_edges = np.array(hist.axis(0).edges(), dtype=np.float64)
    y_edges = np.array(hist.axis(1).edges(), dtype=np.float64)
    bin_contents = np.array(hist.values(), dtype=np.float64)

    # Find the range indices, ensuring None values don't break the function
    x_first_bin = 0 if xmin is None else np.searchsorted(x_edges, xmin, side='left')
    x_last_bin = len(x_edges) - 1 if xmax is None else np.searchsorted(x_edges, xmax, side='right')

    y_first_bin = 0 if ymin is None else np.searchsorted(y_edges, ymin, side='left')
    y_last_bin = len(y_edges) - 1 if ymax is None else np.searchsorted(y_edges, ymax, side='right')

    # Slice the bin contents based on computed indices
    data = bin_contents[x_first_bin:x_last_bin, y_first_bin:y_last_bin]
    bin_edges_x = x_edges[x_first_bin:x_last_bin + 1]
    bin_edges_y = y_edges[y_first_bin:y_last_bin + 1]

    return data.T, bin_edges_x, bin_edges_y




def getPandasFromTH1(hist: TH1):
    """
    Converts a PyROOT TH1 or TProfile object to a pandas DataFrame.

    Parameters:
    hist: The PyROOT TH1 or TProfile object to be converted.

    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TH1.
    """
    if not isinstance(hist, (ROOT.TH1, ROOT.TProfile)):
        raise ValueError(f"{type(hist)} is not a PyROOT TH1 or TProfile object!")

    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX() + 1)], dtype=np.float64)
    y = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX() + 1)], dtype=np.float64)
    ex = np.array([hist.GetBinWidth(i) / 2 for i in range(1, hist.GetNbinsX() + 1)], dtype=np.float64)
    ey = np.array([hist.GetBinError(i) for i in range(1, hist.GetNbinsX() + 1)], dtype=np.float64)

    return pd.DataFrame({
        'x': x,
        'y': y,
        'ex': ex,
        'ey': ey
    })


def getPandasFromUprootTH1(hist):
    """
    Converts an uproot TH1 or TProfile object to a pandas DataFrame.

    Parameters:
    hist: The uproot TH1 or TProfile object to be converted.

    Returns:
    pandas.DataFrame: A DataFrame containing the values of the TH1F.
    """
    if not uproot.Model.is_instance(hist, "TH1"):
        raise ValueError(f"{type(hist)} is not an uproot TH1 object!")

    return pd.DataFrame({
        'x':  np.array(hist.axes[0].centers(), dtype=np.float64),
        'y':  np.array(hist.values(),          dtype=np.float64),
        'ex': np.array((hist.axes[0].edges()[1:] - hist.axes[0].edges()[:-1])/2,
                                               dtype=np.float64),
        'ey': np.array(hist.errors(),          dtype=np.float64)
    })

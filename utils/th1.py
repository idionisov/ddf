from typing import Union
from ROOT import TH1, TH2, TH3
import numpy as np

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

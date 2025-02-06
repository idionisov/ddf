from typing import Union
import ROOT
import numpy as np
import pandas as pd
import uproot
from ddfUtils import getArrayCenters


def getTestHists1D(
    nBins: int   = 10,
    xlow:  float = 0.,
    xhigh: float = 10.
):
    """
    Create test 1D histograms for passed and total events.
    """

    h_total  = ROOT.TH1F('h_total', 'Total Histogram', nBins, xlow, xhigh)
    h_passed = ROOT.TH1F('h_passed', 'Passed Histogram', nBins, xlow, xhigh)

    for i in range(1, nBins + 1):
        h_total.SetBinContent(i, 10)
        h_passed.SetBinContent(i, np.random.randint(0, 10))

    return h_passed, h_total



def getTestHists2D(
    nBinsX: int   = 10,
    xlow:   float = 0.,
    xhigh:  float = 10.,
    nBinsY: int   = 10,
    ylow:   float = 0.,
    yhigh:  float = 10.
):
    """
    Create test 2D histograms for passed and total events.
    """

    h_total  = ROOT.TH2F('h_total',  'Total Histogram',  nBinsX, xlow, xhigh, nBinsY, ylow, yhigh)
    h_passed = ROOT.TH2F('h_passed', 'Passed Histogram', nBinsX, xlow, xhigh, nBinsY, ylow, yhigh)

    for xbin in range(1, nBinsX + 1):
        for ybin in range(1, nBinsY + 1):
            h_total.SetBinContent(xbin, ybin, 10)
            h_passed.SetBinContent(xbin, ybin, np.random.randint(0, 10))

    return h_passed, h_total


def getTestTProfile(
    nBins: int = 10,
    xmin: float = 0.,
    xmax: float = 10.
):
    profile = ROOT.TProfile("pr_test", "Example TProfile", nBins, xmin, xmax)

    rng = np.random.default_rng(seed=42)
    for _ in range(1000):
        x = rng.uniform(xmin, xmax)
        y = np.sin(x) + rng.normal(0, 0.2)
        profile.Fill(x, y)
    return profile


def getTestTProfile2D(
    nBinsX: int = 30,
    xmin:   float = 0.,
    xmax:   float = 10.,
    nBinsY: int = 30,
    ymin:   float = 0.,
    ymax:   float = 10.
):
    pr = ROOT.TProfile2D("pr", "Example TProfile2D", nBinsX, xmin, xmax, nBinsY, ymin, ymax)

    rng = np.random.default_rng(seed=42)
    for _ in range(5000):
        x = rng.uniform(xmin, xmax)
        y = rng.uniform(ymin, ymax)
        z = np.sin(x) * np.cos(y) + rng.normal(0, 0.1)
        pr.Fill(x, y, z)
    return pr


def isTH1(obj, option: str = "") -> bool:
    def isRootTH1(obj) -> bool:
        if isinstance(obj, ROOT.TH1) and not isinstance(obj, (ROOT.TH2, ROOT.TH3, ROOT.TProfile, ROOT.TProfile2D, ROOT.TProfile3D)):
            return True
        return False

    def isUprootTH1(obj) -> bool:
        if hasattr(obj, "classname"):
            if (
                uproot.Model.is_instance(obj, "TH1") and
                not uproot.Model.is_instance(obj, "TH2") and
                not uproot.Model.is_instance(obj, "TH3") and
                not uproot.Model.is_instance(obj, "TProfile") and
                not uproot.Model.is_instance(obj, "TProfile2D") and
                not uproot.Model.is_instance(obj, "TProfile3D")
            ):
                return True
        return False


    if option.lower() == "uproot":
        return isUprootTH1(obj)
    elif option.lower() in ("all", "both"):
        return isRootTH1(obj) or isUprootTH1(obj)
    else:
        return isRootTH1(obj)


def isTProfile(obj, option: str = "") -> bool:
    def isRootTProfile(obj) -> bool:
        if isinstance(obj, ROOT.TProfile) and not isinstance(obj, (ROOT.TProfile2D, ROOT.TProfile3D)):
            return True
        return False

    def isUprootTProfile(obj) -> bool:
        if hasattr(obj, "classname"):
            if (
                uproot.Model.is_instance(obj, "TProfile") and
                not uproot.Model.is_instance(obj, "TProfile2D") and
                not uproot.Model.is_instance(obj, "TProfile3D")
            ):
                return True
        return False


    if option.lower() == "uproot":
        return isUprootTProfile(obj)
    elif option.lower() in ("all", "both"):
        return isRootTProfile(obj) or isUprootTProfile(obj)
    else:
        return isRootTProfile(obj)



def isTH2(obj, option: str = "") -> bool:
    def isRootTH2(obj) -> bool:
        if isinstance(obj, ROOT.TH2) and not isinstance(obj, (ROOT.TH3, ROOT.TProfile2D, ROOT.TProfile3D)):
            return True
        return False

    def isUprootTH2(obj) -> bool:
        if hasattr(obj, "classname"):
            if (
                uproot.Model.is_instance(obj, "TH2") and
                not uproot.Model.is_instance(obj, "TH3") and
                not uproot.Model.is_instance(obj, "TProfile")
            ):
                return True
        return False

    if option.lower() == "uproot":
        return isUprootTH2(obj)
    elif option.lower() in ("all", "both"):
        return isRootTH2(obj) or isUprootTH2(obj)
    else:
        return isRootTH2(obj)


def isTProfile2D(obj, option: str = "") -> bool:
    def isRootTProfile2D(obj) -> bool:
        if isinstance(obj, ROOT.TProfile2D):
            return True
        return False

    def isUprootTProfile2D(obj) -> bool:
        if hasattr(obj, "classname"):
            if uproot.Model.is_instance(obj, "TProfile2D"):
                return True
        return False


    if option.lower() == "uproot":
        return isUprootTProfile2D(obj)
    elif option.lower() in ("all", "both"):
        return isRootTProfile2D(obj) or isUprootTProfile2D(obj)
    else:
        return isRootTProfile2D(obj)


def getNumpyFromTH1(obj,
    xmin: Union[float, int, None] = None,
    xmax: Union[float, int, None] = None
):
    if isTH1(obj) or isTProfile(obj):
        obj = uproot.from_pyroot(obj)

    else:
        if not isTH1(obj, option="uproot") and not isTProfile(obj, option="uproot"):
            raise ValueError("Object is not a ROOT.TH1, uproot.TH1, ROOT.TProfile or uproot.TProfile instance!")

    data, binEdges = obj.to_numpy()
    errors = obj.errors()

    if xmin is not None:
        lowerIndex = np.searchsorted(binEdges, xmin, side="left")

        if binEdges[lowerIndex] < xmin:
            lowerIndex += 1
    else:
        lowerIndex = 0

    if xmax is not None:
        upperIndex = np.searchsorted(binEdges, xmax, side="right")

        if binEdges[upperIndex] > xmax:
            upperIndex -= 1
    else:
        upperIndex = len(binEdges)

    data = data[lowerIndex:upperIndex].astype(np.float64)
    errors = errors[lowerIndex:upperIndex].astype(np.float64)
    binEdges = binEdges[lowerIndex:upperIndex + 1].astype(np.float64)

    return data, errors, binEdges

def getNumpyFromTH2(obj,
    xmin: Union[float, int, None] = None,
    xmax: Union[float, int, None] = None,
    ymin: Union[float, int, None] = None,
    ymax: Union[float, int, None] = None
) -> tuple:
    if isTH2(obj) or isTProfile2D(obj):
        obj = uproot.from_pyroot(obj)
    else:
        if not isTH2(obj, option="uproot") and not isTProfile2D(obj, option="uproot"):
            raise ValueError("Provided object is not a ROOT.TH2, uproot.TH2, ROOT.TProfile2D or an uproot.TProfile2D instance!")


    data = obj.values()
    errors = obj.errors()
    xBinEdges = obj.member("fXaxis").edges()
    yBinEdges = obj.member("fYaxis").edges()

    if xmin is not None:
        xLowerIndex = np.searchsorted(xBinEdges, xmin, side="left")

        if xBinEdges[xLowerIndex] < xmin:
            xLowerIndex += 1
    else:
        xLowerIndex = 0

    if xmax is not None:
        xUpperIndex = np.searchsorted(xBinEdges, xmax, side="right")

        if xBinEdges[xUpperIndex] > xmax:
            xUpperIndex -= 1
    else:
        xUpperIndex = len(xBinEdges)


    if ymin is not None:
        yLowerIndex = np.searchsorted(yBinEdges, ymin, side="left")

        if yBinEdges[yLowerIndex] < ymin:
            yLowerIndex += 1
    else:
        yLowerIndex = 0

    if ymax is not None:
        yUpperIndex = np.searchsorted(yBinEdges, ymax, side="right")

        if yBinEdges[yUpperIndex] > ymax:
            yUpperIndex -= 1
    else:
        yUpperIndex = len(yBinEdges)


    data = data[xLowerIndex:xUpperIndex, yLowerIndex:yUpperIndex].astype(np.float64)
    errors = errors[xLowerIndex:xUpperIndex, yLowerIndex:yUpperIndex].astype(np.float64)
    xBinEdges = xBinEdges[xLowerIndex:xUpperIndex + 1].astype(np.float64)
    yBinEdges = yBinEdges[yLowerIndex:yUpperIndex + 1].astype(np.float64)

    return data.T, errors.T, xBinEdges, yBinEdges




def getPandasFromTH1(obj):
    if not isTH1(obj, option="all") and not isTProfile(obj, option="all"):
        raise ValueError(f"Provided object is not a ROOT.TH1, uproot.TH1, ROOT.TProfile or uproot.TProfile instance!")

    if isTH1(obj) or isTProfile(obj):
        obj = uproot.from_pyroot(obj)

    y  = obj.values()
    ey = obj.errors()
    x  = obj.all_members['fXaxis'].centers()
    ex = obj.all_members['fXaxis'].widths()

    return pd.DataFrame({
        'x':  x,
        'y':  y,
        'ex': ex,
        'ey': ey
    })

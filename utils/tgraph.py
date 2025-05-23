from typing import Union
import ROOT
import numpy as np
import pandas as pd
import uproot


mplm = {
   "o":  20,   # ROOT: Full circle → Matplotlib: Circle
   "s":  21,   # ROOT: Full square → Matplotlib: Square
   "D":  22,   # ROOT: Full diamond → Matplotlib: Diamond
   "^":  23,   # ROOT: Full triangle up → Matplotlib: Triangle up
   "v":  24,   # ROOT: Full triangle down → Matplotlib: Triangle down
   "<":  25,   # ROOT: Full triangle left → Matplotlib: Triangle left
   ">":  26,   # ROOT: Full triangle right → Matplotlib: Triangle right
   "p":  27   # ROOT: Star → Matplotlib: Pentagon
}

def getTestTGraph(nPoints: int = 10):
    x = np.linspace(1, 10, nPoints)
    y = np.sin(x)

    ex = np.full(nPoints, 0.15)
    ey = np.random.uniform(0.05, 0.1, nPoints)

    x  = np.array(x,  dtype=np.float64)
    y  = np.array(y,  dtype=np.float64)

    gr = ROOT.TGraph(nPoints, x, y)
    return gr



def getTestTGraphErrors(nPoints: int = 10):
    x = np.linspace(1, 10, nPoints)
    y = np.sin(x)

    ex = np.full(nPoints, 0.15)
    ey = np.random.uniform(0.05, 0.1, nPoints)

    x  = np.array(x,  dtype=np.float64)
    y  = np.array(y,  dtype=np.float64)
    ex = np.array(ex, dtype=np.float64)
    ey = np.array(ey, dtype=np.float64)

    gr = ROOT.TGraphErrors(nPoints, x, y, ex, ey)
    return gr



def getTestTGraphAsymmErrors(nPoints: int = 10):
    x = np.linspace(1, 10, nPoints)
    y = np.sin(x)

    exl = np.random.uniform(0.1, 0.2, nPoints)
    exh = np.random.uniform(0.1, 0.2, nPoints)
    eyl = np.random.uniform(0.05, 0.1, nPoints)
    eyh = np.random.uniform(0.05, 0.1, nPoints)

    gr = ROOT.TGraphAsymmErrors(
        nPoints, x, y, exl, exh, eyl, eyh
    )
    return gr


def getTestTGraph2D(nPoints: int = 10):
    X, Y = np.meshgrid(
        np.linspace(-5, 5, int(np.sqrt(nPoints))),
        np.linspace(-5, 5, int(np.sqrt(nPoints)))
    )
    Z = np.sin(np.sqrt(X**2 + Y**2))

    x = X.flatten()
    y = Y.flatten()
    z = Z.flatten()

    x = np.array(x, dtype=np.float64)
    y = np.array(y, dtype=np.float64)
    z = np.array(z, dtype=np.float64)

    gr = ROOT.TGraph2D(nPoints, x, y, z)
    return gr



def isTGraph(obj, option: str = "") -> bool:
    def isRootTGraph(obj) -> bool:
        if (
            isinstance(obj, ROOT.TGraph) and
            not isinstance(
                obj, (
                    ROOT.TGraphErrors,
                    ROOT.TGraphAsymmErrors,
                    ROOT.TGraph2D,
                    ROOT.TGraph2DErrors,
                    ROOT.TGraph2DAsymmErrors
                )
            )
        ):
            return True
        return False

    def isUprootTGraph(obj) -> bool:
        if hasattr(obj, "classname"):
            if (
                uproot.Model.is_instance(obj, "TGraph") and
                not uproot.Model.is_instance(obj, "TGraphErrors") and
                not uproot.Model.is_instance(obj, "TGraphAsymmErrors") and
                not uproot.Model.is_instance(obj, "TGraph2D") and
                not uproot.Model.is_instance(obj, "TGraph2DErrors") and
                not uproot.Model.is_instance(obj, "TGraph2DAsymmErrors")
            ):
                return True
        return False


    if option.lower() == "uproot":
        return isUprootTGraph(obj)
    elif option.lower() in ("all", "both"):
        return isRootTGraph(obj) or isUprootTGraph(obj)
    else:
        return isRootTGraph(obj)



def isTGraphErrors(obj, option: str = "") -> bool:
    def isRootTGraphErrors(obj) -> bool:
        if isinstance(obj, ROOT.TGraphErrors):
            return True
        return False

    def isUprootTGraphErrors(obj) -> bool:
        if hasattr(obj, "classname"):
            if uproot.Model.is_instance(obj, "TGraphErrors"):
                return True
        return False


    if option.lower() == "uproot":
        return isUprootTGraphErrors(obj)
    elif option.lower() in ("all", "both"):
        return isRootTGraphErrors(obj) or isUprootTGraphErrors(obj)
    else:
        return isRootTGraphErrors(obj)



def isTGraphAsymmErrors(obj, option: str = "") -> bool:
    def isRootTGraphAsymmErrors(obj) -> bool:
        if isinstance(obj, ROOT.TGraphAsymmErrors):
            return True
        return False

    def isUprootTGraphAsymmErrors(obj) -> bool:
        if hasattr(obj, "classname"):
            if uproot.Model.is_instance(obj, "TGraphAsymmErrors"):
                return True
        return False


    if option.lower() == "uproot":
        return isUprootTGraphAsymmErrors(obj)
    elif option.lower() in ("all", "both"):
        return isRootTGraphAsymmErrors(obj) or isUprootTGraphAsymmErrors(obj)
    else:
        return isRootTGraphAsymmErrors(obj)


def isTGraph2D(obj, option: str = "") -> bool:
    def isRootTGraph2D(obj) -> bool:
        if (
            isinstance(obj, ROOT.TGraph2D) and
            not isinstance(
                obj, (
                    ROOT.TGraph2DErrors,
                    ROOT.TGraph2DAsymmErrors
                )
            )
        ):
            return True
        return False

    def isUprootTGraph2D(obj) -> bool:
        if hasattr(obj, "classname"):
            if (
                uproot.Model.is_instance(obj, "TGraph2D") and
                not uproot.Model.is_instance(obj, "TGraph2DErrors") and
                not uproot.Model.is_instance(obj, "TGraph2DAsymmErrors")
            ):
                return True
        return False


    if option.lower() == "uproot":
        return isUprootTGraph2D(obj)
    elif option.lower() in ("all", "both"):
        return isRootTGraph2D(obj) or isUprootTGraph2D(obj)
    else:
        return isRootTGraph2D(obj)









def getPandasFromTGraph(tgraph):
    if not isTGraph(tgraph, option="all"):
        raise ValueError(f"Provided object is not a ROOT.TGraph or an uproot.TGraph instance!")

    if isTGraph(tgraph):
        tgraph = uproot.from_pyroot(tgraph)

    return pd.DataFrame({
        'x':  np.array(tgraph.member("fX"),   dtype=np.float64),
        'y':  np.array(tgraph.member("fY"),   dtype=np.float64)
    })



def getPandasFromTGraphErrors(tgraph):
    if not isTGraphErrors(tgraph, option="all"):
        raise ValueError(f"Provided object is not a ROOT.TGraphErrors or an uproot.TGraphErrors instance!")

    if isTGraphErrors(tgraph):
        tgraph = uproot.from_pyroot(tgraph)

    return pd.DataFrame({
        'x':  np.array(tgraph.member("fX"),   dtype=np.float64),
        'y':  np.array(tgraph.member("fY"),   dtype=np.float64),
        'ex': np.array(tgraph.member("fEX"),  dtype=np.float64),
        'ey': np.array(tgraph.member("fEY"),  dtype=np.float64)
    })


def getPandasFromTGraphAsymmErrors(tgraph):
    if not isTGraphAsymmErrors(tgraph, option="all"):
        raise ValueError(f"Provided object is not a ROOT.TGraphAsymmErrors or an uproot.TGraphAsymmErrors instance!")

    if isTGraphAsymmErrors(tgraph):
        tgraph = uproot.from_pyroot(tgraph)

    return pd.DataFrame({
        'x':   np.array(tgraph.member("fX"),      dtype=np.float64),
        'y':   np.array(tgraph.member("fY"),      dtype=np.float64),
        'exl': np.array(tgraph.member("fEXlow"),  dtype=np.float64),
        'exh': np.array(tgraph.member("fEXhigh"), dtype=np.float64),
        'eyl': np.array(tgraph.member("fEYlow"),  dtype=np.float64),
        'eyh': np.array(tgraph.member("fEYhigh"), dtype=np.float64)
    })



def getPandasFromTGraph2D(tgraph: ROOT.TGraph2D):
    if not isTGraph2D(tgraph, option="all"):
        raise ValueError(f"Provided object is not a ROOT.TGraph2D or an uproot.TGraph2D instance!")

    if isTGraph2D(tgraph):
        tgraph = uproot.from_pyroot(tgraph)

    return pd.DataFrame({
        'x':  np.array(tgraph.member("fX"),   dtype=np.float64),
        'y':  np.array(tgraph.member("fY"),   dtype=np.float64),
        'z':  np.array(tgraph.member("fZ"),   dtype=np.float64)
    })



def getTGraphErrors(
    x, y, ex, ey,
    title: str = "",
    xTitle: str = "",
    yTitle: str = ""
) -> ROOT.TGraphErrors:
    N  = len(x)

    x  = np.array(x,  dtype=np.float64)
    y  = np.array(y,  dtype=np.float64)
    ex = np.array(ex, dtype=np.float64)
    ey = np.array(ey, dtype=np.float64)

    graph = ROOT.TGraphErrors(N, x, y, ex, ey)
    graph.SetTitle(title)
    graph.GetXaxis().SetTitle(xTitle)
    graph.GetYaxis().SetTitle(yTitle)

    return graph

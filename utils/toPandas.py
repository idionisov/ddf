from typing import Union
import ROOT
import numpy as np
import uproot
from utils.tgraph import isTGraph, isTGraphErrors, isTGraphAsymmErrors, isTGraph2D, \
    getPandasFromTGraph, getPandasFromTGraphErrors, getPandasFromTGraphAsymmErrors, \
    getPandasFromTGraph2D
from utils.th1 import isTH1, isTProfile, isTH2, isTProfile2D, getPandasFromTH1
from utils.teff import getPandasFromTEff1D



def getAsPandas(obj,
    statOption: str = "Clopper Pearson",
    cl: float = 0.6826894921370859
):
    if not (isinstance(obj, ROOT.TObject) or uproot.Model.is_instance(obj, "TObject")):
        raise ValueError("Input is neither a ROOT.TObject nor an uproot.TObject instance!")

    if isinstance(obj, ROOT.TEfficiency):
        if obj.GetDimension() == 1:
            return getPandasFromTEff1D(obj)
        else:
            raise ValueError("The ROOT.TEfficiency instance has to be one dimensional!")


    if hasattr(obj, "classname"):
        if uproot.Model.is_instance(obj, "TEfficiency"):
            if np.ndim(obj.member("fPassedHistogram").values()) == 1:
                return getPandasFromTEff1D(obj, statOption = statOption, cl = cl)


    if isTH1(obj, option="all") or isTProfile(obj, option="all"):
        return getPandasFromTH1(obj)

    elif isTGraph2D(obj, option="all"):
        return getPandasFromTGraph2D(obj)

    elif isTGraphAsymmErrors(obj, option="all"):
        return getPandasFromTGraphAsymmErrors(obj)

    elif isTGraphErrors(obj, option="all"):
        return getPandasFromTGraphErrors(obj)

    elif isTGraph(obj, option="all"):
        return getPandasFromTGraph(obj)

    else:
        raise ValueError(f"Type {type(obj)} is not supported for this function!")

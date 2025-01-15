import ROOT
import re
import numpy as np
from typing import Union
from .th1 import isTH1, isTH2


def getTEff(
    passed: ROOT.TH1,
    total: ROOT.TH1,
    statOption: str = "normal",
    cl: float = 0.682689,
    name: str = "",
    title: str = ""
) -> ROOT.TEfficiency:
    if type(passed) != type(total):
        raise ValueError("Passed and Total Histograms are not of the same type!")

    teff = ROOT.TEfficiency(passed, total)
    teff.SetConfidenceLevel(cl)
    SetStatOption(teff, statOption)
    if name: teff.SetName(name)
    if title: teff.SetTitle(title)

    return teff




def setStatOption(
    teff:       ROOT.TEfficiency,
    statOption: str = "normal"
):
    statOption = statOption.lower()

    normal_options           = {"normal", "kfnormal"}
    clopper_pearson_options  = {"clopper_pearson", "kfcp", "clopper pearson",
                                "clopper-pearson", "clopper.pearson",
                                "clopper:pearson", "clopperpearson"}
    bayesian_options         = {"bayesian", "kbbayesian"}
    wilson_options           = {"wilson", "kfwilson"}
    feldman_cousings_options = {"feldman_cousins", "kffc",
                                "feldman cousins", "feldman-cousings",
                                "feldman:cousins", "feldman.cousins",
                                "feldmancousins"}
    agresti_coull_options    = {"agresti_coull", "kfac",
                                "agresti coull", "agresti-coull",
                                "agresti:coull", "agresti.coull",
                                "agresticoull"}
    mid_p_interval_options   = {"mid_p_interval", "kmidp",
                                "mid p interval", "mid-p-interval",
                                "mid:p:interval", "mid.p.interval",
                                "midpinterval"}
    jeffrey_options          = {"jeffrey", "kbjeffrey"}
    uniform_prior_options    = {"uniform_prior", "kbuniform",
                                "uniform prior", "uniform-prior",
                                "uniform:prior", "uniform.prior",
                                "uniformprior"}

    if statOption in normal_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kFNormal)
    elif statOption in clopper_pearson_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kFCP)
    elif statOption in bayesian_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kBBayesian)
    elif statOption in wilson_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kFWilson)
    elif feldman_cousings_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kFFC)
    elif statOption in agresti_coull_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kFAC)
    elif statOption in mid_p_interval_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kMidP)
    elif statOption in jeffrey_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kBJeffrey)
    elif statOption in uniform_prior_options:
        teff.SetStatisticOption(ROOT.TEfficiency.kBUniform)

    else: raise ValueError(f"Invalid statistic option '{statOption}'!")



def getStatOption(teff: ROOT.TEfficiency) -> str:
    statOption = teff.GetStatisticOption()

    if   statOption==0:  return "Clopper Pearson"
    elif statOption==1:  return "Normal"
    elif statOption==2:  return "Wilson"
    elif statOption==3:  return "Agresti Coull"
    elif statOption==4:  return "Feldman Cousins"
    elif statOption==5:  return "Jeffrey"
    elif statOption==6:  return "Normal"
    elif statOption==7:  return "Uniform Prior"
    elif statOption==8:  return "Bayesian"
    elif statOption==9:  return "Mid P Interval"
    else:                return None


def getGraphFromTEff1D(teff: ROOT.TEfficiency, name: str = '', title: str = '', suffix: str = '') -> ROOT.TGraphAsymmErrors:
    if teff.GetDimension() != 1:
        raise ValueError("TEfficiency object is not one-dimensional!")

    if not name:  name  = teff.GetName()
    if not title: title = teff.GetTitle()
    if suffix:    name = f"{name}_{suffix}"

    Total = teff.GetTotalHistogram()
    nBins = Total.GetNbinsX()

    x   = np.array([Total.GetXaxis().GetBinCenter(bin) for bin in range(1, nBins + 1)], dtype=np.float64)
    y   = np.array([teff.GetEfficiency(bin) for bin in range(1, nBins + 1)], dtype=np.float64)
    ex  = np.array([Total.GetXaxis().GetBinWidth(bin) / 2 for bin in range(1, nBins + 1)], dtype=np.float64)
    eyl = np.array([teff.GetEfficiencyErrorLow(bin) for bin in range(1, nBins + 1)], dtype=np.float64)
    eyh = np.array([teff.GetEfficiencyErrorUp(bin) for bin in range(1, nBins + 1)], dtype=np.float64)

    graph = ROOT.TGraphAsymmErrors(nBins, x, y, ex, ex, eyl, eyh)
    if name.startswith("gr_"): graph.SetName(name)
    else:                      graph.SetName(f"gr_{name}")
    graph.SetTitle(title)

    return graph



def getGraphFromTEff2D(
    teff: ROOT.TEfficiency,
    name: str = "",
    title: str = "",
    suffix: str = ""
) -> ROOT.TGraph2D:
    if teff.GetDimension() != 2:
        raise ValueError("TEfficiency object is not two-dimensional!")

    if not name:  name  = teff.GetName()
    if not title: title = teff.GetTitle()
    if suffix:    name = f"{name}_{suffix}"

    Total = teff.GetTotalHistogram()
    nBinsX = Total.GetNbinsX()
    nBinsY = Total.GetNbinsY()

    x = []
    y = []
    z = []

    for ix in range(1, nBinsX + 1):
        for iy in range(1, nBinsY + 1):
            x.append( Total.GetXaxis().GetBinCenter(ix) )
            y.append( Total.GetYaxis().GetBinCenter(iy) )
            z.append( teff.GetEfficiency(Total.GetBin(ix, iy)) )

    graph = ROOT.TGraph2D(len(x),
        np.array(x, dtype=np.float64),
        np.array(y, dtype=np.float64),
        np.array(z, dtype=np.float64)
    )


    if name.startswith("gr_"): graph.SetName(name)
    else:                      graph.SetName(f"gr_{name}")
    graph.SetTitle(title)

    return graph



def getHistFromTEff2D(teff, name="", title="", suffix="") -> ROOT.TH2D:
    if teff.GetDimension() != 2:
        raise ValueError("TEfficiency object is not two-dimensional!")

    if not name:  name  = teff.GetName()
    if not title: title = teff.GetTitle()
    if suffix:    name = f"{name}_{suffix}"

    hist = teff.CreateHistogram()
    hist.SetName(name)
    hist.SetTitle(title)

    return hist

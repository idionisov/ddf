import ROOT
import re
import numpy as np
import uproot
import pandas as pd
from typing import Union
from utils.th1 import isTH1, isTH2
from utils.tgraph import getPandasFromTGraphAsymmErrors
from ddfUtils import getEffWithError


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
    setStatOption(teff, statOption)
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



def getStatOption(teff: ROOT.TEfficiency) -> Union[str, None]:
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

    if not name:
        name  = teff.GetName()
    if not title:
        title = teff.GetTitle()
    if suffix:
        name = f"{name}_{suffix}"

    Total = teff.GetTotalHistogram()
    nBins = Total.GetNbinsX()

    x   = np.array([Total.GetXaxis().GetBinCenter(bin) for bin in range(1, nBins + 1)], dtype=np.float64)
    y   = np.array([teff.GetEfficiency(bin) for bin in range(1, nBins + 1)], dtype=np.float64)
    ex  = np.array([Total.GetXaxis().GetBinWidth(bin) / 2 for bin in range(1, nBins + 1)], dtype=np.float64)
    eyl = np.array([teff.GetEfficiencyErrorLow(bin) for bin in range(1, nBins + 1)], dtype=np.float64)
    eyh = np.array([teff.GetEfficiencyErrorUp(bin) for bin in range(1, nBins + 1)], dtype=np.float64)

    graph = ROOT.TGraphAsymmErrors(nBins, x, y, ex, ex, eyl, eyh)
    if name.startswith("gr_"):
        graph.SetName(name)
    else:
        graph.SetName(f"gr_{name}")
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

    if not name:
        name  = teff.GetName()
    if not title:
        title = teff.GetTitle()
    if suffix:
        name = f"{name}_{suffix}"

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


    if name.startswith("gr_"):
        graph.SetName(name)
    else:
        graph.SetName(f"gr_{name}")
    graph.SetTitle(title)

    return graph


def getGraphFromTEff(
    teff: ROOT.TEfficiency,
    name: str = "",
    title: str = "",
    suffix: str = ""
):
    if teff.GetDimension() == 1:
        return getGraphFromTEff1D(teff, name, title, suffix)
    elif teff.GetDimension() == 2:
        return getGraphFromTEff2D(teff, name, title, suffix)
    else:
        raise ValueError("TEfficiency object cannot be of dimension higher 2!")


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



def getNumpyFromTEff1D(
    efficiency: ROOT.TEfficiency,
    xmin: Union[float, None] = None,
    xmax: Union[float, None] = None
):
    if efficiency.GetDimension() != 1:
        raise ValueError("TEfficiency is not 1 dimensional!")

    if xmin:
        xFirstBin = efficiency.GetPassedHistogram().FindBin(xmin)
    else:
        xFirstBin = 1

    if xmax:
        xLastBin = efficiency.GetPassedHistogram().FindBin(xmax)
    else:
        xLastBin = efficiency.GetPassedHistogram().GetNbinsX() + 1

    nBins      = xLastBin - xFirstBin
    effs       = np.zeros(nBins)
    errorsUp   = np.zeros(nBins)
    errorsDown = np.zeros(nBins)
    binEdges   = np.zeros(nBins + 1)

    for ix, xbin in enumerate(range(xFirstBin, xLastBin)):
        gbin = efficiency.GetGlobalBin(xbin)

        effs[ix]       = efficiency.GetEfficiency(gbin)
        errorsUp[ix]   = efficiency.GetEfficiencyErrorUp(gbin)
        errorsDown[ix] = efficiency.GetEfficiencyErrorLow(gbin)
        binEdges[ix]   = efficiency.GetPassedHistogram().GetBinLowEdge(xbin)
    binEdges[-1] = efficiency.GetPassedHistogram().GetBinLowEdge(xLastBin)

    return effs, errorsUp, errorsDown, binEdges




def getNumpyFromTEff2D(
    efficiency: ROOT.TEfficiency,
    xmin: Union[float, None] = None,
    xmax: Union[float, None] = None,
    ymin: Union[float, None] = None,
    ymax: Union[float, None] = None
):
    if efficiency.GetDimension() != 2:
        raise ValueError("TEfficiency is not 2 dimensional!")

    if xmin:
        xFirstBin = efficiency.GetPassedHistogram().GetXaxis().FindBin(xmin)
    else:
        xFirstBin = 1

    if xmax:
        xLastBin = efficiency.GetPassedHistogram().GetXaxis().FindBin(xmax)
    else:
        xLastBin = efficiency.GetPassedHistogram().GetXaxis().GetNbins() + 1


    if ymin:
        yFirstBin = efficiency.GetPassedHistogram().GetYaxis().FindBin(ymin)
    else:
        yFirstBin = 1

    if ymax:
        yLastBin = efficiency.GetPassedHistogram().GetYaxis().FindBin(ymax)
    else:
        yLastBin = efficiency.GetPassedHistogram().GetYaxis().GetNbins() + 1


    nBinsX = xLastBin - xFirstBin
    nBinsY = yLastBin - yFirstBin
    effs = np.zeros((nBinsX, nBinsY))
    errorsUp = np.zeros((nBinsX, nBinsY))
    errorsDown = np.zeros((nBinsX, nBinsY))
    xBinEdges = np.zeros(nBinsX + 1)
    yBinEdges = np.zeros(nBinsY + 1)


    for ix in range(nBinsX):
        xBinEdges[ix] = efficiency.GetPassedHistogram().GetXaxis().GetBinLowEdge(xFirstBin + ix)
    xBinEdges[-1] = efficiency.GetPassedHistogram().GetXaxis().GetBinUpEdge(xLastBin - 1)


    for iy in range(nBinsY):
        yBinEdges[iy] = efficiency.GetPassedHistogram().GetYaxis().GetBinLowEdge(yFirstBin + iy)
    yBinEdges[-1] = efficiency.GetPassedHistogram().GetYaxis().GetBinUpEdge(yLastBin - 1)


    for ix in range(nBinsX):
        for iy in range(nBinsY):
            gbin = efficiency.GetGlobalBin(xFirstBin + ix, yFirstBin + iy)
            effs[ix, nBinsY-iy-1] = efficiency.GetEfficiency(gbin)
            errorsUp[ix, nBinsY-iy-1] = efficiency.GetEfficiencyErrorUp(gbin)
            errorsDown[ix, nBinsY-iy-1] = efficiency.GetEfficiencyErrorLow(gbin)

    return effs.T, errorsUp.T, errorsDown.T, xBinEdges, yBinEdges


def getPandasFromTEff1D(teff,
    statOption: str = "Clopper Pearson",
    cl: float = 0.6826894921370859
):
    if not isinstance(teff, ROOT.TEfficiency) and not uproot.Model.is_instance(teff, "TEfficiency"):
        raise ValueError("Provided object is not a ROOT.TEfficiency or an uproot.TEfficiency instance!")

    if isinstance(teff, ROOT.TEfficiency):
        if teff.GetDimension() != 1:
            raise ValueError("Efficiency is not one-dimensional!")

        name = teff.GetName()
        title = teff.GetTitle()
        xAxisTitle = teff.GetPassedHistogram().GetXaxis().GetTitle()
        yAxisTitle = teff.GetPassedHistogram().GetXaxis().GetTitle()

        teff = getGraphFromTEff1D(teff,
            name = name,
            title = f"{title};{xAxisTitle};{yAxisTitle}"
        )
        return getPandasFromTGraphAsymmErrors(teff)

    else:
        print("Converting an uproot TEfficiency to a pandas dataframe!")
        print(">> Discrepancies between original an selected statistic options or confidence levels might lead to unexpected results!")
        print(f">> Statistic option: \033[1;32m{statOption}\033[0m")
        print(f">> Confidence level: \033[1;32m{cl:.03f}\033[0m")

        passed = teff.member("fPassedHistogram").values()
        total  = teff.member("fTotalHistogram").values()
        x  = teff.member("fPassedHistogram").member("fXaxis").centers()
        ex = teff.member("fPassedHistogram").member("fXaxis").widths() / 2

        y   = np.zeros(len(passed), dtype=np.float64)
        eyh = np.zeros(len(passed), dtype=np.float64)
        eyl = np.zeros(len(passed), dtype=np.float64)
        for i in range(len(passed)):
            y[i], eyh[i], eyl[i] = getEffWithError(passed[i], total[i], statOption=statOption, cl=cl)

        return pd.DataFrame({
            'x': x, 'y': y, 'exl': ex, 'exh': ex, 'eyl': eyl, 'eyh': eyh
        })

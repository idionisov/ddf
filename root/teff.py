from typing import Union
import numpy as np
from ROOT import TEfficiency, TGraphAsymmErrors, TH1, TH2, TH1F, TObject


def set_stat_option(
    teff:        TEfficiency,
    stat_option: str = "normal"
):
    so = stat_option.lower()

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

    if so in normal_options:
        teff.SetStatisticOption(TEfficiency.kFNormal)
    elif so in clopper_pearson_options:
        teff.SetStatisticOption(TEfficiency.kFCP)
    elif so in bayesian_options:
        teff.SetStatisticOption(TEfficiency.kBBayesian)
    elif so in wilson_options:
        teff.SetStatisticOption(TEfficiency.kFWilson)
    elif feldman_cousings_options:
        teff.SetStatisticOption(TEfficiency.kFFC)
    elif so in agresti_coull_options:
        teff.SetStatisticOption(TEfficiency.kFAC)
    elif so in mid_p_interval_options:
        teff.SetStatisticOption(TEfficiency.kMidP)
    elif so in jeffrey_options:
        teff.SetStatisticOption(TEfficiency.kBJeffrey)
    elif so in uniform_prior_options:
        teff.SetStatisticOption(TEfficiency.kBUniform)

    else: raise ValueError(f"Invalid statistic option '{stat_option}'!")


def get_graph_from_teff_1D(teff: TEfficiency, teff_name: str='', teff_title: str='') -> TGraphAsymmErrors:
    '''
    Takes a 1D TEfficiency object and returns a TGraphAsymmErrors object,
    whose points are the efficiency with asymmetric errors.
    '''
    
    if not teff_name:
        teff_name = teff.GetName()
    
    if not teff_title:
        teff_title = teff.GetTitle()

    n_bins = teff.GetTotalHistogram().GetNbinsX()
    x   = np.zeros(n_bins, dtype=np.float64)
    y   = np.zeros(n_bins, dtype=np.float64)
    exl = np.zeros(n_bins, dtype=np.float64)
    exh = np.zeros(n_bins, dtype=np.float64)
    eyl = np.zeros(n_bins, dtype=np.float64)
    eyh = np.zeros(n_bins, dtype=np.float64)

    for xbin in range(1, n_bins + 1):
        x_center   = teff.GetTotalHistogram().GetXaxis().GetBinCenter(xbin)
        efficiency = teff.GetEfficiency(xbin)
        errorLow   = teff.GetEfficiencyErrorLow(xbin)
        errorUp    = teff.GetEfficiencyErrorUp(xbin)
        bin_width  = teff.GetTotalHistogram().GetXaxis().GetBinWidth(xbin)

        x[xbin-1]   = x_center
        y[xbin-1]   = efficiency
        exl[xbin-1] = bin_width / 2
        exh[xbin-1] = bin_width / 2
        eyl[xbin-1] = errorLow
        eyh[xbin-1] = errorUp

    graph = TGraphAsymmErrors(n_bins, x, y, exl, exh, eyl, eyh)
    graph.SetName(f"gr_{teff_name}")
    graph.SetTitle(teff_title)

    return graph


def get_teff(h_passed, h_total,
    stat_option:      str   = 'normal',
    confidence_level: float = 0.682689,
    name:             str   = '',
    title:            str   = '',
    as_hist_2d:       bool  = True
) -> TObject:
    '''
    Takes the histograms of passed and total entries and returns the TEfficiency.
    Statistic options are:
    - normal
    - clopper_pearson
    - bayesian
    - wilson
    - feldman_cousins
    - agresti_coull
    - mid_p_interval
    - jeffrey
    - uniform_prior
    - custom_prior
    '''

    teff = TEfficiency(h_passed, h_total)
    teff.SetConfidenceLevel(confidence_level)

    set_stat_option(teff, stat_option)

    if isinstance(h_passed, TH2) and isinstance(h_total, TH2) and as_hist_2d:
        teff = teff.CreateHistogram()
    elif isinstance(h_passed, TH1) and isinstance(h_total, TH1):
        teff = get_graph_from_teff_1D(teff)
        teff.SetMarkerStyle(1)
        teff.SetMinimum(0)
        teff.SetMaximum(1.05)
    else:
        raise ValueError("Inconsistent histograms!")
    
    if name  and teff: teff.SetName(name)
    if title and teff: teff.SetTitle(title)
    return teff

def get_teff_dict(
    h_dict:           dict,
    stat_option:      str = 'normal',
    confidence_level: float = 0.682689,
    suffix:           str = "",
    dict_of_teff:     dict = {},
) -> dict:
    
    for key in h_dict:
        if isinstance(h_dict[key], tuple):
            if isinstance(h_dict[key][0], TH2) and isinstance(h_dict[key][1], TH2):
                name = h_dict[key][0].GetName()

                x_axis_title = h_dict[key][0].GetXaxis().GetTitle()
                y_axis_title = h_dict[key][0].GetYaxis().GetTitle()

                if name.lower().startswith("h1_") or name.lower().startswith("h2_"):
                    name = name[3:]
                name = f"eff_{name}"

                if suffix:
                    name = f"{name}.{suffix}"

                dict_of_teff[key] = get_teff(
                    h_dict[key][0], h_dict[key][1],
                    stat_option=stat_option, confidence_level=confidence_level, name=name, title=f";{x_axis_title};{y_axis_title};Efficiency"
                )
            elif isinstance(h_dict[key][0], TH1) and isinstance(h_dict[key][1], TH1):
                name = h_dict[key][0].GetName()

                x_axis_title = h_dict[key][0].GetXaxis().GetTitle()

                if name.lower().startswith("h1_") or name.lower().startswith("h2_"):
                    name = name[3:]            
                name = f"eff_{name}"

                if suffix:
                    name = f"{name}.{suffix}"

                dict_of_teff[key] = get_teff(
                    h_dict[key][0], h_dict[key][1],
                    stat_option=stat_option, confidence_level=confidence_level, name=name, title=f";{x_axis_title};Efficiency"
                )
            else: raise ValueError("Tuple does not contain histograms!")
        elif isinstance(h_dict[key], dict):
            dict_of_teff[key] = {}

            dict_of_teff[key] = get_teff_dict(h_dict[key],
                stat_option=stat_option, confidence_level=confidence_level, suffix=suffix, dict_of_teff=dict_of_teff[key]
            )
        elif isinstance(h_dict[key], TH1) or isinstance(h_dict[key], TH2): pass
        else: raise ValueError("Dictionary values have to be histograms or dictionaries!")

    return dict_of_teff





def calculate_eff(
    n_passed:         Union[int, float],
    n_total:          Union[int, float],
    stat_option:      str   = "normal",
    confidence_level: float = 0.6826894921370859
):
    '''
    Takes the number of passed and number of total entries and returns the efficiency with its errors up and down.
    Statistic options are:
    - normal
    - clopper_pearson
    - bayesian
    - wilson
    - feldman_cousins
    - agresti_coull
    - mid_p_interval
    - jeffrey
    - uniform_prior
    - custom_prior
    '''

    # Create two histograms with a single bin
    h_total  = TH1F("h_total",  "Total",  1, -1, 1)
    h_passed = TH1F("h_passed", "Passed", 1, -1, 1)
    
    # Fill the histograms with weights that equal the number of entries
    h_total.Fill(0, n_total)
    h_passed.Fill(0, n_passed)
    
    # Get create TEfficiency and set confidence level
    teff = TEfficiency(h_passed, h_total)
    teff.SetConfidenceLevel(confidence_level)

    # Calculate efficiency based on the statistics option selected
    set_stat_option(teff, stat_option)
    
    # Calculate efficiency and its errors
    eff = teff.GetEfficiency(1)
    deff_low, deff_up = teff.GetEfficiencyErrorLow(1), teff.GetEfficiencyErrorUp(1)
    
    return eff, deff_up, deff_low

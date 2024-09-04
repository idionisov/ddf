import numpy as np
import uproot
from typing import Union
from ROOT import TH1, TH2, TProfile, TProfile2D, TEfficiency
from root.h import get_bin_range





def get_th1_as_numpy(hist: TH1,
    x_range: Union[tuple, None] = None
):
    """
    Takes a ROOT TH1 histogram and an x-axis range.
    Returns a numpy array of the bin contents within selected range and an array of the bin edges.
    
    Parameters:
    - hist (TH1): The original histogram.
    - x_range (x_min, x_max) [Optional]: X-axis range.
    
    Returns:
    - numpy.array: An array of the bin contents.
    - numpy.array: An array of the bin edges.
    """
    
    x_first_bin, x_last_bin = get_bin_range(hist, range=x_range, axis="x")
    n_bins    = x_last_bin - x_first_bin
    data      = np.zeros(n_bins)
    bin_edges = np.zeros(n_bins + 1)

    ix = 0
    for xbin in range(x_first_bin, x_last_bin):
        data[ix]      = hist.GetBinContent(xbin)
        bin_edges[ix] = hist.GetBinLowEdge(xbin)
    bin_edges[-1] = hist.GetBinUpEdge(xbin)

    return data, bin_edges



def get_th2_as_numpy(hist: TH2,
    x_range: Union[tuple, None] = None,
    y_range: Union[tuple, None] = None
):
    """
    Takes a ROOT TH2 histogram and ranges for both axes.
    Returns a numpy array of the bin contents within selected ranges and arrays of bin edges.
    
    Parameters:
    - hist (TH1): The original histogram.
    - x_range (x_min, x_max) [Optional]: X-axis range.
    - y_range (y_min, y_max) [Optional]: Y-axis range.
    
    Returns:
    - numpy.array: A 2D array of the bin contents.
    - numpy.array: A 1D array of the x-axis bin edges.
    - numpy.array: A 1D array of the y-axis bin edges.
    """

    x_first_bin, x_last_bin = get_bin_range(hist, range=x_range, axis="x")
    y_first_bin, y_last_bin = get_bin_range(hist, range=y_range, axis="y")

    n_bins_x    = x_last_bin - x_first_bin
    n_bins_y    = y_last_bin - y_first_bin
    data        = np.zeros((n_bins_x, n_bins_y))
    bin_edges_x = np.zeros(n_bins_x + 1)
    bin_edges_y = np.zeros(n_bins_y + 1)


    for ix in range(n_bins_x):
        bin_edges_x[ix] = hist.GetXaxis().GetBinLowEdge(x_first_bin + ix)
    bin_edges_x[-1] = hist.GetXaxis().GetBinUpEdge(x_last_bin - 1)

    for iy in range(n_bins_y):
        bin_edges_y[iy] = hist.GetYaxis().GetBinLowEdge(y_first_bin + iy)
    bin_edges_y[-1] = hist.GetYaxis().GetBinUpEdge(y_last_bin - 1)


    ix = 0
    for xbin in range(x_first_bin, x_last_bin):
        iy=0
        for ybin in range(y_first_bin, y_last_bin):
            data[ix, n_bins_y-iy-1] = hist.GetBinContent(xbin, ybin)

            iy+=1
        ix+=1

    return data.T, bin_edges_x, bin_edges_y



def get_tprofile_1d_as_numpy(profile: TProfile,
    x_range: Union[tuple, None] = None
):
    """
    Takes a ROOT TProfile instance and returns three numpy arrays of the bin contents, errors and the bin edges.
    
    Parameters:
    - profile (TProfile): The original TProfile.
    
    Returns:
    - numpy.array: An array of the bin contents.
    - numpy.array: An array of the bin content errors.
    - numpy.array: An array of the bin edges.
    """

    x_first_bin, x_last_bin = get_bin_range(profile, range=x_range, axis="x")

    n_bins    = x_last_bin - x_first_bin
    data      = np.zeros(n_bins)
    data_err  = np.zeros(n_bins)
    bin_edges = np.zeros(n_bins + 1)

    ix=0
    for xbin in range(x_first_bin, x_last_bin):
        data[ix]      = profile.GetBinContent(xbin)
        data_err[ix]  = profile.GetBinError(xbin)
        bin_edges[ix] = profile.GetBinLowEdge(xbin)
    bin_edges[-1] = profile.GetBinUpEdge(xbin)

    return data, data_err, bin_edges


def get_tprofile_2d_as_numpy(profile,
    x_range: Union[tuple, None] = None,
    y_range: Union[tuple, None] = None
):
    """
    Takes a ROOT TProfile2D instance and ranges for both axes.
    Returns two 2D numpy arrays of the bin contents and errors and
        two 1D arrays of the bin edges along both axes.
    
    Parameters:
    - profile (TProfile): The original TProfile.
    x_min (int | float) [Optional]: Minimum value for x-axis range,
    x_max (int | float) [Optional]: Maximum value for x-axis range,
    y_min (int | float) [Optional]: Minimum value for y-axis range,
    y_max (int | float) [Optional]: Maximum value for y-axis range
    
    Returns:
    - numpy.array: A 2D array of the bin contents.
    - numpy.array: A 2D array of the bin errors.
    - numpy.array: A 1D array of the x-axis bin edges.
    - numpy.array: A 1D array of the y-axis bin edges.
    """
    
    if not isinstance(profile, TProfile2D): raise ValueError("Input must be a TProfile2D object")

    x_first_bin, x_last_bin = get_bin_range(profile, range=x_range, axis="x")
    y_first_bin, y_last_bin = get_bin_range(profile, range=y_range, axis="y")

    n_bins_x    = x_last_bin - x_first_bin
    n_bins_y    = y_last_bin - y_first_bin
    data        = np.zeros((n_bins_x, n_bins_y))
    data_err    = np.zeros((n_bins_x, n_bins_y))
    bin_edges_x = np.zeros(n_bins_x + 1)
    bin_edges_y = np.zeros(n_bins_y + 1)

    for ix in range(n_bins_x):
        bin_edges_x[ix] = profile.GetXaxis().GetBinLowEdge(x_first_bin + ix)
    bin_edges_x[-1] = profile.GetXaxis().GetBinUpEdge(x_last_bin - 1)

    for iy in range(n_bins_y):
        bin_edges_y[iy] = profile.GetYaxis().GetBinLowEdge(y_first_bin + iy)
    bin_edges_y[-1] = profile.GetYaxis().GetBinUpEdge(y_last_bin - 1)

    ix=0
    for xbin in range(x_first_bin, x_last_bin):
        iy=0
        for ybin in range(y_first_bin, y_last_bin):
            data[ix, n_bins_y-iy-1]      = profile.GetBinContent(xbin, ybin)
            data_err[ix, n_bins_y-iy-1]  = profile.GetBinError(xbin, ybin)

            iy+=1
        ix+=1

    return data.T, data_err.T, bin_edges_x, bin_edges_y



def get_tefficiency_1d_as_numpy(efficiency,
    x_range: Union[tuple, None] = None
):
    """
    Takes a ROOT 1D TEfficiency instance and an interval of interest. Returns four numpy arrays:
    1. Array of efficiencies.
    2. Array of upper errors.
    3. Array of lower errors.
    4. Array of bin edges.

    Parameters:
    - efficiency (TEfficiency): The original TEfficiency.
    - x_range (x_min, x_max) [optional]: X-axis range.

    Returns:
    - numpy.array: Array of efficiencies.
    - numpy.array: Array of upper errors.
    - numpy.array: Array of lower errors.
    - numpy.array: Array of bin edges.
    """
    
    if isinstance(efficiency, TEfficiency):
        
        if efficiency.GetDimension() != 1: raise ValueError("TEfficiency is not 1 dimensional!")
        
        if isinstance(x_range, tuple):
            if isinstance(x_range[0], (int, float)):
                x_first_bin = efficiency.GetPassedHistogram().FindBin(x_range[0])
            else:
                x_first_bin = 1

            if isinstance(x_range[1], (int, float)):
                x_last_bin = efficiency.GetPassedHistogram().FindBin(x_range[1])
            else:
                x_last_bin = efficiency.GetPassedHistogram().GetNbinsX() + 1
        else:
            x_first_bin = 1
            x_last_bin  = efficiency.GetPassedHistogram().GetNbinsX() + 1
        
        n_bins      = x_last_bin - x_first_bin
        effs        = np.zeros(n_bins)
        errors_up   = np.zeros(n_bins)
        errors_down = np.zeros(n_bins)
        bin_edges   = np.zeros(n_bins + 1)

        ix = 0
        for xbin in range(x_first_bin, x_last_bin):
            gbin = efficiency.GetGlobalBin(xbin)

            effs[ix]        = efficiency.GetEfficiency(gbin)
            errors_up[ix]   = efficiency.GetEfficiencyErrorUp(gbin)
            errors_down[ix] = efficiency.GetEfficiencyErrorLow(gbin)
            bin_edges[ix]   = efficiency.GetBinLowEdge(gbin)

            ix+=1
        
        bin_edges[-1] = efficiency.GetBinLowEdge(n_bins) + efficiency.GetBinWidth(n_bins)

        return effs, errors_up, errors_down, bin_edges
    else:
        raise ValueError("Input must be a TEfficiency object")
    



def get_tefficiency_2d_as_numpy(efficiency,
    x_range: Union[tuple, None] = None,
    y_range: Union[tuple, None] = None
):
    """
    Takes a ROOT 2D TEfficiency instance and two intervals of interest along both axes.
    Returns three 2D numpy arrays and two 1D numpy arrays:
    1. 2D Array of efficiencies.
    2. 2D Array of upper errors.
    3. 2D Array of lower errors.
    4. 1D Array of X-axis bin edges.
    5. 1D Array of Y-axis bin edges.

    Parameters:
    - efficiency (TEfficiency): The original TEfficiency.
    - x_min (int | float) [optional]: Minimum x-axis value of interest.
    - x_max (int | float) [optional]: Maximum x-axis value of interest.
    - y_min (int | float) [optional]: Minimum y-axis value of interest.
    - y_max (int | float) [optional]: Maximum y-axis value of interest.
    
    Returns:
    - numpy.array: 2D Array of efficiencies.
    - numpy.array: 2D Array of upper errors.
    - numpy.array: 2D Array of lower errors.
    - numpy.array: 1D Array of X-axis bin edges.
    - numpy.array: 1D Array of Y-axis bin edges.
    """
    
    if isinstance(efficiency, TEfficiency):
        
        if efficiency.GetDimension() != 2:
            raise ValueError("TEfficiency is not 2 dimensional!")
        
        if isinstance(x_range, tuple):
            if isinstance(x_range[0], (int, float)):
                x_first_bin = efficiency.GetPassedHistogram().GetXaxis().FindBin(x_range[0])
            else:
                x_first_bin = 1

            if isinstance(x_range[1], (int, float)):
                x_last_bin = efficiency.GetPassedHistogram().GetXaxis().FindBin(x_range[1])
            else:
                x_last_bin = efficiency.GetPassedHistogram().GetXaxis().GetNbinsX() + 1
        else:
            x_first_bin = 1
            x_last_bin  = efficiency.GetPassedHistogram().GetXaxis().GetNbinsX() + 1
        
        if isinstance(y_range, tuple):
            if isinstance(y_range[0], (int, float)):
                y_first_bin = efficiency.GetPassedHistogram().GetYaxis().FindBin(y_range[0])
            else:
                y_first_bin = 1

            if isinstance(y_range[1], (int, float)):
                y_last_bin = efficiency.GetPassedHistogram().GetYaxis().FindBin(y_range[1])
            else:
                y_last_bin = efficiency.GetPassedHistogram().GetYaxis().GetNbinsX() + 1
        else:
            y_first_bin = 1
            y_last_bin  = efficiency.GetPassedHistogram().GetYaxis().GetNbinsX() + 1


        n_bins_x = x_last_bin - x_first_bin
        n_bins_y = y_last_bin - y_first_bin
        effs = np.zeros((n_bins_x, n_bins_y))
        errors_up = np.zeros((n_bins_x, n_bins_y))
        errors_down = np.zeros((n_bins_x, n_bins_y))
        bin_edges_x = np.zeros(n_bins_x + 1)
        bin_edges_y = np.zeros(n_bins_y + 1)


        for ix in range(n_bins_x):
            bin_edges_x[ix] = efficiency.GetPassedHistogram().GetXaxis().GetBinLowEdge(x_first_bin + ix)
        bin_edges_x[-1] = efficiency.GetPassedHistogram().GetXaxis().GetBinUpEdge(x_last_bin - 1)


        for iy in range(n_bins_y):
            bin_edges_y[iy] = efficiency.GetPassedHistogram().GetYaxis().GetBinLowEdge(y_first_bin + iy)
        bin_edges_y[-1] = efficiency.GetPassedHistogram().GetYaxis().GetBinUpEdge(y_last_bin - 1)


        for ix in range(n_bins_x):
            for iy in range(n_bins_y):
                gbin = efficiency.GetGlobalBin(x_first_bin + ix, y_first_bin + iy)
                effs[ix, n_bins_y-iy-1] = efficiency.GetEfficiency(gbin)
                errors_up[ix, n_bins_y-iy-1] = efficiency.GetEfficiencyErrorUp(gbin)
                errors_down[ix, n_bins_y-iy-1] = efficiency.GetEfficiencyErrorLow(gbin)

        return effs.T, errors_up.T, errors_down.T, bin_edges_x, bin_edges_y
    
    else:
        raise ValueError("Input must be a TEfficiency object")
    
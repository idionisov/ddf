from typing import Union
from ROOT import TH1, TH2, TH3, TH1F, TH2F, TProfile, TProfile2D, TEfficiency    
from ._._h import *

def h_normalize(*hists,
                normalized_integral: float = 1.,
                use_integral: bool = True):
    """
    Scale histograms to a given integral or number of entries.

    Parameters:
    - *hists (TH1, TH2 or dict): The histograms to be normalized or their containing dictionaries
    - normalized_integral (float): The integral or number of entries to which they should be normalized.
    - use_integral (bool): Whether to use histogram's integral or number of entries.

    Raises:
    - ValueError: If arguments are not histograms or dictionaries.
    - ZeroDivisionError: If histogram's integral or number of entries is zero.
    """

    for hist in hists:
        if isinstance(hist, (TH1, TH2, TH3)):
            if use_integral:
                integral = hist.Integral()
                if integral == 0:
                    raise ZeroDivisionError("Histogram integral is zero. Cannot normalize.")
                hist.Scale(normalized_integral / integral)
            else:
                entries = hist.GetEntries()
                if entries == 0:
                    raise ZeroDivisionError("Number of entries in histogram is zero. Cannot normalize.")
                hist.Scale(normalized_integral / entries)
        elif isinstance(hist, dict):
            for h in hist.values():
                h_normalize(h, normalized_integral=normalized_integral, use_integral=use_integral)
        else:
            raise ValueError("Arguments must be histograms (TH1, TH2) or dictionaries containing histograms.")





def get_sub_hist(hist,
    x_low:  Union[float, int],
    x_high: Union[float, int],
    y_low:  Union[float, int, None] = None,
    y_high: Union[float, int, None] = None
):
    """
    Extracts the central region of a TH1, TH2, TProfile or TProfile2D object and returns a new one respectively.
    
    Parameters:
    - hist (TH1, TProfile, TH2, TProfile2D): The original object.
    - x_low  (float or int):           The lower bound of the x-axis.
    - x_high (float or int):           The upper bound of the x-axis.
    - y_low  (float or int or None):   The lower bound of the y-axis.
    - y_high (float or int or None):   The upper bound of the y-axis.
    
    Returns:
    - TH1, TH2, TProfile or TProfile2D: A new instance of the object containing the bins within the specified region.
    """

    if (isinstance(hist, TH2) or isinstance(hist, TProfile2D)) and (y_low is not None) and (y_high is not None):
        return get_subTH2(hist, x_low, x_high, y_low, y_high)
    elif isinstance(hist, TH1) or isinstance(hist, TProfile):
        return get_subTH1(hist, x_low, x_high)
    else: return False



def get_test_hists_1D(
    nbins: int   = 10,
    xlow:  float = 0.,
    xhigh: float = 10.
):
    """
    Create test 1D histograms for passed and total events.
    """

    h_total  = TH1F('h_total', 'Total Histogram', nbins, xlow, xhigh)
    h_passed = TH1F('h_passed', 'Passed Histogram', nbins, xlow, xhigh)

    # Fill the histograms with some test data
    for i in range(1, nbins + 1):
        h_total.SetBinContent(i, 10)
        h_passed.SetBinContent(i, np.random.randint(0, 10))

    return h_passed, h_total

def get_test_hists_2D(
    nbins_x: int   = 10,
    nbins_y: int   = 10,
    xlow:    float = 0.,
    xhigh:   float = 10.,
    ylow:    float = 0.,
    yhigh:   float = 10.
):
    """
    Create test 2D histograms for passed and total events.
    """

    h_total  = TH2F('h_total',  'Total Histogram',  nbins_x, xlow, xhigh, nbins_y, ylow, yhigh)
    h_passed = TH2F('h_passed', 'Passed Histogram', nbins_x, xlow, xhigh, nbins_y, ylow, yhigh)

    # Fill the histograms with some test data
    for xbin in range(1, nbins_x + 1):
        for ybin in range(1, nbins_y + 1):
            h_total.SetBinContent(xbin, ybin, 10)
            h_passed.SetBinContent(xbin, ybin, np.random.randint(0, 10))

    return h_passed, h_total


def get_bin_range(obj,
    range: Union[tuple, None],
    axis:  str = "x"
):
    """
    Takes a histogram-like object and optionally x-axis or y-axis ranges.
    Returns the index of the first and last bins of the respective ranges.
    
    Parameters:
    - obj: The histogram-like object.
    - range  (min, max) [Optional]:  The selected axis range.
    - axis (str): The chose axis to which the range applies.
    
    Returns:
    - tuple (first_bin, last_bin): The first and last bins.
    """

    if   axis.lower()=="x": return get_Xbin_range(obj, x_range=range)
    elif axis.lower()=="y": return get_Ybin_range(obj, y_range=range)
    else: raise ValueError(f"{axis} is an invalid axis!")
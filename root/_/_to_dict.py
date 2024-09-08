from ROOT import TH1
from typing import Union
import uproot
import numpy as np


def _get_dict_TH1(hist: TH1):
    """
    Takes a ROOT TH1 histogram and returns a dictionary.
    
    Args:
    - hist (TH1)
    
    Returns:
    - dict(
        'bin_edges': numpy_array,
        'y':         numpy array of contents
        'ey':        numpy array of errors
    )
    """
    
    n_bins    = hist.GetXaxis().GetNbins()
    data      = np.zeros(n_bins,   dtype=np.float64)
    errors    = np.zeros(n_bins,   dtype=np.float64)
    bin_edges = np.zeros(n_bins+1, dtype=np.float64)

    ix = 0
    for xbin in range(1, hist.GetXaxis().GetNbins() + 1):
        data[ix]      = hist.GetBinContent(xbin)
        errors[ix]    = hist.GetBinErrors(xbin)
        bin_edges[ix] = hist.GetXaxis().GetBinLowEdge(xbin)
        ix+=1
    bin_edges[-1] = hist.GetXaxis().GetBinUpEdge(xbin)

    return {
        'bin_edges': bin_edges,
        'y':         data,
        'ey':        errors
    }

def _get_dict_TH1_uproot(hist):
    if not uproot.Model.is_instance(hist, "TH1"): raise ValueError(f"{type(hist)} is not an uproot TH1 object!")

    return {
        'bin_edges': np.array(hist.axis().edges(), dtype=np.float64),
        'y':         np.array(hist.values(),       dtype=np.float64),
        'ey':        np.array(hist.errors(),       dtype=np.float64)
    }
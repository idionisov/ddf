from typing import Union
from ROOT import TH1, TH1I, TH1F, TH1D, TH2I, TH2F, TH2D, TProfile, TProfile2D, TObject, TEfficiency
import numpy as np
import pandas as pd


def get_x_from_bin_edges(bin_edges):
    """
    Calculate the midpoints and widths of bins from a bin edges array.

    Parameters:
    - bin_edges: numpy array of bin edges

    Returns:
    - bin_midpoints: numpy array of midpoints of the bins
    - bin_widths: numpy array of widths of the bins
    """

    # Make sure bin_edges is a numpy array
    bin_edges = np.array(bin_edges)
    
    # Calculate bin midpoints and bin widths
    bin_midpoints = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_widths    = bin_edges[1:] - bin_edges[:-1]
    
    return bin_midpoints, bin_widths


def get_subTH2(hist,
    x_low:  float | int,
    x_high: float | int,
    y_low:  float | int,
    y_high: float | int
) -> TObject:
    """
    Extracts the central region of a TH2 or TProfile2D object and returns a new TH2 or TProfile2D object respectively.
    
    Parameters:
    - hist (TH2 or TProfile2D): The original TH2 histogram.
    - x_low  (float):           The lower bound of the x-axis.
    - x_high (float):           The upper bound of the x-axis.
    - y_low  (float):           The lower bound of the y-axis.
    - y_high (float):           The upper bound of the y-axis.
    
    Returns:
    - TH2 or TProfile2D: A new TH2 or TProfile2D instance containing the bins within the specified region.
    """
    
    # Find the bin numbers corresponding to the specified x and y bounds
    x_bin_low  = hist.GetXaxis().FindBin(x_low)
    x_bin_high = hist.GetXaxis().FindBin(x_high)
    y_bin_low  = hist.GetYaxis().FindBin(y_low)
    y_bin_high = hist.GetYaxis().FindBin(y_high)
    
    # Use the exact bin edges for the new histogram
    new_x_low  = hist.GetXaxis().GetBinLowEdge(x_bin_low)
    new_x_high = hist.GetXaxis().GetBinUpEdge(x_bin_high)
    new_y_low  = hist.GetYaxis().GetBinLowEdge(y_bin_low)
    new_y_high = hist.GetYaxis().GetBinUpEdge(y_bin_high)

    # Create a new histogram with the correct binning
    h_name   = f'{hist.GetName()}_subset'
    h_title  = hist.GetTitle()
    n_bins_x = x_bin_high - x_bin_low + 1
    n_bins_y = y_bin_high - y_bin_low + 1
    
    if isinstance(hist, TH2D):
        h_out = TH2D(h_name, h_title, n_bins_x, new_x_low, new_x_high, n_bins_y, new_y_low, new_y_high)
    elif isinstance(hist, TH2F):
        h_out = TH2F(h_name, h_title, n_bins_x, new_x_low, new_x_high, n_bins_y, new_y_low, new_y_high)
    elif isinstance(hist, TH2I):
        h_out = TH2I(h_name, h_title, n_bins_x, new_x_low, new_x_high, n_bins_y, new_y_low, new_y_high)
    elif isinstance(hist, TProfile2D):
        h_out = TProfile2D(h_name, h_title, n_bins_x, new_x_low, new_x_high, n_bins_y, new_y_low, new_y_high)
    else:
        raise ValueError("Input must be a TH2 or TProfile2D object")
    
    # Fill the new histogram with the appropriate bin contents
    for i in range(x_bin_low, x_bin_high + 1):
        for j in range(y_bin_low, y_bin_high + 1):
            bin_content = hist.GetBinContent(i, j)
            bin_error   = hist.GetBinError(i, j)
            x_center    = hist.GetXaxis().GetBinCenter(i)
            y_center    = hist.GetYaxis().GetBinCenter(j)
            
            if isinstance(hist, TProfile2D):
                bin_entries = hist.GetBinEntries(hist.GetBin(i, j))
                h_out.Fill(x_center, y_center, bin_content, bin_entries)
            else:
                h_out.SetBinContent(h_out.FindBin(x_center, y_center), bin_content)
                h_out.SetBinError(h_out.FindBin(x_center, y_center), bin_error)
    
    return h_out



def get_subTH1(hist,
    x_low: float | int,
    x_high: float | int
) -> TObject:
    """
    Extracts the central region of a TH1 or TProfile histogram and returns a new histogram or profile.
    
    Parameters:
    - hist (TH1 or TProfile): The original histogram.
    - x_low  (float or int):  The lower bound of the x-axis.
    - x_high (float or int):  The upper bound of the x-axis.
    
    Returns:
    - TH1 or TProfile: A new histogram or profile containing the bins within the specified region.
    """
    
    # Find the bin numbers corresponding to the specified x bounds
    x_bin_low  = hist.GetXaxis().FindBin(x_low)
    x_bin_high = hist.GetXaxis().FindBin(x_high)

    # Use the exact bin edges for the new histogram
    new_x_low  = hist.GetXaxis().GetBinLowEdge(x_bin_low)
    new_x_high = hist.GetXaxis().GetBinUpEdge(x_bin_high)
    
    # Create a new histogram for the central region
    h_name   = f'{hist.GetName()}_subset'
    h_title  = hist.GetTitle()
    n_bins_x = x_bin_high - x_bin_low + 1
    
    if isinstance(hist, TH1D):
        h_out = TH1D(h_name, h_title, n_bins_x, new_x_low, new_x_high)
    elif isinstance(hist, TH1F):
        h_out = TH1F(h_name, h_title, n_bins_x, new_x_low, new_x_high)
    elif isinstance(hist, TH1I):
        h_out = TH1I(h_name, h_title, n_bins_x, new_x_low, new_x_high)
    elif isinstance(hist, TProfile):
        h_out = TProfile(h_name, h_title, n_bins_x, new_x_low, new_x_high)
    else:
        raise ValueError("Input must be a TH1 or TProfile object")
    
    for i in range(x_bin_low, x_bin_high + 1):
        bin_content = hist.GetBinContent(i)
        bin_error   = hist.GetBinError(i)
        x_center    = hist.GetXaxis().GetBinCenter(i)
        
        if isinstance(hist, TProfile):
            bin_entries = hist.GetBinEntries(i)
            h_out.Fill(x_center, bin_content, bin_entries)
        else:
            h_out.SetBinContent(h_out.FindBin(x_center), bin_content)
            h_out.SetBinError(h_out.FindBin(x_center), bin_error)
    
    return h_out



def get_Xbin_range(obj,
    x_range: Union[tuple, None]
):
    """
    Takes a histogram-like object and optionally a x-axis range and returns the index of the first and last bins.
    
    Parameters:
    - obj: The histogram-like object.
    - x_range  (x_min, x_max):  The X-axis range of interest.
    
    Returns:
    - tuple (x_first_bin, x_last_bin): The first and last bins.
    """

    if not obj.GetXaxis(): return ValueError(f"Type {type(obj)} doesn't have X bin range!")

    if isinstance(x_range, tuple):
        if isinstance(x_range[0], (int, float)):
            x_first_bin = obj.GetXaxis().FindBin(x_range[0])
        else:
            x_first_bin = 1
    
        if isinstance(x_range[1], (int, float)):
            x_last_bin = obj.GetXaxis().FindBin(x_range[1])
        else:
            x_last_bin = obj.GetXaxis().GetNbins() + 1
    
    else:
        x_first_bin = 1
        x_last_bin  = obj.GetXaxis().GetNbins() + 1
    
    return x_first_bin, x_last_bin


def get_Ybin_range(obj,
    y_range: Union[tuple, None]
):
    """
    Takes a histogram-like object and optionally a y-axis range and returns the index of the first and last bins.
    
    Parameters:
    - obj: The histogram-like object.
    - y_range  (y_min, y_max):  The Y-axis range of interest.
    
    Returns:
    - tuple (y_first_bin, y_last_bin): The first and last bins.
    """
    
    if not obj.GetXaxis(): return ValueError(f"Type {type(obj)} doesn't have X bin range!")

    if isinstance(y_range, tuple):
        if isinstance(y_range[0], (int, float)):
            y_first_bin = obj.GetYaxis().FindBin(y_range[0])
        else:
            y_first_bin = 1
    
        if isinstance(y_range[1], (int, float)):
            y_last_bin = obj.GetYaxis().FindBin(y_range[1])
        else:
            y_last_bin = obj.GetYaxis().GetNbins() + 1
    
    else:
        y_first_bin = 1
        y_last_bin  = obj.GetYaxis().GetNbins() + 1
    
    return y_first_bin, y_last_bin
from typing import Union
import numpy as np
import uproot


def _get_uproot_th1_as_numpy(hist,
    x_range: Union[tuple, None] = None
):
    """
    Takes an uproot TH1 histogram and an x-axis range.
    Returns a numpy array of the bin contents within the selected range and an array of the bin edges.
    
    Parameters:
    - hist (uproot.Model_TH1): The uproot histogram.
    - x_range (x_min, x_max) [Optional]: X-axis range
    
    Returns:
    - numpy.array: An array of the bin contents.
    - numpy.array: An array of the bin edges.
    """

    bin_contents = hist.values()
    bin_edges    = hist.axis().edges()
    
    x_min=x_range[0] if x_range is not None else np.min(bin_edges)
    x_max=x_range[1] if x_range is not None else np.max(bin_edges)

    x_first_bin = np.searchsorted(bin_edges, x_min, side="left")  if x_min is not None else 0
    x_last_bin  = np.searchsorted(bin_edges, x_max, side="right") if x_max is not None else len(bin_edges) - 1
    
    data = bin_contents[x_first_bin:x_last_bin]
    bin_edges = bin_edges[x_first_bin:x_last_bin + 1]
    
    return data, bin_edges




def _get_uproot_th2_as_numpy(hist,
    x_range: Union[tuple, None] = None,
    y_range: Union[tuple, None] = None
):
    """
    Takes an uproot TH2 histogram and ranges for both axes.
    Returns a numpy array of the bin contents within selected ranges and arrays of bin edges.
    
    Parameters:
    - hist (uproot.Model_TH2): The uproot 2D histogram.
    - x_min (float | int) [Optional]: Minimum x-axis value.
    - x_max (float | int) [Optional]: Maximum x-axis value.
    - y_min (float | int) [Optional]: Minimum y-axis value.
    - y_max (float | int) [Optional]: Maximum y-axis value.
    
    Returns:
    - numpy.array: A 2D array of the bin contents.
    - numpy.array: A 1D array of the x-axis bin edges.
    - numpy.array: A 1D array of the y-axis bin edges.
    """

    bin_contents = hist.values()  
    x_edges = hist.axis(0).edges()
    y_edges = hist.axis(1).edges()
    
    x_min=x_range[0] if x_range is not None else np.min(x_edges)
    x_max=x_range[1] if x_range is not None else np.max(x_edges)
    y_min=y_range[0] if y_range is not None else np.min(y_edges)
    y_max=y_range[1] if y_range is not None else np.max(y_edges)

    x_first_bin = np.searchsorted(x_edges, x_min, side="left")  if x_min is not None else 0
    x_last_bin = np.searchsorted(x_edges,  x_max, side="right") if x_max is not None else len(x_edges) - 1
    
    y_first_bin = np.searchsorted(y_edges, y_min, side="left")  if y_min is not None else 0
    y_last_bin = np.searchsorted(y_edges,  y_max, side="right") if y_max is not None else len(y_edges) - 1
    
    data = bin_contents[x_first_bin:x_last_bin, y_first_bin:y_last_bin]
    x_edges_range = x_edges[x_first_bin:x_last_bin + 1]
    y_edges_range = y_edges[y_first_bin:y_last_bin + 1]
    
    return data.T, x_edges_range, y_edges_range



def _get_uproot_tprofile_1d_as_numpy(profile,
    x_range: Union[tuple, None] = None
):
    """
    Takes an uproot TProfile instance and returns three numpy arrays:
    bin contents (mean values), bin content errors, and bin edges.
    
    Parameters:
    - profile (uproot.Model_TProfile): The uproot TProfile histogram.
    - x_range (x_min, x_max) [Optional]: X-axis range
    
    Returns:
    - numpy.array: An array of the bin contents (mean values).
    - numpy.array: An array of the bin content errors.
    - numpy.array: An array of the bin edges.
    """
    
    bin_contents = profile.values()
    bin_errors   = profile.errors()
    bin_edges    = profile.axis().edges()
    
    x_min=x_range[0] if x_range is not None else np.min(bin_edges)
    x_max=x_range[1] if x_range is not None else np.max(bin_edges)

    x_first_bin = np.searchsorted(bin_edges, x_min, side="left")  if x_min is not None else 0
    x_last_bin  = np.searchsorted(bin_edges, x_max, side="right") if x_max is not None else len(bin_edges) - 1
    
    data = bin_contents[x_first_bin:x_last_bin]
    data_err = bin_errors[x_first_bin:x_last_bin]
    bin_edges_range = bin_edges[x_first_bin:x_last_bin + 1]
    
    return data, data_err, bin_edges_range



def _get_uproot_tprofile_2d_as_numpy(profile,
    x_range: Union[tuple, None] = None,
    y_range: Union[tuple, None] = None
):
    """
    Takes an uproot TProfile2D instance and ranges for both axes.
    Returns two 2D numpy arrays of the bin contents and errors and
    two 1D arrays of the bin edges along both axes.
    
    Parameters:
    - profile (uproot.Model_TProfile2D): The uproot TProfile2D histogram.
    - x_range (x_min, x_max) [Optional]: X-axis range.
    - y_range (y_min, y_max) [Optional]: Y-axis range.
    
    Returns:
    - numpy.array: A 2D array of the bin contents (mean values).
    - numpy.array: A 2D array of the bin errors.
    - numpy.array: A 1D array of the x-axis bin edges.
    - numpy.array: A 1D array of the y-axis bin edges.
    """
    

    bin_contents = profile.values()
    bin_errors   = profile.errors()

    x_edges = profile.axis(0).edges()
    y_edges = profile.axis(1).edges()
    
   
    x_min=x_range[0] if x_range is not None else np.min(x_edges)
    x_max=x_range[1] if x_range is not None else np.max(x_edges)
    y_min=y_range[0] if y_range is not None else np.min(y_edges)
    y_max=y_range[1] if y_range is not None else np.max(y_edges)

    x_first_bin = np.searchsorted(x_edges, x_min, side="left")  if x_min is not None else 0
    x_last_bin  = np.searchsorted(x_edges, x_max, side="right") if x_max is not None else len(x_edges) - 1
    
    y_first_bin = np.searchsorted(y_edges, y_min, side="left")  if y_min is not None else 0
    y_last_bin  = np.searchsorted(y_edges, y_max, side="right") if y_max is not None else len(y_edges) - 1
    
    data = bin_contents[x_first_bin:x_last_bin, y_first_bin:y_last_bin]
    data_err = bin_errors[x_first_bin:x_last_bin, y_first_bin:y_last_bin]
    
    x_edges_range = x_edges[x_first_bin:x_last_bin + 1]
    y_edges_range = y_edges[y_first_bin:y_last_bin + 1]
    
    return data.T, data_err.T, x_edges_range, y_edges_range
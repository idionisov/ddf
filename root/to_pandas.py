import pandas as pd
import uproot
import numpy as np
from ROOT import TGraph, TGraph2D, TGraphErrors, TGraph2DErrors, TGraphAsymmErrors
from ._._to_pandas import _get_dataframe_TGraph, _get_dataframe_TGraph2D, \
    _get_dataframe_TGraph2DErrors, _get_dataframe_TGraphAsymmErrors, \
    _get_dataframe_TGraphAsymmErrors_uproot, _get_dataframe_TGraphErrors, \
    _get_dataframe_TH1_uproot, _get_dataframe_TGraphErrors_uproot, _get_dataframe_TGraph_uproot

def get_as_pandas(obj):
    """
    Converts an object to a pandas DataFrame.
    
    Parameters:
    obj: The object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the object.
    """

    if   isinstance(obj, TGraphAsymmErrors): return _get_dataframe_TGraphAsymmErrors(obj)
    elif isinstance(obj, TGraph2DErrors):    return _get_dataframe_TGraph2DErrors(obj)
    elif isinstance(obj, TGraphErrors):      return _get_dataframe_TGraphErrors(obj)
    elif isinstance(obj, TGraph2D):          return _get_dataframe_TGraph2D(obj)
    elif isinstance(obj, TGraph):            return _get_dataframe_TGraph(obj)
    
    elif uproot.Model.is_instance(obj, "TGraphAsymmErrors"):
        return _get_dataframe_TGraphAsymmErrors_uproot(obj)
    elif uproot.Model.is_instance(obj, "TGraphErrors"):
        return _get_dataframe_TGraphErrors_uproot(obj)
    elif uproot.Model.is_instance(obj, "TGraph"):
        return _get_dataframe_TGraph_uproot(obj)
    elif uproot.Model.is_instance(obj, "TH1"):
        return _get_dataframe_TH1_uproot(obj)
    
    else: raise ValueError("Type cannot be converted to pandas dataframe!")
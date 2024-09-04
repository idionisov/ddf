import pandas as pd
import uproot
import numpy as np
from ROOT import TGraph, TGraph2D, TGraphErrors, TGraph2DErrors, TGraphAsymmErrors
from ._._to_pandas import get_dataframe_TGraph, get_dataframe_TGraph2D, \
    get_dataframe_TGraph2DErrors, get_dataframe_TGraphAsymmErrors, \
    get_dataframe_TGraphAsymmErrors_uproot, get_dataframe_TGraphErrors, \
    get_dataframe_TH1_uproot, get_dataframe_TH1F_uproot

def get_as_pandas(obj):
    """
    Converts an object to a pandas DataFrame.
    
    Parameters:
    obj: The object to be converted.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the values of the object.
    """

    if   isinstance(obj, TGraphAsymmErrors): return get_dataframe_TGraphAsymmErrors(obj)
    elif isinstance(obj, TGraph2DErrors):    return get_dataframe_TGraph2DErrors(obj)
    elif isinstance(obj, TGraphErrors):      return get_dataframe_TGraphErrors(obj)
    elif isinstance(obj, TGraph2D):          return get_dataframe_TGraph2D(obj)
    elif isinstance(obj, TGraph):            return get_dataframe_TGraph(obj)
    
    elif isinstance(obj, uproot.models.TGraph.Model_TGraphAsymmErrors_v3):
        return get_dataframe_TGraphAsymmErrors_uproot(obj)
    
    elif (
        isinstance(obj, uproot.models.TH.Model_TProfile_v7) or
        isinstance(obj, uproot.models.TH.Model_TProfile) or
        isinstance(obj, uproot.models.TH.Model_TH1) or
        isinstance(obj, uproot.models.TH.Model_TH1F_v3) or
        isinstance(obj, uproot.models.TH.Model_TH1F) or
        isinstance(obj, uproot.models.TH.Model_TH1I_v3) or
        isinstance(obj, uproot.models.TH.Model_TH1I)
    ):
        return get_dataframe_TH1_uproot(obj)
    
    else: raise ValueError("Type cannot be converted to pandas dataframe!")
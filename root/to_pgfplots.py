import uproot
import uproot.behaviors
import pandas as pd
from ROOT import TGraphAsymmErrors, TGraphErrors, TGraph, TH1, TH2, TProfile, TProfile2D

from ._._to_pgfplots._dataframes import _get_df_xy_as_pfgplot, _get_df_xy_asymm_errors_as_pfgplot, \
    _get_df_xy_errors_as_pfgplot
from ._._to_pgfplots._graphs import _get_TGraph_as_pgfplot, _get_TGraphAsymmErrors_as_pgfplot, \
    _get_TGraphErrors_as_pgfplot, _get_uproot_TGraph_as_pgfplot, _get_uproot_TGraphAsymmErrors_as_pgfplot, \
    _get_uproot_TGraphErrors_as_pgfplot
from ._._to_pgfplots._histograms import _get_TH1_as_pgfplot, \
    _get_TH2_as_pgfplot, _get_uproot_TH1_as_pgfplot, _get_uproot_TH2_as_pgfplot
from ._._to_pgfplots._profiles import _get_TProfile_as_pgfplot, _get_uproot_TProfile_as_pgfplot


def print_pgfplots(obj):
    """
    Outputs code snippet to plot the object with the pgfplots library for LaTeX.
    
    Parameters:
    obj: The object to be plotted.
    """

    # (1) ROOT Objects
    if   isinstance(obj, TGraphAsymmErrors):  print(_get_TGraphAsymmErrors_as_pgfplot(obj))
    elif isinstance(obj, TGraphErrors):       print(_get_TGraphErrors_as_pgfplot(obj))
    elif isinstance(obj, TGraph):             print(_get_TGraph_as_pgfplot(obj))
    elif isinstance(obj, TProfile2D):         print(_get_TH2_as_pgfplot(obj))
    elif isinstance(obj, TH2):                print(_get_TH2_as_pgfplot(obj))
    elif isinstance(obj, TProfile):           print(_get_TProfile_as_pgfplot(obj))
    elif isinstance(obj, TH1):                print(_get_TH1_as_pgfplot(obj))


    # (3) Pandas DataFrames
    elif isinstance(obj, pd.DataFrame):
        if not (
            "x" in obj.columns and
            "y" in obj.columns
        ): raise ValueError("No x and y columns in dataframe.")

        if (
            "exl" in obj.columns and
            "exh" in obj.columns and
            "eyl" in obj.columns and
            "eyh" in obj.columns
        ): print(_get_df_xy_asymm_errors_as_pfgplot(obj))
        
        elif (
            "ex" in obj.columns and
            "ey" in obj.columns
        ): print(_get_df_xy_errors_as_pfgplot(obj))

        else: print(_get_df_xy_as_pfgplot(obj))

    # (2) Uproot Objects
    elif uproot.Model.is_instance(obj, "TGraphAsymmErrors"):   print(_get_uproot_TGraphAsymmErrors_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TGraphErrors"):        print(_get_uproot_TGraphErrors_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TGraph"):              print(_get_uproot_TGraph_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TProfile2D"):          print(_get_uproot_TH2_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TH2"):                 print(_get_uproot_TH2_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TProfile"):            print(_get_uproot_TProfile_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TH1"):                 print(_get_uproot_TH1_as_pgfplot(obj))

    else: raise ValueError("Object cannot be plotted in pgfplots!")
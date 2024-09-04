import uproot
import uproot.behaviors
import pandas as pd
from ROOT import TGraphAsymmErrors, TGraphErrors, TGraph, TH1, TH2, TProfile, TProfile2D

from ._._to_pgfplots._dataframes import get_df_xy_as_pfgplot, get_df_xy_asymm_errors_as_pfgplot, \
    get_df_xy_errors_as_pfgplot
from ._._to_pgfplots._graphs import get_TGraph_as_pgfplot, get_TGraphAsymmErrors_as_pgfplot, \
    get_TGraphErrors_as_pgfplot, get_uproot_TGraph_as_pgfplot, get_uproot_TGraphAsymmErrors_as_pgfplot, \
    get_uproot_TGraphErrors_as_pgfplot
from ._._to_pgfplots._histograms import get_TH1_as_pgfplot, get_TH1_errors_as_pgfplot, \
    get_TH2_as_pgfplot, get_uproot_TH1_as_pgfplot, get_uproot_TH2_as_pgfplot
from ._._to_pgfplots._profiles import get_TProfile_as_pgfplot, get_uproot_TProfile_as_pgfplot


def print_pgfplots(obj):
    """
    Outputs code snippet to plot the object with the pgfplots library for LaTeX.
    
    Parameters:
    obj: The object to be plotted.
    """

    # (1) ROOT Objects
    if   isinstance(obj, TGraphAsymmErrors):  print(get_TGraphAsymmErrors_as_pgfplot(obj))
    elif isinstance(obj, TGraphErrors):       print(get_TGraphErrors_as_pgfplot(obj))
    elif isinstance(obj, TGraph):             print(get_TGraph_as_pgfplot(obj))
    elif isinstance(obj, TH2):                print(get_TH2_as_pgfplot(obj))
    elif isinstance(obj, TProfile2D):         print(get_TH2_as_pgfplot(obj))
    elif isinstance(obj, TH1):                print(get_TH1_as_pgfplot(obj))
    elif isinstance(obj, TProfile):           print(get_TProfile_as_pgfplot(obj))

    # (2) Uproot Objects
    elif uproot.Model.is_instance(obj, "TGraphAsymmErrors"):   print(get_uproot_TGraphAsymmErrors_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TGraphErrors"):        print(get_uproot_TGraphErrors_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TGraph"):              print(get_uproot_TGraph_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TProfile2D"):          print(get_uproot_TH2_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TH2"):                 print(get_uproot_TH2_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TProfile"):            print(get_uproot_TProfile_as_pgfplot(obj))
    elif uproot.Model.is_instance(obj, "TH1"):                 print(get_uproot_TH1_as_pgfplot(obj))

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
        ): print(get_df_xy_asymm_errors_as_pfgplot(obj))
        
        elif (
            "ex" in obj.columns and
            "ey" in obj.columns
        ): print(get_df_xy_errors_as_pfgplot(obj))

        else: print(get_df_xy_as_pfgplot(obj))

    else: raise ValueError("Object cannot be plotted in pgfplots!")
from typing import Union
import numpy as np
import uproot
from ROOT import TObject, TEfficiency, TProfile2D, TH2, TProfile, TH1
from ._._to_numpy._root import _get_tefficiency_1d_as_numpy, _get_tefficiency_2d_as_numpy, \
    _get_th1_as_numpy, _get_th2_as_numpy, _get_tprofile_1d_as_numpy, _get_tprofile_2d_as_numpy
from ._._to_numpy._uproot import _get_uproot_th1_as_numpy, _get_uproot_th2_as_numpy, \
    _get_uproot_tprofile_1d_as_numpy, _get_uproot_tprofile_2d_as_numpy


def get_as_numpy(obj,
    x_range: Union[tuple, None] = None,
    y_range: Union[tuple, None] = None
): 
    if not (isinstance(obj, TObject) or uproot.Model.is_instance(obj, "TObject")):
        raise ValueError("Input must be a ROOT or an uproot TObject instance!")

    if isinstance(obj, TEfficiency):
        if obj.GetDimension() == 2:
            return _get_tefficiency_2d_as_numpy(obj, x_range, y_range)
        elif obj.GetDimension() == 1:
            return _get_tefficiency_1d_as_numpy(obj, x_range)
        else: raise ValueError("The TEfficiency object is not one or two dimensional!")
    
    
    elif isinstance(obj, TProfile2D): return _get_tprofile_2d_as_numpy(obj, x_range, y_range)
    elif isinstance(obj, TH2):        return _get_th2_as_numpy(obj, x_range, y_range)
    elif isinstance(obj, TProfile):   return _get_tprofile_1d_as_numpy(obj, x_range)
    elif isinstance(obj, TH1):        return _get_th1_as_numpy(obj, x_range)
    

    elif uproot.Model.is_instance(obj, "TProfile2D"): return _get_uproot_tprofile_2d_as_numpy(obj, x_range)
    elif uproot.Model.is_instance(obj, "TH2"):        return _get_uproot_th2_as_numpy(obj, x_range)
    elif uproot.Model.is_instance(obj, "TProfile"):   return _get_uproot_tprofile_1d_as_numpy(obj, x_range)
    elif uproot.Model.is_instance(obj, "TH1"):        return _get_uproot_th1_as_numpy(obj, x_range)
    
    else: raise ValueError(f"Type {type(obj)} is cannot be converted to numpy!")
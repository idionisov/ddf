import uproot
from ._._to_dict import get_dict_TH1_uproot

def get_as_dict(obj):
    if uproot.Model.is_instance(obj, "TH1"): return get_dict_TH1_uproot(obj)
    else: raise ValueError("Object type cannot be returned as dict!")
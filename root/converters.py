import ROOT
import uproot

from .utils import teff, tgraph, th1


def to_numpy(input_object, **kwargs):
    if isinstance(input_object, str):
        input_object = uproot.open(input_object)

    if not (isinstance(input_object, ROOT.TObject) or uproot.Model.is_instance(input_object, "TObject")):
        raise ValueError("Input is neither a ROOT.TObject nor an uproot.TObject instance!")

    object_type_name = str(type(input_object)).lower()

    if any(type_key in object_type_name for type_key in ("th1", "th2", "tprofile")):
        return th1.hist_to_numpy(input_object, **kwargs)

    elif any(type_key in object_type_name for type_key in ("tgraph", "tgraph2d")):
        return tgraph.graph_to_numpy(input_object, **kwargs)

    elif isinstance(input_object, ROOT.TEfficiency) or "tefficiency" in object_type_name:
        if hasattr(input_object, "GetDimension") and input_object.GetDimension() > 2:
            raise ValueError("The TEfficiency object is not one or two dimensional!")
        else:
            return teff.teff_to_numpy(input_object, **kwargs)

    else:
        raise ValueError(f"Type {type(input_object)} cannot be converted to numpy!")


def to_pandas(input_object, **kwargs):
    if isinstance(input_object, str):
        input_object = uproot.open(input_object)

    if not (isinstance(input_object, ROOT.TObject) or uproot.Model.is_instance(input_object, "TObject")):
        raise ValueError("Input is neither a ROOT.TObject nor an uproot.TObject instance!")

    object_type_name = str(type(input_object)).lower()

    if any(type_key in object_type_name for type_key in ("th1", "tprofile")):
        return th1.hist_to_pandas(input_object, **kwargs)

    elif any(type_key in object_type_name for type_key in ("tgraph", "tgraph2d")):
        return tgraph.graph_to_pandas(input_object, **kwargs)

    elif isinstance(input_object, ROOT.TEfficiency) or "tefficiency" in object_type_name:
        if hasattr(input_object, "GetDimension") and input_object.GetDimension() > 2:
            raise ValueError("The TEfficiency object is not one or two dimensional!")
        else:
            return teff.teff_to_pandas(input_object, **kwargs)

    else:
        raise ValueError(f"Type {type(input_object)} cannot be converted to pandas!")

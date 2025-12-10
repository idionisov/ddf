import ROOT
import uproot

from .utils import teff, tgraph, th1


def to_numpy(obj, **kwargs):
    if not (isinstance(obj, ROOT.TObject) or uproot.Model.is_instance(obj, "TObject")):
        raise ValueError("Input is neither a ROOT.TObject nor an uproot.TObject instance!")

    elif any(s in str(type(obj)).lower() for s in ("th1", "th2")):
        return th1.hist_to_numpy(obj, **kwargs)

    elif any(s in str(type(obj)).lower() for s in ("tgraph", "tgraph2d")):
        return tgraph.graph_to_numpy(obj, **kwargs)

    elif isinstance(obj, ROOT.TEfficiency):
        if obj.GetDimension() > 2:
            raise ValueError("The TEfficiency object is not one or two dimensional!")
        else:
            return teff.teff_to_numpy(obj, **kwargs)

    else:
        raise ValueError(f"Type {type(obj)} is cannot be converted to numpy!")




def to_pandas(obj, **kwargs):
    if not (isinstance(obj, ROOT.TObject) or uproot.Model.is_instance(obj, "TObject")):
        raise ValueError("Input is neither a ROOT.TObject nor an uproot.TObject instance!")

    elif "th1" in str(type(obj)).lower():
        return th1.hist_to_pandas(obj, **kwargs)

    elif any(s in str(type(obj)).lower() for s in ("tgraph", "tgraph2d")):
        return tgraph.graph_to_pandas(obj, **kwargs)

    elif isinstance(obj, ROOT.TEfficiency):
        if obj.GetDimension() > 2:
            raise ValueError("The TEfficiency object is not one or two dimensional!")
        else:
            return teff.teff_to_numpy(obj, **kwargs)

    else:
        raise ValueError(f"Type {type(obj)} is cannot be converted to numpy!")

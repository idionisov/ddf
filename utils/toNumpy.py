from utils.th1 import isTH1, isTH2, isTProfile, isTProfile2D, \
    getNumpyFromTH2, getNumpyFromTProfile2D, getNumpyFromTProfile, \
    getNumpyFromTH1
from teff import getNumpyFromTEff2D, getNumpyFromTEff1D



def getAsNumpy(obj,
    xmin: Union[float, int, None] = None,
    xmax: Union[float, int, None] = None,
    ymin: Union[float, int, None] = None,
    ymax: Union[float, int, None] = None
):

    if not (isinstance(obj, ROOT.TObject) or uproot.Model.is_instance(obj, "TObject")):
        raise ValueError("Input is neither a ROOT.TObject nor an uproot.TObject instance!")

    if isinstance(obj, ROOT.TEfficiency):
        if obj.GetDimension() == 2:
            return getNumpyFromTEff2D(obj, xmin, xmax, ymin, ymax)
        elif obj.GetDimension() == 1:
            return getNumpyFromTeff1D(obj, xmin, xmax)
        else:
            raise ValueError("The TEfficiency object is not one or two dimensional!")

    elif isTProfile2D(obj, option="all"):
        return getNumpyFromTProfile2D(obj, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    elif isTH2(obj, option="all"):
        return getNumpyFromTH2(obj, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    elif isTProfile(obj, option="all"):
        return getNumpyFromTProfile(obj, xmin=xmin, xmax=xmax)

    elif isTH1(obj, option="all"):
        return getNumpyFromTH1(obj, xmin=xmin, xmax=xmax)

    else:
        raise ValueError(f"Type {type(obj)} is cannot be converted to numpy!")

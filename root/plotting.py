import matplotlib.pyplot as plt
import pandas as pd
import ROOT

from . import converters


def errplot(obj,
    cols: dict = {
        "x":   "x",
        "y":   "y",
        "z":   "z",
        "ex":  "ex",
        "ey":  "ey",
        "exl": "exl",
        "exh": "exh",
        "eyl": "eyl",
        "eyh": "eyh",
    },
    ** kwargs
):
    df = converters.to_pandas(obj, cols)

    # ---- Extract x-errors ----
    ex = None
    if cols["ex"] in df:
        ex = df[cols["ex"]]
    elif cols["exl"] in df and cols["exh"] in df:
        ex = [df[cols["exl"]], df[cols["exh"]]]

    # ---- Extract y-errors ----
    ey = None
    if cols["ey"] in df:
        ey = df[cols["ey"]]
    elif cols["eyl"] in df and cols["eyh"] in df:
        ey = [df[cols["eyl"]], df[cols["eyh"]]]

    # ---- Plot ----
    name = obj.GetName() if hasattr(obj, "GetName") else None

    plt.errorbar(
        df[cols["x"]],
        df[cols["y"]],
        xerr=ex,
        yerr=ey,
        label=name,
        **kwargs
    )

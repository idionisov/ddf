import uproot


def get_dict_TH1_uproot(hist):
    if not uproot.Model.is_instance(hist, "TH1"): return ValueError(f"{type(hist)} is not an uproot TH1 object!")

    return {
        'bin_edges': hist.axis().edges(),
        'y':         hist.values(),
        'ey':        hist.errors()
    }
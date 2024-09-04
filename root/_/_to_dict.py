import uproot


def get_dict_TH1_uproot(
    hist: uproot.models.TH.Model_TH1F_v3 | uproot.models.TH.Model_TH1D_v3 | uproot.models.TH.Model_TH1I_v3
):
    return {
        'bin_edges': hist.axis().edges(),
        'y':         hist.values(),
        'ey':        hist.errors()
    }
from ROOT import TChain, TGraph, kBlack, MuFilter, TClonesArray, sndRecoTrack, TMath, TVector3
from snd.trk import xy_eff_range, is_good, is_within_veto_bar, is_within_us5_bar, is_within_ds3
import numpy as np
from typing import Callable


eff_xy_box = TGraph(5,
    np.array(
        [xy_eff_range['min']['x'], xy_eff_range['min']['x'], xy_eff_range['max']['x'], xy_eff_range['max']['x'], xy_eff_range['min']['x']],
        dtype=float
    ),
    np.array(
        [xy_eff_range['min']['y'], xy_eff_range['max']['y'], xy_eff_range['max']['y'], xy_eff_range['min']['y'], xy_eff_range['min']['y']],
        dtype=float
    )
)
eff_xy_box.SetName('eff_xy_box')
eff_xy_box.SetLineColor(kBlack)
eff_xy_box.SetLineWidth(3)
eff_xy_box.SetMarkerSize(0)


def is_good_track_of_track_type(
    track_type:  int,
    track1:      sndRecoTrack,
    mf_hits:     TClonesArray,
    mf:          MuFilter,
    chi2ndf_max: float = 1e6
) -> bool:
    if track_type==11:
        if (
            track1.getTrackType() != 13 or
            not is_good(track1) or
            not is_within_veto_bar(track1, mf_hits, mf) or
            track1.getChi2Ndf() > chi2ndf_max
        ): return False
        else: return True

    elif track_type==1:
        if (
            track1.getTrackType() != 3 or
            not is_good(track1) or
            not is_within_veto_bar(track1, mf_hits, mf) or
            track1.getChi2Ndf() > chi2ndf_max
        ): return False
        else: return True

    elif track_type==13:
        if (
            track1.getTrackType() != 11 or
            not is_good(track1, xz_ang_max=0.022) or
            not is_within_us5_bar(track1, mf_hits, mf) or
            not is_within_ds3(track1) or
            track1.getChi2Ndf() > chi2ndf_max
        ): return False
        else: return True

    elif track_type==3:
        if(
            track1.getTrackType() != 1 or
            not is_good(track1, xz_ang_max=0.022) or
            not is_within_us5_bar(track1, mf_hits, mf) or
            not is_within_ds3(track1) or
            track1.getChi2Ndf() > chi2ndf_max
        ): return False
        else: return True

    else: return False


def ref1_is_within_eff_area(
    ref1: TVector3,
    x_min: float = -43.,
    x_max: float = -10.,
    y_min: float = 18.,
    y_max: float = 50.
) -> bool:
    if (
        ref1.X() >= x_min and
        ref1.X() <= x_max and
        ref1.Y() >= y_min and
        ref1.Y() <= y_max
    ): return True
    else: return False

def ref1_and_ref2_are_within_allowed_distance(
    ref1: TVector3,
    ref2: TVector3,
    allowed_distance: float = 3.
) -> bool:
    if (
        TMath.Abs(ref2.X()-ref1.X()) <= allowed_distance and
        TMath.Abs(ref2.Y()-ref1.Y()) <= allowed_distance
    ): return True
    else: return False

def track_comparison_eff(
    histograms: dict,
    event: TChain,
    mufilter: MuFilter,
    run_or_mcSet: int | str,
    fill_hists_func:  Callable,
    track_types: list  = [1, 11, 3, 13],
    xy_eff_range: dict = {
        "min": {"x": -43, "y": 18},
        "max": {"x": -10, "y": 50}
    },
    z_ref: float = 490.,
    weight: int | float = 1
):
    for tt in track_types:
        for trk1 in event.Reco_MuonTracks:

            if not is_good_track_of_track_type(tt, trk1, event.Digi_MuFilterHits, mufilter): continue

            fill_hists_func(histograms, event, trk1, run_or_mcSet, tt, z_ref, xy_eff_range, weight=weight)

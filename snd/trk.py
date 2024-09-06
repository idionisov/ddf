from ._._trk import *
from ROOT import sndRecoTrack, MuFilterHit, MuFilter, TVector3, TMath, TClonesArray

def is_good(
    track: sndRecoTrack,
    xz_ang_min:  float = -0.08,
    xz_ang_max:  float =  0.08,
    yz_ang_min:  float = -0.08,
    yz_ang_max:  float =  0.08,
    chi2ndf_max: float =  1e6,
    chi2ndf_min: float =  0.,
    trkP_max:    int   =  999,
    trkP_min:    int   =  0
) -> bool:
    """
    Checks if an sndRecoTrack is 'good'.

    Parameters:
    - track (sndRecoTrack): The track to be assessed.
    - xz_ang_min (float):   The largest allowed negative angle in XZ plane in rad.
    - xz_ang_max (float):   The largest allowed positive angle in XZ plane in rad.
    - yz_ang_min (float):   The largest allowed negative angle in YZ plane in rad.
    - yz_ang_max (float):   The largest allowed positive angle in YZ plane in rad.

    Returns:
    - bool: whether the track is good or not.
    """

    if track.getNdf()==0 or track.getTrackMom().Z()==0: return False
    
    track_xz_angle = track.getAngleXZ()
    track_yz_angle = track.getAngleYZ()
    chi2ndf = track.getChi2Ndf()
    trkP = track.getTrackPoints().size()

    if (
        track.getTrackFlag() and
        track_xz_angle >= xz_ang_min and
        track_xz_angle <= xz_ang_max and
        track_yz_angle >= yz_ang_min and
        track_yz_angle <= yz_ang_max and
        chi2ndf <= chi2ndf_max and
        chi2ndf >= chi2ndf_min and
        trkP <= trkP_max and
        trkP >= trkP_min
    ): return True
    else: return False


def get_doca(
    mf_hit: MuFilterHit,
    track:  sndRecoTrack,
    MuFi:   MuFilter
) -> float:
    """
    Gets the distance of closest approach to an activated MuFitler detector element.

    Parameters:
    - mf_hit (MuFilterHit): The hit with respecto to which the doca is calculated.
    - track (sndRecoTrack): The track.
    - MuFi (MuFilter):      The MuFilter module of the geofile accedssed through SndlhcGeo::GeoInterface.

    Returns:
    - float: the distance of closest approach in cm.
    """

    left  = TVector3()
    right = TVector3()
    MuFi.GetPosition(mf_hit.GetDetectorID(), left, right)

    mom = track.getTrackMom()
    pos = track.getStart()
    pq  = left-pos
    uCrossv = (right - left).Cross(mom)
    doca = pq.Dot(uCrossv)/uCrossv.Mag()
    return TMath.Abs(doca)


def get_intersection(track: sndRecoTrack, Z: float) -> TVector3:
    """
    Gets the intersection point of an sndRecoTrack with a plane at a given Z.
    The Z-plane is perpendicular to the X and Y axes.

    Parameters:
    - track (sndRecoTrack): The track that crosses the plane at the given Z.
    - Z (float): The Z-coordinate of the plane in cm.

    Returns:
    - TVector3: The vector giving the point of intersection.
    """

    track_start = track.getStart()
    track_mom   = track.getTrackMom()
    track_slope = (Z - track_start.Z())/track_mom.Z()

    intersection_point = TVector3(
        track_start.X() + track_slope*track_mom.X(),
        track_start.Y() + track_slope*track_mom.Y(),
        Z
    )
    return intersection_point

def is_within_ds3(track: sndRecoTrack) -> bool:
    """
    Checks whether an sndRecoTrack passes through the DS3 acceptance.

    Parameters:
    - track (sndRecoTrack): The track.

    Returns:
    - bool: Whether the track passes through the DS3 acceptance.
    """

    is_within_DS3 = False

    x_max = 4.713
    x_min = -55.287
    y_min = 12.770
    y_max = 72.770

    ds3_point = get_intersection(track, 538.366)

    if (
        ds3_point.X() > x_min and
        ds3_point.X() < x_max and
        ds3_point.Y() > y_min and
        ds3_point.Y() < y_max
    ): is_within_DS3 = True
    return is_within_DS3

def get_station(z: float) -> int:
    """
    Gets the station that corresponds to a given Z-coordinate value.
    Returns values from 0 to 4 for SciFi and 0 to 2 for DS.

    Parameters:
    - Z (float): The Z-coordinate.

    Returns:
    - int: The station number that corresponds to the given Z.
    """

    if   z > 285 and z < 306:   return 0
    elif z > 306 and z < 320:   return 1
    elif z > 320 and z < 333:   return 2
    elif z > 333 and z < 346:   return 3
    elif z > 346 and z < 360:   return 4

    elif z > 485 and z < 505:   return 0
    elif z > 505 and z < 530:   return 1
    elif z > 530 and z < 550:   return 2

    else: return -999


def is_within_us5_bar(track: sndRecoTrack, mf_hits: TClonesArray, MuFi: MuFilter) -> bool:
    """
    Checks whether an sndRecoTrack passes within 3 cm of an activated US5 bar.

    Parameters:
    - track (sndRecoTrack): The track.
    - mf_hits (TClonesArray): The array of all MuFilterHits.
    - MuFi (MuFilter):      The MuFilter module of the geofile accedssed through SndlhcGeo::GeoInterface.

    Returns:
    - bool: Whether the track passes within 3 cm of an activated US5 bar.
    """

    is_within_us5 = False
    for mf_hit in mf_hits:
        if (mf_hit.GetSystem() != 2 and mf_hit.GetPlane() != 4): continue
        if (get_doca(mf_hit, track, MuFi) <= 3):
            is_within_us5 = True
            break
    return is_within_us5


def is_within_veto_bar(track: sndRecoTrack, mf_hits: TClonesArray, MuFi: MuFilter) -> bool:
    """
    Checks whether an sndRecoTrack passes within 3 cm of an activated veto bar.

    Parameters:
    - track (sndRecoTrack): The track.
    - mf_hits (TClonesArray): The array of all MuFilterHits.
    - MuFi (MuFilter): The MuFilter module of the geofile accedssed through SndlhcGeo::GeoInterface.

    Returns:
    - bool: Whether the track passes within 3 cm of an activated veto bar.
    """

    is_within_veto = False
    for mf_hit in mf_hits:
        if (mf_hit.GetSystem() != 1): continue
        if (get_doca(mf_hit, track, MuFi) <= 3):
            is_within_veto = True
            break
    return is_within_veto


def get_anti_tt(tt: int)->int:
    if   tt==1:  return 3
    elif tt==3:  return 1
    elif tt==11: return 13
    elif tt==13: return 11
    else: raise ValueError(f"{tt} is an invalid track type!")

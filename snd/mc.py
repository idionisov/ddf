from ROOT import TMath, TChain, TVector3, sndRecoTrack, ShipMCTrack
from .trk import get_intersection

PbPb_factors: dict = {
    'EMD': 0.1388888888888889,
    'NI':  2.003205128205128
}


def there_is_a_muon(
    mc_event: TChain
) -> bool:
    '''
    Checks if there is a passing muon in a Monte Carlo event.

    Args:
    - mc_event (TChain)

    Returns:
    - bool: Whether there was a passing muon in this event.
    '''

    for mcTrack in mc_event.MCTrack:
        if TMath.Abs(mcTrack.GetPdgCode()) == 13:
            return True
    return False


def should_be_a_track(
    mc_event:   TChain,
    nMCPoints:  dict = {
        'sf': {'H': {}, 'V': {}},
        'ds': {'H': {}, 'V': {}}
    }
) -> dict:
    """
    Checks if an SND@LHC event satisfies the conditions for track reconstruction to take place

    Parameters:
    - mc_event (TChain);
    - nMCPoints (dict):    Dictionary of the number of monte carlo hits in both
        vertical and horizontal planes and in both Scifi and DS subsystems.
        {
            'sf': {'H': {}, 'V': {}},
            'ds': {'H': {}, 'V': {}}
        }

    Returns:
    - dict of two bools for the two systems about where a track is reconstructible.
        {
            'sf': bool,
            'ds': bool
        }
    """

    nScifiPoints = {'H': 0, 'V': 0}
    nDSPoints    = {'H': 0, 'V': 0}

    nMCPoints['sf']['H'] = {1:0, 2:0, 3:0, 4:0, 5:0}
    nMCPoints['sf']['V'] = {1:0, 2:0, 3:0, 4:0, 5:0}
    nMCPoints['ds']['H'] = {1:0, 2:0, 3:0, 4:0}
    nMCPoints['ds']['V'] = {1:0, 2:0, 3:0, 4:0}

    should_be_reconstructed = {'sf': False, 'ds': False}
    for mc_point in mc_event.ScifiPoint:
        if (TMath.Abs(mc_point.PdgCode()) == 13 and mc_point.GetTrackID() == 0):
            detID = mc_point.GetDetectorID()

            # Checking for reconstructibility of SciFi tracks

            # Second digit:
            #   - type of the plane:
            #       - 0: Horizontal fiber plane
            #       - 1: Vertical fiber plane
            if int( (detID/100000)%2 ) == 0:
                nMCPoints['sf']['H'][int(detID/1e+6)]+=1
            elif int( (detID/100000)%2 ) == 1:
                nMCPoints['sf']['V'][int(detID/1e+6)]+=1

            for sf_plane in range(1, len(nMCPoints['sf']['V'])+1):

                if nMCPoints['sf']['V'][sf_plane]>0:
                    nScifiPoints['V']+=1

                if nMCPoints['sf']['H'][sf_plane]>0:
                    nScifiPoints['H']+=1


    # Checking for reconstructibility of DS tracks
    #   - MC point detector ID > 30000
    for mc_point in mc_event.MuFilterPoint:
        if abs(mc_point.PdgCode())==13 and mc_point.GetTrackID()==0 :
            detID = mc_point.GetDetectorID()
            if detID < 30000: continue

            if detID%1000 > 59:
                nMCPoints['ds']['V'][int(detID/1000) % 10 + 1] += 1
            else:
                nMCPoints['ds']['H'][int(detID/1000) % 10 + 1] += 1


        for ds_plane in range(1, 5):
            if nMCPoints['ds']['V'][ds_plane] > 0: nDSPoints['V'] += 1
            if nMCPoints['ds']['H'][ds_plane] > 0: nDSPoints['H'] += 1

    # Define a reconstructible SciFi track
    # as having at least 3H + 3V muon MC points in SciFi
    if (nScifiPoints['H'] >= 3 and nScifiPoints['V'] >= 3):
        should_be_reconstructed['sf'] = True

    if (nDSPoints['H'] >= 3 and nDSPoints['V'] >= 3):
        should_be_reconstructed['ds'] = True

    return should_be_reconstructed


def get_angle_xz(mc_track) -> float:
    """
    Parameters:
    - mc_track (ShipMCTrack).

    Returns:
    - The XZ projection of the mc_track angle in radians.
    """
    px = mc_track.GetPx()
    pz = mc_track.GetPz()
    return TMath.ATan(px/pz)

def get_angle_yz(mc_track) -> float:
    """
    Parameters:
    - mc_track (ShipMCTrack).

    Returns:
    - The YZ projection of the mc_track angle in radians.
    """
    py = mc_track.GetPy()
    pz = mc_track.GetPz()
    return TMath.ATan(py/pz)

def get_intersection_mc(mc_track, z: float = 490.) -> TVector3:
    """
    Parameters:
    - mc_track (ShipMCTrack);
    - z  (float):    z-coordinate of a plane that's perpendicular to x and y axes.

    Returns:
    - TVector3 of intersection point of the mc_track with the plane at the given z.
    """

    px = mc_track.GetPx()
    py = mc_track.GetPy()
    pz = mc_track.GetPz()

    px_0 = mc_track.GetStartX()
    py_0 = mc_track.GetStartY()
    pz_0 = mc_track.GetStartZ()

    t = (z - pz_0) / pz

    x = px_0 + px * t
    y = py_0 + py * t

    return TVector3(x, y, z)



def tracks_match(
    track:    sndRecoTrack,
    mc_track: ShipMCTrack,
    z_ref:    float = 490.
) -> bool:
    """
    Parameters:
    - track:   (sndRecoTrack): reconstructed track;
    - mc_track (ShipMCTrack): simulated track;
    - z_ref    (float): z-coordinate of the reference plane.

    Returns:
    - bool: Whether the tracks are matched or not.
    """

    x = {
        1: get_intersection_mc(mc_track, z_ref).X(),
        2: get_intersection(track, z_ref).X()
    }
    y = {
        1: get_intersection_mc(mc_track, z_ref).Y(),
        2: get_intersection(track, z_ref).Y()
    }
    
    track_start = track.getStart()
    track_stop  = track.getStop()
    
    z0 = track_start.Z()
    x0 = {
        1: track_start.X(),
        2: get_intersection_mc(mc_track, z0).X()
    }
    y0 = {
        1: track_start.Y(),
        2: get_intersection_mc(mc_track, z0).Y()
    }
    
    z1 = track_stop.Z()
    x1 = {
        1: track_stop.X(),
        2: get_intersection_mc(mc_track, z1).X()
    }
    y1 = {
        1: track_stop.Y(),
        2: get_intersection_mc(mc_track, z1).Y()
    }

    dX = {
        'ref':   abs(x[1]  - x[2] ),
        'start': abs(x0[1] - x0[2]),
        'end':   abs(x1[1] - x1[2])
    }
    dY = {
        'ref':   abs(y[1]  - y[2] ),
        'start': abs(y0[1] - y0[2]),
        'end':   abs(y1[1] - y1[2])
    }

    dXZ = abs(get_angle_xz(mc_track) - 1e3*track.getAngleXZ())
    dYZ = abs(get_angle_yz(mc_track) - 1e3*track.getAngleYZ())

    tt = track.getTrackType()
    if tt==1 or tt==11:
        if (
            dX['ref'] <= 0.2 and dX['start'] <= 0.045 and dX['end'] <= 0.045 and
            dY['ref'] <= 0.2 and dY['start'] <= 0.045 and dY['end'] <= 0.045 and
            dXZ <= 5 and dYZ <= 5
        ):  return True
        else: return False    
    elif tt==3 or tt==13:
        if (
            dX['ref'] <= 1.5 and dX['start'] <= 1.5 and dX['end'] <= 1.5 and
            dY['ref'] <= 1.5 and dY['start'] <= 1.5 and dY['end'] <= 1.5 and
            dXZ <= 5 and dYZ <= 5
        ):  return True
        else: return False
    else: return False

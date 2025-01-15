import ROOT
import glob
from typing import Union

def nType(tt: int) -> str:
    if   tt==1  or tt==3:  return 'clusters'
    elif tt==11 or tt==13: return 'hits'
    else: raise ValueError(f"{tt} is an invalid track type!")

def nName(tt: int) -> str:
    if   tt == 1:  return 'Scifi clusters'
    elif tt == 11: return 'Scifi hits'
    elif tt == 3:  return 'DS clusters'
    elif tt == 13: return 'DS hits'
    else: raise ValueError(f"{tt} is an invalid track type!")





def getTChain(inputDir: str, files: str) -> ROOT.TChain:
    try:
        file_ = getAllFiles(inputDir, files)[0]
        tfile = ROOT.TFile.Open(file_)
    except Exception as e:
        print(f"Error opening file: {e}")
        return None


def getTtFromSys(system: str) -> tuple:
    if system.lower()=="sf" or system.lower()=="scifi":
        return 1, 11
    elif system.lower()=="ds" or system.lower()=="downstream":
        return 3, 13
    else:
        raise ValueError(f"{system} is not a valid system!")

def getN(
    tt: int,
    event: Union[ROOT.TChain, None] = None,
    sf_hits: Union[ROOT.TClonesArray, None] = None,
    sf_clusters: Union[ROOT.TClonesArray, None] = None,
    mf_hits: Union[ROOT.TClonesArray, None] = None,
    mf_clusters: Union[ROOT.TClonesArray, None] = None
) -> int:

    if tt==1:
        if isinstance(sf_clusters, ROOT.TClonesArray):
            return sf_clusters.GetEntries()
        elif isinstance(event, ROOT.TChain): return event.Cluster_Scifi.GetEntries()
        else: raise ValueError("Insufficient input parameters provided.")

    elif tt==11:
        if isinstance(sf_hits, ROOT.TClonesArray): return sf_hits.GetEntries()
        elif isinstance(event, ROOT.TChain): return event.Digi_ScifiHits.GetEntries()
        else: raise ValueError("Insufficient input parameters provided.")

    elif tt==3:
        if isinstance(mf_clusters, ROOT.TClonesArray):
            return mf_clusters.GetEntries()
        elif isinstance(event, ROOT.TChain):
            return event.Cluster_Mufi.GetEntries()
        else: raise ValueError("Insufficient input parameters provided.")

    elif tt==13:
        if isinstance(mf_hits, ROOT.TClonesArray):
            return sum(1 for mf_hit in mf_hits if mf_hit.GetSystem() == 3)
        elif isinstance(event, ROOT.TChain):
            return sum(1 for mf_hit in event.Digi_MuFilterHits if mf_hit.GetSystem() == 3)
        else: raise ValueError("Insufficient input parameters provided.")

    else: raise ValueError(f"Invalid track type: {tt}.")


def thereIsAMuon(
    mcEvent: ROOT.TChain
) -> bool:
    for mcTrack in mcEvent.MCTrack:
        if abs(mcTrack.GetPdgCode()) == 13:
            return True
    return False



def sfTrackIsReconstructible(
    mcEvent: ROOT.TChain
) -> dict:
    nMCPoints = {
        'h': {1:0, 2:0, 3:0, 4:0, 5:0},
        'v': {1:0, 2:0, 3:0, 4:0, 5:0}
    }

    nScifiPoints = {'h': 0, 'v': 0}
    nDSPoints    = {'h': 0, 'v': 0}

    for mcPoint in mcEvent.ScifiPoint:
        if not (
            abs(mcPoint.PdgCode()) == 13 and
            mcPoint.GetTrackID() == 0
        ): continue

        detID = mcPoint.GetDetectorID()

        # Checking for reconstructibility of SciFi tracks

        # Second digit:
        #   - type of the plane:
        #       - 0: Horizontal fiber plane
        #       - 1: Vertical fiber plane
        if int( (detID/100000)%2 ) == 0:
            nMCPoints['h'][int(detID/1e+6)]+=1
        elif int( (detID/100000)%2 ) == 1:
            nMCPoints['v'][int(detID/1e+6)]+=1

        for sfPlane in range(1, len(nMCPoints['v'])+1):
            if nMCPoints['v'][sfPlane]>0:
                nScifiPoints['v']+=1

            if nMCPoints['h'][sfPlane]>0:
                nScifiPoints['h']+=1

    if (nScifiPoints['h'] >= 3 and nScifiPoints['v'] >= 3):
        return True
    else:
        return False



def dsTrackIsReconstructible(
    mcEvent: ROOT.TChain
) -> dict:
    nMCPoints = {
        'h': {1:0, 2:0, 3:0, 4:0},
        'v': {1:0, 2:0, 3:0, 4:0}
    }
    nDSPoints = {'h': 0, 'v': 0}

    for mcPoint in mcEvent.MuFilterPoint:
        if (
            abs(mcPoint.PdgCode())==13 and
            mcPoint.GetTrackID()==0
        ):
            detID = mcPoint.GetDetectorID()
            if detID < 30000: continue

            if detID%1000 > 59:
                nMCPoints['v'][int(detID/1000) % 10 + 1] += 1
            else:
                nMCPoints['h'][int(detID/1000) % 10 + 1] += 1


        for dsPlane in range(1, 5):
            if nMCPoints['v'][dsPlane] > 0: nDSPoints['v'] += 1
            if nMCPoints['h'][dsPlane] > 0: nDSPoints['h'] += 1

    if (nDSPoints['h'] >= 3 and nDSPoints['v'] >= 3):
        return True
    else:
        return False

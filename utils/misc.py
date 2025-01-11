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

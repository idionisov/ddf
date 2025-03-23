import re, os, json, time
import ROOT
import glob
import numpy as np
import pandas as pd
import datetime
from typing import Union
from ddfUtils import getSubDirPath, getAllFiles

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



def getFill(run: int, jsonFile: str = "/eos/user/i/idioniso/1_Data/sndRuns.json"):
    def getFillFromJson(
        run: int,
        jsonFile: str = "/eos/user/i/idioniso/1_Data/sndRuns.json"
    ):
        run = str(run)
        with open(jsonFile, "r") as f:
            data = json.load(f)
        return data.get(run)

    fill = getFillFromJson(run, jsonFile)
    if fill is None:
        def getFillFromRoot(run: int):
            year = getRunYear(run)
            if year==2024:
                rootDir =  "/eos/experiment/sndlhc/convertedData/physics/2024/run_2412"
            else:
                rootDir = f"/eos/experiment/sndlhc/convertedData/physics/{year}"
            dataDir = f"{rootDir}/run_{run:06d}"

            try:
                file_ = getAllFiles(dataDir, "*.root")[0]
                tfile = ROOT.TFile.Open(file_)
            except Exception as e:
                raise ValueError(f"Error opening file: {e}")
                return None

            if tfile.Get("cbmsim"):
                ttree = tfile.Get("cbmsim")
            elif tfile.Get("rawConv"):
                ttree = tfile.Get("rawConv")
            else:
                raise ValueError("No tree found")
                return None

            try:
                ttree.GetEntry(0)
                return int(ttree.EventHeader.GetFillNumber())
            except Exception as e:
                raise ValueError(f"Error accessing data: {e}")
                return None

        fill = getFillFromRoot(run)

    if fill is None:
        raise ValueError(f"Fill number not found for run {run}")
    else:
        return fill





def getRuns(year: int):
    if year==2024:
        path = "/eos/experiment/sndlhc/convertedData/physics/2024/run_2412"
        runs = [int(re.search(r'run_(\d+)', d).group(1)) for d in os.listdir(path) if re.match(r'run_\d+', d)]
        return runs

    path = f"/eos/experiment/sndlhc/convertedData/physics/{year}"
    runs = [int(re.search(r'run_(\d+)', d).group(1)) for d in os.listdir(path) if re.match(r'run_\d+', d)]
    return runs


def getRunYear(run: int) -> int:
    yi = 2022
    yf = datetime.date.today().year

    for y in range(yi, yf+1):
        runs = getRuns(y)

        if run in runs:
            return y

    raise ValueError(f"Run {run} was not found!")


def getRunDirectory(run: int) -> str:
    year = getRunYear(run)
    if year == 2024:
        path = f"/eos/experiment/sndlhc/convertedData/physics/2024/run_2412/run_{run:06d}"
    else:
        path = f"/eos/experiment/sndlhc/convertedData/physics/{year}/run_{run:06d}"
    return path


def getRunFiles(run: int):
    runDir = getRunDirectory(run)

    rootFiles = glob.glob(
        os.path.join(runDir, "sndsw_raw-*.root")
    )
    return rootFiles


def getRunEntries(run: int) -> int:
    dir = getRunDirectory(run)
    tree = ROOT.TChain("cbmsim")
    tree.Add(f"{dir}/sndsw_raw-*.root")

    nEntries = tree.GetEntries()
    if nEntries == 0:
        tree = ROOT.TChain("rawConv")
        tree.Add(f"{dir}/sndsw_raw-*.root")
        nEntries = tree.GetEntries()

    return nEntries




def getLumiEos(run: int) -> float:
    def makeUnixTime(year, month, day, hour, minute, second) :
        dt = datetime.datetime(year, month, day, hour, minute, second)
        return time.mktime(dt.timetuple())

    atlas_online_lumi = ROOT.TChain("atlas_lumi")

    fill = getFill(run)

    input_dir = "/eos/experiment/sndlhc/atlas_lumi"
    atlas_online_lumi.Add(f"{input_dir}/fill_{fill:06d}.root")

    delivered_inst_lumi = []
    delivered_unix_timestamp = []
    delivered_run_number = []
    delivered_fill_number = []
    fill = 0

    for entry in atlas_online_lumi :
        delivered_inst_lumi.append(entry.var)
        delivered_unix_timestamp.append(entry.unix_timestamp)

    recorded_mask = np.array(True)
    delivered_inst_lumi = np.array(delivered_inst_lumi)
    delivered_unix_timestamp = np.array(delivered_unix_timestamp)

    delivered_deltas = delivered_unix_timestamp[1:] - delivered_unix_timestamp[:-1]
    delivered_mask = delivered_deltas < 600

    delivered_run = np.logical_and(delivered_unix_timestamp[1:] > fill, delivered_mask)


    return np.cumsum(
        np.multiply(
            delivered_deltas[delivered_run], delivered_inst_lumi[1:][delivered_run]
        )
    )[-1]/1e3


def getLumiSupertable(run: int) -> float:
    runYear = getRunYear(run)
    fill = getFill(run)

    supertable = f"/eos/user/i/idioniso/1_Data/supertable{runYear}.csv"
    st = pd.read_csv(supertable)
    st['ATLAS Int. Lumi [1/nb]'] = st['ATLAS Int. Lumi [1/nb]'].astype(float)
    st['Fill'] = st['Fill'].astype(int)

    lumi = st.loc[st['Fill'] == fill, 'ATLAS Int. Lumi [1/nb]'].values[0]
    return lumi

def getLumi(run: int, option: str = "eos") -> float:
    if option.lower() in ["eos"]:
        return getLumiEos(run)
    elif option.lower() in ["supertable", "st"]:
        return getLumiSupertable(run)
    else:
        raise ValueError(f"Invalid option: {option}")



def getRunTimestamp(run: int, fromRoot: bool):
    def getRunTimestampFromRoot(run: int):
        dir = getRunDirectory(run)
        tree = ROOT.TChain("cbmsim")
        tree.Add(f"{dir}/sndsw_raw-*.root")

        if tree.GetEntries() == 0:
            raise ValueError(f"No root files found for run {run}")

        tree.GetEntry(0)
        return tree.EventHeader.GetUTCtimestamp()

    if fromRoot:
        return getRunTimestampFromRoot(run)
    else:
        fill = getFill(run)
        year = getRunYear(run)
        supertable = f"/eos/user/i/idioniso/1_Data/supertable{year}.csv"
        if os.path.exists(supertable):
            st = pd.read_csv(supertable)

            if fill in st['Fill'].values:
                timestamp = st.loc[st['Fill'] == fill, 'Fill Start']
                return int(timestamp.iloc[0])/1e3
            return None
        else:
            dir = getRunDirectory(run)
            tree = ROOT.TChain("cbmsim")
            tree.Add(f"{dir}/sndsw_raw-*.root")

            if tree.GetEntries() == 0:
                raise ValueError(f"No root files found for run {run}")

            tree.GetEntry(0)
            return tree.EventHeader.GetUTCtimestamp()


def getRunDateFromRoot(run: int):
    year = getRunYear(run)

    inputDir = f"/eos/experiment/sndlhc/convertedData/physics/{year}/run_{run:06d}"
    try:
        tfile = ROOT.TFile.Open(f"{inputDir}/sndsw_raw-0000.root")
    except Exception as e:
        print(f"Error opening file: {e}")
        return None
    if tfile.Get("cbmsim"):
        ttree = tfile.Get("cbmsim")
    elif tfile.Get("rawConv"):
        ttree = tfile.Get("rawConv")
    else:
        raise ValueError("No tree of name cbmsim/rawConv was found!")

    try:
        ttree.GetEntry(0)
        utc_timestamp = ttree.EventHeader.GetUTCtimestamp()
        date_ = datetime.datetime.utcfromtimestamp(utc_timestamp)
        return date_
    except Exception as e:
        print(f"Error accessing data: {e}")
        return None

def getRunDateFromSupertable(run: int):
    return datetime.datetime.fromtimestamp(getRunTimestamp(run), tz=datetime.timezone.utc)

def getRunDate(run: int, option: str = "st"):
    if option.lower() in ["st", "supertable"]:
        return getRunDateFromSupertable(run)
    elif option.lower() in ["eos", "root"]:
        return getRunDateFromRoot(run)
    else:
        raise ValueError(f"Invalid option: {option}")

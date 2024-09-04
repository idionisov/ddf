from subprocess import run
from typing import Callable
from time import time
from ddf.pyfuncs import print_status_with_time
from ROOT import SNDLHCEventHeader, TChain, TClonesArray, TGraphAsymmErrors, TEfficiency
import numpy as np
import roostyling

def get_snd_year(snd_run: int) -> int:
    '''
    Get the year that corresponds to an SND@LHC run.
    '''
    return int(run(['get_run_year', f'{snd_run}'], capture_output=True).stdout.decode('utf-8'));

def get_snd_years(snd_runs: list) -> dict:
    '''
    Provided with a list of SND@LHC runs, returns a dictionary
    whose keys are those runs and whose values are the years
    that correspond to them.
    '''

    years = {}
    for snd_run in snd_runs:
        years[snd_run] = get_snd_year(snd_run)

    return years

def get_station(Z: float) -> int:
    '''
    Returns the SciFi or DS station (beggining at 0)
    of a hit/cluster given its Z coordinate.
    '''

    if   Z > 285 and Z < 306:   return 0
    elif Z > 306 and Z < 320:   return 1
    elif Z > 320 and Z < 333:   return 2
    elif Z > 333 and Z < 346:   return 3
    elif Z > 346 and Z < 360:   return 4

    elif Z > 485 and Z < 505:   return 0
    elif Z > 505 and Z < 530:   return 1
    elif Z > 530 and Z < 550:   return 2

    else: return -999


def get_event_bunch_structure(
    event_header: SNDLHCEventHeader
) -> dict:
    '''
    Get a dictionary of the bunch structure of an SNDLHCEventHeader.
    '''

    bunch_structure = {'IP1': False, 'IP2': False, 'B1':  False, 'B2':  False, 'B1Only': False, 'B2noB1': False}

    if event_header.isIP1():    bunch_structure['IP1']    = True
    if event_header.isIP2():    bunch_structure['IP2']    = True
    if event_header.isB1():     bunch_structure['B1']     = True
    if event_header.isB2():     bunch_structure['B2']     = True
    if event_header.isB1Only(): bunch_structure['B1Only'] = True
    if event_header.isB2noB1(): bunch_structure['B2noB1'] = True

    return bunch_structure

def init_input_files(
    snd_runs = [7080],
    selection: str = "*"
) -> dict:
    '''
    Initialize the input files for every run (Data only).
    Returns a dictionary containing all directories containing the files
    for the corresponding snd run.
    '''

    input_files = {}
    years = {}
    for run in snd_runs:
        years[run] = get_snd_year(run)
        input_files[run] = f"$SND_DATA/{years[run]}/run_{run:06d}/1_Tracks/{selection}.root"

    return input_files


def init_cbmsim_data(
    input_files: dict,
) -> dict:
    '''
    Initialize the TTree/TChain for every run (Data only).
    Returns two dictionaries:
    - First, the dictionary containing the TTree/TChain objects;
    - Second, the dictionary containing the number of their entries.
    '''

    cbmsim = {}
    nentries = {}
    for k in input_files.keys():

        if isinstance(k, int):
            cbmsim[k] = TChain('cbmsim')
            cbmsim[k].Add(input_files[k])
            nentries[k] = cbmsim[k].GetEntries()

            print(f" >> Run {k} events:\t{nentries[k]:,}")

    return cbmsim, nentries


def init_cbmsim_mc_PbPb(
    mc_factors: dict = {
        'EMD': 0.1388888888888889,
        'NI':  2.003205128205128
    }
):
    '''
    Initialize the TTree/TChain for Ion collision Monte Carlo.
    Returns one dictionary and one integer:
    - First, the dictionary containing the TTree/TChain objects of both mc types;
    - Second, the number of entries in the dataset.
    '''

    mc_types = list(mc_factors.keys())

    input_files = {}
    cbmsim      = {}
    nentries    = 0

    for mc_type in mc_types:
        input_files[mc_type] = f"$SND_MC/muonReco_MC-{mc_type}_PbPb.root"

        cbmsim[mc_type] = TChain('cbmsim')
        cbmsim[mc_type].Add(input_files[mc_type])

        nentries += cbmsim[mc_type].GetEntries()

    print(f" >> Monte Carlo (PbPb) events:\t{nentries:,}")

    return cbmsim, nentries

def init_cbmsim_mc_pp():
    '''
    Initialize the TTree/TChain for Proton collision Monte Carlo.
    Returns one TChain and one integer:
    - First, the TChain object of the dataset;
    - Second, the number of entries in the dataset.
    '''

    input_files = "$SND_MC/muonReco_MC_pp.root"

    cbmsim = TChain('cbmsim')
    cbmsim.Add(input_files)

    nentries = cbmsim.GetEntries()

    print(f" >> Monte Carlo (pp) events:\t{nentries:,}")

    return cbmsim, nentries



def get_N(
    track_type:  int,
    event:       TChain | None = None,
    sf_hits:     TClonesArray | None = None,
    sf_clusters: TClonesArray | None = None,
    mf_hits:     TClonesArray | None = None,
    mf_clusters: TClonesArray | None = None
) -> int:
    '''
    Get the number of Scifi/DS hits/clusters depending on the track type provided.
    '''

    if track_type==1:
        if isinstance(sf_clusters, TClonesArray):
            return sf_clusters.GetEntries()
        elif isinstance(event, TChain): return event.Cluster_Scifi.GetEntries()
        else: raise ValueError("Insufficient input parameters provided.")
    
    elif track_type==11:
        if isinstance(sf_hits, TClonesArray): return sf_hits.GetEntries()
        elif isinstance(event, TChain): return event.Digi_ScifiHits.GetEntries()
        else: raise ValueError("Insufficient input parameters provided.")
            
    elif track_type==3:
        if isinstance(mf_clusters, TClonesArray):
            return mf_clusters.GetEntries()
        elif isinstance(event, TChain):
            return event.Cluster_Mufi.GetEntries()
        else: raise ValueError("Insufficient input parameters provided.")
    
    elif track_type==13:
        if isinstance(mf_hits, TClonesArray):
            return sum(1 for mf_hit in mf_hits if mf_hit.GetSystem() == 3)
        elif isinstance(event, TChain):
            return sum(1 for mf_hit in event.Digi_MuFilterHits if mf_hit.GetSystem() == 3)
        else: raise ValueError("Insufficient input parameters provided.")
    
    else: raise ValueError("The track type is invalid.")
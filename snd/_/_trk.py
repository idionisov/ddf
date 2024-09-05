import numpy as np

xy_full_range: dict = {
    'min': {'x': -70, 'y': -5},
    'max': {'x':  10, 'y': 75}
}

xy_eff_range = {
    'min': {'x': -43, 'y': 18},
    'max': {'x': -10, 'y': 50}
}

track_types = (1, 3, 11, 13)

def sys(track_type: int) -> str:
    '''
    For each track type, returns the corresponding detector subsystem as string abbreviation.
    '''
    if   track_type==1 or track_type==11: return 'sf'
    elif track_type==3 or track_type==13: return 'ds'
    else: raise ValueError(f"{track_type} is an invalid track type!")

def sys_name(track_type: int) -> str:
    '''
    For each track type, returns the corresponding detector subsystem's full name.
    '''

    if   track_type==1 or track_type==11: return 'Scifi'
    elif track_type==3 or track_type==13: return 'DS'
    else: raise ValueError(f"{track_type} is an invalid track type!")


def alg(track_type: int) -> str:
    '''
    For each track type, returns the corresponding tracking algorithm as an abbreviation.
    '''

    if   track_type==1  or track_type==3:  return 'st'
    elif track_type==11 or track_type==13: return 'ht'
    else: raise ValueError(f"{track_type} is an invalid track type!")


def alg_name(track_type: int) -> str:
    '''
    For each track type, returns the corresponding tracking algorithm's name.
    '''

    if   track_type==1  or track_type==3:  return 'simple tracking'
    elif track_type==11 or track_type==13: return 'Hough transform'
    else: raise ValueError(f"{track_type} is an invalid track type!")

def n_type(track_type: int) -> str:
    '''
    Returns the building blocks (hits/clusters) for a given track type.
    '''

    if   track_type==1  or track_type==3:  return 'clusters'
    elif track_type==11 or track_type==13: return 'hits'
    else: raise ValueError(f"{track_type} is an invalid track type!")

def n_name(track_type: int) -> str:
    '''
    Returns the building blocks (hits/clusters) for a given track type.
    '''

    if   track_type == 1:  return 'Scifi clusters'
    elif track_type == 11: return 'Scifi hits'
    elif track_type == 3:  return 'DS clusters'
    elif track_type == 13: return 'DS hits'
    else: raise ValueError(f"{track_type} is an invalid track type!")


class range_tt:
    def __init__(self, min: dict, max: dict):
        self.min = min
        self.max = max

n_range = range_tt(
    min = {1: 5,  11: 5,   3: 5,  13: 5},
    max = {1: 55, 11: 125, 3: 20, 13: 60}
)

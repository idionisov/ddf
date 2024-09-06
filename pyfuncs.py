from typing import Union
from time import time
from datetime import datetime
from scipy.stats import norm
from ._._pyfuncs import _clopper_pearson_interval, _bayesian_interval

def get_cl_sigma(sigma: int = 1) -> float:
    """
    Args:
        σ (int): Number of standard deviations of confidence level.

    Returns:
        CL (float): The confidence level as a float from 0 to 1. 
    """
    return 2 * norm.cdf(sigma) - 1

def get_current_dmy():
    day   = datetime.now().day
    month = datetime.now().month
    year  = datetime.now().year
    return day, month, year


def dicts_have_the_same_structure(
    dict1: dict,
    dict2: dict
) -> bool:
    if dict1.keys() != dict2.keys():
        return False
    
    for key in dict1:
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            if not dicts_have_the_same_structure(dict1[key], dict2[key]):
                return False
        else:
            if type(dict1[key]) != type(dict2[key]):
                return False
    return True


def get_eff_with_error(
    passed:           Union[int, float],
    total:            Union[int, float],
    stat_option:      str   = "kfcp",
    confidence_level: float = 0.6826894921370859
):
    stat_option = stat_option.lower()
    
    clopper_pearson_options = {"clopper_pearson", "kfcp", "clopper pearson", 
                               "clopper-pearson", "clopper.pearson", 
                               "clopper:pearson", "clopperpearson"}
    bayesian_options = {"bayesian", "kbbayesian"}
    allowed_options = clopper_pearson_options.join(bayesian_options)    

    if stat_option in clopper_pearson_options:
        eff, deff_up, deff_low = _clopper_pearson_interval(passed, total, confidence_level=confidence_level)
    elif stat_option in {"bayesian", "kbbayesian"}:
        eff, deff_up, deff_low = _bayesian_interval(passed, total, confidence_level=confidence_level)
    else: raise ValueError(f"Invalid statistic option '{stat_option}'! Allowed options are: {', '.join(allowed_options)}")

    return eff, deff_up, deff_low




def get_sec_as_hms(duration: float) -> tuple:
    hours   = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = (duration % 3600) % 60
    
    return hours, minutes, seconds


def get_axi_axj(i: int, ncols: int):
    
    ax_i=i//ncols
    ax_j=i%ncols

    return ax_i, ax_j


def print_status_with_time(i, iMax, start_time):
    '''
    Given an entry index, number of entries and start time,
    prints the progress percentage and elapsed time
    since the start of the loop.
    '''

    if i<0 or iMax<0:
        raise ValueError("Only positive numbers of current entry and total number of entries are allowed!")

    if iMax==0:
        raise ValueError("Total number of entries shouldn't be zero!")


    elapsed_time = time() - start_time
    percent = i*100/iMax
    
    h, m, s = get_sec_as_hms(elapsed_time)
    
    out1 = "\r\033[1;31m >>"
    out2 = f"{out1} \033[1;32m [".rjust(5) + f"{percent:.02f}".zfill(5) + "%]\033[0m".ljust(13)
    out3 = f"{i+1:,}/{iMax:,}".ljust(25)
    out4 = "\033[1;34m" + f"{h:02d}:{m:02d}:{round(s):02d}\033[0m"
    out5 = " (hh:mm:ss)"
    out  = out1 + out2 + out3 + out4 + out5

    if i+1 != iMax: print(out,        flush=True, end=" ")
    else:           print(f"{out}\n", flush=True, end="\n")



def print_status(i, iMax, start_time: float, count: int = 0) -> int:
    '''
    Given an entry index, number of entries, start time and a count number,
    prints the progress percentage and elapsed time if a second has passed
    since the previous count increment.
    '''

    if (time() - start_time > count):
        print_status_with_time(i, iMax, start_time)
        count += 1
    elif (i == iMax-1):
        print_status_with_time(i, iMax, start_time)

    return count

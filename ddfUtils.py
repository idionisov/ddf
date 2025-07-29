import os, glob
import numpy as np
from time import time
from typing import Union
from scipy.stats import beta, norm
from scipy.optimize import root_scalar


def getSubDirPath(
    TopDir:  str,
    RootDir: str = "/eos/experiment/sndlhc/convertedData/physics"
):
    """
    Return a list of full paths to subdirectories named `TopDir`,
    starting from `root_path`.
    """

    matchingDirs = []
    for dirpath, dirnames, _ in os.walk(RootDir):
        if os.path.basename(dirpath) == TopDir:
            matchingDirs.append(dirpath)
    return matchingDirs

def getAllFiles(inputDir: str, files: str) -> list:
    """
    Get list of all files matching pattern in a directory.

    Args:
        inputDir: Directory path to search in
        files: File pattern to match

    Returns:
        list: List of files matching the pattern
    """
    return glob.glob(f"{inputDir}/{files}")



def getSecAsHMS(duration: float) -> tuple:
    """
    Convert seconds to hours, minutes, seconds.

    Args:
        duration: Time duration in seconds

    Returns:
        tuple: (hours, minutes, seconds)
    """
    hours   = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = (duration % 3600) % 60

    return hours, minutes, seconds




def printStatusWithTime(i, iMax, start_time):
    """
    Print status with elapsed time in formatted output.

    Args:
        i: Current iteration number
        iMax: Maximum number of iterations
        start_time: Start time of process

    Raises:
        ValueError: If i or iMax are negative, or if iMax is zero
    """
    if i<0 or iMax<0:
        raise ValueError("Only positive numbers of current entry and total number of entries are allowed!")

    if iMax==0:
        raise ValueError("Total number of entries shouldn't be zero!")


    elapsed_time = time() - start_time
    percent = i*100/iMax

    h, m, s = getSecAsHMS(elapsed_time)

    out1 = "\r\033[1;31m >>"
    out2 = f"{out1} \033[1;32m [".rjust(5) + f"{percent:.02f}".zfill(5) + "%]\033[0m".ljust(13)
    out3 = f"{i+1:,}/{iMax:,}".ljust(25)
    out4 = "\033[1;34m" + f"{h:02d}:{m:02d}:{round(s):02d}\033[0m"
    out5 = " (hh:mm:ss)"
    out  = out1 + out2 + out3 + out4 + out5

    if i+1 != iMax: print(out,        flush=True, end=" ")
    else:           print(f"{out}\n", flush=True, end="\n")

def printStatus(i, iMax, start_time: float, count: int = 0) -> int:
    """
    Print periodic status updates.

    Args:
        i: Current iteration number
        iMax: Maximum number of iterations
        start_time: Start time of process
        count: Counter for controlling update frequency

    Returns:
        int: Updated count value
    """
    if (time() - start_time > count):
        printStatusWithTime(i, iMax, start_time)
        count += 1
    elif (i == iMax-1):
        printStatusWithTime(i, iMax, start_time)

    return count





def getClopperPearsonInterval(
    passed: int,
    total: int,
    cl: float = 0.6826894921370859
) -> tuple:
    """
    Calculate Clopper-Pearson confidence interval for binomial proportion.

    Args:
        passed: Number of successes
        total: Total number of trials
        cl: Confidence level (default is 1-sigma)

    Returns:
        tuple: (efficiency, upper error, lower error)
    """
    efficiency = passed/total

    alpha = 1 - cl
    lower_bound = beta.ppf(alpha / 2, passed, total - passed + 1)
    upper_bound = beta.ppf(1 - alpha / 2, passed + 1, total - passed)

    return efficiency, abs(efficiency - upper_bound), abs(efficiency - lower_bound)




def getBayesianInterval(
    passed:      Union[float, int],
    total:       Union[float, int],
    alpha_prior: float = 1,
    beta_prior:  float = 1,
    cl:          float = 0.6826894921370859
) -> tuple:
    """
    Calculate Bayesian confidence interval for binomial proportion.

    Args:
        passed: Number of successes
        total: Total number of trials
        alpha_prior: Prior alpha parameter for beta distribution
        beta_prior: Prior beta parameter for beta distribution
        cl: Confidence level (default is 1-sigma)

    Returns:
        tuple: (efficiency, upper error, lower error)
    """
    alpha_post = alpha_prior + passed
    beta_post = beta_prior + total - passed

    lower_bound = beta.ppf((1 - cl) / 2, alpha_post, beta_post)
    upper_bound = beta.ppf(1 - (1 - cl) / 2, alpha_post, beta_post)
    efficiency = passed/total

    return efficiency, abs(efficiency - upper_bound), abs(efficiency - lower_bound)



def getEffWithError(
    passed:      Union[int, float],
    total:       Union[int, float],
    statOption:  str   = "Clopper Pearson",
    cl:          float = 0.6826894921370859
) -> tuple:
    """
    Calculate efficiency and errors using specified statistical method.

    Args:
        passed: Number of successes
        total: Total number of trials
        statOption: Statistical method to use ('Clopper Pearson' or 'Bayesian')
        cl: Confidence level (default is 1-sigma)

    Returns:
        tuple: (efficiency, upper error, lower error)

    Raises:
        ValueError: If invalid statistical method is specified
    """
    statOption = statOption.lower()

    clopper_pearson_options = {"clopper_pearson", "kfcp", "clopper pearson",
                               "clopper-pearson", "clopper.pearson",
                               "clopper:pearson", "clopperpearson"}
    bayesian_options = {"bayesian", "kbbayesian"}
    allowed_options = clopper_pearson_options | bayesian_options  # Combine sets using union operator

    if statOption in clopper_pearson_options:
        eff, deff_up, deff_low = getClopperPearsonInterval(passed, total, cl=cl)
    elif statOption in bayesian_options:  # Use bayesian_options directly here
        eff, deff_up, deff_low = getBayesianInterval(passed, total, cl=cl)
    else:
        raise ValueError(f"Invalid statistic option '{statOption}'! Allowed options are: {', '.join(allowed_options)}")

    return eff, deff_up, deff_low



def getArrayCenters(array, round: int = 2):
    array = np.array(array, dtype=np.float64)
    return np.round(0.5 * (array[:-1] + array[1:]), round)






def getSystematicVarianceChi2Method(x, statVariances, sysVariances):
    x = np.asarray(x)
    N = len(x)
    statVariances = np.asarray(statVariances)
    sysVariances = np.asarray(sysVariances)

    xVar = statVariances + sysVariances


    def getChi2(s):
        if s < 0:
            return np.inf
        varTotal = xVar + s**2
        weights = 1 / varTotal
        xHat = np.sum(x * weights) / np.sum(weights)
        return np.sum((x - xHat)**2 / varTotal) - (N - 1)


    sMax = np.std(x) * 10 + 0.01
    chiLow = getChi2(1e-10)
    chiHigh = getChi2(sMax)

    if chiLow * chiHigh > 0:
        return 0.0

    result = root_scalar(getChi2, bracket=[1e-10, sMax], method='brentq')
    if not result.converged:
        raise RuntimeError("Root finding did not converge.")

    return result.root**2




def getFluxWithAllVariances(
    fluxes, fluxStatVars, fluxSysLVars, fluxSysEffVars, rhoL: float = 0, rhoEff: float = 0.8
):
    fluxes = np.asarray(fluxes)
    N = len(fluxes)

    fluxStatVars = np.asarray(fluxStatVars)
    fluxSysLVars = np.asarray(fluxSysLVars)
    fluxSysEffVars = np.asarray(fluxSysEffVars)

    fluxStatSigmas = np.sqrt(fluxStatVars)
    fluxSysLSigmas = np.sqrt(fluxSysLVars)
    fluxSysEffSigmas = np.sqrt(fluxSysEffVars)

    # Combine systematic variances
    fluxSysVars = fluxSysLVars + fluxSysEffVars
    fluxSysSigmas = np.sqrt(fluxSysVars)

    # Construct total covariance matrix
    covMat = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            cov = 0.0
            if i == j:
                cov = fluxStatVars[i] + fluxSysVars[i]
            else:
                cov += rhoEff * fluxSysEffSigmas[i] * fluxSysEffSigmas[j]
                cov += rhoL   * fluxSysLSigmas[i] * fluxSysLSigmas[j]
            covMat[i, j] = cov

    covMatInv = inv(covMat)

    ones = np.ones(N)
    meanFlux = (ones @ covMatInv @ fluxes) / (ones @ covMatInv @ ones)
    fluxVar = 1 / (ones @ covMatInv @ ones)

    chi2 = (fluxes - meanFlux) @ covMatInv @ (fluxes - meanFlux)
    pVal = 1 - chi2_dist.cdf(chi2, df=N - 1)

    def f(s2):
        denom = fluxStatVars + fluxSysVars + s2
        weighted_mean = np.sum(fluxes / denom) / np.sum(1 / denom)
        return np.sum(((fluxes - weighted_mean)**2) / denom) - (N - 1)

    try:
        sysMethodVar = brentq(f, 0, 1e10)
    except ValueError:
        sysMethodVar = 0.0

    return {
        "flux": meanFlux,
        "stat": fluxVar,
        "sysL": np.max(fluxSysLVars),
        "sysEff": np.max(fluxSysEffVars),
        "sysMethod": sysMethodVar
    }, {
        "chi2": chi2,
        "pVal": pVal
    }

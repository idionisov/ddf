import os, glob
from time import time

def getSubDirPath(
    TopDir:  str,
    RootDir: str = "/eos/experiment/sndlhc/convertedData/physics",
) -> str:
    for dirPath, dirNames, fileNames in os.walk(RootDir):
        if TopDir in dirNames:
            return os.path.join(dirPath, TopDir)
        else:
            raise ValueError(f"No subdirectory '{TopDir}' was found in {RootDir}!")

def getAllFiles(inputDir: str, files: str) -> list:
    return glob.glob(f"{inputDir}/{files}")



def getSecAsHMS(duration: float) -> tuple:
    hours   = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = (duration % 3600) % 60

    return hours, minutes, seconds




def printStatusWithTime(i, iMax, start_time):
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
    if (time() - start_time > count):
        printStatusWithTime(i, iMax, start_time)
        count += 1
    elif (i == iMax-1):
        printStatusWithTime(i, iMax, start_time)

    return count

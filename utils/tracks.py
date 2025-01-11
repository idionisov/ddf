def att(tt: int) -> int:
    if   tt==1:  return 3
    elif tt==3:  return 1
    elif tt==11: return 13
    elif tt==13: return 11
    else: raise ValueError(f"{tt} is an invalid track type!")

def sys(tt: int) -> str:
    if   tt==1 or tt==11: return "sf"
    elif tt==3 or tt==13: return "ds"
    else:  raise ValueError(f"{tt} is an invalid track type!")

def alg(tt: int) -> str:
    if   tt==1  or tt==3:  return "st"
    elif tt==11 or tt==13: return "ht"
    else:  raise ValueError(f"{tt} is an invalid track type!")

def system(tt: int) -> str:
    if   tt==1 or tt==11: return "Scifi"
    elif tt==3 or tt==13: return "DS"
    else:  raise ValueError(f"{tt} is an invalid track type!")

def algorithm(tt: int) -> str:
    if   tt==1  or tt==3:  return "simple tracking"
    elif tt==11 or tt==13: return "Hough transform"
    else:  raise ValueError(f"{tt} is an invalid track type!")

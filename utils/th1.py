from ROOT import TH1, TH2, TH3

def isTH1(obj):
    if isinstance(obj, TH1) and not isinstance(obj, (TH2, TH3)):
        return True
    else:
        return False


def isTH2(obj):
    if isinstance(obj, TH2) and not isinstance(obj, TH3):
        return True
    else:
        return False

import ROOT

def axes(*objects, 
    axesTitleSize:    float = 0.04, 
    XaxisOffset:      float = 1.25, 
    YaxisOffset:      float = 1.25, 
    centerAxesTitles: bool  = True
):
    for object in objects:
        object.GetXaxis().CenterTitle(centerAxesTitles)
        object.GetYaxis().CenterTitle(centerAxesTitles)

        object.GetXaxis().SetTitleSize(axesTitleSize)
        object.GetYaxis().SetTitleSize(axesTitleSize)

        object.GetXaxis().SetTitleOffset(XaxisOffset)
        object.GetYaxis().SetTitleOffset(YaxisOffset)

        if hasattr(object, 'GetZaxis'):
            object.GetZaxis().CenterTitle(centerAxesTitles)

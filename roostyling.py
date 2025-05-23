from typing import Union
import ROOT


def axes(
    *objects,
    axesTitleSize: float = 0.04,
    XaxisOffset: float = 1.25,
    YaxisOffset: float = 1.25,
    centerAxesTitles: bool = True
):
    for object in objects:
        object.GetXaxis().CenterTitle(centerAxesTitles)
        object.GetYaxis().CenterTitle(centerAxesTitles)

        object.GetXaxis().SetTitleSize(axesTitleSize)
        object.GetYaxis().SetTitleSize(axesTitleSize)

        object.GetXaxis().SetTitleOffset(XaxisOffset)
        object.GetYaxis().SetTitleOffset(YaxisOffset)

        if hasattr(object, "GetZaxis"):
            object.GetZaxis().CenterTitle(centerAxesTitles)


def setSndStyle():

    # for the canvas:
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
    ROOT.gStyle.SetCanvasDefH(600)
    ROOT.gStyle.SetCanvasDefW(600)
    ROOT.gStyle.SetCanvasDefX(10)
    ROOT.gStyle.SetCanvasDefY(10)

    ROOT.gStyle.SetPadBorderMode(0)
    ROOT.gStyle.SetPadColor(ROOT.kWhite)
    ROOT.gStyle.SetPadGridX(False)
    ROOT.gStyle.SetPadGridY(False)
    ROOT.gStyle.SetGridColor(0)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridWidth(1)

    # For the frame:
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetFrameBorderSize(1)
    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetFrameFillStyle(0)
    ROOT.gStyle.SetFrameLineColor(1)
    ROOT.gStyle.SetFrameLineStyle(1)
    ROOT.gStyle.SetFrameLineWidth(2)

    # For the histo:
    ROOT.gStyle.SetHistLineColor(ROOT.kBlue)
    ROOT.gStyle.SetHistLineStyle(0)
    ROOT.gStyle.SetHistLineWidth(2)

    ROOT.gStyle.SetEndErrorSize(2)

    ROOT.gStyle.SetMarkerStyle(20)

    # For the fit/function:
    ROOT.gStyle.SetOptFit(1)
    ROOT.gStyle.SetFitFormat("5.4g")
    ROOT.gStyle.SetFuncColor(2)
    ROOT.gStyle.SetFuncStyle(1)
    ROOT.gStyle.SetFuncWidth(1)

    # For the date:
    ROOT.gStyle.SetOptDate(0)

    # For the statistics box:
    ROOT.gStyle.SetOptFile(0)
    ROOT.gStyle.SetOptStat(0)  # To display the mean and RMS:   SetOptStat("mr")
    ROOT.gStyle.SetStatColor(ROOT.kWhite)
    ROOT.gStyle.SetStatFont(42)
    ROOT.gStyle.SetStatFontSize(0.025)
    ROOT.gStyle.SetStatTextColor(1)
    ROOT.gStyle.SetStatFormat("6.4g")
    ROOT.gStyle.SetStatBorderSize(1)
    ROOT.gStyle.SetStatH(0.1)
    ROOT.gStyle.SetStatW(0.15)

    # Margins:
    # ROOT.gStyle.SetPadTopMargin(0.05)
    # ROOT.gStyle.SetPadBottomMargin(0.15)
    # ROOT.gStyle.SetPadLeftMargin(0.15)
    # ROOT.gStyle.SetPadRightMargin(0.05)

    # For the Global title:

    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetTitleFont(42)
    ROOT.gStyle.SetTitleColor(1)
    ROOT.gStyle.SetTitleTextColor(1)
    ROOT.gStyle.SetTitleFillColor(10)
    ROOT.gStyle.SetTitleFontSize(0.05)

    # For the axis titles:

    ROOT.gStyle.SetTitleColor(1, "XYZ")
    ROOT.gStyle.SetTitleFont(42, "XYZ")
    ROOT.gStyle.SetTitleSize(0.06, "XYZ")
    ROOT.gStyle.SetTitleXOffset(1)
    ROOT.gStyle.SetTitleYOffset(1.25)

    # For the axis labels:

    ROOT.gStyle.SetLabelColor(1, "XYZ")
    ROOT.gStyle.SetLabelFont(42, "XYZ")
    ROOT.gStyle.SetLabelOffset(0.007, "XYZ")
    ROOT.gStyle.SetLabelSize(0.04, "XYZ")

    # For the axis:

    ROOT.gStyle.SetAxisColor(1, "XYZ")
    ROOT.gStyle.SetStripDecimals(True)
    ROOT.gStyle.SetTickLength(0.03, "XYZ")
    ROOT.gStyle.SetNdivisions(510, "XYZ")
    ROOT.gStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
    ROOT.gStyle.SetPadTickY(1)

    # Change for log plots:
    # ROOT.gStyle.SetOptLogx(0)
    # ROOT.gStyle.SetOptLogy(0)
    # ROOT.gStyle.SetOptLogz(0)

    # Legend options:
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetLegendTextSize(0.022)

    # Postscript options:
    # ROOT.gStyle.SetPaperSize(20.,26.)
    # ROOT.gStyle.SetHatchesLineWidth(5)
    # ROOT.gStyle.SetHatchesSpacing(0.05)


def addRootLabel(
    pad: Union[ROOT.TPad, ROOT.TCanvas, None],
    textFactor: float = 0.4,
    textOffset: float = 0.01,
    extraText: Union[str, None] = None,
    textIn: bool = True,
    rfrac: float = 0.0,
    mainText: str = "SND@LHC",
):
    if pad is None:
        pad = ROOT.gPad

    pad.Update()

    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()

    SNDTextSize = t * textFactor
    SNDTextVerticalOffset = textOffset

    pad.cd()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)

    latex.SetTextFont(61)
    latex.SetTextAlign(11)
    latex.SetTextSize(SNDTextSize)
    latex.SetText(0, 0, mainText)

    sndX = SNDTextSize * 2 * (1 - rfrac)

    if not textIn:
        latex.DrawLatex(l, 1 - t + SNDTextVerticalOffset, mainText)
    else:
        latex.DrawLatex(
            l + 0.03, 1 - t - SNDTextVerticalOffset - 1.2 * SNDTextSize, mainText
        )

    extraTextSize = SNDTextSize * 0.8
    latex.SetTextFont(52)
    latex.SetTextSize(extraTextSize)
    latex.SetTextAlign(11)
    if not textIn:
        latex.DrawLatex(l + 0.03 + 1.5 * sndX, 1 - t + SNDTextVerticalOffset, extraText)
    else:
        latex.DrawLatex(
            l + 0.03, 1 - t - SNDTextVerticalOffset - 2 * SNDTextSize, extraText
        )

    pad.Update()
    return



markers = {
    "ddf": [ROOT.kFullSquare, ROOT.kFullTriangleUp, ROOT.kFullCircle, ROOT.kFullDiamond, ROOT.kFullTriangleDown, ROOT.kFullCross]
}
linestyles = {
    "ddf": []
}

def setDdfpubStyle():

    # for the canvas:
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
    ROOT.gStyle.SetCanvasDefH(600)
    ROOT.gStyle.SetCanvasDefW(600)
    ROOT.gStyle.SetCanvasDefX(10)
    ROOT.gStyle.SetCanvasDefY(10)

    ROOT.gStyle.SetPadBorderMode(0)
    ROOT.gStyle.SetPadColor(ROOT.kWhite)
    ROOT.gStyle.SetPadGridX(False)
    ROOT.gStyle.SetPadGridY(False)
    ROOT.gStyle.SetGridColor(0)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridWidth(1)

    # For the frame:
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetFrameBorderSize(1)
    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetFrameFillStyle(0)
    ROOT.gStyle.SetFrameLineColor(1)
    ROOT.gStyle.SetFrameLineStyle(1)
    ROOT.gStyle.SetFrameLineWidth(2)

    # For the histo:
    ROOT.gStyle.SetHistLineColor(ROOT.kBlack)
    ROOT.gStyle.SetHistLineStyle(0)
    ROOT.gStyle.SetHistLineWidth(2)

    ROOT.gStyle.SetEndErrorSize(2)

    ROOT.gStyle.SetMarkerStyle(20)

    # For the fit/function:
    ROOT.gStyle.SetOptFit(1)
    ROOT.gStyle.SetFitFormat("5.4g")
    ROOT.gStyle.SetFuncColor(2)
    ROOT.gStyle.SetFuncStyle(1)
    ROOT.gStyle.SetFuncWidth(1)

    # For the date:
    ROOT.gStyle.SetOptDate(0)

    # For the statistics box:
    ROOT.gStyle.SetOptFile(0)
    ROOT.gStyle.SetOptStat(0)  # To display the mean and RMS:   SetOptStat("mr")
    ROOT.gStyle.SetStatColor(ROOT.kWhite)
    ROOT.gStyle.SetStatFont(42)
    ROOT.gStyle.SetStatFontSize(0.025)
    ROOT.gStyle.SetStatTextColor(1)
    ROOT.gStyle.SetStatFormat("6.4g")
    ROOT.gStyle.SetStatBorderSize(1)
    ROOT.gStyle.SetStatH(0.1)
    ROOT.gStyle.SetStatW(0.15)

    # Margins:
    # ROOT.gStyle.SetPadTopMargin(0.05)
    # ROOT.gStyle.SetPadBottomMargin(0.15)
    # ROOT.gStyle.SetPadLeftMargin(0.15)
    # ROOT.gStyle.SetPadRightMargin(0.05)

    # For the Global title:

    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetTitleFont(42)
    ROOT.gStyle.SetTitleColor(1)
    ROOT.gStyle.SetTitleTextColor(1)
    ROOT.gStyle.SetTitleFillColor(10)
    ROOT.gStyle.SetTitleFontSize(0.05)

    # For the axis titles:

    ROOT.gStyle.SetTitleColor(1, "XYZ")
    ROOT.gStyle.SetTitleFont(42, "XYZ")
    ROOT.gStyle.SetTitleSize(0.06, "XYZ")
    ROOT.gStyle.SetTitleXOffset(1)
    ROOT.gStyle.SetTitleYOffset(1.25)

    # For the axis labels:

    ROOT.gStyle.SetLabelColor(1, "XYZ")
    ROOT.gStyle.SetLabelFont(42, "XYZ")
    ROOT.gStyle.SetLabelOffset(0.007, "XYZ")
    ROOT.gStyle.SetLabelSize(0.04, "XYZ")

    # For the axis:

    ROOT.gStyle.SetAxisColor(1, "XYZ")
    ROOT.gStyle.SetStripDecimals(True)
    ROOT.gStyle.SetTickLength(0.03, "XYZ")
    ROOT.gStyle.SetNdivisions(510, "XYZ")
    ROOT.gStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
    ROOT.gStyle.SetPadTickY(1)

    # Change for log plots:
    # ROOT.gStyle.SetOptLogx(0)
    # ROOT.gStyle.SetOptLogy(0)
    # ROOT.gStyle.SetOptLogz(0)

    # Legend options:
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetLegendTextSize(0.022)

    # Postscript options:
    # ROOT.gStyle.SetPaperSize(20.,26.)
    # ROOT.gStyle.SetHatchesLineWidth(5)
    # ROOT.gStyle.SetHatchesSpacing(0.05)

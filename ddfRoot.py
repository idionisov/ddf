from typing import Union, Iterable
import re
import ROOT
import numpy as np
from utils.th1 import isTH1, isTH2, getNumpyFromTH2, getPandasFromUprootTH1
from utils.teff import getStatOption, setStatOption, getGraphFromTEff1D, \
    getGraphFromTEff2D, getTEff, getHistFromTEff2D
from utils.tgraph import getPandasFromTGraph, getPandasFromTGraph2D, \
    getPandasFromTGraphErrors, getPandasFromTGraphAsymmErrors
from utils.misc import getN





class DdfBaseEff:
    def __init__(self,
        StatOption: str,
        CL: float,
        Name: Union[str, None],
        Title: Union[str, None]
    ):
        self.StatOption = StatOption
        self.CL = CL
        self.Name = Name
        self.Title = Title
        self.TEfficiency = None

    def GetTEfficiency(self, Passed, Total):
        teff = ROOT.TEfficiency(Passed, Total)
        teff.SetConfidenceLevel(self.CL)
        setStatOption(teff, self.StatOption)
        if self.Name:   teff.SetName(self.Name)
        if self.Title:  teff.SetTitle(self.Title)
        return teff

    def Print(self):
        print("DDF Efficiency:")
        if self.Name:  print(f" > Name:             {self.Name}")
        if self.Title: print(f" > Title:            {self.Title}")
        print(f" > Confidence Level: {self.CL}")
        print(f" > Stat Option:      {self.StatOption}")




class DdfEff1D(DdfBaseEff):
    def __init__(self,
        Passed: Union[ROOT.TH1, None],
        Total: Union[ROOT.TH1, None],
        StatOption: str = "Clopper Pearson",
        CL: float = 0.682689,
        Name: Union[str, None] = None,
        Title: Union[str, None] = None
    ):
        if not (isTH1(Passed) and isTH1(Total) and type(Passed) == type(Total)):
            raise ValueError("Passed and Total histograms must be 1D and of the same type!")

        super().__init__(StatOption, CL, Name, Title)
        self.Passed = Passed
        self.Total = Total
        self.Dim = 1
        self.TEfficiency = self.GetTEfficiency(Passed, Total)


    def GetGraph(self) -> ROOT.TGraph:
        return getGraphFromTEff1D(self.TEfficiency, self.Name, self.Title)



class DdfEff2D(DdfBaseEff):
    def __init__(self,
        Passed: Union[ROOT.TH2, None],
        Total: Union[ROOT.TH2, None],
        StatOption: str = "Clopper Pearson",
        CL: float = 0.682689,
        Name: Union[str, None] = None,
        Title: Union[str, None] = None
    ):
        if not (isTH2(Passed) and isTH2(Total) and type(Passed) == type(Total)):
            raise ValueError("Passed and Total histograms must be 2D and of the same type!")

        super().__init__(StatOption, CL, Name, Title)
        self.Passed = Passed
        self.Total = Total
        self.Dim = 2
        self.TEfficiency = self.GetTEfficiency(Passed, Total)

    def GetGraph(self) -> ROOT.TGraph2D:
        return getGraphFromTEff2D(self.TEfficiency, self.Name, self.Title)


    def GetTH2(self) -> ROOT.TH2:
        return getHistFromTEff2D(self.TEfficiency, self.Name, self.Title)





class DdfEff:
    def __init__(self,
        Passed: Union[ROOT.TH2, ROOT.TH1, None] = None,
        Total: Union[ROOT.TH2, ROOT.TH1, None] = None,
        TEfficiency: Union[ROOT.TEfficiency, None] = None,
        StatOption: str = "Clopper Pearson",
        CL: float = 0.682689,
        Name: Union[str, None] = None,
        Title: Union[str, None] = None
    ):
        if TEfficiency:
            self.Passed = TEfficiency.GetPassedHistogram()
            self.Total = TEfficiency.GetTotalHistogram()
            self.Dim = TEfficiency.GetDimension()
            self.TEfficiency = TEfficiency
            self.Name = TEfficiency.GetName()
            self.Title = TEfficiency.GetTitle()

        elif Passed and Total:
            if isTH2(Passed) and isTH2(Total):
                self.impl = DdfEff2D(Passed, Total, StatOption, CL, Name, Title)
            elif isTH1(Passed) and isTH1(Total):
                self.impl = DdfEff1D(Passed, Total, StatOption, CL, Name, Title)
            else:
                raise ValueError("Passed and Total histograms must be of the same dimensionality and type!")

            self.__dict__.update(self.impl.__dict__)

        else:
            raise ValueError("Either TEfficiency or Passed/Total histograms must be provided!")




    def GetGraph(self):
        return self.impl.GetGraph()

    def GetTH2(self) -> ROOT.TH2:
        return getHistFromTEff2D(self.TEfficiency, self.Name, self.Title)

    def Print(self):
        print("DDF Efficiency:")
        if self.Name:  print(f" > Name:             {self.Name}")
        if self.Title: print(f" > Title:            {self.Title}")
        print(f" > Confidence Level: {self.CL}")
        print(f" > Stat Option:      {self.StatOption}")



def getTEffDict(
    hists: dict,
    statOption: str = 'normal',
    cl: float = 0.682689,
    suffix: str = "",
    asDdf: bool = True,
    teffs: dict = {}
) -> dict:

    for key in hists:
        if isinstance(hists[key], tuple):
            if len(hists[key]) != 2:
                raise ValueError("Tuple does not contain exactly two objects!")

            passed, total = hists[key]

            if not (isinstance(passed, ROOT.TH1) and isinstance(total, ROOT.TH1)):
                raise ValueError("The two objects in the tuple are not ROOT Histograms!")

            if type(passed) != type(total):
                raise ValueError("The two histograms are not of the same type!")


            name = passed.GetName()
            xTitle = passed.GetXaxis().GetTitle()

            if isTH1(passed):
                title = f";{xTitle};Efficiency"
            elif isTH2(passed):
                yTitle = passed.GetYaxis().GetTitle()
                title = f";{xTitle};{yTitle};Efficiency"
            else:
                raise ValueError("Histograms have to be one or two dimensional!")

            if re.match(r"h\d+_", name.lower()):
                name = f"eff_{name[3:]}"

            if suffix:
                name = f"{name}.{suffix}"

            if asDdf:
                teffs[key] = DdfEff(
                    Passed = passed,
                    Total = total,
                    StatOption = statOption,
                    CL = cl,
                    Name = name,
                    Title = title
                )
                if teffs[key].Dim==1:
                    teffs[key]=teffs[key].GetGraph()
                    teffs[key].SetMinimum(0)
                    teffs[key].SetMaximum(1.05)
                else:
                    teffs[key] = getHistFromTEff2D(teffs[key].TEfficiency)

            else:
                teffs[key] = getTEff(
                    passed = passed,
                    total = total,
                    statOption = statOption,
                    cl=cl, name=name, title=title
                )
                teffs[key].SetMinimum(0)
                teffs[key].SetMaximum(1.05)



        elif isinstance(hists[key], dict):
            teffs[key] = getTEffDict(
                hists = hists[key],
                statOption = statOption,
                cl = cl,
                suffix = suffix,
                teffs = teffs.get(key, {})
            )


        else:
            continue

    return teffs



def _saveToRoot(*objects,
    fout: Union[ROOT.TFile, str],
    directory: str = "",
    print_filename: bool = True
):
    if isinstance(fout, str):
        fout = ROOT.TFile(fout, "recreate")

    def recursive_save(obj, current_dir, path=""):
        if isinstance(obj, ROOT.TObject):
            current_dir.cd()
            obj.Write()

        elif isinstance(obj, DdfEff):
            current_dir.cd()
            obj.TEfficiency.Write()


        elif isinstance(obj, dict):
            for sub_key, sub_obj in obj.items():
                sub_key_str = str(sub_key)  # Ensure sub_key is a string
                sub_dir_path = f"{path}/{sub_key_str}" if path else sub_key_str

                if not current_dir.GetDirectory(sub_key_str):
                    current_dir.mkdir(sub_key_str)

                sub_dir = current_dir.GetDirectory(sub_key_str)
                recursive_save(sub_obj, sub_dir, sub_dir_path)


        elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
            for sub_obj in obj:
                recursive_save(sub_obj, current_dir, path)

        else:
            raise ValueError(f"unsupported object type: {type(obj)}")

    if not fout.GetDirectory(directory) and directory:
        fout.mkdir(directory)

    current_dir = fout.GetDirectory(directory) if directory else fout
    for obj in objects:
        recursive_save(obj, current_dir)

    if print_filename:
        print(f"Output file: {fout.GetName()}")

    fout.cd()





def saveToRoot(
    *objects,
    fout: Union[ROOT.TFile, str],
    directory: str = "",
    print_filename: bool = True,
    nested: bool = False
):
    if isinstance(fout, str):
        fout = ROOT.TFile(fout, "recreate")

    def recursive_save(obj, current_dir, path=""):
        if isinstance(obj, ROOT.TObject):
            current_dir.cd()
            obj.Write()

        elif isinstance(obj, DdfEff):
            current_dir.cd()
            obj.TEfficiency.Write()

        elif isinstance(obj, dict):
            for sub_key, sub_obj in obj.items():
                if not nested:
                    recursive_save(sub_obj, current_dir, path)
                else:
                    sub_key_str = str(sub_key)  # Ensure sub_key is a string
                    sub_dir_path = f"{path}/{sub_key_str}" if path else sub_key_str

                    if not current_dir.GetDirectory(sub_key_str):
                        current_dir.mkdir(sub_key_str)

                    sub_dir = current_dir.GetDirectory(sub_key_str)
                    recursive_save(sub_obj, sub_dir, sub_dir_path)

        elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
            for sub_obj in obj:
                recursive_save(sub_obj, current_dir, path)

        else:
            raise ValueError(f"Unsupported object type: {type(obj)}")

    if not fout.GetDirectory(directory) and directory:
        fout.mkdir(directory)

    current_dir = fout.GetDirectory(directory) if directory else fout
    for obj in objects:
        recursive_save(obj, current_dir)

    if print_filename:
        print(f"Output file: {fout.GetName()}")

    fout.cd()

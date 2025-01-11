import ROOT
import os
import glob
from datetime import datetime
from typing import Union
from SndlhcGeo import GeoInterface
from ddfUtils import getSubDirPath, getAllFiles
from utils.tracks import sys, alg, system, algorithm, att
from utils.misc import nType, nName, getTChain, getTtFromSys


class SndData:
    def __init__(self,
        Run: int,
        InputDir: str,
        Files: str = "*",
        Geofile: Union[str, None] = None
    ):
        self.Run = Run

        if Files.endswith(".root"):
            self.Files = Files
        else:
            self.Files = f"{Files}.root"

        self.InputDir = getSubDirPath(TopDir=f"run_{Run:06d}", RootDir=InputDir)
        self.Date = self.GetDate()
        self.Fill = self.GetFill()
        self.Tree = self.GetTChain(getSubDirPath(TopDir=f"run_{Run:06d}", RootDir=InputDir), Files)

        if Geofile:
            self.Geofile = Geofile
            self.GeoInterface = GeoInterface(Geofile)
            self.Scifi = GeoInterface(Geofile).modules["Scifi"]
            self.Mufi = GeoInterface(Geofile).modules["MuFilter"]

    def SetInputDir(self):
        self.InputDir = getSubDirPath(TopDir=f"run_{self.Run:06d}", RootDir=self.InputDir)

    def GetDate(self) -> datetime:
        try:
            file_ = self.GetAllFiles()[0]
            tfile = ROOT.TFile.Open(file_)
        except Exception as e:
            print(f"Error opening file: {e}")
            return None
        if tfile.Get("cbmsim"):
            ttree = tfile.Get("cbmsim")
        elif tfile.Get("rawConv"):
            ttree = tfile.Get("rawConv")
        else:
            return None

        try:
            ttree.GetEntry(0)
            utc_timestamp = ttree.EventHeader.GetUTCtimestamp()
            date_ = datetime.utcfromtimestamp(utc_timestamp)
            return date_
        except Exception as e:
            print(f"Error accessing data: {e}")
            return None

    def GetFill(self) -> int:
        try:
            file_ = self.GetAllFiles()[0]
            tfile = ROOT.TFile.Open(file_)
        except Exception as e:
            print(f"Error opening file: {e}")
            return None
        if tfile.Get("cbmsim"):
            ttree = tfile.Get("cbmsim")
        elif tfile.Get("rawConv"):
            ttree = tfile.Get("rawConv")
        else:
            return None

        try:
            ttree.GetEntry(0)
            return int(ttree.EventHeader.GetFillNumber())
        except Exception as e:
            print(f"Error accessing data: {e}")
            return None

    def GetTChain(self, InputDir: str, Files: str) -> ROOT.TChain:
        try:
            file_ = self.GetAllFiles()[0]
            tfile = ROOT.TFile.Open(file_)
        except Exception as e:
            print(f"Error opening file: {e}")
            return None

        if tfile.Get("cbmsim"):
            tchain = ROOT.TChain("cbmsim")
        elif tfile.Get("rawConv"):
            tchain = ROOT.TChain("rawConv")
        else: return None

        tchain.Add(f"{InputDir}/{Files}")
        return tchain



    def GetAllFiles(self) -> list:
        return getAllFiles(self.InputDir, self.Files)

    def GetInput(self) -> str:
        return f"{self.InputDir}/{self.Files}"

    def InitGeo(self):
        if not (self.Scifi and self.Mufi):
            raise ValueError("Geo modules for Scifi and DS are not valid or are not provided!")

        self.Tree.GetEntry(0)
        self.Scifi.InitEvent(self.Tree.EventHeader)
        self.Mufi.InitEvent(self.Tree.EventHeader)

    def Print(self):
        print("SND@LHC Dataset:")
        print(f" > Run:     {self.Run}")
        print(f" > Fill:    {self.Fill}")
        print(f" > Input:   {self.GetInput()}")
        print(f" > Date:    {self.Date.day:02d}/{self.Date.month:02d}/{self.Date.year:04d}")
        print(f" > Entries: {self.Tree.GetEntries():,}")

        if self.GeoInterface:
            print(f" > Geofile: {self.Geofile}")




class SndMCData:
    def __init__(self,
        InputDir: str,
        Files: str,
        Geofile: Union[str, None] = None
    ):
        self.InputDir = InputDir
        self.Tree = self.GetTChain(InputDir, Files)
        if Files.endswith(".root"):
            self.Files = Files
        else:
            self.Files = f"{Files}.root"
        if Geofile: self.Geofile = Geofile

    def SetInputDir(self, InputDir: str):
        self.InputDir = InputDir

    def GetTChain(self, InputDir: str, Files: str) -> ROOT.TChain:
        try:
            file_ = self.GetAllFiles()[0]
            tfile = ROOT.TFile.Open(file_)
        except Exception as e:
            print(f"Error opening file: {e}")
            return None

        if tfile.Get("cbmsim"):
            tchain = ROOT.TChain("cbmsim")
        elif tfile.Get("rawConv"):
            tchain = ROOT.TChain("rawConv")
        else:
            return None

        tchain.Add(f"{InputDir}/{Files}")
        return tchain


    def GetAllFiles(self) -> list:
        return glob.glob(f"{self.InputDir}/{self.Files}")

    def GetInput(self) -> str:
        return f"{self.InputDir}/{self.Files}"


    def Print(self):
        print("SND@LHC Dataset:")
        print(f" > Run:     {self.Run}")
        print(f" > Fill:    {self.Fill}")
        print(f" > Input:   {self.GetInput()}")
        print(f" > Date:    {self.Date.day:02d}/{self.Date.month:02d}/{self.Date.year:04d}")
        print(f" > Entries: {self.Tree.GetEntries():,}")




class DdfTrack():
    def __init__(self,
        Track: ROOT.sndRecoTrack,
        Event: Union[ROOT.SNDLHCEventHeader, ROOT.TChain, None] = None,
        IP1_Angle: float = 20.
    ):
        self.sndRecoTrack = Track
        if Event is not None:
            if isinstance(Event, ROOT.TChain):
                self.Event = Event
                self.EventHeader = Event.EventHeader
            elif isinstance(Event, ROOT.SNDLHCEventHeader):
                self.EventHeader = Event.EventHeader
        self.Start = Track.getStart()
        self.Stop = Track.getStop()
        self.Mom = Track.getTrackMom()
        self.tt = Track.getTrackType()
        self.Flag = Track.getTrackFlag()
        self.Chi2 = Track.getChi2()
        self.Ndf = Track.getNdf()
        self.Chi2Ndf = Track.getChi2Ndf()
        self.SlopeXZ = Track.getSlopeXZ()
        self.SlopeYZ = Track.getSlopeYZ()
        self.XZ = Track.getAngleXZ()
        self.YZ = Track.getAngleYZ()


    def GetPoints(self) -> ROOT.std.vector:
        return self.sndRecoTrack.getTrackPoints()


    def IsIP1(self,
        event: Union[ROOT.SNDLHCEventHeader, None] = None
    ) -> Union[bool , None]:
        if event is None: return None

        if (
            self.Flag and
            self.Mom.Z() and
            event.isIP1() and
            abs(self.XZ*1e3) <= IP1_Angle and
            abs(self.YZ*1e3) <= IP1_Angle
        ):
            return True
        else:
            return False

    def GetDoca(self,
        mf_hit: ROOT.MuFilterHit,
        MuFi:   ROOT.MuFilter
    ) -> float:

        left  = ROOT.TVector3()
        right = ROOT.TVector3()
        MuFi.GetPosition(mf_hit.GetDetectorID(), left, right)

        mom = self.Mom
        pos = self.Start
        pq  = left-pos
        uCrossv = (right - left).Cross(mom)
        doca = pq.Dot(uCrossv)/uCrossv.Mag()

        return ROOT.TMath.Abs(doca)

    def GetPointAtZ(self, Z: float) -> ROOT.TVector3:
        track_slope = (Z - self.Start.Z())/self.Mom.Z()

        intersection_point = ROOT.TVector3(
            self.Start.X() + track_slope*self.Mom.X(),
            self.Start.Y() + track_slope*self.Mom.Y(),
            Z
        )
        return intersection_point

    def IsWithinAref(self,
        Zref: float,
        xmin: float = -42.,
        xmax: float = -10.,
        ymin: float =  19.,
        ymax: float =  48.
    ) -> bool:
        ref = self.GetPointAtZ(Zref)
        if (
            ref.X() >= xmin and
            ref.X() <= xmax and
            ref.Y() >= ymin and
            ref.Y() <= ymax
        ):
            return True
        else:
            return False

    def IsWithinDS3(self,
        xmin: float = 12.770,
        xmax: float = 4.713,
        ymin: float = 12.770,
        ymax: float = 72.770
    ) -> bool:
        ds3 = self.GetPointAtZ(538.366)
        if (
            ds3.X() > xmin and
            ds3.X() < xmax and
            ds3.Y() > ymin and
            ds3.Y() < ymax
        ):
           return True
        else:
           return False

    def IsWithinUS5Bar(self,
        mufi: ROOT.MuFilter,
        eventOrMfHits: Union[ROOT.TChain, ROOT.TClonesArray, None] = None
    ) -> bool:
        if eventOrMfHits is not None:
            if isinstance(eventOrMfHits, ROOT.TClonesArray):
                mf_hits = eventOrMfHits
            else:
                mf_hits = eventOrMfHits.Digi_MuFilterHits
        else:
            if self.Event:
                mf_hits = self.Event.Digi_MuFilterHits
            else:
                raise ValueError("Neither MuFilterHits nor an event was provided!")

        return any(
            mf_hit.GetSystem()==2 and mf_hit.GetPlane()==4 and self.GetDoca(mf_hit, mufi) <= 3
            for mf_hit in mf_hits
        )


    def IsWithinVetoBar(self,
        mufi: ROOT.MuFilter,
        eventOrMfHits: Union[ROOT.TChain, ROOT.TClonesArray, None] = None
    ) -> bool:
        if eventOrMfHits is not None:
            if isinstance(eventOrMfHits, ROOT.TClonesArray):
                mf_hits = eventOrMfHits
            else:
                mf_hits = eventOrMfHits.Digi_MuFilterHits
        else:
            if self.Event:
                mf_hits = self.Event.Digi_MuFilterHits
            else:
                raise ValueError("Neither MuFilterHits nor an event was provided!")
        del eventOrMfHits

        for mf_hit in mf_hits:
            if (mf_hit.GetSystem() != 1): continue
            if (self.GetDoca(mf_hit, mufi) <= 3):
                return True
        return False

    def IsGood(self,
        xz_min:      float = -0.08,
        xz_max:      float =  0.08,
        yz_min:      float = -0.08,
        yz_max:      float =  0.08,
        chi2ndf_max: float =  1e6,
        chi2ndf_min: float =  0.,
        trkP_max:    int   =  999,
        trkP_min:    int   =  0
    ) -> bool:
        if self.Ndf==0 or self.Mom.Z()==0:
            return False

        if (
            self.Flag and
            self.XZ >= xz_min and
            self.XZ <= xz_max and
            self.YZ >= yz_min and
            self.YZ <= yz_max and
            self.Chi2Ndf <= chi2ndf_max and
            self.Chi2Ndf >= chi2ndf_min and
            self.GetPoints().size() <= trkP_max and
            self.GetPoints().size() >= trkP_min
        ):
            return True
        else:
            return False


    def att(self) -> int:
        return att(self.tt)

    def Sys(self) -> str:
        return sys(self.tt)

    def System(self) -> str:
        return system(self.tt)

    def Alg(self) -> str:
        return alg(self.tt)

    def Algorithm(self) -> str:
        return algorithm(self.tt)

    def nType(self) -> str:
        return nType(self.tt)

    def nName(self) -> str:
        return nName(self.tt)

    def Print(self):
        print("DDF SND@LHC Track:")
        print(f" > Type: {self.System()} {self.Algorithm()}")
        print(f" > XZ:   {1e3*self.XZ} mrad")
        print(f" > YZ:   {1e3*self.YZ} mrad")

        if self.Event is not None:
            print(" > Event:")
            print(f"    >> Number:    {self.Event.GetEventNumber():,}")
            print(f"    >> Time:      {self.Event.GetTimeAsString()}")
        else:
            print(f" > Event:     None")








class DdfMCTrack():
    def __init__(self,
        Track: ROOT.ShipMCTrack,
        Event: Union[ROOT.TChain, ROOT.SNDLHCEventHeader, None] = None,
        IP1_Angle: float = 20.
    ):
        self.ShipMCTrack = Track
        if Event is not None:
            if isinstance(Event, ROOT.TChain):
                self.Event = Event
                self.EventHeader = Event.EventHeader
            elif isinstance(Event, ROOT.SNDLHCEventHeader):
                self.EventHeader = Event.EventHeader

        self.w = Track.GetWeight()
        self.Start = ROOT.TVector3(Track.GetStartX(), Track.GetStartY(), Track.GetStartZ())
        self.Mom = Track.GetP()
        self.Pdg = Track.GetPdgCode()
        self.XZ = ROOT.TMath.ATan(Track.GetPx()/Track.GetPz())
        self.YZ = ROOT.TMath.ATan(Track.GetPy()/Track.GetPz())


    def GetPointAtZ(self, Z: float) -> ROOT.TVector3:
        px = self.ShipMCTrack.GetPx()
        py = self.ShipMCTrack.GetPy()
        pz = self.ShipMCTrack.GetPz()

        px_0 = self.ShipMCTrack.GetStartX()
        py_0 = self.ShipMCTrack.GetStartY()
        pz_0 = self.ShipMCTrack.GetStartZ()

        t = (Z - pz_0) / pz

        x = px_0 + px * t
        y = py_0 + py * t

        return ROOT.TVector3(x, y, Z)




    def Print(self):
        print("DDF SND@LHC MCTrack:")
        print(f" > PDG:            {self.Pdg}")
        print(f" > XZ:             {1e3*self.XZ} mrad")
        print(f" > YZ:             {1e3*self.YZ} mrad")

        if self.Event is not None:
            print(f" > Event Number:   {self.EventHeader.GetEventNumber():,}")
        else:
            print(" > Event:          None")

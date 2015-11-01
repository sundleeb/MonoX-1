
from ROOT import *
import ROOT as r
from optparse import OptionParser
import re, array, sys, numpy, os

gROOT.ProcessLine(
    "struct eff_t {\
     Double_t         metV;\
     Double_t         metVUp;\
     Double_t         metVDown;\
    }" )
#gROOT.ProcessLine(
#    "struct eff_t {\
#     Float_t         metV;\
#    }" )

parser = OptionParser()
parser.add_option('--file'       ,action='store',type='string',dest='file'      ,default='boosted-combo.root',                       help='File to Correct')
parser.add_option('--fileM'      ,action='store',type='string',dest='fileM'     ,default='recoilfits/recoilfit_zmmData_pf_v2.root',  help='RecoilFitMu')
parser.add_option('--fileG'      ,action='store',type='string',dest='fileG'     ,default='recoilfits/recoilfit_gjetsData_pf_v1.root',help='RecoilFitGamma')
(options,args) = parser.parse_args()

lFileM = r.TFile(options.fileM)
U1M  = lFileM.FindObjectAny("PFu1Mean_0")
lFileG = r.TFile(options.fileG)
U1G  = lFileG.FindObjectAny("PFu1Mean_0")

def unc2(iFit,iVal):
    lE2 = iFit.GetParError(0) + iVal*iFit.GetParError(1) + iVal*iVal*iFit.GetParError(2)
    if abs(iFit.GetParError(3)) > 0:
        lE2 += iVal*iVal*iVal*     iFit.GetParError(3)
    if abs(iFit.GetParError(4)) > 0:
        lE2 += iVal*iVal*iVal*iVal*iFit.GetParError(4)
    if abs(iFit.GetParError(5)) > 0 and iFit.GetParameter(3) == 0:
        lE2 += iVal*iVal*               iFit.GetParError(5)
    if abs(iFit.GetParError(5)) > 0 and iFit.GetParameter(3) != 0:
        lE2 += iVal*iVal*iVal*iVal*iVal*iFit.GetParError(5)
    if abs(iFit.GetParError(6)) > 0:
        lE2 += iVal*iVal*iVal*iVal*iVal*iVal*iFit.GetParError(6)
    return lE2

def combinedUnc(iFit0,iFit1,iVal):
    return sqrt(unc2(iFit0,iVal)+unc2(iFit1,iVal))

def adjust(met,metphi,vphi,shiftAdd,shiftSub,unc=0):
    lVec = r.TLorentzVector()
    lVec.SetPtEtaPhiM(met,0,metphi,0)
    shift = shiftAdd-shiftSub
    if unc != 0:
        shift+=unc
    lShift = r.TLorentzVector()
    lShift.SetPtEtaPhiM(abs(shift),0,vphi,0)
    if shift < 0:
        lShift.RotateZ(r.TMath.Pi())
    lVec += lShift
    #if met > 450:
    #    print met,"  - ",shift,shiftAdd,shiftSub,lShift.Pt()
    return lVec.Pt()

def addFootprint(name,iNtuple,iFileName,iUnc):
    postfix='_FP'
    if iUnc == 1:
        postfix += 'Up'
    if iUnc == -1:
        postfix += 'Down'
    lFile  = r.TFile(iFileName,'UPDATE')
    lTree = iNtuple.CloneTree(0)
    lTree.SetName (iNtuple.GetName() +postfix)
    lTree.SetTitle(iNtuple.GetTitle()+postfix)
    lEff=eff_t()
    lTree.SetBranchAddress( 'mvamet',AddressOf(lEff,"metV"))
    iNtuple.GetEntry(1)
    isZMM    = name.find('di_muon') > -1
    isZEE    = name.find('di_electron') > -1
    isPhoton = name.find('photon') > -1
    iNtuple.GetEntry(0)
    isDM     = iNtuple.dmpt > 2
    isGen    = iNtuple.genVpt > 2
    isJet    = iNtuple.genjetpt > 2
    print "Zll",isZMM,"ZEE",isZEE,"Gamma",isPhoton,"DM",isDM,"Gen",isGen,"Jet",isJet
    for i0 in range(0,iNtuple.GetEntriesFast()):
        iNtuple.GetEntry(i0)
        if isPhoton:
            pUnc = combinedUnc(U1G,U1M,iNtuple.ptpho)
            lEff.metV         = adjust(iNtuple.mvamet,iNtuple.mvametphi,iNtuple.phipho,U1G.Eval(iNtuple.ptpho   ),U1M.Eval(iNtuple.ptpho),iUnc*pUnc)
        elif isZMM or isZEE:
            pUnc =  combinedUnc(U1G,U1M,iNtuple.ptll)
            lEff.metV         = adjust(iNtuple.mvamet,iNtuple.mvametphi,iNtuple.phill,U1G.Eval(iNtuple.ptll    ),U1M.Eval(iNtuple.ptll),iUnc*pUnc)
        elif isDM:
            pUnc =  combinedUnc(U1G,U1M,iNtuple.dmpt)
            lEff.metV         = adjust(iNtuple.mvamet,iNtuple.mvametphi,iNtuple.dmphi,U1G.Eval(iNtuple.dmpt    ),U1M.Eval(iNtuple.dmpt),iUnc*pUnc)
        elif isGen and iNtuple.genVpt > 1:
            pUnc =  combinedUnc(U1G,U1M,iNtuple.genVpt)
            lEff.metV         = adjust(iNtuple.mvamet,iNtuple.mvametphi,iNtuple.genVphi,U1G.Eval(iNtuple.genVpt  ),U1M.Eval(iNtuple.genVpt),iUnc*pUnc)
        elif isJet:
            pUnc = combinedUnc(U1G,U1M,iNtuple.genjetpt)
            lEff.metV         = adjust(iNtuple.mvamet,iNtuple.mvametphi,iNtuple.genjetphi,U1G.Eval(iNtuple.genjetpt),U1M.Eval(iNtuple.genjetpt),iUnc*pUnc)
        lTree.Fill()
    lTree.Write()

lBaseFile=r.TFile(options.file)
for sample in lBaseFile.GetListOfKeys():
    print "Sample :",sample.ReadObj().GetName()
    pTree = lBaseFile.Get(sample.ReadObj().GetName())
    sampleName = sample.ReadObj().GetName()
    if sampleName.find('photon') < 0 and sampleName.find('electron') < 0 :
        continue
    if sampleName.find('single_electron') > 0: 
        continue
    if sampleName.find('data') <  0: 
        continue
    print "FIXING:",sample.ReadObj().GetName()
    addFootprint(sampleName,pTree,options.file,0)
    addFootprint(sampleName,pTree,options.file,1)
    addFootprint(sampleName,pTree,options.file,-1)
   

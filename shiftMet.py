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

lBaseFile  = r.TFile.Open(options.file,'UPDATE')
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
    lTree = pTree.CloneTree(0)
    lTree.SetName (pTree.GetName() )
    lTree.SetTitle(pTree.GetTitle())
    lEff=eff_t()
    lTree.SetBranchAddress( 'mvamet',AddressOf(lEff,"metV"))
    lTree.Branch( 'mvamet_fpup',     AddressOf(lEff,"metVUp"),"metVUp/D")
    lTree.Branch( 'mvamet_fpdwn',    AddressOf(lEff,"metVDown"),"metVDown/D")
    pTree.GetEntry(1)
    isZMM    = sample.ReadObj().GetName().find('di_muon') > -1
    isZEE    = sample.ReadObj().GetName().find('di_electron') > -1
    isPhoton = sample.ReadObj().GetName().find('photon') > -1
    isDM     = pTree.dmpt > 2
    isGen    = pTree.genVpt > 2
    isJet    = pTree.genjetpt > 2
    print "Zll",isZMM,"ZEE",isZEE,"Gamma",isPhoton,"DM",isDM,"Gen",isGen,"Jet",isJet
    for i0 in range(0,pTree.GetEntriesFast()):
        pTree.GetEntry(i0)
        if isPhoton:
            lEff.metV         = adjust(pTree.mvamet,pTree.mvametphi,pTree.phipho,U1G.Eval(pTree.ptpho   ),U1M.Eval(pTree.ptpho))
            lEff.metVUp       = adjust(pTree.mvamet,pTree.mvametphi,pTree.phipho,U1G.Eval(pTree.ptpho   ),U1M.Eval(pTree.ptpho),   combinedUnc(U1G,U1M,pTree.ptpho))
            lEff.metVDown     = adjust(pTree.mvamet,pTree.mvametphi,pTree.phipho,U1G.Eval(pTree.ptpho   ),U1M.Eval(pTree.ptpho),-1*combinedUnc(U1G,U1M,pTree.ptpho))
        elif isZMM or isZEE:
            lEff.metV         = adjust(pTree.mvamet,pTree.mvametphi,pTree.phill,U1G.Eval(pTree.ptll    ),U1M.Eval(pTree.ptll))
            lEff.metVUp       = adjust(pTree.mvamet,pTree.mvametphi,pTree.phill,U1G.Eval(pTree.ptll    ),U1M.Eval(pTree.ptll),   combinedUnc(U1G,U1M,pTree.ptpho))
            lEff.metVDown     = adjust(pTree.mvamet,pTree.mvametphi,pTree.phill,U1G.Eval(pTree.ptll    ),U1M.Eval(pTree.ptll),-1*combinedUnc(U1G,U1M,pTree.ptpho))
        elif isDM:
            lEff.metV         = adjust(pTree.mvamet,pTree.mvametphi,pTree.dmphi,U1G.Eval(pTree.dmpt    ),U1M.Eval(pTree.dmpt))
            lEff.metVUp       = adjust(pTree.mvamet,pTree.mvametphi,pTree.dmphi,U1G.Eval(pTree.dmpt    ),U1M.Eval(pTree.dmpt),   combinedUnc(U1G,U1M,pTree.dmpt))
            lEff.metVDown     = adjust(pTree.mvamet,pTree.mvametphi,pTree.dmphi,U1G.Eval(pTree.dmpt    ),U1M.Eval(pTree.dmpt),-1*combinedUnc(U1G,U1M,pTree.dmpt))
        elif isGen and pTree.genVpt > 1:
            lEff.metV         = adjust(pTree.mvamet,pTree.mvametphi,pTree.genVphi,U1G.Eval(pTree.genVpt  ),U1M.Eval(pTree.genVpt))
            lEff.metVUp       = adjust(pTree.mvamet,pTree.mvametphi,pTree.genVphi,U1G.Eval(pTree.genVpt  ),U1M.Eval(pTree.genVpt),   combinedUnc(U1G,U1M,pTree.genVpt))
            lEff.metVDown     = adjust(pTree.mvamet,pTree.mvametphi,pTree.getVphi,U1G.Eval(pTree.genVpt  ),U1M.Eval(pTree.genVpt),-1*combinedUnc(U1G,U1M,pTree.genVpt))
        elif isJet:
            lEff.metV         = adjust(pTree.mvamet,pTree.mvametphi,pTree.genjetphi,U1G.Eval(pTree.genjetpt),U1M.Eval(pTree.genjetpt))
            lEff.metVUp       = adjust(pTree.mvamet,pTree.mvametphi,pTree.genjetphi,U1G.Eval(pTree.genjetpt),U1M.Eval(pTree.genjetpt),   combinedUnc(U1G,U1M,pTree.genjetpt))
            lEff.metVDown     = adjust(pTree.mvamet,pTree.mvametphi,pTree.genjetphi,U1G.Eval(pTree.genjetpt),U1M.Eval(pTree.genjetpt),-1*combinedUnc(U1G,U1M,pTree.genjetpt))
        #if pTree.mvamet > 450:
        #    print pTree.mvamet," - ",lEff.metV,pTree.ptpho
        lTree.Fill()
    lTree.Write()
    lTree.Write()
   

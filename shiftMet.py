from ROOT import *
import ROOT as r
from optparse import OptionParser
import re, array, sys, numpy, os

gROOT.ProcessLine(
    "struct eff_t {\
     Double_t         metV;\
    }" )
#gROOT.ProcessLine(
#    "struct eff_t {\
#     Float_t         metV;\
#    }" )

parser = OptionParser()
parser.add_option('--file'       ,action='store',type='string',dest='file'      ,default='boosted-combo.root',  help='File to Correct')
(options,args) = parser.parse_args()

lBaseFile  = r.TFile.Open(options.file,'UPDATE')
for sample in lBaseFile.GetListOfKeys():
    print "Sample :",sample.ReadObj().GetName()
    pTree = lBaseFile.Get(sample.ReadObj().GetName())
    sampleName = sample.ReadObj().GetName()
    #if sampleName.find('Zll') < 0 and sampleName.find('Znunu') < 0 and sampleName.find('H') < 0 and sampleName.find('photon') < 0:
    if sampleName.find('Met') < 0  and sampleName.find('photon') < 0 and sampleName.find('electron') < 0 :
        continue
    if sampleName.find('single_electron') > 0: 
        continue
    print "FIXING:",sample.ReadObj().GetName()
    lTree = pTree.CloneTree(0)
    lTree.SetName (pTree.GetName() )
    lTree.SetTitle(pTree.GetTitle())
    lEff=eff_t()
    lTree.SetBranchAddress( 'mvamet',    AddressOf(lEff,"metV"))
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
            lEff.metV         = pTree.mvamet+0.032*pTree.ptpho-0.3
        elif isZMM or isZEE:
            lEff.metV         = pTree.mvamet+0.032*pTree.ptll-0.3
        elif isDM:
            lEff.metV         = pTree.mvamet+0.032*pTree.dmpt-0.3
        elif isGen and pTree.genVpt > 1:
            lEff.metV         = pTree.mvamet+0.032*pTree.genVpt-0.3
        elif isJet:
            lEff.metV         = pTree.mvamet+0.032*pTree.genjetpt-0.3
        lTree.Fill()
    lTree.Write()
    lTree.Write()
   

from ROOT import *
import ROOT as r
from optparse import OptionParser
import re, array, sys, numpy, os

gROOT.ProcessLine(
    "struct eff_t {\
     Float_t         metV;\
    }" )

parser = OptionParser()
parser.add_option('--file'       ,action='store',type='string',dest='file'      ,default='boosted-combo.root',  help='File to Correct')
(options,args) = parser.parse_args()

lBaseFile  = r.TFile.Open(options.file,'UPDATE')
for sample in lBaseFile.GetListOfKeys():
    print "Sample :",sample.ReadObj().GetName()
    pTree = lBaseFile.Get(sample.ReadObj().GetName())
    if (sample.ReadObj().GetName().find('di_muon_control') < 0 and  sample.ReadObj().GetName().find('photon_control') < 0) or sample.ReadObj().GetName().find('data_di_muon_control') > 0:
      continue
    print "FIXING:",sample.ReadObj().GetName()
    lTree = pTree.CloneTree(0)
    lTree.SetName (pTree.GetName() )
    lTree.SetTitle(pTree.GetTitle())
    lEff=eff_t()
    lTree.SetBranchAddress( 'mvamet',    AddressOf(lEff,"metV"))
    isData   = sample.ReadObj().GetName().find('data') > -1
    isPhoton = sample.ReadObj().GetName().find('Zll_di_muon_control') < 0
    for i0 in range(0,pTree.GetEntriesFast()):
        pTree.GetEntry(i0)
        if isPhoton:
            if isData:
                lEff.metV     = pTree.mvamet+0.032*pTree.ptpho-0.3
            else:
                lEff.metV     = pTree.mvamet+0.032*pTree.ptpho-0.3
        else:
            lEff.metV         = pTree.mvamet+0.032*pTree.ptll-0.3
        lTree.Fill()
    lTree.Write()
    lTree.Write()
   

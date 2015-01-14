from ROOT import *
import ROOT as r
import re, array, sys, numpy

gROOT.ProcessLine(
    "struct met_t {\
     Float_t         metV;\
     Float_t         metPhi;\
    }" )
    
def correctNtuple(iNtuple,iRecoil,iFileName,iUnc):
    postfix='Met'
    if iUnc == 1:
        postfix += '_Up'
    if iUnc == -1:
        postfix += '_Down'
    lFile  = r.TFile(iFileName,'UPDATE')
    lTree = iNtuple.CloneTree(0)
    lTree.SetName (iNtuple.GetName() +postfix)
    lTree.SetTitle(iNtuple.GetTitle()+postfix)
    lMet=met_t()
    lTree.SetBranchAddress( 'mvamet',    AddressOf(lMet,"metV"))
    lTree.SetBranchAddress( 'mvametphi', AddressOf(lMet,"metPhi"))
    for i0 in range(0,iNtuple.GetEntriesFast()):
        iNtuple.GetEntry(i0)
        pPt       = iNtuple.genjetpt * 1.15 # correction factor from gen jet pT to recoil pT
        #if (iNtuple.GetName()).find('H') > 0:
        #    pPt       = iNtuple.dmpt
        if iNtuple.genVpt > 5 :
            pPt       = iNtuple.genVpt
        pMet      = iRecoil.CorrectType1(iNtuple.mvamet,iNtuple.mvametphi,pPt,0,0,0,0,0, iUnc, -iUnc,0)
        lMet.metV   = pMet[0]
        lMet.metPhi = pMet[1]
        lTree.Fill()
    lTree.Write()

sys.path.append("configs")
import categories_config_vtag_met as x

r.gROOT.SetBatch(1)
r.gROOT.ProcessLine('.L ./RecoilCorrector.hh+')

for cat_id,cat in enumerate(x.categories):
    Recoil = r.RecoilCorrector(cat['recoilMC'])
    Recoil.addDataFile(cat['recoilData'])
    Recoil.addMCFile(cat['recoilMC'])
    lBaseFile  = r.TFile.Open(cat['in_file_name'])
    samples = cat['metsamples']
    print samples
    for sample in samples:
        print "Sample :",sample
        pTree = lBaseFile.Get(sample)
        correctNtuple(pTree,Recoil,cat['in_file_name'], 0)
        correctNtuple(pTree,Recoil,cat['in_file_name'], 1)
        correctNtuple(pTree,Recoil,cat['in_file_name'],-1)

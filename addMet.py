from ROOT import *
import ROOT as r
import re, array, sys, numpy

gROOT.ProcessLine(
    "struct met_t {\
     Float_t         metV;\
     Float_t         metPhi;\
     Float_t         metRaw;\
    }" )
    
#gROOT.ProcessLine(
#    "struct met_t {\
#     Float_t         metV;\
#     Float_t         metPhi;\
#     Float_t         metRaw;\
#    }" )
    
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
    lTree.Branch( 'metRaw',    AddressOf(lMet,"metRaw"),"metRaw/F")
    for i0 in range(0,iNtuple.GetEntriesFast()):
        iNtuple.GetEntry(i0)
        pPt       = iNtuple.genjetpt * 1.15 # correction factor from gen jet pT to recoil pT
        if (iNtuple.GetName()).find('H') > 0:
            pPt       = iNtuple.dmpt
        if iNtuple.genVpt > 5 :
            pPt       = iNtuple.genVpt
        pPhi          = iNtuple.mvametphi+r.TMath.Pi()
        if iNtuple.genVphi != 0 : 
            pPhi = iNtuple.genVphi
        if pPhi > r.TMath.Pi():
            pPhi = pPhi-r.TMath.Pi()
        pMet      = iRecoil.CorrectType2(iNtuple.mvamet,iNtuple.mvametphi,pPt,pPhi,0,0,0,0, iUnc, -iUnc,0)
        #print pMet[0],' - ',iNtuple.mvamet
        lMet.metV   = pMet[0]
        lMet.metPhi = pMet[1]
        lMet.metRaw = iNtuple.mvamet
        lTree.Fill()
    lTree.Write()

sys.path.append("configs")
x = __import__(sys.argv[1]) 
#import categories_config_vtag_Bambu as x

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

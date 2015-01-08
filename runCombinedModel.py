#from combineControlRegions import *
from counting_experiment import *
import ROOT as r 
r.gROOT.SetBatch(1)

fkFactor = r.TFile.Open("/afs/cern.ch/work/n/nckw/public/monojet/Photon_Z_NLO_kfactors.root")
nlo_pho = fkFactor.Get("pho_NLO_LO")
nlo_zjt = fkFactor.Get("Z_NLO_LO")
nlo_pho_mrUp = fkFactor.Get("pho_NLO_LO_mrUp")
nlo_zjt_mrUp = fkFactor.Get("Z_NLO_LO_mrUp")
nlo_pho_mrDown = fkFactor.Get("pho_NLO_LO_mrDown")
nlo_zjt_mrDown = fkFactor.Get("Z_NLO_LO_mrDown")
nlo_pho_mfUp = fkFactor.Get("pho_NLO_LO_mfUp")
nlo_zjt_mfUp = fkFactor.Get("Z_NLO_LO_mfUp")
nlo_pho_mfDown = fkFactor.Get("pho_NLO_LO_mfDown")
nlo_zjt_mfDown = fkFactor.Get("Z_NLO_LO_mfDown")

def cmodel(cid,nam,_f,_fOut, out_ws):

  _fin = _f.Get("category_%s"%nam)

  _wspace = _fin.Get("wspace_%s"%nam)
  _photon_datasetname = "photon_data"
  _gjet_mcname 	      = "photon_gjet"
  _dimuon_datasetname = "dimuon_data"
  _dimuon_backgroundsname = "dimuon_all_background"

  metname = "mvamet"
  gvptname= "genVpt"
  try:
    mt = _wspace.var(metname)
    mt.GetName()
  except:
    metname = "mvamet_"
    gvptname = "genVpt_"
  # First we need to re-build the nominal templates from the datasets modifying the weights

  target = _fin.Get("signal_zjets")
  Zmm = _fin.Get("dimuon_zll")
  #Pho = _fin.Get("photon_gjet")
  ZmmScales = target.Clone(); ZmmScales.SetName("zmm_weights_%s"%nam)
  #PhotonScales = target.Clone(); PhotonScales.SetName("photon_weights_%s"%nam)

  # run through 3 datasets, photon, etc and generate a template from histograms 
  # We only nned to make NLO versions of Z(vv) and Photon :) 
  # This class lets us run through corrections 
  r.gROOT.ProcessLine(".L diagonalizer.cc+")
  from ROOT import diagonalizer
  diag = diagonalizer(_wspace)
 
  #Loop Over Systematics also?
  Pho = target.Clone(); Pho.SetName("photon_weights_denom_%s"%nam)
  for b in range(Pho.GetNbinsX()): Pho.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho,nlo_pho,gvptname,_wspace.var(metname),_wspace.data(_gjet_mcname))

  Zvv = target.Clone(); Zvv.SetName("photon_weights_nom_%s"%nam)
  for b in range(Zvv.GetNbinsX()): Zvv.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv,nlo_zjt,gvptname,_wspace.var(metname),_wspace.data("signal_zjets"))
  
  #################################################################################################################
  # now do systematic parts
  Pho_mrUp = target.Clone(); Pho.SetName("photon_weights_denom_mrUp_%s"%nam)
  for b in range(Pho_mrUp.GetNbinsX()): Pho_mrUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mrUp,nlo_pho_mrUp,gvptname,_wspace.var(metname),_wspace.data(_gjet_mcname))

  Zvv_mrUp = target.Clone(); Zvv_mrUp.SetName("photon_weights_nom_mrUp_%s"%nam)
  for b in range(Zvv_mrUp.GetNbinsX()):Zvv_mrUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mrUp,nlo_zjt_mrUp,gvptname,_wspace.var(metname),_wspace.data("signal_zjets"))

  Pho_mrDown = target.Clone(); Pho.SetName("photon_weights_denom_mrDown_%s"%nam)
  for b in range(Pho_mrDown.GetNbinsX()): Pho_mrDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mrDown,nlo_pho_mrDown,gvptname,_wspace.var(metname),_wspace.data(_gjet_mcname))

  Zvv_mrDown = target.Clone(); Zvv_mrDown.SetName("photon_weights_nom_mrDown_%s"%nam)
  for b in range(Zvv_mrDown.GetNbinsX()): Zvv_mrDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mrDown,nlo_zjt_mrDown,gvptname,_wspace.var(metname),_wspace.data("signal_zjets"))

  Pho_mfUp = target.Clone(); Pho.SetName("photon_weights_denom_mfUp_%s"%nam)
  for b in range(Pho_mfUp.GetNbinsX()): Pho_mfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mfUp,nlo_pho_mfUp,gvptname,_wspace.var(metname),_wspace.data(_gjet_mcname))

  Zvv_mfUp = target.Clone(); Zvv_mfUp.SetName("photon_weights_nom_mfUp_%s"%nam)
  for b in range(Zvv_mfUp.GetNbinsX()): Zvv_mfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mfUp,nlo_zjt_mfUp,gvptname,_wspace.var(metname),_wspace.data("signal_zjets"))

  Pho_mfDown = target.Clone(); Pho.SetName("photon_weights_denom_mfDown_%s"%nam)
  for b in range(Pho_mfDown.GetNbinsX()): Pho_mfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mfDown,nlo_pho_mfDown,gvptname,_wspace.var(metname),_wspace.data(_gjet_mcname))

  Zvv_mfDown = target.Clone(); Zvv_mfDown.SetName("photon_weights_nom_mfDown_%s"%nam)
  for b in range(Zvv_mfDown.GetNbinsX()): Zvv_mfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mfDown,nlo_zjt_mfDown,gvptname,_wspace.var(metname),_wspace.data("signal_zjets"))
  ##################################################################################################################

  # Have to also add one per systematic variation :(, 
  Zvv.Divide(Pho); 		 Zvv.SetName("photon_weights_%s"%nam)
  Zvv_mrUp.Divide(Pho_mrUp); 	 Zvv_mrUp.SetName("photon_weights_%s_mr_Up"%nam);_fOut.WriteTObject(Zvv_mrUp)
  Zvv_mrDown.Divide(Pho_mrDown); Zvv_mrDown.SetName("photon_weights_%s_mr_Down"%nam);_fOut.WriteTObject(Zvv_mrDown)
  Zvv_mfUp.Divide(Pho_mfUp); 	 Zvv_mfUp.SetName("photon_weights_%s_mf_Up"%nam);_fOut.WriteTObject(Zvv_mfUp)
  Zvv_mfDown.Divide(Pho_mfDown); Zvv_mfDown.SetName("photon_weights_%s_mf_Down"%nam);_fOut.WriteTObject(Zvv_mfDown)

  ZmmScales.Divide(Zmm)
  PhotonScales = Zvv.Clone()

  #_fOut.WriteTObject(Zvv) # these are photon scales
  _fOut.WriteTObject(PhotonScales)
  _fOut.WriteTObject(ZmmScales)

  _bins = []  # take bins from some histogram
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  CRs = [
  # Channel(_wspace,0,_wspace.data(_photon_datasetname),Zvv,"Purity:0.9399+(8.46e-5)*x")  # stupid linear fit of Purities, should move to flat 
  # Channel(_wspace,0,_wspace.data(_photon_datasetname),Zvv,"Purity:0.97")  # stupid linear fit of Purities, should move to flat 
   Channel("Photon+jet",_wspace,0,_wspace.data(_photon_datasetname),PhotonScales,"Purity:0.97")  # stupid linear fit of Purities, should move to flat 
 , Channel("Dimuon",_wspace,1,_wspace.data(_dimuon_datasetname),ZmmScales,_dimuon_backgroundsname)
  ]
  #Add Systematic ? This time we add them as nuisance parameters.

  #_control_regions[0].add_systematic_shape("MuonEfficiency",_fin)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma 
  CRs[1].add_systematic_yield("MuonEfficiency",0.01)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma, a number means make a new global scaling (lnN)
  CRs[0].add_systematic_shape("mr",_fOut) 
  CRs[0].add_systematic_shape("mf",_fOut) 
  CRs[0].add_systematic_yield("ewk",0.05) 
  CRs[0].add_systematic_yield("PhotonEfficiency",0.01)  
  # We want to make a combined model which performs a simultaneous fit in all three categories so first step is to build a combined model in all three 
  #CombinedControlRegionFit(nam,_fin,_fOut,_wspace,_bins,metname,"doubleExponential_dimuon_data","doubleExponential_dimuon_mc","signal_zjets",CRs)
  return Category(cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,"doubleExponential_dimuon_data","doubleExponential_dimuon_mc","signal_zjets",CRs,diag)
  
_fOut = r.TFile("photon_dimuon_combined_model.root","RECREATE")
# run once per category
categories = ["inclusive","resolved","boosted"]
_f = r.TFile.Open("mono-x-vtagged.root")
out_ws = r.RooWorkspace("combinedws","Combined Workspace")
out_ws._import = getattr(out_ws,"import")
# Need to setup the things here for combined dataset, need to add all possible sample types first because otherwise RooFit throws a fit! 
sample = r.RooCategory("bin_number","Bin Number")
obs    = r.RooRealVar("observed","Observed Events bin",1)
out_ws._import(sample)  # Global variables for dataset
out_ws._import(obs)
obsargset = r.RooArgSet(out_ws.var("observed"),out_ws.cat(sample.GetName()))
combined_obsdata = r.RooDataSet("combinedData","Data in all Bins",obsargset)
out_ws._import(combined_obsdata)

cmb_categories=[]
for cid,cn in enumerate(categories): 
        _fDir = _fOut.mkdir("category_%s"%cn)
	cmb_categories.append(cmodel(cid,cn,_f,_fDir,out_ws))

# Now loop through and init all the bins ?!

combined_obsdata.Print("v")
for cid,cn in enumerate(cmb_categories):
	cn.init_channels()
# Now we consruct the fit ourselves, first thing is to make a combined dataset and combined pdf
# Loop through ALL of the bins 
#for cat in cmb_categories:
    
   #cmb_categories[-1].save()

print "Produced combined Z(mm) + photon fits -> ", _fOut.GetName()
_fOut.Close()

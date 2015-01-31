#from combineControlRegions import *
from counting_experiment import *
import ROOT as r 
r.gROOT.SetBatch(1)
r.gROOT.ProcessLine(".L diagonalizer.cc+")
from ROOT import diagonalizer


#fkFactor = r.TFile.Open("/afs/cern.ch/work/n/nckw/public/monojet/Photon_Z_NLO_kfactors.root")
fkFactor = r.TFile.Open("Photon_Z_NLO_kfactors.root")
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
nlo_ewkUp    = fkFactor.Get("EWK_Up")
nlo_ewkDown  = fkFactor.Get("EWK_Dwon")
print "!!!!!",nlo_ewkUp.GetName()," -- ",nlo_ewkDown.GetName()

def cmodelW(cid,nam,_f,_fOut, out_ws, diag):
  _fin = _f.Get("category_%s"%nam)

  _wspace = _fin.Get("wspace_%s"%nam)
  _singlemuon_datasetname = "singlemuon_data"
  _singlemuon_backgroundsname = "singlemuon_all_background"

  target = _fin.Get("signal_wjets")
  Wmn    = _fin.Get("singlemuon_wjets")
  WmnScales = target.Clone(); WmnScales.SetName("wmn_weights_%s"%nam)
  WmnScales.Divide(Wmn)  # scales account for muon in/out of acceptance 
  _fOut.WriteTObject(WmnScales)

  metname = "mvamet"
  gvptname= "genVpt"
  try:
    mt = _wspace.var(metname)
    mt.GetName()
  except:
    metname = "mvamet_"
    gvptname = "genVpt_"
   
  _bins = []  # take bins from some histogram
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  CRs = [
  Channel("Singlemuon",_wspace,out_ws,cid,0,_wspace.data(_singlemuon_datasetname),WmnScales,_singlemuon_backgroundsname)
  ]
  #Add Systematic ? This time we add them as nuisance parameters.

  CRs[0].add_nuisance("MuonEfficiency",0.01)
  CRs[0].add_nuisance("xs_dibosons",0.1,True)   # is a background systematic

  # We want to make a combined model which performs a simultaneous fit in all three categories so first step is to build a combined model in all three
  # Could rewrite this to need less arguments ?
  cat =  Category("WJets",cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,"doubleExponential_singlemuon_data%s"%nam,"doubleExponential_singlemuon_mc%s"%nam,"signal_wjets",CRs,diag)
  return cat

def cmodel(cid,nam,_f,_fOut, out_ws, diag):

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
  #diag = diagonalizer(_wspace)
 
  #Loop Over Systematics also?
  Pho = target.Clone(); Pho.SetName("photon_weights_denom_%s"%nam)
  for b in range(Pho.GetNbinsX()): Pho.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho,nlo_pho,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv = target.Clone(); Zvv.SetName("photon_weights_nom_%s"%nam)
  for b in range(Zvv.GetNbinsX()): Zvv.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv,nlo_zjt,gvptname,metname,_wspace.data("signal_zjets"))
  
  #################################################################################################################
  # now do systematic parts
  Pho_mrUp = target.Clone(); Pho.SetName("photon_weights_denom_mrUp_%s"%nam)
  for b in range(Pho_mrUp.GetNbinsX()): Pho_mrUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mrUp,nlo_pho_mrUp,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mrUp = target.Clone(); Zvv_mrUp.SetName("photon_weights_nom_mrUp_%s"%nam)
  for b in range(Zvv_mrUp.GetNbinsX()):Zvv_mrUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mrUp,nlo_zjt_mrUp,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mrDown = target.Clone(); Pho.SetName("photon_weights_denom_mrDown_%s"%nam)
  for b in range(Pho_mrDown.GetNbinsX()): Pho_mrDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mrDown,nlo_pho_mrDown,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mrDown = target.Clone(); Zvv_mrDown.SetName("photon_weights_nom_mrDown_%s"%nam)
  for b in range(Zvv_mrDown.GetNbinsX()): Zvv_mrDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mrDown,nlo_zjt_mrDown,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mfUp = target.Clone(); Pho.SetName("photon_weights_denom_mfUp_%s"%nam)
  for b in range(Pho_mfUp.GetNbinsX()): Pho_mfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mfUp,nlo_pho_mfUp,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mfUp = target.Clone(); Zvv_mfUp.SetName("photon_weights_nom_mfUp_%s"%nam)
  for b in range(Zvv_mfUp.GetNbinsX()): Zvv_mfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mfUp,nlo_zjt_mfUp,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mfDown = target.Clone(); Pho.SetName("photon_weights_denom_mfDown_%s"%nam)
  for b in range(Pho_mfDown.GetNbinsX()): Pho_mfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mfDown,nlo_pho_mfDown,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mfDown = target.Clone(); Zvv_mfDown.SetName("photon_weights_nom_mfDown_%s"%nam)
  for b in range(Zvv_mfDown.GetNbinsX()): Zvv_mfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mfDown,nlo_zjt_mfDown,gvptname,metname,_wspace.data("signal_zjets"))

  Zvv_ewkDown = target.Clone(); Zvv_ewkDown.SetName("photon_weights_%s_ewk_Down"%nam)
  for b in range(Zvv_ewkDown.GetNbinsX()): Zvv_ewkDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkDown,nlo_ewkDown,gvptname,metname,_wspace.data("signal_zjets"))

  Zvv_ewkUp   = target.Clone(); Zvv_ewkUp   .SetName("photon_weights_%s_ewk_Up"%nam)
  for b in range(Zvv_ewkUp.GetNbinsX()): Zvv_ewkUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkUp,nlo_ewkUp,gvptname,metname,_wspace.data("signal_zjets"))
  
  nlo_ewkFlat = nlo_ewkUp.Clone("ewk_Base")
  nlo_ewkFlat.Divide(nlo_ewkFlat)
  Zvv_ewkBase = target.Clone(); Zvv_ewkBase  .SetName("photon_weights_%s_ewk_Base"%nam)
  for b in range(Zvv_ewkBase.GetNbinsX()): Zvv_ewkBase.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkBase,nlo_ewkFlat,gvptname,metname,_wspace.data("signal_zjets"))
  ##################################################################################################################

  # Have to also add one per systematic variation :(, 
  Zvv.Divide(Pho); 		 Zvv.SetName("photon_weights_%s"%nam)
  Zvv_mrUp.Divide(Pho_mrUp); 	 Zvv_mrUp.SetName("photon_weights_%s_mr_Up"%nam);_fOut.WriteTObject(Zvv_mrUp)
  Zvv_mrDown.Divide(Pho_mrDown); Zvv_mrDown.SetName("photon_weights_%s_mr_Down"%nam);_fOut.WriteTObject(Zvv_mrDown)
  Zvv_mfUp.Divide(Pho_mfUp); 	 Zvv_mfUp.SetName("photon_weights_%s_mf_Up"%nam);_fOut.WriteTObject(Zvv_mfUp)
  Zvv_mfDown.Divide(Pho_mfDown); Zvv_mfDown.SetName("photon_weights_%s_mf_Down"%nam);_fOut.WriteTObject(Zvv_mfDown)
  
  # Divide out the nominal photon for the EWK corrections as this is already the relative difference
  Zvv_ewkUp  .Divide(Zvv_ewkBase)
  Zvv_ewkDown.Divide(Zvv_ewkBase)
  Zvv_ewkUp  .Multiply(Zvv)
  Zvv_ewkDown.Multiply(Zvv)
  
  _fOut.WriteTObject(Zvv_ewkDown)
  _fOut.WriteTObject(Zvv_ewkUp)

  ZmmScales.Divide(Zmm)
  PhotonScales = Zvv.Clone()

  #_fOut.WriteTObject(Zvv) # these are photon scales
  _fOut.WriteTObject(PhotonScales)
  _fOut.WriteTObject(ZmmScales)


  _bins = []  # take bins from some histogram
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  CRs = [
   Channel("Photon+jet",_wspace,out_ws,cid,0,_wspace.data(_photon_datasetname),PhotonScales,"Purity:0.97")  # stupid linear fit of Purities, should move to flat 
  ,Channel("Dimuon",_wspace,out_ws,cid,1,_wspace.data(_dimuon_datasetname),ZmmScales,_dimuon_backgroundsname)
  ]
  #Add Systematic ? This time we add them as nuisance parameters.

  CRs[0].add_nuisance_shape("mr",_fOut) 
  CRs[0].add_nuisance_shape("mf",_fOut) 
  #CRs[0].add_nuisance("ewk",0.05) 
  #CRs[0].add_nuisance_shape("ewk",_fOut,"SetTo=1") 
  CRs[0].add_nuisance("PhotonEfficiency",0.01) 
  CRs[1].add_nuisance("MuonEfficiency",0.01)
  CRs[0].add_nuisance("purity",0.01,True)   # is a background systematic
  CRs[1].add_nuisance("xs_dibosons",0.1,True)   # is a background systematic

  # We want to make a combined model which performs a simultaneous fit in all three categories so first step is to build a combined model in all three
  cat =  Category("ZJets",cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,"doubleExponential_dimuon_data%s"%nam,"doubleExponential_dimuon_mc%s"%nam,"signal_zjets",CRs,diag)
#  cat.addVar("jet1pt",25,150,1000)
#  cat.addVar("mll",25,75,125)
#  cat.addVar("mt",30,50,200)
#  cat.addVar("njets",10,0,10)
#  cat.addVar("lep1pt",25,0,500)
#  cat.addVar("ptll",40,100,1000)
#  cat.addTarget("dimuon_zll",1)
#  cat.addTarget("singlemuon_zll",1)
  return cat 
  
#----------------------------------------------------------------------------------------------------------------------------------------------------------//
_fOut = r.TFile("photon_dimuon_combined_model.root","RECREATE")
# run once per category
categories = ["inclusive","resolved","boosted"]
#categories = ["boosted","resolved"]
#categories = ["inclusive"]
_f = r.TFile.Open("mono-x-vtagged.root")
out_ws = r.RooWorkspace("combinedws","Combined Workspace")
out_ws._import = getattr(out_ws,"import")

# Need to setup the things here for combined dataset, need to add all possible sample types first because otherwise RooFit throws a fit! 
sampleType  = r.RooCategory("bin_number","Bin Number");
obs         = r.RooRealVar("observed","Observed Events bin",1)

out_ws._import(sampleType)  # Global variables for dataset
out_ws._import(obs)
obsargset   = r.RooArgSet(out_ws.var("observed"),out_ws.cat("bin_number"))

cmb_categories=[]
diag_combined = diagonalizer(out_ws)
for cid,cn in enumerate(categories): 
        _fDir = _fOut.mkdir("category_%s"%cn)
	cmb_categories.append(cmodel(cid,cn,_f,_fDir,out_ws,diag_combined))
        _fDirW = _fOut.mkdir("Wcategory_%s"%cn)
	cmb_categories.append(cmodelW(10+cid,cn,_f,_fDirW,out_ws,diag_combined))
# Had to define the types before adding to the combined dataset
for cid,cn in enumerate(cmb_categories):
	cn.init_channels()
        channels = cn.ret_channels()
        for ch in channels: ch.Print()
out_ws.Print('v')
# Next we want to build a list of all of the nuisance parameters which will be in the fit :), this is performed with add_nuisance
ext_constraints = r.RooArgSet() 
hasSys = False

for cn in cmb_categories:
 for cr in cn.ret_control_regions():
  nuisances = cr.ret_nuisances()+cr.ret_bkg_nuisances()
  for nuis in nuisances:
   hasSys=True
   ext_constraints.add(out_ws.pdf("const_%s"%nuis))

ext_constraints.Print("v")
# Now we have the observation and expectation of all of the bins, make a combined pdf and fit!
# ------------------------------------------------------------
# WRITE THE FIT PART HERE
combined_pdf = r.RooSimultaneous("combined_pdf","combined_pdf",out_ws.cat(sampleType.GetName()))
# Loop through every bin and add the Poisson Pdf
for cid,cn in enumerate(cmb_categories):
  channels = cn.ret_channels()
  for ch in channels: 
    combined_pdf.addPdf(out_ws.pdf("pdf_%s"%ch.ret_binid()),ch.ret_binid())
if hasSys: combined_fit_result = combined_pdf.fitTo(out_ws.data("combinedData"),r.RooFit.Save(),r.RooFit.ExternalConstraints(ext_constraints))
else: combined_fit_result = combined_pdf.fitTo(out_ws.data("combinedData"),r.RooFit.Save())
# ------------------------------------------------------------
# Now Generate the systematics coming from the fitting 
npars = diag_combined.generateVariations(combined_fit_result)
h2covar = diag_combined.retCovariance()
_fOut.WriteTObject(h2covar)
h2corr = diag_combined.retCorrelation()
_fOut.WriteTObject(h2corr)
# ------------------------------------------------------------
for cat in cmb_categories:
   cat.save_model(diag_combined)          # Saves the nominal model and makes templates for variations from each uncorrelated parameter :) 
   cat.generate_systematic_templates(diag_combined,npars)
   cat.make_post_fit_plots() # Makes Post-fit to CR plots including approximated error bands from fit variations 
   cat.save() # make plots, save histograms and canvases

for cid,cn in enumerate(cmb_categories):
   channels = cn.ret_channels()
   for ch in channels: ch.Print()

print "Init pars"
combined_fit_result.floatParsInit().Print("v")
print "Final pars"
combined_fit_result.floatParsFinal().Print("v")
# END
print "Produced combined Z(mm) + photon fits -> ", _fOut.GetName()
_fOut.Close()
# END

#from combineControlRegions import *
from counting_experiment import *
import ROOT as r 
r.gROOT.SetBatch(1)
r.gROOT.ProcessLine(".L diagonalizer.cc+")
from ROOT import diagonalizer


def cmodel(cid,nam,_f,_fOut, out_ws, diag):

  _fin = _f.Get("category_%s"%nam)

  _wspace = _fin.Get("wspace_%s"%nam)
  

  metname = "mvamet"
  gvptname= "genVpt"

  try:
    mt = _wspace.var(metname)
    mt.GetName()

  except:
    metname = "mvamet_"

  # First we need to re-build the nominal templates from the datasets modifying the weights
  targetmc     = _fin.Get("signal_wjets")
  controlmc    = _fin.Get("singlemuon_wjets")  # defines in / out acceptance

  WScales = targetmc.Clone(); WScales.SetName("wlv_weights_%s"%nam)
  WScales.Divide(controlmc)
 

  _fOut.WriteTObject(WScales)


  _bins = []  # take bins from some histogram
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  CRs = [
   Channel("W#rightarrow(#mu#nu)+jet",_wspace,out_ws,cid,0,_wspace.data("singlemuon_data"),WScales,"singlemuon_all_background")  # stupid linear fit of Purities, should move to flat 
  #Channel("Dimuon",_wspace,out_ws,cid,0,_wspace.data(_dimuon_datasetname),ZmmScales,_dimuon_backgroundsname)
  ]
  #Add Systematic ? This time we add them as nuisance parameters.

  CRs[0].add_nuisance("MuonEfficiency",0.01)
  CRs[0].add_nuisance("xs_backgroundss",0.1,True)   # is a background systematic

  # Make bin-to-bin errors ?!
  # We want to make a combined model which performs a simultaneous fit in all three categories so first step is to build a combined model in all three 
  return Category(cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,"signal_wjets",CRs,diag)
  
#----------------------------------------------------------------------------------------------------------------------------------------------------------//
_fOut = r.TFile("wjets_model.root","RECREATE")
# run once per category
categories = ["inclusive","resolved","boosted"]
#categories = ["boosted","resolved"]
#categories = ["inclusive"]
_f = r.TFile.Open("mono-x-vtagged.root")
out_ws = r.RooWorkspace("combinedws","WJets")
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
# Had to define the types before adding to the combined dataset
for cid,cn in enumerate(cmb_categories):
	cn.init_channels()
        channels = cn.ret_channels()
        for ch in channels: ch.Print()
out_ws.Print('v')
for cid,cn in enumerate(cmb_categories):
   channels = cn.ret_channels()
   for ch in channels: ch.Print()
#sys.exit()
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
_fOut.WriteTObject(out_ws)
for cid,cn in enumerate(cmb_categories):
   channels = cn.ret_channels()
   for ch in channels: ch.Print()
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

# END
print "Produced W+jets fits -> ", _fOut.GetName()
_fOut.Close()
# END

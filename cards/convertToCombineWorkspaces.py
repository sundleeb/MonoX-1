# This tool converts the histograms/workspaces into the correct setup for directly including the 
# Control regions into the combine tools, should only NEED this to combine with other channels but its nice anyway

varname = "mvamet"

import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
# Output file/ws
fout = ROOT.TFile("mono-x-backgrounds.root","RECREATE")
wsout_combine = ROOT.RooWorkspace("mono-x-ws","mono-x-ws")
wsout_combine._import = getattr(wsout_combine,"import") # workaround: import is a python keyword

# Categories, must be ordered the same as in runCombinedModel.py!
#categories = ["monojet","resolved","boosted"]

categories = {
	 "monojet":0
	,"resolved":1
	,"boosted":2
	}

# Two main input files, these are photon_dimuon_blah.root and mono-x-vtagged.root
# May as well grab the complicated one first 
f_combined_model = ROOT.TFile.Open("photon_dimuon_vBin.root")  # --> Output from runCombinedModel.py
wsin_combine = f_combined_model.Get("combinedws")
wsin_combine.loadSnapshot("PRE_EXT_FIT_Clean")

f_simple_hists = ROOT.TFile.Open("mono-x-vtagged.root")	# --> Output from buildModel.py
# The ever important "X" parameter should come from where? 
# For now we assume it comes from one place but, do it per channel

for cat in (categories.keys()):
  icat = categories[cat]
  # Pick up the category folder 
  fdir = f_simple_hists.Get("category_%s"%cat)
  wlocal = fdir.Get("wspace_%s"%cat)
  # import a Renamed copy of the variable ...
  varl = wlocal.var(varname)
  varnameext = varname+"_%s"%cat
  varl.SetName(varnameext)
  # Keys in the fdir 
  keys_local = fdir.GetListOfKeys() 
  for key in keys_local: 
    obj = key.ReadObj()
    if type(obj)!=type(ROOT.TH1F()): continue
    title = obj.GetTitle()
    if title != "base": continue # Forget all of the histos which aren't the observable variable
    name = obj.GetName()
    if not obj.Integral() > 0 : obj.SetBinContent(1,0.0001) # otherwise Combine will complain!
    print "Creating Data Hist for ", name 
    #dhist = ROOT.RooDataHist(cat+"_"+name,"DataSet - %s, %s"%(cat,name),ROOT.RooArgList(wsin_combine.var(varname)),obj)
    dhist = ROOT.RooDataHist(cat+"_"+name,"DataSet - %s, %s"%(cat,name),ROOT.RooArgList(varl),obj)
    dhist.Print("v")
    wsout_combine._import(dhist)

  # pick up the number of bins FROM one of the usual guys 
  samplehist = fdir.Get("signal_data")
  nbins = samplehist.GetNbinsX()

  # next Add in the V-jets backgrounds MODELS
  wjets_expectations = ROOT.RooArgList()
  for b in range(nbins):
    wjets_expectations.add(wsin_combine.var("model_mu_cat_1%d_bin_%d"%(icat,b)))
  #wjets_phist = ROOT.RooParametricHist("%s_signal_wjets_model"%cat,"Model Shape for W+jets in Category %s"%cat,wsin_combine.var(varname),wjets_expectations,samplehist)
  wjets_phist = ROOT.RooParametricHist("%s_signal_wjets_model"%cat,"Model Shape for W+jets in Category %s"%cat,varl,wjets_expectations,samplehist)
  wjets_phist_norm = ROOT.RooAddition("%s_norm"%wjets_phist.GetName(),"Total number of expected events in %s"%wjets_phist.GetName(),wjets_expectations);

  # next Add in the V-jets backgrounds MODELS
  zjets_expectations = ROOT.RooArgList()
  for b in range(nbins):
    zjets_expectations.add(wsin_combine.var("model_mu_cat_%d_bin_%d"%(icat,b)))
  #zjets_phist = ROOT.RooParametricHist("%s_signal_zjets_model"%cat,"Model Shape for Z+jets in Category %s"%cat,wsin_combine.var(varname),zjets_expectations,samplehist)
  zjets_phist = ROOT.RooParametricHist("%s_signal_zjets_model"%cat,"Model Shape for Z+jets in Category %s"%cat,varl,zjets_expectations,samplehist)
  zjets_phist_norm = ROOT.RooAddition("%s_norm"%zjets_phist.GetName(),"Total number of expected events in %s"%zjets_phist.GetName(),zjets_expectations);

  # Finally add the CONTROL Regions (note backgrounds, except photon, already there)
  # Photon Control Region
  photon_expectations = ROOT.RooArgList()
  for b in range(nbins):
    photon_expectations.add(wsin_combine.function("pmu_cat_%d_ch_0_bin_%d"%(icat,b)))
  #p_phist = ROOT.RooParametricHist("%s_photon_gjet_model"%cat,"Expected Shape for Photons in Photon plus Jet in Category %s"%cat,wsin_combine.var(varname),photon_expectations,samplehist)
  p_phist = ROOT.RooParametricHist("%s_photon_gjet_model"%cat,"Expected Shape for Photons in Photon plus Jet in Category %s"%cat,varl,photon_expectations,samplehist)
  p_phist_norm = ROOT.RooAddition("%s_norm"%p_phist.GetName(),"Total number of expected events in %s"%p_phist.GetName(),photon_expectations);
  # Photon backgrounds not yet produced, do that now!
  pho_bkg_hist = f_combined_model.Get("category_%s/ZJets_photon_gjet_backgrounds_combined_model"%cat)
  pho_bkg_dhist = ROOT.RooDataHist(cat+"_photon_purity_bkg","DataSet - %s, %s"%(cat,name),ROOT.RooArgList(varl),pho_bkg_hist)

  # Dimuon Control Region
  dimuon_expectations = ROOT.RooArgList()
  for b in range(nbins):
    dimuon_expectations.add(wsin_combine.function("pmu_cat_%d_ch_1_bin_%d"%(icat,b)))
  #z_phist = ROOT.RooParametricHist("%s_dimuon_zjets_model"%cat,"Expected Shape for Z in Dimuon control region in Category %s"%cat,wsin_combine.var(varname),dimuon_expectations,samplehist)
  z_phist = ROOT.RooParametricHist("%s_dimuon_zjets_model"%cat,"Expected Shape for Z in Dimuon control region in Category %s"%cat,varl,dimuon_expectations,samplehist)
  z_phist_norm = ROOT.RooAddition("%s_norm"%z_phist.GetName(),"Total number of expected events in %s"%z_phist.GetName(),dimuon_expectations);

  # Single-muon Control Region
  singlemuon_expectations = ROOT.RooArgList()
  for b in range(nbins):
    singlemuon_expectations.add(wsin_combine.function("pmu_cat_1%d_ch_0_bin_%d"%(icat,b)))
  #w_phist = ROOT.RooParametricHist("%s_singlemuon_wjets_model"%cat,"Expected Shape for W in Single muon control region in Category %s"%cat,wsin_combine.var(varname),singlemuon_expectations,samplehist)
  w_phist = ROOT.RooParametricHist("%s_singlemuon_wjets_model"%cat,"Expected Shape for W in Single muon control region in Category %s"%cat,varl,singlemuon_expectations,samplehist)
  w_phist_norm = ROOT.RooAddition("%s_norm"%w_phist.GetName(),"Total number of expected events in %s"%w_phist.GetName(),singlemuon_expectations);

  wsout_combine._import(zjets_phist)
  wsout_combine._import(wjets_phist)
  wsout_combine._import(p_phist)
  wsout_combine._import(pho_bkg_dhist)
  wsout_combine._import(z_phist)
  wsout_combine._import(w_phist)
  wsout_combine._import(zjets_phist_norm,ROOT.RooFit.RecycleConflictNodes())
  wsout_combine._import(wjets_phist_norm,ROOT.RooFit.RecycleConflictNodes())
  wsout_combine._import(p_phist_norm,ROOT.RooFit.RecycleConflictNodes())
  wsout_combine._import(z_phist_norm,ROOT.RooFit.RecycleConflictNodes())
  wsout_combine._import(w_phist_norm,ROOT.RooFit.RecycleConflictNodes())


fout.WriteTObject(wsout_combine)
wsout_combine.Print()

# HELP US OUT BY PRINTING NUISANCES 
allparams = ROOT.RooArgList(wsout_combine.allVars())
for pi in range(allparams.getSize()):
#for par in allparams:
  par = allparams.at(pi)
  if not par.getAttribute("NuisanceParameter_EXTERNAL") : continue 
  if par.getAttribute("BACKGROUND_NUISANCE"): continue # these aren't in fact used for combine
  print par.GetName(), "param", par.getVal(), "1" 
print "Done -- Combine Ready Workspace inside ",fout.GetName()


import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

def convertToCombineWorkspace(wsin_combine,f_simple_hists,categories,cmb_categories,controlregions_def):

#wsout_combine = ROOT.RooWorkspace("mono-x-ws","mono-x-ws")
#wsout_combine._import = getattr(wsout_combine,"import") # workaround: import is a python keyword
#wsin_combine = f_combined_model.Get("combinedws")
  wsin_combine.loadSnapshot("PRE_EXT_FIT_Clean")

  for icat, cat in enumerate(categories):

   # Pick up the category folder 
   fdir = f_simple_hists.Get("category_%s"%cat)
   wlocal = fdir.Get("wspace_%s"%cat)

   # pick up the number of bins FROM one of the usual guys 
   samplehist = fdir.Get("signal_data")
   nbins = samplehist.GetNbinsX()
   varname = samplehist.GetXaxis().GetTitle()

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
    dhist = ROOT.RooDataHist(cat+"_"+name,"DataSet - %s, %s"%(cat,name),ROOT.RooArgList(varl),obj)
    dhist.Print("v")
    wsin_combine._import(dhist)


   # next Add in the V-jets backgrounds MODELS
   for crd,crn in enumerate(controlregions_def):
     # check the category 
     x = __import__(crn)
     expectations = ROOT.RooArgList()
     for b in range(nbins):
       #print "model_mu_cat_%d_bin_%d"%(10*crd+icat,b), wsin_combine.var( "model_mu_cat_%d_bin_%d"%(10*crd+icat,b))
       expectations.add(wsin_combine.var("model_mu_cat_%d_bin_%d"%(10*crd+icat,b)))
     phist = ROOT.RooParametricHist("%s_signal_%s_model"%(cat,x.model),"Model Shape for %s in Category %s"%(x.model,cat),varl,expectations,samplehist)
     phist_norm = ROOT.RooAddition("%s_norm"%phist.GetName(),"Total number of expected events in %s"%phist.GetName(),expectations)

     wsin_combine._import(phist)
     wsin_combine._import(phist_norm)


     # now loop through the "control regions" for this guy 
     for cid,cn in enumerate(cmb_categories):
       	if cn.catid != 10*crd+icat : continue
	for cr in cn.ret_control_regions():
	 print "CHECK", cn.catid,cr.chid
         chid = cr.chid
         cr_expectations = ROOT.RooArgList()
         for b in range(nbins):
          cr_expectations.add(wsin_combine.function("pmu_cat_%d_ch_%d_bin_%d"%(icat+10*crd,chid,b)))
         p_phist = ROOT.RooParametricHist("%s_%s_%s_model"%(cat,cr.crname,x.model),"Expected Shape for %s in control region in Category %s"%(cr.crname,cat),varl,cr_expectations,samplehist)
         p_phist_norm = ROOT.RooAddition("%s_norm"%p_phist.GetName(),"Total number of expected events in %s"%p_phist.GetName(),cr_expectations);
         wsin_combine._import(p_phist)
         wsin_combine._import(p_phist_norm)

  allparams = ROOT.RooArgList(wsin_combine.allVars())
  for pi in range(allparams.getSize()):
  #for par in allparams:
    par = allparams.at(pi)
    if not par.getAttribute("NuisanceParameter_EXTERNAL") : continue 
    if par.getAttribute("BACKGROUND_NUISANCE"): continue # these aren't in fact used for combine
    print par.GetName(), "param", par.getVal(), "1" 
  #print "Done -- Combine Ready Workspace inside ",fout.GetName()


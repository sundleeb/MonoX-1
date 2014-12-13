# Script to build a rather specific binned shape model
# We have a dataset (observation) and a parameteric model (pdf)
# and a set of bins we want to build from them
# Please note This script only exists because of how ridiculous RooFit is not evaluating integrals over bins!!!!
# N. Wardle 

import sys,array
from counting_experiment import *

import ROOT as r

_bins = []
 
def fillModelHist(model_hist,channels):

  for i,ch in enumerate(channels):
    if i>=len(_bins)-1: break
    model_hist.SetBinContent(i+1,ch.ret_model())

# This is a bit silly but necessary for naming conventions 
def getNormalizedHist(hist):
  thret = hist.Clone()
  nb = hist.GetNbinsX()
  for b in range(1,nb+1): 
    sfactor = 1./hist.GetBinWidth(b)
    thret.SetBinContent(b,hist.GetBinContent(b)*sfactor)
    thret.SetBinError(b,hist.GetBinError(b)*sfactor)
    #thret.GetYaxis().SetTitle("Events")
    thret.GetYaxis().SetTitle("Events/GeV")
  return thret

#Main 
# some globals

def CombinedControlRegionFit(
  _fin #TDirectory   
  ,_fOut #and output file 
  ,_wspace # RooWorkspace
  ,_examplehistname # histogram template
  ,_varname	    # name of the variale
  ,_pdfname	    # name of a double exp pdf
  ,_target_datasetname # only for initial fit values
  ,_control_regions # CRs constructed
   ):

  # Make some output directory
  _fout = _fOut.mkdir("combined_control_fit") 

  th_ex = _fin.Get(_examplehistname)

  #_bins = []  # take bins from some histogram
  for b in range(th_ex.GetNbinsX()+1):
    _bins.append(th_ex.GetBinLowEdge(b+1))

  _var  = _wspace.var(_varname)

  _pdf  = _wspace.pdf(_pdfname)
  _data_mc = _wspace.data(_target_datasetname)
  _pdf.fitTo(_data_mc)  # Just initialises parameters 

  _norm = r.RooRealVar("%s_norm"%_target_datasetname,"Norm",_wspace.data(_target_datasetname).sumEntries())
  _norm.setConstant(False)
  fr = _var.frame()
  _wspace.data(_target_datasetname).plotOn(fr,r.RooFit.Binning(200))
  _pdf.plotOn(fr)
  #_pdf.paramOn(fr)
  c = r.TCanvas("zjets_signalregion_mc_fit")
  fr.Draw()

  # Setup stuff for the simultaneous fitting, this isn't particularly good since we loop twice without needing to
  sample = r.RooCategory("bin_number","bin_number")
  for j,cr in enumerate(_control_regions):
   for i,bl in enumerate(_bins):
    if i >= len(_bins)-1 : continue
    sample.defineType("ch_%d_bin_%d"%(j,i),MAXBINS*j+i)

  # Loop again, this time setting up each of the bins and linking the pdf 
  # Construct a "channel" (bin) from each bin of the histogram
  channels = []
  combined_obsdata = 0
  for j,cr in enumerate(_control_regions):
   for i,bl in enumerate(_bins):
    if i >= len(_bins)-1 : continue

    xmin,xmax = bl,_bins[i+1]

    ch = Bin(j,i,_var,cr.ret_dataset(),_pdf,_norm,_wspace,xmin,xmax)
    ch.set_control_region(cr)
    if cr.has_background(): ch.add_background(cr.ret_background())
    ch.set_label(sample) # should import the sample category label
    ch.set_sfactor(cr.ret_sfactor(i))
    # This has to the the last thing
    ch.setup_expect_var()

    obsargset = r.RooArgSet(_wspace.var("observed"),_wspace.cat(sample.GetName()))
    if i==0 and j==0 : combined_obsdata = r.RooDataSet("combinedData","Data in all Bins",obsargset)
    ch.add_to_dataset(combined_obsdata)
    #ch.Print()
    channels.append(ch)

  # Now we make a roosimultaneous pdf from the product of the bin pdfs!
  binset = r.RooArgList("bins_set")

  # now we have to build the combined dataset/pdf -> Observation in each bin (var is just obs) and the pdf (already availale)
  # -> Make a RooSimultaneous across each channel

  combined_pdf = r.RooSimultaneous("combined_pdf","combined_pdf",_wspace.cat(sample.GetName()))
  for ch in channels:
    print _wspace.pdf("pdf_%s"%ch.ret_binid())
    combined_pdf.addPdf(_wspace.pdf("pdf_%s"%ch.ret_binid()),ch.ret_binid())

  # Now check systematics, we wont use this right now
  """
  ext_constraints = r.RooArgSet()
  hasSys = False
  for cr in _control_regions:
    nuisances = cr.ret_nuisances()
    for nuis in nuisances:
      hasSys=True
      ext_constraints.add(_wspace.pdf("const_%s"%nuis))
  """
  # THE FIIIIIIIIIIIIIT!!!!!!!!!!!!!!!!!!!!!!!!!!!! ################################
  # NEED to add constrain terms on top -> Nah, don't bother!
  combined_fit_result = combined_pdf.fitTo(combined_obsdata,r.RooFit.Save())
  # #################################################################################

  # plot on NEW fit ? 
  #_pdf.plotOn(fr,r.RooFit.LineColor(r.kRed),r.RooFit.Normalization(_norm.getVal(),r.RooAbsReal.NumEvent))
  # Having fit, we can spit out every channel expectation and observation into a histogram!
  c2 = r.TCanvas("compare_models")
  model_hist = r.TH1F("combined_model","combined_model",len(_bins)-1,array.array('d',_bins))
  fillModelHist(model_hist,channels)
  channels[0].Print()
  model_hist.SetLineWidth(2)
  model_hist.SetLineColor(1)
  #_fout = r.TFile("combined_model.root","RECREATE")
  _fout.WriteTObject(model_hist)

  # Now plot the control Regions too!
  crhists = []
  canvs   = []
  for j,cr in enumerate(_control_regions):
    c3 = r.TCanvas("c_%s"%cr.ret_name())
    cr_hist = r.TH1F("control_region_%s"%cr.ret_name(),"%s control region"%cr.ret_name(),len(_bins)-1,array.array('d',_bins))
    da_hist = r.TH1F("data_control_region_%s"%cr.ret_name(),"data %s control region"%cr.ret_name(),len(_bins)-1,array.array('d',_bins))
    mc_hist = r.TH1F("mc_control_region_%s"%cr.ret_name(),"mc %s control region"%cr.ret_name(),len(_bins)-1,array.array('d',_bins))
  
    bc = 1
    for i in range(j*(len(_bins)-1),(j+1)*(len(_bins)-1) ):
      ch = channels[i]
      #if i>=len(_bins)-1: break
      print "Channel", j, "Bin ",i, channels[i].ret_expected()
      cr_hist.SetBinContent(bc,ch.ret_expected())
      da_hist.SetBinContent(bc,ch.ret_observed())
      mc_hist.SetBinContent(bc,ch.ret_background())
      print ch.ret_background()
      da_hist.SetBinError(bc,(ch.ret_observed())**0.5)
      cr_hist.SetFillColor(r.kBlue-9)
      mc_hist.SetFillColor(r.kRed+3)
      bc+=1

    cr_hist = getNormalizedHist(cr_hist)
    da_hist = getNormalizedHist(da_hist)
    mc_hist = getNormalizedHist(mc_hist)
    cr_hist.SetLineColor(1)
    mc_hist.SetLineColor(1)
    da_hist.SetMarkerColor(1)
    da_hist.SetLineColor(1)
    da_hist.SetMarkerStyle(20)
    crhists.append(da_hist)
    crhists.append(cr_hist)
    crhists.append(mc_hist)
    da_hist.Draw("Pe")
    cr_hist.Draw("samehist")
    mc_hist.Draw("samehist")
    da_hist.Draw("Pesame")
    canvs.append(c3)
    _fout.WriteTObject(cr_hist)
    _fout.WriteTObject(da_hist)
    _fout.WriteTObject(mc_hist)
    _fout.WriteTObject(c3)

  # Ok now the task will be to calculate the uncertainties!, simply diagonalize again and re-calculate histograms given +/- 1 sigmas
  # The first kind are rather straightforward and due to statistical uncertainties
  r.gROOT.ProcessLine(".L diagonalizer.cc+")
  from ROOT import diagonalizer
  diag = diagonalizer(_wspace)
  npars = diag.generateVariations(combined_fit_result)
  h2covar = diag.retCovariance()
  _fout.WriteTObject(h2covar)
  canv = r.TCanvas("canv_variations")
  model_hist_spectrum = getNormalizedHist(model_hist)
  model_hist_spectrum.Draw()
  systs = []

  for par in range(npars):
    hist_up = r.TH1F("combined_model_par_%d_Up"%par,"combined_model par %d Up 1 sigma"%par  ,len(_bins)-1,array.array('d',_bins))
    hist_dn = r.TH1F("combined_model_par_%d_Down"%par,"combined_model par %d Up 1 sigma"%par,len(_bins)-1,array.array('d',_bins))
 
    diag.setEigenset(par,1)  # up variation
    fillModelHist(hist_up,channels)

    diag.setEigenset(par,-1)  # up variation
    fillModelHist(hist_dn,channels)

    # Reset parameter values 
    diag.resetPars()
    canv.cd()
    hist_up.SetLineWidth(2)
    hist_dn.SetLineWidth(2)
    hist_up.SetLineColor(par+2)
    hist_dn.SetLineColor(par+2)
    hist_dn.SetLineStyle(2)

    _fout.WriteTObject(hist_up)
    _fout.WriteTObject(hist_dn)

    hist_up = getNormalizedHist(hist_up)
    hist_dn = getNormalizedHist(hist_dn)
  
    systs.append(hist_up)
    systs.append(hist_dn)

    hist_up.Draw("samehist")
    hist_dn.Draw("samehist")

    ct = r.TCanvas("sys_par_%d"%par)
    flat = model_hist.Clone()
    hist_up_cl = hist_up.Clone()
    hist_dn_cl = hist_dn.Clone()
    hist_up_cl.Divide(model_hist_spectrum)
    hist_dn_cl.Divide(model_hist_spectrum)
    hist_up_cl.Draw('hist')
    hist_dn_cl.Draw('histsame')
    flat.Divide(model_hist)
    flat.Draw("histsame")
    _fout.WriteTObject(ct)

  for ch in channels: ch.Print()
  # Final step is to produce alternate templates due to systematic shifts. Loope through and re-fit for each change.
  all_systs = []
  for cr in _control_regions: 
    for sysk in cr.systematics.keys():
  	all_systs.append(sysk)
  all_systs = set(all_systs)

  for syst in all_systs: 
    #BLEH swap out the scale-factors for new set, simply amounts to resetting the s-factors for each :)
    # need to figure out what cr is and what ch is 
    for i,ch in enumerate(channels):
      cr = _control_regions[ch.chid]
      ch.set_sfactor(cr.ret_sfactor(ch.id,syst,1))

    combined_pdf.fitTo(combined_obsdata)
    model_hist_sys_up = r.TH1F("combined_model_%sUp"%syst,"combined_model %s Up 1 sigma"%syst  ,len(_bins)-1,array.array('d',_bins))#Sys_Up
    fillModelHist(model_hist_sys_up,channels)

    # Reset the scale_factors
    for i,ch in enumerate(channels):
      cr = _control_regions[ch.chid]
      ch.set_sfactor(cr.ret_sfactor(ch.id,syst,-1))

    combined_pdf.fitTo(combined_obsdata)
    model_hist_sys_dn = r.TH1F("combined_model_%sDown"%syst,"combined_model %s Sown 1 sigma"%syst  ,len(_bins)-1,array.array('d',_bins))#Sys_Dn
    fillModelHist(model_hist_sys_dn,channels)
    # remake combined fit!
    _fout.WriteTObject(model_hist_sys_up)
    _fout.WriteTObject(model_hist_sys_dn)

  _fout.WriteTObject(c)
  _fout.WriteTObject(canv)
  #_fout.Close()

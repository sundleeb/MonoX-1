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
  cname # name for the parametric variation templates
  ,_fin #TDirectory   
  ,_fout #and output file 
  ,_wspace # RooWorkspace
  ,_bins  # just get the bins
  ,_varname	    # name of the variale
  ,_pdfname	    # name of a double exp pdf
  ,_pdfname_zvv	    # name of a double exp pdf to use as zvv mc fit
  ,_target_datasetname # only for initial fit values
  ,_control_regions # CRs constructed
   ):

  # Make some output directory
  #_fout = _fOut.mkdir("combined_control_fit") 

  #th_ex = _fin.Get(_examplehistname)
  #th_ex.SetName(th_ex.GetName()+cname)
  r.gROOT.ProcessLine(".L diagonalizer.cc+")
  from ROOT import diagonalizer
  diag = diagonalizer(_wspace)

  _var  = _wspace.var(_varname)

  _pdf      = _wspace.pdf(_pdfname)
  _pdf_orig = _wspace.pdf(_pdfname_zvv)
  _data_mc  = _wspace.data(_target_datasetname)

  diag.freezeParameters(_pdf_orig.getParameters(_data_mc),False)
  _pdf_orig.fitTo(_data_mc)  # Just initialises parameters 
  _pdf.fitTo(_data_mc)       # Just initialises parameters 

  _norm = r.RooRealVar("%s_norm"%_target_datasetname,"Norm",_wspace.data(_target_datasetname).sumEntries())
  _norm.removeRange()
  _norm_orig= r.RooRealVar("%s_norm_orig"%_target_datasetname,"Norm_orig",_wspace.data(_target_datasetname).sumEntries())
  _norm.setConstant(False)
  _norm_orig.setConstant(True)
  _wspace._import(_norm)
  _wspace._import(_norm_orig)
  fr = _var.frame()
  _wspace.data(_target_datasetname).plotOn(fr,r.RooFit.Binning(200))
  diag.freezeParameters(_pdf_orig.getParameters(_data_mc))
  _pdf_orig.plotOn(fr)
  _pdf.getParameters(_data_mc).Print("v")
  _pdf_orig.getParameters(_data_mc).Print("v")
  #sys.exit()

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
  cr_histos_exp_prefit=[]
  for j,cr in enumerate(_control_regions):
  #save the prefit histos
    cr_pre_hist = r.TH1F("control_region_%s"%cr.ret_name(),"Expected %s control region"%cr.ret_name(),len(_bins)-1,array.array('d',_bins))
    bc=1
    for i in range(j*(len(_bins)-1),(j+1)*(len(_bins)-1) ):
      ch = channels[i]
      #if i>=len(_bins)-1: break
      cr_pre_hist.SetBinContent(bc,ch.ret_expected())
      bc+=1
    cr_pre_hist.SetLineWidth(2)
    cr_pre_hist.SetLineColor(r.kGreen+1)
    cr_histos_exp_prefit.append(cr_pre_hist.Clone())
  # THE FIIIIIIIIIIIIIT!!!!!!!!!!!!!!!!!!!!!!!!!!!! ################################
  # NEED to add constrain terms on top -> Nah, don't bother!
  combined_fit_result = combined_pdf.fitTo(combined_obsdata,r.RooFit.Save())
  # #################################################################################
  # Make the ratio of new/original fits
  ratioargs = r.RooArgList(_norm,_pdf,_norm_orig,_pdf_orig)
  pdf_ratio = r.RooFormulaVar("ratio_correction_%s"%cname,"Correction for Zvv from dimuon+photon control regions","@0*@1/(@2*@3)",ratioargs)
  _wspace._import(pdf_ratio)
  #

  # plot on NEW fit ? 
  _pdf.plotOn(fr,r.RooFit.LineColor(r.kRed),r.RooFit.Normalization(_norm.getVal(),r.RooAbsReal.NumEvent))
  #_pdf.paramOn(fr)
  c = r.TCanvas("zjets_signalregion_mc_fit_before_after")
  fr.GetXaxis().SetTitle("fake MET (GeV)")
  fr.GetYaxis().SetTitle("Events/GeV")
  fr.SetTitle("")
  fr.Draw()
  _fout.WriteTObject(c)

  crat = r.TCanvas("ratio_correction")
  frrat = _var.frame()
  pdf_ratio.plotOn(frrat)
  frrat.Draw()
  _fout.WriteTObject(crat)

  # Having fit, we can spit out every channel expectation, we can correct the MC using it!
  c2 = r.TCanvas("compare_models")
  model_hist = r.TH1F("%s_combined_model"%cname,"combined_model",len(_bins)-1,array.array('d',_bins))
  #fillModelHist(model_hist,channels)
  diag.generateWeightedTemplate(model_hist,_wspace.function(pdf_ratio.GetName()),_wspace.var(_var.GetName()),_wspace.data(_target_datasetname))
  channels[0].Print()
  model_hist.SetLineWidth(2)
  model_hist.SetLineColor(1)
  #_fout = r.TFile("combined_model.root","RECREATE")
  _fout.WriteTObject(model_hist)

  # Now plot the control Regions too!
  crhists = []
  canvs   = []

  lat = r.TLatex();
  lat.SetNDC();
  lat.SetTextSize(0.04);
  lat.SetTextFont(42);
  
  for j,cr in enumerate(_control_regions):
    c3 = r.TCanvas("c_%s"%cr.ret_name(),"",800,800)
    cr_hist = r.TH1F("control_region_%s"%cr.ret_name(),"Expected %s control region"%cr.ret_name(),len(_bins)-1,array.array('d',_bins))
    da_hist = r.TH1F("data_control_region_%s"%cr.ret_name(),"data %s control region"%cr.ret_name(),len(_bins)-1,array.array('d',_bins))
    mc_hist = r.TH1F("mc_control_region_%s"%cr.ret_name(),"Background %s control region"%cr.ret_name(),len(_bins)-1,array.array('d',_bins))
    da_hist.SetTitle("") 
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
    pre_hist = getNormalizedHist(cr_histos_exp_prefit[j])
    cr_hist.SetLineColor(1)
    mc_hist.SetLineColor(1)
    da_hist.SetMarkerColor(1)
    da_hist.SetLineColor(1)
    da_hist.SetMarkerStyle(20)
    crhists.append(da_hist)
    crhists.append(cr_hist)
    crhists.append(mc_hist)
    crhists.append(pre_hist)

    pad1 = r.TPad("p1","p1",0,0.28,1,1)
    pad1.SetBottomMargin(0.01)
    pad1.SetCanvas(c3)
    pad1.Draw()
    pad1.cd()
    tlg = r.TLegend(0.6,0.67,0.89,0.89)
    tlg.SetFillColor(0)
    tlg.SetTextFont(42)
    tlg.AddEntry(da_hist,"Data - %s"%cr.ret_title(),"PEL") 
    tlg.AddEntry(cr_hist,"Expected (post-fit)","F") 
    tlg.AddEntry(mc_hist,"Backgrounds Component","F")
    tlg.AddEntry(pre_hist,"Expected (pre-fit)","L")
    da_hist.GetYaxis().SetTitle("Events/GeV");
    da_hist.GetXaxis().SetTitle("fake MET (GeV)");
    da_hist.Draw("Pe")
    cr_hist.Draw("samehist")
    mc_hist.Draw("samehist")
    pre_hist.Draw("samehist")
    da_hist.Draw("Pesame")
    tlg.Draw()
    lat.DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
    pad1.SetLogy()

    # Ratio plot
    c3.cd()
    pad2 = r.TPad("p2","p2",0,0.068,1,0.28)
    pad2.SetTopMargin(0.02)
    pad2.SetCanvas(c3)
    pad2.Draw()
    pad2.cd()
    ratio = da_hist.Clone()
    ratio_pre = da_hist.Clone()
    ratio.GetYaxis().SetRangeUser(0.01,1.99)
    ratio.Divide(cr_hist)
    ratio_pre.Divide(pre_hist)
    ratio.GetYaxis().SetTitle("Data/Bkg")
    ratio.GetYaxis().SetNdivisions(5)
    ratio.GetYaxis().SetLabelSize(0.1)
    ratio.GetYaxis().SetTitleSize(0.12)
    ratio.GetXaxis().SetTitleSize(0.085)
    ratio.GetXaxis().SetLabelSize(0.12)
    crhists.append(ratio)
    crhists.append(ratio_pre)
    ratio.GetXaxis().SetTitle("")
    ratio.Draw()
    ratio_pre.SetLineColor(pre_hist.GetLineColor())
    ratio_pre.SetMarkerColor(pre_hist.GetLineColor())
    line = r.TLine(da_hist.GetXaxis().GetXmin(),1,da_hist.GetXaxis().GetXmax(),1)
    line.SetLineColor(2)
    line.SetLineWidth(3)
    line.Draw()
    ratio.Draw("same")
    ratio_pre.Draw("pelsame")
    ratio.Draw("samepel")


    canvs.append(c3)
    _fout.WriteTObject(cr_hist)
    _fout.WriteTObject(da_hist)
    _fout.WriteTObject(mc_hist)
    _fout.WriteTObject(c3)

  for bl in channels : bl.Print()
  print _wspace.data(_target_datasetname).sumEntries(), _wspace.var(_norm.GetName()).getVal();
  # Do we really need to re-get the pdf_ratio?dd
  # Ok now the task will be to calculate the uncertainties!, simply diagonalize again and re-calculate histograms given +/- 1 sigmas
  # The first kind are rather straightforward and due to statistical uncertainties
  npars = diag.generateVariations(combined_fit_result)
  h2covar = diag.retCovariance()
  _fout.WriteTObject(h2covar)
  leg_var = r.TLegend(0.56,0.42,0.89,0.89)
  leg_var.SetFillColor(0)
  leg_var.SetTextFont(42)

  canv = r.TCanvas("canv_variations")
  canvr = r.TCanvas("canv_variations_ratio")
  model_hist_spectrum = getNormalizedHist(model_hist)
  model_hist_spectrum.Draw()
  systs = []
  sys_c=0
  for par in range(npars):
    hist_up = r.TH1F("%s_combined_model_par_%d_Up"%(cname,par),"combined_model par %d Up 1 sigma"%par  ,len(_bins)-1,array.array('d',_bins))
    hist_dn = r.TH1F("%s_combined_model_par_%d_Down"%(cname,par),"combined_model par %d Up 1 sigma"%par,len(_bins)-1,array.array('d',_bins))
 
    diag.setEigenset(par,1)  # up variation
    #fillModelHist(hist_up,channels)
    diag.generateWeightedTemplate(hist_up,_wspace.function(pdf_ratio.GetName()),_wspace.var(_var.GetName()),_wspace.data(_target_datasetname))

    diag.setEigenset(par,-1)  # up variation
    #fillModelHist(hist_dn,channels)
    diag.generateWeightedTemplate(hist_dn,_wspace.function(pdf_ratio.GetName()),_wspace.var(_var.GetName()),_wspace.data(_target_datasetname))

    # Reset parameter values 
    diag.resetPars()
    canv.cd()
    hist_up.SetLineWidth(2)
    hist_dn.SetLineWidth(2)
    if sys_c+2 == 10: sys_c+=1
    hist_up.SetLineColor(sys_c+2)
    hist_dn.SetLineColor(sys_c+2)
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
    hist_up_cl = hist_up.Clone();hist_up_cl.SetName(hist_up_cl.GetName()+"_ratio")
    hist_dn_cl = hist_dn.Clone();hist_dn_cl.SetName(hist_dn_cl.GetName()+"_ratio")
    hist_up_cl.Divide(model_hist_spectrum)
    hist_dn_cl.Divide(model_hist_spectrum)
    hist_up_cl.Draw('hist')
    hist_dn_cl.Draw('histsame')
    flat.Divide(model_hist)
    flat.Draw("histsame")
    _fout.WriteTObject(ct)
    canvr.cd()
    if par==0: flat.Draw("hist")
    systs.append(flat)
    systs.append(hist_up_cl)
    systs.append(hist_dn_cl)
    hist_up_cl.Draw('histsame')
    hist_dn_cl.Draw('histsame')
    leg_var.AddEntry(hist_up_cl,"Parameter %d"%par,"L")
    sys_c+=1
  
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
    #fillModelHist(model_hist_sys_up,channels)
    diag.generateWeightedTemplate(model_hist_sys_up,_wspace.function(pdf_ratio.GetName()),_wspace.var(_var.GetName()),_wspace.data(_target_datasetname))

    # Reset the scale_factors
    for i,ch in enumerate(channels):
      cr = _control_regions[ch.chid]
      ch.set_sfactor(cr.ret_sfactor(ch.id,syst,-1))

    combined_pdf.fitTo(combined_obsdata)
    model_hist_sys_dn = r.TH1F("combined_model_%sDown"%syst,"combined_model %s Sown 1 sigma"%syst  ,len(_bins)-1,array.array('d',_bins))#Sys_Dn
    #fillModelHist(model_hist_sys_dn,channels)
    diag.generateWeightedTemplate(model_hist_sys_dn,_wspace.function(pdf_ratio.GetName()),_wspace.var(_var.GetName()),_wspace.data(_target_datasetname))
    # remake combined fit!
    _fout.WriteTObject(model_hist_sys_up)
    _fout.WriteTObject(model_hist_sys_dn)
    model_hist_sys_up= getNormalizedHist(model_hist_sys_up)
    model_hist_sys_dn= getNormalizedHist(model_hist_sys_dn)
    if sys_c+2 == 10 : sys_c+=1
    model_hist_sys_up.SetLineColor(sys_c+2)
    model_hist_sys_dn.SetLineColor(sys_c+2)
    model_hist_sys_up.SetLineWidth(2)
    model_hist_sys_dn.SetLineWidth(2)
    model_hist_sys_dn.SetLineStyle(2)

    canv.cd()
    model_hist_sys_up.Draw("histsame")
    model_hist_sys_dn.Draw("histsame")
    systs.append(model_hist_sys_up)
    systs.append(model_hist_sys_dn)
    model_hist_sys_up_cl = model_hist_sys_up.Clone(); model_hist_sys_up_cl.SetName(model_hist_sys_up_cl.GetName()+"_ratio")
    model_hist_sys_dn_cl = model_hist_sys_dn.Clone(); model_hist_sys_dn_cl.SetName(model_hist_sys_dn_cl.GetName()+"_ratio")
    model_hist_sys_up_cl.Divide(model_hist_spectrum)
    model_hist_sys_dn_cl.Divide(model_hist_spectrum)
    systs.append(model_hist_sys_up_cl)
    systs.append(model_hist_sys_dn_cl)
    canvr.cd()
    model_hist_sys_up_cl.Draw("histsame")
    model_hist_sys_dn_cl.Draw("histsame")

    leg_var.AddEntry(model_hist_sys_up,"%s"%syst,"L")
    sys_c+=1

  _fout.WriteTObject(c)
  canv.cd(); 
  leg_var.Draw()
  canvr.cd();
  leg_var.Draw()
  _fout.WriteTObject(canv)
  _fout.WriteTObject(canvr)
  #_fout.Close()

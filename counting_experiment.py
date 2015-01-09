import ROOT as r
import sys
import array 

MAXBINS=100

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


class Bin:
 def __init__(self,catid,chid,id,var,datasetname,pdf,norm,wspace,wspace_out,xmin,xmax):

   self.chid	  = chid# This is the thing that links two bins from different controls togeher
   self.id        = id
   self.type_id   = 10*MAXBINS*catid+MAXBINS*chid+id
   self.binid     = "cat_%d_ch_%d_bin_%d"%(catid,chid,id)
   self.wspace_out = wspace_out
   self.set_wspace(wspace)
   self.set_norm_var(norm)

   self.var	  = self.wspace.var(var.GetName())
   self.dataset   = self.wspace.data(datasetname)
   self.pdf	  = pdf 
   self.rngename = "rnge_%s"%self.binid
   self.var.setRange(self.rngename,xmin,xmax)
   self.xmin = xmin
   self.xmax = xmax
   self.cen = (xmax+xmin)/2

   self.binerror = 10

   self.o	= self.dataset.sumEntries("%s>=%g && %s<%g "%(var.GetName(),xmin,var.GetName(),xmax))
   #self.o	= (self.wspace.data(datasetname)).sumEntries("1>0",self.rngename)
   self.obs	= self.wspace_out.var("observed")#r.RooRealVar("observed","Observed Events bin",1)
   #self.setup_expect_var(self)
   self.argset = r.RooArgSet(self.var)
   self.obsargset=r.RooArgSet(self.wspace_out.var("observed"),self.wspace_out.cat("bin_number"))
   self.var.setRange("fullRange",self.var.getMin(),self.var.getMax())
   
   self.pdfFullInt = pdf.createIntegral(self.argset,r.RooFit.Range("fullRange"),r.RooFit.NormSet(self.argset))
   #if not self.wspace.var(self.pdfFullInt.GetName()) : self.wspace._import(self.pdfFullInt)
   self.wspace._import(self.pdfFullInt,r.RooFit.RecycleConflictNodes())
   self.b  = 0
   self.constBkg = True

 def add_background(self,bkg):
   if "Purity" in bkg:
     tmp_pfunc = r.TF1("tmp_bkg_%s"%self.id,bkg.split(":")[-1]) #?
     self.b       = tmp_pfunc.Eval(self.cen)
     self.constBkg = False
   else:
     bkg_set      = self.wspace.data(bkg)
     self.b	= bkg_set.sumEntries("%s>=%g && %s<%g "%(self.var.GetName(),self.xmin,self.var.GetName(),self.xmax)) 

 def set_label(self,cat):
   self.categoryname = cat.GetName()
   #self.wspace._import(cat,r.RooFit.RecycleConflictNodes())

 def set_wspace(self,w):
   self.wspace = w
   self.wspace._import = getattr(self.wspace,"import") # workaround: import is a python keyword

 def set_norm_var(self,v):
   self.normvar = self.wspace.var(v.GetName())

 def set_sfactor(self,val):
   #print "Scale Factor for " ,self.binid,val
   if self.wspace.var("sfactor_%s"%self.binid): 
    self.sfactor.setVal(val)
    self.wspace.var(self.sfactor.GetName()).setVal(val)
   else:
     self.sfactor = r.RooRealVar("sfactor_%s"%self.binid,"Scale factor for bin %s"%self.binid,val,0.00001,10000); 
     self.sfactor.removeRange()
     self.sfactor.setConstant()
     self.wspace._import(self.sfactor,r.RooFit.RecycleConflictNodes())

 def setup_expect_var(self):
   # This will be the RooRealVar containing the value of the number of expected events in this bin
   self.integral = self.pdf.createIntegral(self.argset,r.RooFit.Range(self.rngename),r.RooFit.NormSet(self.argset))
   self.wspace._import(self.integral,r.RooFit.RecycleConflictNodes())
   if not self.wspace.function("model_mu_%d"%self.id):
     self.model_mu = r.RooFormulaVar("model_mu_%d"%self.id,"Model of N expected events in %d"%self.id,"@0*@1/@2",r.RooArgList(
        self.wspace.function(self.integral.GetName())
     	,self.wspace.var(self.normvar.GetName())
	,self.wspace.function(self.pdfFullInt.GetName()))) # in reality this will be given and depend on the integral of the pdf!
     self.wspace._import(self.model_mu,r.RooFit.RecycleConflictNodes())
   else: self.model_mu = self.wspace.function("model_mu_%d"%self.id)

   arglist = r.RooArgList((self.model_mu),self.wspace.var(self.sfactor.GetName()))
   
   # Multiply by each of the uncertainties in the control region, dont alter the Poisson pdf, we will add the constraint at the end. Actually we won't use this right now.
   nuisances = self.cr.ret_nuisances()
   if len(nuisances)>0:
     prod = 0
     if len(nuisances)>1:
       nuis_args = r.RooArgList()
       for nuis in nuisances:
        print "Adding Nuisance ", nuis 
     	delta_nuis = r.RooFormulaVar("delta_%s_%s"%(self.binid,nuis),"Delta Change from %s"%nuis,"1+@0",r.RooArgList(self.wspace.var("nuis_%s"%nuis)))
        self.wspace._import(delta_nuis,r.RooFit.RecycleConflictNodes())
     	nuis_args.add(self.wspace.function(delta_nuis.GetName()))
       nuis_args.Print("v")
       prod = r.RooProduct("prod_%s"%self.binid,"Nuisance Modifier",nuis_args)
       prod.Print("v")
     else: 
       print "Adding Nuisance ", nuisances[0]
       prod = r.RooFormulaVar("prod_%s"%self.binid,"Delta Change from %s"%nuisances[0],"1+@0",r.RooArgList(self.wspace.var("nuis_%s"%nuisances[0])))
     arglist.add(prod)
     self.pure_mu = r.RooFormulaVar("pmu_%s"%self.binid,"Number of expected (signal) events in %s"%self.binid,"(@0/@1)*@2",arglist)
   else: self.pure_mu = r.RooFormulaVar("pmu_%s"%self.binid,"Number of expected (signal) events in %s"%self.binid,"(@0/@1)",arglist)
   # Finally we add in the background 
   bkgArgList = r.RooArgList(self.pure_mu)
   if self.constBkg: self.mu = r.RooFormulaVar("mu_%s"%self.binid,"Number of expected events in %s"%self.binid,"%f+@0"%self.b,bkgArgList)
   else : self.mu = r.RooFormulaVar("mu_%s"%self.binid,"Number of expected events in %s"%self.binid,"@0/%f"%self.b,bkgArgList)
 
   self.mu.Print("v")
   print self.mu.getVal()
   #self.mu = r.RooFormulaVar("mu_%s"%self.binid,"Number of expected events in %s"%self.binid,"@0/(@1*@2)",r.RooArgList(self.integral,self.sfactor,self.pdfFullInt))
   self.wspace._import(self.mu,r.RooFit.RecycleConflictNodes())
   self.wspace._import(self.obs,r.RooFit.RecycleConflictNodes())
   self.wspace.factory("Poisson::pdf_%s(observed,mu_%s)"%(self.binid,self.binid))

 def add_to_dataset(self):
   # create a dataset called observed
   self.wspace_out.var("observed").setVal(self.o)
   self.wspace_out.cat(self.categoryname).setIndex(self.type_id)
   lv = self.wspace_out.var("observed")
   lc = self.wspace_out.cat("bin_number")
   local_obsargset = r.RooArgSet(lv,lc)
   if not self.wspace_out.data("combinedData"): 
     obsdata = r.RooDataSet("combinedData","Data in all Bins",local_obsargset)
     self.wspace_out._import(obsdata)
   else:obsdata = self.wspace_out.data("combinedData")
   obsdata.addFast(local_obsargset)
  
 def set_control_region(self,control):
   self.cr = control
 def ret_binid(self):
   return self.binid
 def ret_observed_dset(self):
   return self.wspace.data(dsname)
 def ret_observed(self):
   return self.o
 def ret_err(self):
   return self.binerror
 def add_err(self,e):
   self.binerror = (self.binerror**2+e**2)**0.5
 def ret_expected(self):
   return self.wspace.function(self.mu.GetName()).getVal()
 def ret_background(self):
   if self.constBkg: return self.b
   else: return (1-self.b)*(self.ret_expected())
 def ret_model(self):
   return self.wspace.function(self.model_mu.GetName()).getVal()
 def ret_model_err(self):
   print self.model_mu.GetName(), self.model_mu.getVal()
   return self.wspace.function(self.model_mu.GetName()).getError()

 def Print(self):
   print "Channel/Bin -> ", self.chid,self.binid, ", Var -> ",self.var.GetName(), ", Range -> ", self.xmin,self.xmax 
   print " .... observed = ",self.o, ", expected = ", self.wspace.function(self.mu.GetName()).getVal(), " (of which %f is background)"%self.ret_background(), ", scale factor = ", self.wspace.function(self.sfactor.GetName()).getVal() 

class Channel:
  # This class holds a "channel" which is as dumb as saying it holds a dataset and scale factors 
  def __init__(self,cname,wspace,id,data,scalefactors,bkg):
    self.chid = id
    self.data = data
    self.scalefactors = scalefactors
    self.chname = "ControlRegion_%d"%self.chid
    self.backgroundname  = bkg
    self.set_wspace(wspace)
    self.nuisances = []
    self.systematics = {}
    self.crname = cname
  def ret_title(self):
    return self.crname
  def add_systematic_shape(self,sys,file):
    sfup = self.scalefactors.GetName()+"_%s_"%sys+"Up"
    sfdn = self.scalefactors.GetName()+"_%s_"%sys+"Down"
    print "Looking for systematic shapes ... %s,%s"%(sfup,sfdn)
    self.systematics[sys] = [file.Get(sfup),file.Get(sfdn)]
    
  def add_systematic_yield(self,sys,kappa):
    sfup = self.scalefactors.GetName()+"_%s_"%sys+"Up"
    sfdn = self.scalefactors.GetName()+"_%s_"%sys+"Down"
    sfup = self.scalefactors.Clone(); sfup.SetName(self.scalefactors.GetName()+"_%s_"%sys+"Up")
    sfdn = self.scalefactors.Clone(); sfdn.SetName(self.scalefactors.GetName()+"_%s_"%sys+"Down")
    # log-normal scalefactors
    sfup.Scale(1+kappa)
    sfdn.Scale(1./(1+kappa))
    self.systematics[sys] = [sfup,sfdn]

  def add_nuisance(self,name,size):
    print "Error, Nuisance parameter model not supported fully for shape variations, dont use it!" 
    self.nuis = r.RooRealVar("nuis_%s"%name,"Nuisance - %s"%name,0,-3,3);
    self.wspace._import(self.nuis)
    self.cont = r.RooGaussian("const_%s"%name,"Constraint - %s"%name,self.wspace.var(self.nuis.GetName()),r.RooFit.RooConst(0),r.RooFit.RooConst(size));
    self.wspace._import(self.cont)
    self.nuisances.append(name)

  def set_wspace(self,w):
   self.wspace = w
   self.wspace._import = getattr(self.wspace,"import") # workaround: import is a python keyword

  def ret_nuisances(self):
    return self.nuisances

  def ret_name(self):
    return self.chname

  def ret_dataset(self):
    return self.data.GetName()

  def ret_chid(self):
    return self.chid

  def ret_sfactor(self,i,sys="",direction=1):
    if sys and sys in self.systematics.keys():
      if direction >0 :index=0
      else :index=1
      return self.systematics[sys][index].GetBinContent(i+1)
    else: return self.scalefactors.GetBinContent(i+1)

  def ret_background(self):
    return self.backgroundname

  def has_background(self):
    return len(self.backgroundname)

class Category:
  # This class holds a "category" which contains a bunch of channels
  # It needs to hold a combined_pdf object, a combined_dataset object and 
  # the target dataset for this channel 
  def __init__(self,
   catid
   ,cname 		# name for the parametric variation templates
   ,_fin 		# TDirectory   
   ,_fout 		# and output file 
   ,_wspace 		# RooWorkspace (in)
   ,_wspace_out 	# RooWorkspace (out)
   ,_bins  		# just get the bins
   ,_varname	    	# name of the variale
   ,_pdfname	    	# name of a double exp pdf
   ,_pdfname_zvv	# name of a double exp pdf to use as zvv mc fit
   ,_target_datasetname # only for initial fit values
   ,_control_regions 	# CRs constructed 
   ,diag		# a diagonalizer object
  ):
   self.cname = cname;
   self.catid = catid;
   # A crappy way to store canvases to be saved in the end
   self.canvases = {}
   self.histograms = []

   self._fin  = _fin 
   self._fout = _fout

   self._wspace = _wspace
   self._wspace_out = _wspace_out

   self.channels = []
   self.all_hists = []
   self.cr_prefit_hists = []
   # Setup a bunch of the attributes for this category 
   self._var      = _wspace.var(_varname)
   self._varname  = _varname
   self._bins     = _bins[:]
   self._control_regions = _control_regions
   self._pdf      = _wspace.pdf(_pdfname)
   self._pdf_orig = _wspace.pdf(_pdfname_zvv)
   self._data_mc  = _wspace.data(_target_datasetname)
   self._pdfname = _pdfname
   self._pdfname_zvv  =_pdfname_zvv
   self._target_datasetname = _target_datasetname
   self.sample = self._wspace_out.cat("bin_number")
   self._obsvar = self._wspace_out.var("observed")
   #self._obsdata = self._wspace_out.data("combinedData")

   self._norm = r.RooRealVar("%s_%s_norm"%(cname,_target_datasetname),"Norm",_wspace.data(_target_datasetname).sumEntries())
   self._norm.removeRange()
   self._norm_orig= r.RooRealVar("%s_%s_norm_orig"%(cname,_target_datasetname),"Norm_orig",_wspace.data(_target_datasetname).sumEntries())
   self._norm.setConstant(False)
   self._norm_orig.setConstant(True)
   self._wspace._import(self._norm)
   self._wspace._import(self._norm_orig)

   diag.freezeParameters(self._pdf_orig.getParameters(self._data_mc),False)
   #self._pdf_orig.fitTo(self._data_mc)  # Just initialises parameters 
   #self._pdf.fitTo(self._data_mc)       # Just initialises parameters 
   # Now we loop over the CR's and bins to produce the counting experiments for this category 
   # A fit of the original pdf to the Zvv data will help kick things off
   diag.freezeParameters(self._pdf_orig.getParameters(self._data_mc),True)
   for j,cr in enumerate(self._control_regions):
    for i,bl in enumerate(self._bins):
     if i >= len(self._bins)-1 : continue
     self.sample.defineType("cat_%d_ch_%d_bin_%d"%(self.catid,j,i),10*MAXBINS*catid+MAXBINS*j+i)
     self.sample.setIndex(10*MAXBINS*catid+MAXBINS*j+i)

  def fillExpectedHist(self,cr,expected_hist):
   bc=0
   for i,ch in enumerate(self.channels):
     if ch.chid == cr.chid:
       bc+=1
       expected_hist.SetBinContent(bc,ch.ret_expected())
       expected_hist.SetBinError(bc,ch.ret_err())

  def fillObservedHist(self,cr,observed_hist):
   bc=0
   for i,ch in enumerate(self.channels):
     if ch.chid == cr.chid:
       bc+=1
       observed_hist.SetBinContent(bc,ch.ret_observed())
       observed_hist.SetBinError(bc,(ch.ret_observed())**0.5)

  def fillBackgroundHist(self,cr,background_hist):
   bc=0
   for i,ch in enumerate(self.channels):
     if ch.chid == cr.chid:
       bc+=1
       background_hist.SetBinContent(bc,ch.ret_background())

  def fillModelHist(self,model_hist):
   for i,ch in enumerate(self.channels):
     if i>=len(self._bins)-1: break
     model_hist.SetBinContent(i+1,ch.ret_model())

  def init_channels(self):
   sample = self._wspace_out.cat("bin_number") #r.RooCategory("bin_number","bin_number")
   sample.Print()
   #for j,cr in enumerate(self._control_regions):
   for j,cr in enumerate(self._control_regions):
    for i,bl in enumerate(self._bins):
     if i >= len(self._bins)-1 : continue
     xmin,xmax = bl,self._bins[i+1]
     ch = Bin(self.catid,j,i,self._var,cr.ret_dataset(),self._pdf,self._norm,self._wspace,self._wspace_out,xmin,xmax)
     ch.set_control_region(cr)
     if cr.has_background(): ch.add_background(cr.ret_background())
     ch.set_label(sample) # should import the sample category label
     ch.set_sfactor(cr.ret_sfactor(i))
     # This has to the the last thing
     ch.setup_expect_var()
     ch.add_to_dataset()
     self.channels.append(ch)
   
   
   for j,cr in enumerate(self._control_regions):
   #save the prefit histos
    cr_pre_hist = r.TH1F("control_region_%s"%cr.ret_name(),"Expected %s control region"%cr.ret_name(),len(self._bins)-1,array.array('d',self._bins))
    self.fillExpectedHist(cr,cr_pre_hist)
    cr_pre_hist.SetLineWidth(2)
    cr_pre_hist.SetLineColor(r.kRed)
    self.all_hists.append(cr_pre_hist.Clone())
    self.cr_prefit_hists.append(cr_pre_hist.Clone())
   

  def ret_channels(self): 
   return self.channels

  def generate_systematic_templates(self):
   # The parameters have changed so re-generate the templates
   # We also re-calculate the expectations in each CR to update the errors for the plotting 
   return 0

  

  def make_post_fit_plots(self):
   # first put central value post fit curve onto canvas
   # Now start making the first plot
   self.fr = self._var.frame()
   self._wspace.data(self._target_datasetname).plotOn(self.fr,r.RooFit.Binning(200))
   self._pdf_orig.plotOn(self.fr)
   c = r.TCanvas("zjets_signalregion_mc_fit_before_after")
   self.fr.GetXaxis().SetTitle("fake MET (GeV)")
   self.fr.GetYaxis().SetTitle("Events/GeV")
   self.fr.SetTitle("")
   self._pdf.plotOn(self.fr,r.RooFit.LineColor(r.kBlue))
   self.fr.Draw()
   self._fout.WriteTObject(c)    
 
   lat = r.TLatex();
   lat.SetNDC();
   lat.SetTextSize(0.04);
   lat.SetTextFont(42);

   # now build post fit plots in each control region with some indication of systematic variations from fit?
   for j,cr in enumerate(self._control_regions):
    c = r.TCanvas("c_%s"%cr.ret_name(),"",800,800)
    cr_hist = r.TH1F("%s_control_region_%s"%(self.cname,cr.ret_name()),"Expected %s control region"%cr.ret_name(),len(self._bins)-1,array.array('d',self._bins))
    da_hist = r.TH1F("%s_data_control_region_%s"%(self.cname,cr.ret_name()),"data %s control region"%cr.ret_name(),len(self._bins)-1,array.array('d',self._bins))
    mc_hist = r.TH1F("%s_mc_control_region_%s"%(self.cname,cr.ret_name()),"Background %s control region"%cr.ret_name(),len(self._bins)-1,array.array('d',self._bins))
    self.fillObservedHist(cr,da_hist)
    self.fillBackgroundHist(cr,mc_hist)
    self.fillExpectedHist(cr,cr_hist)
    da_hist.SetTitle("") 
    cr_hist.SetFillColor(r.kBlue-10)
    mc_hist.SetFillColor(r.kRed+1)

    cr_hist = getNormalizedHist(cr_hist)
    da_hist = getNormalizedHist(da_hist)
    mc_hist = getNormalizedHist(mc_hist)
    pre_hist = getNormalizedHist(self.cr_prefit_hists[j])

    cr_hist.SetLineColor(r.kBlue)
    cr_hist.SetLineWidth(2)
    mc_hist.SetLineColor(1)
    mc_hist.SetLineWidth(2)
    da_hist.SetMarkerColor(1)
    da_hist.SetLineColor(1)
    da_hist.SetLineWidth(2)
    da_hist.SetMarkerStyle(20)
    self.histograms.append(da_hist)
    self.histograms.append(cr_hist)
    self.histograms.append(mc_hist)
    self.histograms.append(pre_hist)
    
    c.cd()
    pad1 = r.TPad("p1","p1",0,0.28,1,1)
    pad1.SetBottomMargin(0.01)
    pad1.SetCanvas(c)
    pad1.Draw()
    pad1.cd()
    tlg = r.TLegend(0.6,0.67,0.89,0.89)
    tlg.SetFillColor(0)
    tlg.SetTextFont(42)
    tlg.AddEntry(da_hist,"Data - %s"%cr.ret_title(),"PEL") 
    tlg.AddEntry(cr_hist,"Expected (post-fit)","FL") 
    tlg.AddEntry(mc_hist,"Backgrounds Component","F")
    tlg.AddEntry(pre_hist,"Expected (pre-fit)","L")
    da_hist.GetYaxis().SetTitle("Events/GeV");
    da_hist.GetXaxis().SetTitle("fake MET (GeV)");
    da_hist.Draw("Pe")
    cr_hist.Draw("sameE2")
    cr_line = cr_hist.Clone(); cr_line.SetFillColor(0)
    self.all_hists.append(cr_line)
    pre_hist.Draw("samehist")
    cr_line.Draw("histsame")
    mc_hist.Draw("samehist")
    da_hist.Draw("Pesame")
    tlg.Draw()
    lat.DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
    pad1.SetLogy()
    pad1.RedrawAxis()

    # Ratio plot
    c.cd()
    pad2 = r.TPad("p2","p2",0,0.068,1,0.28)
    pad2.SetTopMargin(0.02)
    pad2.SetCanvas(c)
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
    self.all_hists.append(ratio)
    self.all_hists.append(ratio_pre)
    ratio.GetXaxis().SetTitle("")
    ratio.Draw()
    ratio_pre.SetLineColor(pre_hist.GetLineColor())
    ratio_pre.SetMarkerColor(pre_hist.GetLineColor())
    ratio_pre.SetLineWidth(2)
    line = r.TLine(da_hist.GetXaxis().GetXmin(),1,da_hist.GetXaxis().GetXmax(),1)
    line.SetLineColor(1)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()
    ratio.Draw("same")
    ratio_pre.Draw("pelsame")
    ratio.Draw("samepel")
    self.all_hists.append(line)
    self._fout.WriteTObject(c) 

  def save(self):
   #for canv in self.canvases.keys():
   #  self._fout.WriteTObject(self.canvases[canv])
   for hist in self.histograms:
     self._fout.WriteTObject(hist)

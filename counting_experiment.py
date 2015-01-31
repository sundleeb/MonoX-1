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
   self.catid	  = catid
   self.type_id   = 10*MAXBINS*catid+MAXBINS*chid+id
   self.binid     = "cat_%d_ch_%d_bin_%d"%(catid,chid,id)
   self.wspace_out = wspace_out
   self.set_wspace(wspace)
   self.set_norm_var(norm)

   self.var	  = self.wspace_out.var(var.GetName())
   #self.var	  = self.wspace.var(var.GetName())
   self.dataset   = self.wspace.data(datasetname)
   if not self.wspace_out.pdf(pdf.GetName()): self.wspace_out._import(pdf,r.RooFit.RecycleConflictNodes())
   self.pdf	  = self.wspace_out.pdf(pdf.GetName())

   self.rngename = "rnge_%s"%self.binid
   self.var.setRange(self.rngename,xmin,xmax)
   self.xmin = xmin
   self.xmax = xmax
   self.cen = (xmax+xmin)/2

   self.binerror = 0

   self.o	= self.dataset.sumEntries("%s>=%g && %s<%g "%(var.GetName(),xmin,var.GetName(),xmax))
   #self.o	= (self.wspace.data(datasetname)).sumEntries("1>0",self.rngename)
   self.obs	= self.wspace_out.var("observed")#r.RooRealVar("observed","Observed Events bin",1)
   #self.setup_expect_var(self)
   self.argset = r.RooArgSet(wspace.var(self.var.GetName())) # <-------------------------- Check this is cool
   self.obsargset=r.RooArgSet(self.wspace_out.var("observed"),self.wspace_out.cat("bin_number"))
   self.var.setRange("fullRange_%d"%self.catid,self.wspace.var(self.var.GetName()).getMin(),self.wspace.var(self.var.GetName()).getMax())
   
   self.pdfFullInt = pdf.createIntegral(self.argset,r.RooFit.Range("fullRange_%d"%self.catid),r.RooFit.NormSet(self.argset))
   #if not self.wspace.var(self.pdfFullInt.GetName()) : self.wspace._import(self.pdfFullInt)
   self.wspace_out._import(self.pdfFullInt)
   self.b  = 0
   self.expected_init = 0
   #self.constBkg = True

 def add_background(self,bkg):
   if "Purity" in bkg:
     tmp_pfunc = r.TF1("tmp_bkg_%s"%self.id,bkg.split(":")[-1]) #?
     b = self.o*(1-tmp_pfunc.Eval(self.cen))
     #self.constBkg = False
   else:
     bkg_set      = self.wspace.data(bkg)
     #if not self.wspace_out.data(bkg): self.wspace_out._import(bkg)
     b	= bkg_set.sumEntries("%s>=%g && %s<%g "%(self.var.GetName(),self.xmin,self.var.GetName(),self.xmax)) 
 
   # Now model nuisances for background
   nuisances = self.cr.ret_bkg_nuisances()
   if len(nuisances)>0:
     prod = 0
     if len(nuisances)>1:
       nuis_args = r.RooArgList()
       for nuis in nuisances: 
        print "Adding Background Nuisance ", nuis 
	# Nuisance*Scale is the model 
	#form_args = r.RooArgList(self.wspace_out.var("nuis_%s"%nuis),self.wspace_out.function("sys_function_%s_%s"%(nuis,self.binid)))
	form_args = r.RooArgList(self.wspace_out.function("sys_function_%s_%s"%(nuis,self.binid)))
     	delta_nuis = r.RooFormulaVar("delta_bkg_%s_%s"%(self.binid,nuis),"Delta Change from %s"%nuis,"1+@0",form_args)
        self.wspace_out._import(delta_nuis,r.RooFit.RecycleConflictNodes())
     	nuis_args.add(self.wspace_out.function(delta_nuis.GetName()))
       prod = r.RooProduct("prod_background_%s"%self.binid,"Nuisance Modifier",nuis_args)
     else: 
       print "Adding Background Nuisance ", nuisances[0]
       prod = r.RooFormulaVar("prod_background_%s"%self.binid,"Delta Change in Background from %s"%nuisances[0],"1+@0",r.RooArgList(self.wspace_out.function("sys_function_%s_%s"%(nuisances[0],self.binid))))
     self.b = r.RooFormulaVar("background_%s"%self.binid,"Number of expected background events in %s"%self.binid,"@0*%f"%b,r.RooArgList(prod))
   else: self.b = r.RooFormulaVar("background_%s"%self.binid,"Number of expected background events in %s"%self.binid,"@0",r.RooArgList(r.RooFit.RooConst(b)))
   self.wspace_out._import(self.b)
   self.b = self.wspace_out.function(self.b.GetName())
   self.b_init = self.wspace_out.function(self.b.GetName()).getVal()

 def set_label(self,cat):
   self.categoryname = cat.GetName()
   #self.wspace._import(cat,r.RooFit.RecycleConflictNodes())

 def set_wspace(self,w):
   self.wspace = w
   self.wspace._import = getattr(self.wspace,"import") # workaround: import is a python keyword

 def set_norm_var(self,v):
   if not self.wspace_out.var(v.GetName()) : self.wspace_out._import(v)
   self.normvar = self.wspace_out.var(v.GetName())

 def set_sfactor(self,val):
   #print "Scale Factor for " ,self.binid,val
   if self.wspace_out.var("sfactor_%s"%self.binid): 
    self.sfactor.setVal(val)
    self.wspace_out.var(self.sfactor.GetName()).setVal(val)
   else:
     self.sfactor = r.RooRealVar("sfactor_%s"%self.binid,"Scale factor for bin %s"%self.binid,val,0.00001,10000); 
     self.sfactor.removeRange()
     self.sfactor.setConstant()
     self.wspace_out._import(self.sfactor,r.RooFit.RecycleConflictNodes())

 def setup_expect_var(self):
   # This will be the RooRealVar containing the value of the number of expected events in this bin
   self.integral = self.pdf.createIntegral(self.argset,r.RooFit.Range(self.rngename),r.RooFit.NormSet(self.argset))
   self.wspace_out._import(self.integral,r.RooFit.RecycleConflictNodes())
   if not self.wspace_out.function("model_mu_cat_%d_bin_%d"%(self.catid,self.id,)):
     self.model_mu = r.RooFormulaVar("model_mu_cat_%d_bin_%d"%(self.catid,self.id),"Model of N expected events in %d"%self.id,"@0*@1/@2",r.RooArgList(
        self.wspace_out.function(self.integral.GetName())
     	,self.wspace_out.var(self.normvar.GetName())
	,self.wspace_out.function(self.pdfFullInt.GetName()))) # in reality this will be given and depend on the integral of the pdf!
     self.wspace_out._import(self.model_mu,r.RooFit.RecycleConflictNodes())
   else: self.model_mu = self.wspace_out.function("model_mu_cat_%d_bin_%d"%(self.catid,self.id))

   arglist = r.RooArgList((self.model_mu),self.wspace_out.var(self.sfactor.GetName()))

   # Multiply by each of the uncertainties in the control region, dont alter the Poisson pdf, we will add the constraint at the end. Actually we won't use this right now.
   nuisances = self.cr.ret_nuisances()
   if len(nuisances)>0:
     prod = 0
     if len(nuisances)>1:
       nuis_args = r.RooArgList()
       for nuis in nuisances: 
        print "Adding Nuisance ", nuis 
	# Nuisance*Scale is the model 
	#form_args = r.RooArgList(self.wspace_out.var("nuis_%s"%nuis),self.wspace_out.function("sys_function_%s_%s"%(nuis,self.binid)))
	form_args = r.RooArgList(self.wspace_out.function("sys_function_%s_%s"%(nuis,self.binid)))
     	delta_nuis = r.RooFormulaVar("delta_%s_%s"%(self.binid,nuis),"Delta Change from %s"%nuis,"1+@0",form_args)
        self.wspace_out._import(delta_nuis,r.RooFit.RecycleConflictNodes())
     	nuis_args.add(self.wspace_out.function(delta_nuis.GetName()))
       prod = r.RooProduct("prod_%s"%self.binid,"Nuisance Modifier",nuis_args)
     else: 
       print "Adding Nuisance ", nuisances[0]
       prod = r.RooFormulaVar("prod_%s"%self.binid,"Delta Change from %s"%nuisances[0],"1+@0",r.RooArgList(self.wspace_out.function("sys_function_%s_%s"%(nuisances[0],self.binid))))
     arglist.add(prod)
     self.pure_mu = r.RooFormulaVar("pmu_%s"%self.binid,"Number of expected (signal) events in %s"%self.binid,"(@0*@1)*@2",arglist)
   else: self.pure_mu = r.RooFormulaVar("pmu_%s"%self.binid,"Number of expected (signal) events in %s"%self.binid,"(@0*@1)",arglist)
   # Finally we add in the background 
   bkgArgList = r.RooArgList(self.pure_mu,self.wspace_out.function(self.b.GetName()))
   #if self.constBkg: self.mu = r.RooFormulaVar("mu_%s"%self.binid,"Number of expected events in %s"%self.binid,"%f+@0"%self.b,bkgArgList)
   #else : self.mu = r.RooFormulaVar("mu_%s"%self.binid,"Number of expected events in %s"%self.binid,"@0/%f"%self.b,bkgArgList)
   self.mu = r.RooFormulaVar("mu_%s"%self.binid,"Number of expected events in %s"%self.binid,"@0+@1",bkgArgList)
 
   #self.mu = r.RooFormulaVar("mu_%s"%self.binid,"Number of expected events in %s"%self.binid,"@0/(@1*@2)",r.RooArgList(self.integral,self.sfactor,self.pdfFullInt))
   self.wspace_out._import(self.mu,r.RooFit.RecycleConflictNodes())
   self.wspace_out._import(self.obs,r.RooFit.RecycleConflictNodes())
   self.wspace_out.factory("Poisson::pdf_%s(observed,mu_%s)"%(self.binid,self.binid))
   self.expected_init = self.mu.getVal()


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
   obsdata = self.wspace_out.data("combinedData")
   obsdata.addFast(local_obsargset)
  
 def set_control_region(self,control):
   self.cr = control
 def ret_binid(self):
   return self.binid
 def ret_observed_dset(self):
   return self.wspace_out.data(dsname)
 def ret_observed(self):
   return self.o
 def ret_err(self):
   return self.binerror
 def add_err(self,e):
   self.binerror = (self.binerror**2+e**2)**0.5
 def ret_expected(self):
   return self.wspace_out.function(self.mu.GetName()).getVal()
 def ret_expected_init(self):
   return self.expected_init
 def ret_expected_err(self):
   return self.wspace_out.function(self.mu.GetName()).getError()
 def ret_background(self):
   #if self.constBkg: return self.b
   #else: return (1-self.b)*(self.ret_expected())
   return self.wspace_out.function(self.b.GetName()).getVal()
 def ret_background_init(self):
   return self.b_init
 def ret_model(self):
   return self.wspace_out.function(self.model_mu.GetName()).getVal()
 def ret_model_err(self):
   print self.model_mu.GetName(), self.model_mu.getVal()
   return self.wspace_out.function(self.model_mu.GetName()).getError()

 def Print(self):
   print "Channel/Bin -> ", self.chid,self.binid, ", Var -> ",self.var.GetName(), ", Range -> ", self.xmin,self.xmax 
   print " .... observed = ",self.o, ", expected = ", self.wspace_out.function(self.mu.GetName()).getVal(), " (of which %f is background)"%self.ret_background(), ", scale factor = ", self.wspace_out.function(self.sfactor.GetName()).getVal() 

class Channel:
  # This class holds a "channel" which is as dumb as saying it holds a dataset and scale factors 
  def __init__(self,cname,wspace,wspace_out,catid,id,data,scalefactors,bkg):
    self.catid = catid
    self.chid = id
    self.data = data
    self.scalefactors = scalefactors
    self.chname = "ControlRegion_%d"%self.chid
    self.backgroundname  = bkg
    self.wspace_out = wspace_out
    self.set_wspace(wspace)
    self.nuisances = []
    self.bkg_nuisances = []
    self.systematics = {}
    self.crname = cname
    self.nbins  = scalefactors.GetNbinsX()
  def ret_title(self):
    return self.crname
  def add_systematic_shape(self,sys,file):
    sys.exit("Nothing Will Happen with add_systematic, use add_nuisance")
    sfup = self.scalefactors.GetName()+"_%s_"%sys+"Up"
    sfdn = self.scalefactors.GetName()+"_%s_"%sys+"Down"
    print "Looking for systematic shapes ... %s,%s"%(sfup,sfdn)
    self.systematics[sys] = [file.Get(sfup),file.Get(sfdn)]
    
  def add_systematic_yield(self,sys,kappa):
    sys.exit("Nothing Will Happen with add_systematic, use add_nuisance")
    sfup = self.scalefactors.GetName()+"_%s_"%sys+"Up"
    sfdn = self.scalefactors.GetName()+"_%s_"%sys+"Down"
    sfup = self.scalefactors.Clone(); sfup.SetName(self.scalefactors.GetName()+"_%s_"%sys+"Up")
    sfdn = self.scalefactors.Clone(); sfdn.SetName(self.scalefactors.GetName()+"_%s_"%sys+"Down")
    # log-normal scalefactors
    sfup.Scale(1+kappa)
    sfdn.Scale(1./(1+kappa))
    self.systematics[sys] = [sfup,sfdn]
  
  def add_nuisance(self,name,size,bkg=False):
    #print "Error, Nuisance parameter model not supported fully for shape variations, dont use it!" 
    if not(self.wspace_out.var("nuis_%s"%name)): 
      nuis = r.RooRealVar("nuis_%s"%name,"Nuisance - %s"%name,0,-3,3);
      self.wspace_out._import(nuis)
      cont = r.RooGaussian("const_%s"%name,"Constraint - %s"%name,self.wspace_out.var(nuis.GetName()),r.RooFit.RooConst(0),r.RooFit.RooConst(1));
      self.wspace_out._import(cont)

    # run through all of the bins in the control regions and create a function to interpolate
    for b in range(self.nbins):
      func = r.RooFormulaVar("sys_function_%s_cat_%d_ch_%d_bin_%d"%(name,self.catid,self.chid,b)\
	,"Systematic Varation"\
      	,"@0*%f"%size,r.RooArgList(self.wspace_out.var("nuis_%s"%name)))
      if not self.wspace_out.function(func.GetName()) :self.wspace_out._import(func)
    # else 
    #  nuis = self.wspace_out.var("nuis_%s"%name)
    if bkg: self.bkg_nuisances.append(name)
    else:   self.nuisances.append(name)
    
  def add_nuisance_shape(self,name,file,setv=""):
    if not(self.wspace_out.var("nuis_%s"%name)) :
      nuis = r.RooRealVar("nuis_%s"%name,"Nuisance - %s"%name,0,-3,3);
      self.wspace_out._import(nuis)
      nuis_IN = r.RooRealVar("nuis_IN_%s"%name,"Constraint Mean - %s"%name,0,-10,10);
      nuis_IN.setConstant()
      self.wspace_out._import(nuis_IN)

      cont = r.RooGaussian("const_%s"%name,"Constraint - %s"%name,self.wspace_out.var(nuis.GetName()),self.wspace_out.var(nuis_IN.GetName()),r.RooFit.RooConst(1));
      self.wspace_out._import(cont)

    sfup = self.scalefactors.GetName()+"_%s_"%name+"Up"
    sfdn = self.scalefactors.GetName()+"_%s_"%name+"Down"
    print "Looking for systematic shapes ... %s,%s"%(sfup,sfdn)
    sysup,sysdn =  file.Get(sfup),file.Get(sfdn)
    # Now we loop through each bin and construct a polynomial function per bin 
    for b in range(self.nbins):
    	nsf = 1./(self.scalefactors.GetBinContent(b+1))
	vu = 1./(sysup.GetBinContent(b+1)) - nsf 
	vd = 1./(sysdn.GetBinContent(b+1)) - nsf  # Note this should be <ve if down is lower, its not a bug
	coeff_a = 0.5*(vu+vd)
	coeff_b = 0.5*(vu-vd)
        func = r.RooFormulaVar("sys_function_%s_cat_%d_ch_%d_bin_%d"%(name,self.catid,self.chid,b) \
		,"Systematic Varation"\
		,"(%f*@0*@0+%f*@0)/%f"%(coeff_a,coeff_b,nsf) \
		#,"(%f*@0*@0+%f*@0)"%(coeff_a,coeff_b) \
		,r.RooArgList(self.wspace_out.var("nuis_%s"%name))) # this is now relative deviation, SF-SF_0 = func => SF = SF_0*(1+func/SF_0)
	self.wspace_out.var("nuis_%s"%name).setVal(0)
        if not self.wspace_out.function(func.GetName()) :self.wspace_out._import(func)
    if setv!="":
      if "SetTo" in setv: 
       vv = float(setv.split("=")[1])
       self.wspace_out.var("nuis_IN_%s"%name).setVal(vv)
       self.wspace_out.var("nuis_%s"%name).setVal(vv)
    self.nuisances.append(name)

  def set_wspace(self,w):
   self.wspace = w
   self.wspace._import = getattr(self.wspace,"import") # workaround: import is a python keyword
  
  def ret_bkg_nuisances(self):
    return self.bkg_nuisances

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
      return 1./(self.systematics[sys][index].GetBinContent(i+1))
    else: return 1./(self.scalefactors.GetBinContent(i+1))

  def ret_background(self):
    return self.backgroundname

  def has_background(self):
    return len(self.backgroundname)

class Category:
  # This class holds a "category" which contains a bunch of channels
  # It needs to hold a combined_pdf object, a combined_dataset object and 
  # the target dataset for this channel 
  def __init__(self, corrname
   ,catid
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
   self.GNAME = corrname
   self.cname = cname;
   self.catid = catid;
   # A crappy way to store canvases to be saved in the end
   self.canvases = {}
   self.histograms = []
   self.model_hist = 0
   self._fin  = _fin 
   self._fout = _fout

   self._wspace = _wspace
   self._wspace_out = _wspace_out
   #self.diag = diag
   self.additional_vars = {}
   self.additional_targets = []

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
   if self._wspace_out.var(self._var.GetName()): a = 1
#     if self._var.getMin()< self._wspace_out.var(self._var.GetName()).getMin() : self._wspace_out.var(self._var.GetName()).setMin(self._var.getMin())
#     if self._var.getMax()> self._wspace_out.var(self._var.GetName()).getMax() : self._wspace_out.var(self._var.GetName()).setMin(self._var.getMax())
#     if self._var.getMin()> self._wspace_out.var(self._var.GetName()).getMin() : self._var.setMin(self._wspace_out.var(self._var.GetName()).getMin())
#     if self._var.getMax()< self._wspace_out.var(self._var.GetName()).getMax() : self._var.setMax(self._wspace_out.var(self._var.GetName()).getMax())

   else: self._wspace_out._import(self._var,r.RooFit.RecycleConflictNodes())
   self._var = self._wspace_out.var(self._var.GetName())
   self._norm = r.RooRealVar("%s_%s_norm"%(cname,_target_datasetname),"Norm",_wspace.data(_target_datasetname).sumEntries(),0,100000)
   self._norm.removeMax()
   self._norm_orig= r.RooRealVar("%s_%s_norm_orig"%(cname,_target_datasetname),"Norm_orig",_wspace.data(_target_datasetname).sumEntries(),0,10000)
   self._norm.setConstant(False)
   self._norm_orig.setConstant(True)
   self._wspace_out._import(self._norm)
   self._wspace_out._import(self._norm_orig)
   self._wspace_out._import(self._pdf)
   self._wspace_out._import(self._pdf_orig)

   diag.freezeParameters(self._pdf_orig.getParameters(self._data_mc),False)
   self._pdf_orig.fitTo(self._data_mc)  # Just initialises parameters 
   self._pdf.fitTo(self._data_mc)       # Just initialises parameters 
   # Now we loop over the CR's and bins to produce the counting experiments for this category 
   # A fit of the original pdf to the Zvv data will help kick things off
   self._pdf      = self._wspace_out.pdf(_pdfname)
   diag.freezeParameters(self._pdf_orig.getParameters(self._data_mc),True)
   self._norm_orig.setConstant(True)
   for j,cr in enumerate(self._control_regions):
    for i,bl in enumerate(self._bins):
     if i >= len(self._bins)-1 : continue
     self.sample.defineType("cat_%d_ch_%d_bin_%d"%(self.catid,j,i),10*MAXBINS*catid+MAXBINS*j+i)
     self.sample.setIndex(10*MAXBINS*catid+MAXBINS*j+i)

  
   # Now we have to build the ratio (correction) and import to new workspace
   ratioargs = r.RooArgList(self._wspace_out.var(self._norm.GetName())
   	                   ,self._wspace_out.pdf(self._pdf.GetName())
			   ,self._wspace_out.var(self._norm_orig.GetName())
			   ,self._wspace_out.pdf(self._pdf_orig.GetName()))
   self.pdf_ratio = r.RooFormulaVar("ratio_correction_%s"%cname,"Correction for Zvv from dimuon+photon control regions","@0*@1/(@2*@3)",ratioargs)
   self._wspace_out._import(self.pdf_ratio)
   self._wspace._import(self.pdf_ratio)

  def addTarget(self,vn,CR):  # Note, I need to know WHICH correction to run, signal is -1, others are 0,1 etc you know!
   self.additional_targets.append([vn,CR])
  def addVar(self,vnam,n,xmin,xmax):
   self.additional_vars[vnam] = [n,xmin,xmax]

  def fillExpectedHist(self,cr,expected_hist):
   bc=0
   for i,ch in enumerate(self.channels):
     if ch.chid == cr.chid:
       bc+=1
       expected_hist.SetBinContent(bc,ch.ret_expected())
       expected_hist.SetBinError(bc,ch.ret_err())
  
  def fillExpectedMinusBkgHistOrig(self,cr,expected_hist):
   bc=0
   for i,ch in enumerate(self.channels):
     if ch.chid == cr.chid:
       bc+=1
       expected_hist.SetBinContent(bc,ch.ret_expected_init()-ch.ret_background_init())
       expected_hist.SetBinError(bc,0)

  def fillExpectedMinusBkgHist(self,cr,expected_hist):
   bc=0
   for i,ch in enumerate(self.channels):
     if ch.chid == cr.chid:
       bc+=1
       expected_hist.SetBinContent(bc,ch.ret_expected()-ch.ret_background())
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
   
  def ret_control_regions(self): 
   return self._control_regions

  def ret_channels(self): 
   return self.channels

  def generate_systematic_templates(self,diag,npars):
   if self.model_hist == 0 : 
     sys.exit("Error in generate_systematic_templates: cannot generate template variations before nominal model is created, first run Category.save_model() !!!! ")

   # First store nominal values in control regions (to make error bands)
   nominals = []
   for j,cr in enumerate(self._control_regions):
     nominal_values = []
     for i,ch in enumerate(self.channels):
       if ch.chid != cr.chid: continue
       nominal_values.append(ch.ret_expected())
     nominals.append(nominal_values)
     	
   # The parameters have changed so re-generate the templates
   # We also re-calculate the expectations in each CR to update the errors for the plotting 
   leg_var = r.TLegend(0.56,0.42,0.89,0.89)
   leg_var.SetFillColor(0)
   leg_var.SetTextFont(42)

   # We will make a plot along the way
   canvr = r.TCanvas("canv_variations_ratio")
   canv  = r.TCanvas("canv_variations")
   model_hist_spectrum = getNormalizedHist(self.model_hist)
   model_hist_spectrum.SetTitle("")
   model_hist_spectrum.GetXaxis().SetTitle("E_{T}^{miss} (GeV)")
   model_hist_spectrum.Draw()
   self.all_hists.append(model_hist_spectrum)

   sys_c=0

   for par in range(npars):
    hist_up = r.TH1F("%s_combined_model_par_%d_Up"%(self.GNAME,par),"combined_model par %d Up 1 sigma - %s "%(par,self.cname)  ,len(self._bins)-1,array.array('d',self._bins))
    hist_dn = r.TH1F("%s_combined_model_par_%d_Down"%(self.GNAME,par),"combined_model par %d Down 1 sigma - %s"%(par,self.cname),len(self._bins)-1,array.array('d',self._bins))
 
    diag.setEigenset(par,1)  # up variation
    #fillModelHist(hist_up,channels)
    diag.generateWeightedTemplate(hist_up,self._wspace_out.function(self.pdf_ratio.GetName()),self._wspace_out.var(self._var.GetName()),self._wspace.data(self._target_datasetname))

    # Also want to calculate for each control region an error per bin associated, its very easy to do, but only do it for "Up" variation and the error will symmetrize itself
    for j,cr in enumerate(self._control_regions):
     chi = 0
     for i,ch in enumerate(self.channels):
       if ch.chid != cr.chid: continue
       derr = abs(ch.ret_expected()-nominals[j][chi])
       ch.add_err(derr); chi+=1

    diag.setEigenset(par,-1)  # up variation
    #fillModelHist(hist_dn,channels)
    diag.generateWeightedTemplate(hist_dn,self._wspace_out.function(self.pdf_ratio.GetName()),self._wspace_out.var(self._var.GetName()),self._wspace.data(self._target_datasetname))

    # Reset parameter values 
    diag.resetPars()

    # make the plots
    canv.cd()
    hist_up.SetLineWidth(2)
    hist_dn.SetLineWidth(2)
    if sys_c+2 == 10: sys_c+=1
    hist_up.SetLineColor(sys_c+2)
    hist_dn.SetLineColor(sys_c+2)
    hist_dn.SetLineStyle(2)

    #_fout.WriteTObject(hist_up)
    #_fout.WriteTObject(hist_dn)
    self.histograms.append(hist_up.Clone())
    self.histograms.append(hist_dn.Clone())

    hist_up = getNormalizedHist(hist_up)
    hist_dn = getNormalizedHist(hist_dn)
    self.all_hists.append(hist_up)
    self.all_hists.append(hist_dn)

    hist_up.Draw("samehist")
    hist_dn.Draw("samehist")

    flat = self.model_hist.Clone()
    hist_up_cl = hist_up.Clone();hist_up_cl.SetName(hist_up_cl.GetName()+"_ratio")
    hist_dn_cl = hist_dn.Clone();hist_dn_cl.SetName(hist_dn_cl.GetName()+"_ratio")
    hist_up_cl.Divide(model_hist_spectrum)
    hist_dn_cl.Divide(model_hist_spectrum)
    flat.Divide(self.model_hist)

    # ratio plot
    canvr.cd()
    flat.SetTitle("")
    flat.GetXaxis().SetTitle("E_{T}^{miss} (GeV)")
    flat.GetYaxis().SetRangeUser(0.85,1.2)
    if par==0: flat.Draw("hist")
    self.all_hists.append(flat)
    self.all_hists.append(hist_up_cl)
    self.all_hists.append(hist_dn_cl)
    hist_up_cl.Draw('histsame')
    hist_dn_cl.Draw('histsame')
    leg_var.AddEntry(hist_up_cl,"Parameter %d"%par,"L")
    sys_c+=1

   canv.cd() ; leg_var.Draw()
   canvr.cd(); leg_var.Draw()
   self._fout.WriteTObject(canv)
   self._fout.WriteTObject(canvr)

  def save_model(self,diag):
   # Need to make ratio 
   self.model_hist = r.TH1F("%s_combined_model"%(self.cname),"combined_model - %s"%(self.cname),len(self._bins)-1,array.array('d',self._bins))
   #fillModelHist(model_hist,channels)
   diag.generateWeightedTemplate(self.model_hist,self._wspace_out.function(self.pdf_ratio.GetName()),self._wspace_out.var(self._var.GetName()),self._wspace.data(self._target_datasetname))
   self.model_hist.SetLineWidth(2)
   self.model_hist.SetLineColor(1)
   #_fout = r.TFile("combined_model.root","RECREATE")
   #_fout.WriteTObject(self.model_hist)
   self.model_hist.SetName("%s_combined_model"%self.GNAME)
   self.histograms.append(self.model_hist)

   for tg_v in self.additional_targets:
     tg = tg_v[0] 
     cr_i = tg_v[1]
     # Make the ratio of post-to-pre fit for the given CR 
     model_tg = r.TH1F("%s_combined_model"%(tg),"combined_model - %s"%(self.cname),len(self._bins)-1,array.array('d',self._bins))
     if cr_i<0:
       diag.generateWeightedTemplate(model_tg,self._wspace_out.function(self.pdf_ratio.GetName()),self._wspace_out.var(self._var.GetName()),self._wspace.data(tg))
     else: 
       histCorr =r.TH1F("%s_TMPCORRECION_"%(tg),"combined_model CORRECION - %s"%(self.cname),len(self._bins)-1,array.array('d',self._bins)) 
       self.fillExpectedMinusBkgHist(self._control_regions[cr_i],histCorr) 
       histDenum =r.TH1F("%s_TMPCORRECION_DEMONIMATOR"%(tg),"combined_model CORRECION - %s"%(self.cname),len(self._bins)-1,array.array('d',self._bins)) 
       self.fillExpectedMinusBkgHistOrig(self._control_regions[cr_i],histDenum)
       histCorr.Divide(histDenum)
       diag.generateWeightedTemplate(model_tg,histCorr,self._varname,self._varname,self._wspace.data(tg)) 
     self.histograms.append(model_tg.Clone())

   # Also make a weighted version of each other variable
   for varx in self.additional_vars.keys():
     nb = self.additional_vars[varx][0]; min = self.additional_vars[varx][1]; max = self.additional_vars[varx][2]
     model_hist_vx = r.TH1F("combined_model%s"%(varx),"combined_model - %s"%(self.cname),nb,min,max)
     diag.generateWeightedTemplate(model_hist_vx,self._wspace_out.function(self.pdf_ratio.GetName()),varx,self._wspace_out.var(self._var.GetName()),self._wspace.data(self._target_datasetname))
     self.histograms.append(model_hist_vx.Clone())

     for ti,tg_v in enumerate(self.additional_targets):
       tg = tg_v[0] 
       cr_i = tg_v[1]
       model_hist_vx_tg = r.TH1F("%s_combined_model%s"%(tg,varx),"combined_model - %s"%(self.cname),nb,min,max)
       if cr_i<0 :
         diag.generateWeightedTemplate(model_hist_vx_tg,self._wspace_out.function(self.pdf_ratio.GetName()),varx,self._wspace_out.var(self._var.GetName()),self._wspace.data(tg))
       else :
         histCorr =r.TH1F("%s_TMPCORRECION_"%(tg),"combined_model CORRECION - %s"%(self.cname),len(self._bins)-1,array.array('d',self._bins)) 
         self.fillExpectedMinusBkgHist(self._control_regions[cr_i],histCorr) 
         histDenum =r.TH1F("%s_TMPCORRECION_DEMONIMATOR"%(tg),"combined_model CORRECION - %s"%(self.cname),len(self._bins)-1,array.array('d',self._bins)) 
         self.fillExpectedMinusBkgHistOrig(self._control_regions[cr_i],histDenum)
         histCorr.Divide(histDenum)
         diag.generateWeightedTemplate(model_hist_vx_tg,histCorr,self._varname,varx,self._wspace.data(tg))
       self.histograms.append(model_hist_vx_tg.Clone())



  def make_post_fit_plots(self):
   # first put central value post fit curve onto canvas
   # Now start making the first plot
   self.fr = self._wspace.var(self._var.GetName()).frame()
   self._wspace.data(self._target_datasetname).plotOn(self.fr,r.RooFit.Binning(200))
   self._pdf_orig.plotOn(self.fr,r.RooFit.LineColor(r.kRed))
   c = r.TCanvas("%sregion_mc_fit_before_after"%(self._target_datasetname))
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
    mc_hist.SetFillColor(r.kGray)

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
    tlg = r.TLegend(0.54,0.53,0.89,0.89)
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
    pad2 = r.TPad("p2","p2",0,0.068,1,0.285)
    pad2.SetTopMargin(0.04)
    pad2.SetCanvas(c)
    pad2.Draw()
    pad2.cd()
    # Need to make sure cr hist has no errors for when we divide
    cr_hist_noerr = cr_hist.Clone(); cr_hist_noerr.SetName(cr_hist.GetName()+"noerr")
    for b in range(cr_hist_noerr.GetNbinsX()): cr_hist_noerr.SetBinError(b+1,0)
    pre_hist_noerr = pre_hist.Clone(); pre_hist_noerr.SetName(pre_hist.GetName()+"noerr")
    for b in range(pre_hist_noerr.GetNbinsX()): pre_hist_noerr.SetBinError(b+1,0)

    ratio = da_hist.Clone()
    ratio_pre = da_hist.Clone()
    ratio.GetYaxis().SetRangeUser(0.01,1.99)
    ratio.Divide(cr_hist_noerr)
    ratio_pre.Divide(pre_hist_noerr)
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
    eline = ratio.Clone(); eline.SetName("OneWithError_%s"%ratio.GetName())
    self.all_hists.append(eline)
    for b in range(ratio.GetNbinsX()):
      eline.SetBinContent(b+1,1)
      if cr_hist.GetBinContent(b+1)>0: eline.SetBinError(b+1,cr_hist.GetBinError(b+1)/cr_hist.GetBinContent(b+1))
    eline.SetFillColor(r.kBlue-10)
    eline.SetLineColor(r.kBlue-10)
    eline.SetMarkerSize(0)
    eline.Draw("sameE2")
    line = r.TLine(da_hist.GetXaxis().GetXmin(),1,da_hist.GetXaxis().GetXmax(),1)
    line.SetLineColor(1)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()
    ratio.Draw("same")
    ratio_pre.Draw("pelsame")
    ratio.Draw("samepel")
    self.all_hists.append(line)
    pad2.RedrawAxis()
    self._fout.WriteTObject(c) 

  def save(self):
   #for canv in self.canvases.keys():
   #  self._fout.WriteTObject(self.canvases[canv])
   for hist in self.histograms:
     self._fout.WriteTObject(hist)

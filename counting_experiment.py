import ROOT as r
import sys

MAXBINS=100
class Bin:
 def __init__(self,chid,id,var,datasetname,pdf,norm,wspace,xmin,xmax):

   self.chid	  = chid# This is the thing that links two bins from different controls togeher
   self.id        = id
   self.type_id   = MAXBINS*chid+id
   self.binid     = "ch_%d_bin_%d"%(chid,id)
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

   self.dataset.Print("V")
   self.o	= self.dataset.sumEntries("%s>=%g && %s<%g "%(var.GetName(),xmin,var.GetName(),xmax))
   #self.o	= (self.wspace.data(datasetname)).sumEntries("1>0",self.rngename)
   self.obs	= r.RooRealVar("observed","Observed Events bin",1)
   #self.setup_expect_var(self)
   self.argset = r.RooArgSet(self.var)
   self.var.setRange("fullRange",self.var.getMin(),self.var.getMax())
   
   self.pdfFullInt = pdf.createIntegral(self.argset,r.RooFit.Range("fullRange"),r.RooFit.NormSet(self.argset))
   #if not self.wspace.var(self.pdfFullInt.GetName()) : self.wspace._import(self.pdfFullInt)
   self.wspace._import(self.pdfFullInt,r.RooFit.RecycleConflictNodes())
   print self.wspace.function(self.pdfFullInt.GetName())
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
   self.wspace._import(cat,r.RooFit.RecycleConflictNodes())

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

 def add_to_dataset(self,obsdata):
   # create a dataset 
   self.wspace.var("observed").setVal(self.o)
   #self.wspace.cat(self.categoryname).defineType(self.binid,self.id)
   self.wspace.cat(self.categoryname).setIndex(self.type_id)
   local_obsargset = r.RooArgSet(self.wspace.var("observed"),self.wspace.cat(self.categoryname))
   obsdata.add(local_obsargset)
   #self.wspace._import(self.obsdata)
  
 def set_control_region(self,control):
   self.cr = control
 def ret_binid(self):
   return self.binid
 def ret_observed_dset(self):
   return self.wspace.data(dsname)
 def ret_observed(self):
   return self.o
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
    sys.exit()
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

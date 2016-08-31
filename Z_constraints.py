import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "zg"

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname    = "phoPtHighMet"          # Observable variable name 

  target             = _fin.Get("signal_zg")      # define monimal (MC) of which process this config will model
  controlmc          = _fin.Get("dimu_zg")        # defines Zmm MC of which process will be controlled by
  controlmc_e        = _fin.Get("diel_zg")        # defines Zmm MC of which process will be controlled by

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = target.Clone(); ZmmScales.SetName("dimu_weights_%s"%cid)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  ZeeScales = target.Clone(); ZeeScales.SetName("diel_weights_%s"%cid)
  ZeeScales.Divide(controlmc_e)
  _fOut.WriteTObject(ZeeScales)  # always write out to the directory 
  
  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
  Channel("dimu",_wspace,out_ws,cid+'_'+model,ZmmScales)
  ,Channel("diel",_wspace,out_ws,cid+'_'+model,ZeeScales)
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  for b in range(target.GetNbinsX()):
    err = ZmmScales.GetBinError(b+1)
    if not ZmmScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZmmScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZmmScales.Clone(); byb_u.SetName("dimu_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dimuCR",b))
    byb_u.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)+err)
    byb_d = ZmmScales.Clone(); byb_d.SetName("dimu_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dimuCR",b))
    if (ZmmScales.GetBinContent(b+1)-err > 0):
      byb_d.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)-err)
    else:
      byb_d.SetBinContent(b+1,1)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dimuCR",b),_fOut)

  for b in range(target.GetNbinsX()):
    err = ZeeScales.GetBinError(b+1)
    if not ZeeScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZeeScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZeeScales.Clone(); byb_u.SetName("diel_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dielCR",b))
    byb_u.SetBinContent(b+1,ZeeScales.GetBinContent(b+1)+err)
    byb_d = ZeeScales.Clone(); byb_d.SetName("diel_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dielCR",b))
    if (ZeeScales.GetBinContent(b+1)-err > 0):
      byb_d.SetBinContent(b+1,ZeeScales.GetBinContent(b+1)-err)
    else:
      byb_d.SetBinContent(b+1,1)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dielCR",b),_fOut)

  #######################################################################################################
  
  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,target.GetName(),CRs,diag)
  # Return of course
  return cat


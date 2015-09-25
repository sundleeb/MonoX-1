import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "wjets"
def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%nam)
  _wspace = _fin.Get("wspace_%s"%nam)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName = "WJets" # Give a name of the process being modelled
  metname = "mvamet"    # Observable variable name 
  targetmc     = _fin.Get("signal_wjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("singlemuon_wjets")  # defines in / out acceptance

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  WScales = targetmc.Clone(); WScales.SetName("wmn_weights_%s"%nam)
  WScales.Divide(controlmc)
  _fOut.WriteTObject(WScales)  # always write out to the directory 
  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid,INTEGER,DATASET,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # note that INTEGER *must* be 0,1,2... increasing with each channel added 
  # DATASET should be the observed data (pulled as a RooDataHist from the workspace, as shown
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("singlemuon",_wspace,out_ws,cid,0,_wspace.data("singlemuon_data"),WScales)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
  CRs[0].add_nuisance("pdf_CT10",0.006)
  CRs[0].add_nuisance("CMS_eff_m",0.01)
  #######################################################################################################


  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  # Return of course
  return cat


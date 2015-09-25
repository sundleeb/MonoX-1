import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "zjets"
def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%nam)
  _wspace = _fin.Get("wspace_%s"%nam)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname = "mvamet"    # Observable variable name 
  targetmc     = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("dimuon_zjets")  # defines in / out acceptance

  controlmc_photon   = _fin.Get("photon_gjet")  # defines in / out acceptance
  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = targetmc.Clone(); ZmmScales.SetName("zmm_weights_%s"%nam)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  PhotonScales = targetmc.Clone(); PhotonScales.SetName("photon_weights_%s"%nam)
  PhotonScales.Divide(controlmc_photon)
  _fOut.WriteTObject(PhotonScales)  # always write out to the directory 


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
   Channel("photon",_wspace,out_ws,cid,0,_wspace.data("photon_data"),PhotonScales) 
  ,Channel("dimuon",_wspace,out_ws,cid,1,_wspace.data("dimuon_data"),ZmmScales)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
  CRs[1].add_nuisance("pdf",0.01)
  CRs[1].add_nuisance("CMS_eff_m",0.01)

  PhotonScales_up = PhotonScales.Clone(); PhotonScales_up.SetName("photon_weights_dummy_Up")
  PhotonScales_dn = PhotonScales.Clone(); PhotonScales_dn.SetName("photon_weights_dummy_Down")
  for b in range(PhotonScales.GetNbinsX()):
   PhotonScales_up.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)*1.3)
   PhotonScales_dn.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)*0.7)
  _fOut.WriteTObject(PhotonScales_up)
  _fOut.WriteTObject(PhotonScales_dn)

  CRs[1].add_nuisance_shape("dummy",_fOut) 
  # CRs[1].add_nuisance_shape("dummy",_fOut,"SetTo=1") # note, there is additional option to set nominal value of parameter, this can also be set later in the datacard of course!
  #######################################################################################################


  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  # Return of course
  return cat


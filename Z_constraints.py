import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "zjets"

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname    = "met"          # Observable variable name 
  gvptname   = "genBos_pt"    # Weights are in generator pT
  wvarname   = "scaleMC_w"

  target             = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc          = _fin.Get("Zmm_zll")           # defines Zmm MC of which process will be controlled by
  controlmc_photon   = _fin.Get("gjets_gjets")       # defines Gjets MC of which process will be controlled by

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = target.Clone(); ZmmScales.SetName("zmm_weights_%s"%cid)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  my_function(_wspace,_fin,_fOut,cid,diag)
  PhotonScales = _fOut.Get("photon_weights_%s"%cid)

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
   Channel("photon",_wspace,out_ws,cid+'_'+model,PhotonScales) 
  ,Channel("dimuon",_wspace,out_ws,cid+'_'+model,ZmmScales)
  #,Channel("wjetssignal",_wspace,out_ws,cid+'_'+model,WZScales)
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  # Bin by bin nuisances to cover statistical uncertainties ...
  for b in range(target.GetNbinsX()):
    err = PhotonScales.GetBinError(b+1)
    if not PhotonScales.GetBinContent(b+1)>0: continue 
    relerr = err/PhotonScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = PhotonScales.Clone(); byb_u.SetName("photon_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"photonCR",b))
    byb_u.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)+err)
    byb_d = PhotonScales.Clone(); byb_d.SetName("photon_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"photonCR",b))
    byb_d.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"photonCR",b),_fOut)

  for b in range(target.GetNbinsX()):
    err = ZmmScales.GetBinError(b+1)
    if not ZmmScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZmmScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZmmScales.Clone(); byb_u.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dimuonCR",b))
    byb_u.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)+err)
    byb_d = ZmmScales.Clone(); byb_d.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dimuonCR",b))
    if (ZmmScales.GetBinContent(b+1)-err > 0):
      byb_d.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)-err)
    else:
      byb_d.SetBinContent(b+1,1)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dimuonCR",b),_fOut)

  #######################################################################################################
  
  CRs[0].add_nuisance_shape("scale",_fOut) 
  CRs[0].add_nuisance_shape("pdf",_fOut) 
  CRs[0].add_nuisance("PhotonEfficiency",0.01) 

  #######################################################################################################


  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,target.GetName(),CRs,diag)
  # Return of course
  return cat

# My Function. Just to put all of the complicated part into one function
def my_function(_wspace,_fin,_fOut,nam,diag):

  metname    = "met"          # Observable variable name 
  gvptname   = "genBos_pt"    # Weights are in generator pT
  #wvarname   = "scaleMC_w"
  wvarname   = "mcWeight"

  target             = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc          = _fin.Get("Zmm_zll")           # defines Zmm MC of which process will be controlled by
  controlmc_photon   = _fin.Get("gjets_gjets")       # defines Gjets MC of which process will be controlled by

  _gjet_mcname 	     = "gjets_gjets"
  GJet               = _fin.Get("gjets_gjets")

  fkFactor = r.TFile.Open("files/qcd_13TeV.root")

  nlo_pho  = fkFactor.Get("pho_kfactor") # this one is simply 1
  nlo_zjt  = fkFactor.Get("z_kfactor") # this one is simply 1
  
  nlo_zjt_pdfUp   = fkFactor.Get("z_pdfUp")
  nlo_zjt_pdfDown = fkFactor.Get("z_pdfDown")

  nlo_pho_pdfUp   = fkFactor.Get("pho_pdfUp")
  nlo_pho_pdfDown = fkFactor.Get("pho_pdfDown")

  nlo_zjt_scaleUp   = fkFactor.Get("z_scaleUp")
  nlo_zjt_scaleDown = fkFactor.Get("z_scaleDown")

  nlo_pho_scaleUp   = fkFactor.Get("pho_scaleUp")
  nlo_pho_scaleDown = fkFactor.Get("pho_scaleDown")

  # Historical reasons not touchign the nlo reweighting although it is being
  # scaled by simply 1.

  Pho = target.Clone(); Pho.SetName("photon_weights_denom_%s"%nam)
  for b in range(Pho.GetNbinsX()): Pho.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho,nlo_pho,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv = target.Clone(); Zvv.SetName("photon_weights_nom_%s"%nam)
  for b in range(Zvv.GetNbinsX()): Zvv.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv,nlo_zjt,gvptname,metname,_wspace.data("signal_zjets"))

  PhotonOverZ = Pho.Clone(); PhotonOverZ.SetName("PhotonOverZNLO")
  PhotonOverZ.Divide(Zvv)
  PhotonOverZ.Multiply(target)
  PhotonOverZ.Divide(GJet)

  # Would like to get rid of this if wvarname is set to 1 at the moment.
  diag.generateWeightedDataset("photon_gjet_nlo",PhotonOverZ,wvarname,metname,_wspace,"gjets_gjets")

  PhotonSpectrum = Pho.Clone(); PhotonSpectrum.SetName("photon_spectrum_%s_"%nam)
  ZvvSpectrum 	 = Zvv.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)
  _fOut.WriteTObject( PhotonSpectrum )
  _fOut.WriteTObject( ZvvSpectrum )

  #################################################################################################################
  # now do systematic parts
  Pho_scaleUp = target.Clone(); Pho_scaleUp.SetName("photon_weights_denom_scaleUp_%s"%nam)
  for b in range(Pho_scaleUp.GetNbinsX()): Pho_scaleUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_scaleUp,nlo_pho_scaleUp,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_scaleUp = target.Clone(); Zvv_scaleUp.SetName("photon_weights_nom_scaleUp_%s"%nam)
  for b in range(Zvv_scaleUp.GetNbinsX()):Zvv_scaleUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_scaleUp,nlo_zjt_scaleUp,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_scaleDown = target.Clone(); Pho_scaleDown.SetName("photon_weights_denom_scaleDown_%s"%nam)
  for b in range(Pho_scaleDown.GetNbinsX()): Pho_scaleDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_scaleDown,nlo_pho_scaleDown,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_scaleDown = target.Clone(); Zvv_scaleUp.SetName("photon_weights_nom_scaleDown_%s"%nam)
  for b in range(Zvv_scaleDown.GetNbinsX()):Zvv_scaleDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_scaleDown,nlo_zjt_scaleDown,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_pdfUp = target.Clone(); Pho_pdfUp.SetName("photon_weights_denom_pdfUp_%s"%nam)
  for b in range(Pho_pdfUp.GetNbinsX()): Pho_pdfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_pdfUp,nlo_pho_pdfUp,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_pdfUp = target.Clone(); Zvv_pdfUp.SetName("photon_weights_nom_pdfUp_%s"%nam)
  for b in range(Zvv_pdfUp.GetNbinsX()):Zvv_pdfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_pdfUp,nlo_zjt_pdfUp,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_pdfDown = target.Clone(); Pho_pdfDown.SetName("photon_weights_denom_pdfDown_%s"%nam)
  for b in range(Pho_pdfDown.GetNbinsX()): Pho_pdfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_pdfDown,nlo_pho_pdfDown,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_pdfDown = target.Clone(); Zvv_pdfUp.SetName("photon_weights_nom_pdfDown_%s"%nam)
  for b in range(Zvv_pdfDown.GetNbinsX()):Zvv_pdfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_pdfDown,nlo_zjt_pdfDown,gvptname,metname,_wspace.data("signal_zjets"))

  #################################################################################################################

  # Have to also add one per systematic variation :(, 
  Zvv.Divide(Pho); Zvv.SetName("photon_weights_%s"%nam)

  Zvv_scaleUp.Divide(Pho_scaleUp); 	 Zvv_scaleUp.SetName("photon_weights_%s_scale_Up"%nam);_fOut.WriteTObject(Zvv_scaleUp)
  Zvv_scaleDown.Divide(Pho_scaleDown);   Zvv_scaleDown.SetName("photon_weights_%s_scale_Down"%nam);_fOut.WriteTObject(Zvv_scaleDown)

  Zvv_pdfUp.Divide(Pho_pdfUp); 	        Zvv_pdfUp.SetName("photon_weights_%s_pdf_Up"%nam);_fOut.WriteTObject(Zvv_pdfUp)
  Zvv_pdfDown.Divide(Pho_pdfDown); 	Zvv_pdfDown.SetName("photon_weights_%s_pdf_Down"%nam);_fOut.WriteTObject(Zvv_pdfDown)
  
  PhotonScales = Zvv.Clone()
  _fOut.WriteTObject(PhotonScales)


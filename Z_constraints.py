import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
# Second is a list of histos which will addtionally be converted to RooDataHists, leave blank if not needed
model = "zjets"
convertHistograms = []

# My Function. Just to put all of the complicated part into one function
def my_function(_wspace,_fin,_fOut,nam,diag):

  metname = "mvamet"    # Observable variable name 
  gvptname = "genVpt"    # Weights are in generator pT
  wvarname= "weight"
  target     = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("dimuon_zll")  # defines in / out acceptance
  controlmce    = _fin.Get("dielectron_zll")  # defines in / out acceptance

  controlmc_photon   = _fin.Get("photon_gjet")  # defines in / out acceptance
  controlmc_wlv      = _fin.Get("signal_wjets")  # defines in / out acceptance

  _gjet_mcname 	      = "photon_gjet"
  GJet = _fin.Get("photon_gjet")

  fkFactor = r.TFile.Open("files/Photon_Z_NLO_kfactors_w80pcorr.root")
  nlo_pho = fkFactor.Get("pho_NLO_LO")
  nlo_zjt = fkFactor.Get("Z_NLO_LO")
  nlo_pho_mrUp = fkFactor.Get("pho_NLO_LO_mrUp")
  nlo_zjt_mrUp = fkFactor.Get("Z_NLO_LO_mrUp")
  nlo_pho_mrDown = fkFactor.Get("pho_NLO_LO_mrDown")
  nlo_zjt_mrDown = fkFactor.Get("Z_NLO_LO_mrDown")
  nlo_pho_mfUp = fkFactor.Get("pho_NLO_LO_mfUp")
  nlo_zjt_mfUp = fkFactor.Get("Z_NLO_LO_mfUp")
  nlo_pho_mfDown = fkFactor.Get("pho_NLO_LO_mfDown")
  nlo_zjt_mfDown = fkFactor.Get("Z_NLO_LO_mfDown")

  nlo_pho_mr2Up = fkFactor.Get("pho_NLO_LO_mr2Up")
  nlo_zjt_mr2Up = fkFactor.Get("Z_NLO_LO_mr2Up")
  nlo_pho_mr2Down = fkFactor.Get("pho_NLO_LO_mr2Down")
  nlo_zjt_mr2Down = fkFactor.Get("Z_NLO_LO_mr2Down")
  nlo_pho_mf2Up = fkFactor.Get("pho_NLO_LO_mf2Up")
  nlo_zjt_mf2Up = fkFactor.Get("Z_NLO_LO_mf2Up")
  nlo_pho_mf2Down = fkFactor.Get("pho_NLO_LO_mf2Down")
  nlo_zjt_mf2Down = fkFactor.Get("Z_NLO_LO_mf2Down")

  nlo_zjt_pdfUp  = fkFactor.Get("Z_NLO_LO_pdfUp")
  nlo_zjt_pdfDown = fkFactor.Get("Z_NLO_LO_pdfDown")

  nlo_ewkUp    = fkFactor.Get("EWK_Up")
  nlo_ewkDown  = fkFactor.Get("EWK_Dwon")

  fFFactor = r.TFile.Open("files/FP.root")
  nlo_FPUp    = fFFactor.Get("FP_Up")
  nlo_FPDown  = fFFactor.Get("FP_Down")

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
  diag.generateWeightedDataset("photon_gjet_nlo",PhotonOverZ,wvarname,metname,_wspace,"photon_gjet")

  PhotonSpectrum = Pho.Clone(); PhotonSpectrum.SetName("photon_spectrum_%s_"%nam)
  ZvvSpectrum 	 = Zvv.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)
  _fOut.WriteTObject( PhotonSpectrum )
  _fOut.WriteTObject( ZvvSpectrum )

  #################################################################################################################
  # now do systematic parts
  Pho_mrUp = target.Clone(); Pho.SetName("photon_weights_denom_mrUp_%s"%nam)
  for b in range(Pho_mrUp.GetNbinsX()): Pho_mrUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mrUp,nlo_pho_mrUp,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mrUp = target.Clone(); Zvv_mrUp.SetName("photon_weights_nom_mrUp_%s"%nam)
  for b in range(Zvv_mrUp.GetNbinsX()):Zvv_mrUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mrUp,nlo_zjt_mrUp,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mrDown = target.Clone(); Pho.SetName("photon_weights_denom_mrDown_%s"%nam)
  for b in range(Pho_mrDown.GetNbinsX()): Pho_mrDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mrDown,nlo_pho_mrDown,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mrDown = target.Clone(); Zvv_mrDown.SetName("photon_weights_nom_mrDown_%s"%nam)
  for b in range(Zvv_mrDown.GetNbinsX()): Zvv_mrDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mrDown,nlo_zjt_mrDown,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mfUp = target.Clone(); Pho.SetName("photon_weights_denom_mfUp_%s"%nam)
  for b in range(Pho_mfUp.GetNbinsX()): Pho_mfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mfUp,nlo_pho_mfUp,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mfUp = target.Clone(); Zvv_mfUp.SetName("photon_weights_nom_mfUp_%s"%nam)
  for b in range(Zvv_mfUp.GetNbinsX()): Zvv_mfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mfUp,nlo_zjt_mfUp,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mfDown = target.Clone(); Pho.SetName("photon_weights_denom_mfDown_%s"%nam)
  for b in range(Pho_mfDown.GetNbinsX()): Pho_mfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mfDown,nlo_pho_mfDown,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mfDown = target.Clone(); Zvv_mfDown.SetName("photon_weights_nom_mfDown_%s"%nam)
  for b in range(Zvv_mfDown.GetNbinsX()): Zvv_mfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mfDown,nlo_zjt_mfDown,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mr2Up = target.Clone(); Pho.SetName("photon_weights_denom_mr2Up_%s"%nam)
  for b in range(Pho_mr2Up.GetNbinsX()): Pho_mr2Up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mr2Up,nlo_pho_mr2Up,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mr2Up = target.Clone(); Zvv_mr2Up.SetName("photon_weights_nom_mr2Up_%s"%nam)
  for b in range(Zvv_mr2Up.GetNbinsX()):Zvv_mr2Up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mr2Up,nlo_zjt_mr2Up,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mr2Down = target.Clone(); Pho.SetName("photon_weights_denom_mr2Down_%s"%nam)
  for b in range(Pho_mr2Down.GetNbinsX()): Pho_mr2Down.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mr2Down,nlo_pho_mr2Down,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mr2Down = target.Clone(); Zvv_mr2Down.SetName("photon_weights_nom_mr2Down_%s"%nam)
  for b in range(Zvv_mr2Down.GetNbinsX()): Zvv_mr2Down.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mr2Down,nlo_zjt_mr2Down,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mf2Up = target.Clone(); Pho.SetName("photon_weights_denom_mf2Up_%s"%nam)
  for b in range(Pho_mf2Up.GetNbinsX()): Pho_mf2Up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mf2Up,nlo_pho_mf2Up,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mf2Up = target.Clone(); Zvv_mf2Up.SetName("photon_weights_nom_mf2Up_%s"%nam)
  for b in range(Zvv_mf2Up.GetNbinsX()): Zvv_mf2Up.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mf2Up,nlo_zjt_mf2Up,gvptname,metname,_wspace.data("signal_zjets"))

  Pho_mf2Down = target.Clone(); Pho.SetName("photon_weights_denom_mf2Down_%s"%nam)
  for b in range(Pho_mf2Down.GetNbinsX()): Pho_mf2Down.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho_mf2Down,nlo_pho_mf2Down,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv_mf2Down = target.Clone(); Zvv_mf2Down.SetName("photon_weights_nom_mf2Down_%s"%nam)
  for b in range(Zvv_mf2Down.GetNbinsX()): Zvv_mf2Down.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_mf2Down,nlo_zjt_mf2Down,gvptname,metname,_wspace.data("signal_zjets"))

  Zvv_pdfDown = target.Clone(); Zvv_pdfDown.SetName("photon_weights_nom_pdfDown_%s"%nam)
  for b in range(Zvv_pdfDown.GetNbinsX()): Zvv_pdfDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_pdfDown,nlo_zjt_pdfDown,gvptname,metname,_wspace.data("signal_zjets"))
  Zvv_pdfUp = target.Clone(); Zvv_pdfUp.SetName("photon_weights_nom_pdfUp_%s"%nam)
  for b in range(Zvv_pdfUp.GetNbinsX()): Zvv_pdfUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_pdfUp,nlo_zjt_pdfUp,gvptname,metname,_wspace.data("signal_zjets"))

  # Notice that the EWKUp was calculated on the g/Z ratio and Down is its inverse, so since we are 
  # here going to correct the Z, we using the Down as the Up :)
  Zvv_ewkDown = target.Clone(); Zvv_ewkDown.SetName("photon_weights_%s_ewk_Down"%nam)
  for b in range(Zvv_ewkDown.GetNbinsX()): Zvv_ewkDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkDown,nlo_ewkUp,gvptname,metname,_wspace.data("signal_zjets"))

  Zvv_ewkUp   = target.Clone(); Zvv_ewkUp   .SetName("photon_weights_%s_ewk_Up"%nam)
  for b in range(Zvv_ewkUp.GetNbinsX()): Zvv_ewkUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkUp,nlo_ewkDown,gvptname,metname,_wspace.data("signal_zjets"))

  nlo_ewkFlat = nlo_ewkDown.Clone("ewk_Base")
  nlo_ewkFlat.Divide(nlo_ewkFlat)
  Zvv_ewkBase = target.Clone(); Zvv_ewkBase  .SetName("photon_weights_%s_ewk_Base"%nam)
  for b in range(Zvv_ewkBase.GetNbinsX()): Zvv_ewkBase.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_ewkBase,nlo_ewkFlat,gvptname,metname,_wspace.data("signal_zjets"))


  Zvv_FPDown = target.Clone(); Zvv_FPDown.SetName("photon_weights_%s_fp_Down"%nam)
  for b in range(Zvv_FPDown.GetNbinsX()): Zvv_FPDown.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_FPDown,nlo_FPDown,gvptname,metname,_wspace.data("signal_zjets"))

  Zvv_FPUp   = target.Clone(); Zvv_FPUp   .SetName("photon_weights_%s_fp_Up"%nam)
  for b in range(Zvv_FPUp.GetNbinsX()): Zvv_FPUp.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv_FPUp,nlo_FPUp,gvptname,metname,_wspace.data("signal_zjets"))
  ##################################################################################################################


  # Have to also add one per systematic variation :(, 
  Zvv.Divide(Pho); 		 Zvv.SetName("photon_weights_%s"%nam)
  Zvv_mrUp.Divide(Pho_mrUp); 	 Zvv_mrUp.SetName("photon_weights_%s_mr_Up"%nam);_fOut.WriteTObject(Zvv_mrUp)
  Zvv_mrDown.Divide(Pho_mrDown); Zvv_mrDown.SetName("photon_weights_%s_mr_Down"%nam);_fOut.WriteTObject(Zvv_mrDown)
  Zvv_mfUp.Divide(Pho_mfUp); 	 Zvv_mfUp.SetName("photon_weights_%s_mf_Up"%nam);_fOut.WriteTObject(Zvv_mfUp)
  Zvv_mfDown.Divide(Pho_mfDown); Zvv_mfDown.SetName("photon_weights_%s_mf_Down"%nam);_fOut.WriteTObject(Zvv_mfDown)
  Zvv_mr2Up.Divide(Pho_mr2Up); 	 Zvv_mr2Up.SetName("photon_weights_%s_mr2_Up"%nam);_fOut.WriteTObject(Zvv_mr2Up)
  Zvv_mr2Down.Divide(Pho_mr2Down); Zvv_mr2Down.SetName("photon_weights_%s_mr2_Down"%nam);_fOut.WriteTObject(Zvv_mr2Down)
  Zvv_mf2Up.Divide(Pho_mf2Up); 	 Zvv_mf2Up.SetName("photon_weights_%s_mf2_Up"%nam);_fOut.WriteTObject(Zvv_mf2Up)
  Zvv_mf2Down.Divide(Pho_mf2Down); Zvv_mf2Down.SetName("photon_weights_%s_mf2_Down"%nam);_fOut.WriteTObject(Zvv_mf2Down)

  Zvv_pdfUp.Divide(Pho); 	 Zvv_pdfUp.SetName("photon_weights_%s_pdf_Up"%nam);_fOut.WriteTObject(Zvv_pdfUp)
  Zvv_pdfDown.Divide(Pho); 	Zvv_pdfDown.SetName("photon_weights_%s_pdf_Down"%nam);_fOut.WriteTObject(Zvv_pdfDown)
  
  # Divide out the nominal photon for the EWK corrections as this is already the relative difference
  Zvv_ewkUp  .Divide(Zvv_ewkBase)
  Zvv_ewkDown.Divide(Zvv_ewkBase)
  Zvv_ewkUp  .Multiply(Zvv)
  Zvv_ewkDown.Multiply(Zvv)

  Zvv_FPUp  .Divide(Zvv_ewkBase)
  Zvv_FPDown.Divide(Zvv_ewkBase)
  Zvv_FPUp  .Multiply(Zvv)
  Zvv_FPDown.Multiply(Zvv)

  #_fOut.WriteTObject(Zvv_ewkDown)
  #_fOut.WriteTObject(Zvv_ewkUp)
  _fOut.WriteTObject(Zvv_FPDown)
  _fOut.WriteTObject(Zvv_FPUp)

  PhotonScales = Zvv.Clone()

  #_fOut.WriteTObject(Zvv) # these are photon scales
  _fOut.WriteTObject(PhotonScales)


  for b in range(target.GetNbinsX()):
    ewk_u = PhotonScales.Clone(); ewk_u.SetName("photon_weights_%s_ewk_%s_bin%d_Up"%(nam,nam,b))
    ewk_d = PhotonScales.Clone(); ewk_d.SetName("photon_weights_%s_ewk_%s_bin%d_Down"%(nam,nam,b))
    for j in range(target.GetNbinsX()):
      if j==b: 
	ewk_u.SetBinContent(j+1,Zvv_ewkUp.GetBinContent(j+1))
	ewk_d.SetBinContent(j+1,Zvv_ewkDown.GetBinContent(j+1))
	break
    _fOut.WriteTObject(ewk_u)
    _fOut.WriteTObject(ewk_d)

  controlmc_wlv      = _fin.Get("signal_wjets")  # defines in / out acceptance
  WZScales = target.Clone(); WZScales.SetName("wz_weights_%s"%nam)
  WZScales.Divide(controlmc_wlv)
  _fOut.WriteTObject(WZScales)  # always write out to the directory 

  for b in range(target.GetNbinsX()):
    ewk_u = WZScales.Clone(); ewk_u.SetName("wz_weights_%s_ewk_W_%s_bin%d_Up"%(nam,nam,b))
    ewk_d = WZScales.Clone(); ewk_d.SetName("wz_weights_%s_ewk_W_%s_bin%d_Down"%(nam,nam,b))
    for j in range(target.GetNbinsX()):
      if j==b: 
	ewk_u.SetBinContent(j+1,WZScales.GetBinContent(j+1)*1.1)
	ewk_d.SetBinContent(j+1,WZScales.GetBinContent(j+1)*0.9)
	break
    _fOut.WriteTObject(ewk_u)
    _fOut.WriteTObject(ewk_d)

  # finally make a photon background dataset 
  fPurity = r.TFile.Open("files/photonPurity.root")
  ptphopurity = fPurity.Get("data")
  photon_background = PhotonScales.Clone(); photon_background.SetName("photon_gjet_background")
  for b in range(ptphopurity.GetNbinsX()): 
  	ptphopurity.SetBinContent(b+1,1-ptphopurity.GetBinContent(b+1))  # background is 1-purity
  for b in range(photon_background.GetNbinsX()): 
  	photon_background.SetBinContent(b+1,0)
  ptphopurity.Print()
  diag.generateWeightedTemplate(photon_background,ptphopurity,"ptpho",metname,_wspace.data("photon_data"))
  #photon_background.SetTitle("base") # --> Makes sure this gets converted to RooDataHist laters
  #_fin.WriteTObject(photon_background);
  # store the histogram to be written out later 
  convertHistograms.append(photon_background)

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname = "mvamet"    # Observable variable name 
  targetmc     = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("dimuon_zll")  # defines in / out acceptance
  controlmce    = _fin.Get("dielectron_zll")  # defines in / out acceptance

  controlmc_photon   = _fin.Get("photon_gjet")  # defines in / out acceptance
  controlmc_wlv      = _fin.Get("signal_wjets")  # defines in / out acceptance

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = targetmc.Clone(); ZmmScales.SetName("zmm_weights_%s"%cid)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 
  ZeeScales = targetmc.Clone(); ZeeScales.SetName("zee_weights_%s"%cid)
  ZeeScales.Divide(controlmce)
  _fOut.WriteTObject(ZeeScales)  # always write out to the directory 

  #PhotonScales = targetmc.Clone(); PhotonScales.SetName("photon_weights_%s"%cid)
  #PhotonScales.Divide(controlmc_photon)
  #_fOut.WriteTObject(PhotonScales)  # always write out to the directory 

  WZScales = targetmc.Clone(); WZScales.SetName("wz_weights_%s"%cid)
  WZScales.Divide(controlmc_wlv)
  _fOut.WriteTObject(WZScales)  # always write out to the directory 

  my_function(_wspace,_fin,_fOut,cid,diag)
  PhotonScales = _fOut.Get("photon_weights_%s"%cid)
  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("photon",_wspace,out_ws,cid+'_'+model,PhotonScales) 
  ,Channel("dimuon",_wspace,out_ws,cid+'_'+model,ZmmScales)
  ,Channel("dielectron",_wspace,out_ws,cid+'_'+model,ZeeScales)
  #,Channel("wjetssignal",_wspace,out_ws,cid+'_'+model,WZScales)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
  CRs[0].add_nuisance_shape("mr",_fOut) 
  CRs[0].add_nuisance_shape("mf",_fOut) 
  CRs[0].add_nuisance_shape("mr2",_fOut) 
  CRs[0].add_nuisance_shape("mf2",_fOut) 
  CRs[0].add_nuisance_shape("pdf",_fOut) 
  CRs[0].add_nuisance_shape("fp",_fOut) 
  CRs[0].add_nuisance("PhotonEfficiency",0.01) 
  CRs[1].add_nuisance("CMS_eff_m",0.01)
  CRs[2].add_nuisance("CMS_eff_e",0.01)

  # Now for each bin in the distribution, we make one EWK uncertainty which is the size of  the Up/Down variation --> Completely uncorrelated between bins
  #for b in range(targetmc.GetNbinsX()):
   # CRs[2].add_nuisance_shape("ewk_W_%s_bin%d"%(cid,b),_fOut)

  # Now for each bin in the distribution, we make one EWK uncertainty which is the size of  the Up/Down variation --> Completely uncorrelated between bins
  for b in range(targetmc.GetNbinsX()):
    CRs[0].add_nuisance_shape("ewk_%s_bin%d"%(cid,b),_fOut,"SetTo=1")

  # Bin by bin nuisances to cover statistical uncertainties ...
  for b in range(targetmc.GetNbinsX()):
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

  for b in range(targetmc.GetNbinsX()):
    err = ZmmScales.GetBinError(b+1)
    if not ZmmScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZmmScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZmmScales.Clone(); byb_u.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dimuonCR",b))
    byb_u.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)+err)
    byb_d = ZmmScales.Clone(); byb_d.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dimuonCR",b))
    byb_d.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dimuonCR",b),_fOut)

  for b in range(targetmc.GetNbinsX()):
    err = ZeeScales.GetBinError(b+1)
    if not ZeeScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZeeScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZeeScales.Clone(); byb_u.SetName("zee_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dielectronCR",b))
    byb_u.SetBinContent(b+1,ZeeScales.GetBinContent(b+1)+err)
    byb_d = ZeeScales.Clone(); byb_d.SetName("zee_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dielectronCR",b))
    byb_d.SetBinContent(b+1,ZeeScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[2].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dielectronCR",b),_fOut)
  #######################################################################################################


  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  # Return of course
  cat.addTarget("photon_gjet_background",-2)# -2 means dont apply any correction # make histogram for this guy?
  return cat


from combineControlRegions import *
import ROOT as r 

# These are the "nominal" scale-factors TEMPORARY SINCE NOONE DID PHOTONS YET!
fMarco    = r.TFile.Open("output_model_marco_edit.root")

ZmmScales = (fMarco.Get("category_0/Zmm_weights")).Clone() #Need to make sure these are made in previous steps!!!
PhoScales = (fMarco.Get("category_0/photon_model/Photon_to_Zvv_weights_met")).Clone()
# for now no photons so....

_f = r.TFile.Open("mono-x.root")
_fin = _f.Get("category_monojet")

_wspace = _fin.Get("wspace_monojet")
_photon_datasetname = "photon_data"
_dimuon_datasetname = "dimuon_data"
_dimuon_backgroundsname = "dimuon_backgrounds"

CRs = [
 Channel(_wspace,0,_wspace.data(_photon_datasetname),PhoScales,"Purity:0.9399+(8.46e-5)*x")  # stupid linear fit of Purities
,Channel(_wspace,1,_wspace.data(_dimuon_datasetname),ZmmScales,_dimuon_backgroundsname)
]
  #Add Systematic -> Fit will be re-run once per systematic

  #_control_regions[0].add_systematic_shape("MuonEfficiency",_fin)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma 
CRs[1].add_systematic_yield("MuonEfficiency",0.1)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma, a number means make a new global scaling (lnN)
CRs[0].add_systematic_yield("MuR_theory",0.1)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma, a number means make a new global scaling (lnN)
CRs[0].add_systematic_yield("MuF_theory",0.1)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma, a number means make a new global scaling (lnN)

_fOut = r.TFile("combined_model_test.root","RECREATE")

CombinedControlRegionFit(_fin,_fOut,_wspace,"signal_data","mvamet","doubleExponential_dimuon_data","signal_zjets",CRs)
print "Produced combined Z(mm) + photon fits -> ", _fOut.GetName()
_fOut.Close()

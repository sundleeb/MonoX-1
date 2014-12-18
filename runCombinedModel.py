from combineControlRegions import *
import ROOT as r 
r.gROOT.SetBatch(1)
def cmodel(nam,_f,_fOut):

  _fin = _f.Get("category_%s"%nam)

  _wspace = _fin.Get("wspace_%s"%nam)
  _photon_datasetname = "photon_data"
  _dimuon_datasetname = "dimuon_data"
  _dimuon_backgroundsname = "dimuon_all_background"

  target = _fin.Get("signal_zjets")
  Pho = _fin.Get("photon_gjet")
  Zmm = _fin.Get("dimuon_zll")
  PhoScales = target.Clone(); PhoScales.SetName("photon_weights")
  ZmmScales = target.Clone(); ZmmScales.SetName("zmm_weights")

  # Have to also add one per systematic variation :(, do later
  PhoScales.Divide(Pho)
  ZmmScales.Divide(Zmm)
  _fOut.WriteTObject(PhoScales)
  _fOut.WriteTObject(ZmmScales)

  _bins = []  # take bins from some histogram
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  CRs = [
   Channel(_wspace,0,_wspace.data(_photon_datasetname),PhoScales,"Purity:0.9399+(8.46e-5)*x")  # stupid linear fit of Purities, should move to flat 
  ,Channel(_wspace,1,_wspace.data(_dimuon_datasetname),ZmmScales,_dimuon_backgroundsname)
  ]
  #Add Systematic -> Fit will be re-run once per systematic

  #_control_regions[0].add_systematic_shape("MuonEfficiency",_fin)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma 
  CRs[1].add_systematic_yield("MuonEfficiency",0.1)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma, a number means make a new global scaling (lnN)
  #CRs[0].add_systematic_yield("MuR_theory",0.1)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma, a number means make a new global scaling (lnN)
  #CRs[0].add_systematic_yield("MuF_theory",0.1)  # looks for weights of the form XXX _MuonEfficiency +1 and -1 sigma, a number means make a new global scaling (lnN)

  # Still some naming issues so check if mvamet or mvamet_
  metname = "mvamet"
  try:
    mt = _wspace.var(metname)
    mt.GetName()
  except:
    metname = "mvamet_"
  CombinedControlRegionFit(nam,_fin,_fOut,_wspace,_bins,metname,"doubleExponential_dimuon_data","signal_zjets",CRs)

_fOut = r.TFile("photon_dimuon_combined_model.root","RECREATE")
# run once per category
categories = ["inclusive","resolved","boosted"]
_f = r.TFile.Open("mono-x-vtagged.root")
for cn in categories: 
        _fDir = _fOut.mkdir("category_%s"%cn)
	cmodel(cn,_f,_fDir)

print "Produced combined Z(mm) + photon fits -> ", _fOut.GetName()
_fOut.Close()

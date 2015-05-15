# This tool converts the signals (usually because there is some additional systematics /
# reweighting to be done so we need those histograms

import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

varname = "mvamet"

categories = [
	 "monojet"
	,"resolved"
	,"boosted"
	]

# open up the backgrounds workspace since it holds also the RooRealVar!
fi_   = ROOT.TFile.Open("mono-x-backgrounds.root")
fi_ws = fi_.Get("mono-x-ws")

for cat in categories:

  ou_ws = ROOT.RooWorkspace("signal_higgs_ws","Signal Model")
  ou_ws._import = getattr(ou_ws,"import") # workaround: import is a python keyword

  fdir = ROOT.TFile.Open("card_%s.root"%cat)
  varl = fi_ws.var(varname+"_%s"%cat)

  fout = ROOT.TFile("signal_%s.root"%cat,"RECREATE")

  keys_local = fdir.GetListOfKeys() 
  keynames = []
  for key in keys_local:
    obj = key.ReadObj()
    if type(obj)!=type(ROOT.TH1F()): continue
    name = obj.GetName()
    print name
    keynames.append(name)

  keynames = set(keynames)
  for kj in keynames:
    obj = fdir.Get(kj)
    print "Creating Data Hist for ", kj
    dhist = ROOT.RooDataHist(cat+"_"+kj,"DataSet - %s, %s"%(cat,kj),ROOT.RooArgList(varl),obj)
    ou_ws._import(dhist)

  fout.WriteTObject(ou_ws)
  fout.Close()

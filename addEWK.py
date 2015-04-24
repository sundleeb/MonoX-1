import ROOT

fExt = ROOT.TFile("Photon_Z_NLO_kfactors.root","UPDATE")
fOld = ROOT.TFile.Open("/afs/cern.ch/work/n/nckw//public/monojet/Photon_Z_NLO_kfactors.root")

ewkUp = fOld.Get("EWK_Up")
ewkDn = fOld.Get("EWK_Dwon")

fExt.WriteTObject(ewkUp)
fExt.WriteTObject(ewkDn)
fExt.Close()
print "Added EWK Correction from %s to %s"%(fOld.GetName(),fExt.GetName())


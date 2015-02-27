import ROOT
f = ROOT.TFile.Open("monojet_vjets_mva_aug26.root")

npdfs = 26
dummy = f.Get("Wlv_PDF_CT10_1Up")

allU = [f.Get("Wlv_PDF_CT10_%dUp"%d)   for d in range(1,npdfs+1)]
allD = [f.Get("Wlv_PDF_CT10_%dDown"%d) for d in range(1,npdfs+1)]

band = dummy.Clone(); band.SetTitle("band")
for b in range(dummy.GetNbinsX()):
  bvec = [u.GetBinContent(b+1) for u in allU]
  bvec+= [d.GetBinContent(b+1) for d in allD]

  maxu = max(bvec)
  minu = min(bvec)

  mid = (maxu+minu)/2
  diff = abs(maxu-mid)
  band.SetBinContent(b+1,1)
  band.SetBinError(b+1,diff/mid)

band.SetLineWidth(2)
band.SetLineStyle(2)
bandE = band.Clone()
bandE.SetFillColor(ROOT.kOrange)
band.Draw("hist")
bandE.Draw("sameE2")
band.Draw("histsame")
raw_input() 

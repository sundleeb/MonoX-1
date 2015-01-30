import ROOT
import numpy
# Note, LO are already spectra but NLO are not
def getNormalizedHist(hist, templatehist):
  nb = hist.GetNbinsX()
  thret = templatehist.Clone()
  for b in range(1,nb+1): 
    sfactor = 1./templatehist.GetBinWidth(b)
    thret.SetBinContent(b,hist.GetBinContent(b)*sfactor)
    thret.SetBinError(b,hist.GetBinError(b)*sfactor)
  thret.GetYaxis().SetTitle("Events/GeV")
  return thret

def makeHist(gr,dir,h):
  rethist = h.Clone(); rethist.SetName("tmp")
  for b in range(h.GetNbinsX()):
   val = gr.GetBinContent(b+1)
   # find error 
   if dir<0 :error = -1*gr.GetBinError(b+1)
   else :error = gr.GetBinError(b+1)
   rethist.SetBinContent(b+1,val+error)
  return rethist

savehists = []

#PHOLOfile  = ROOT.TFile.Open("/afs/cern.ch/work/n/nckw/monojet/photon/CMSSW_5_3_14/src/PhotonGen.root")
ZvvLOfile  = ROOT.TFile.Open("/afs/cern.ch/work/n/nckw/private/monojet/xsec_lo_photon_Z.root")
NLOfile =  ROOT.TFile.Open(  "/afs/cern.ch/work/n/nckw/private/monojet/xsec_nlo_photon_Z.root")

# Right now the NLO are of by a factor of 1000./2480000 (pho) 1000./9944999(Z)

LOh_pho  = ZvvLOfile.Get("photon_0"); LOh_pho.SetName("gen_pt_pho_lo")
LOh_Z    = ZvvLOfile.Get("zjets_0"); LOh_Z.SetName("gen_pt_zvv_lo")
LOh_pho = getNormalizedHist(LOh_pho,LOh_pho)
LOh_Z   = getNormalizedHist(LOh_Z,LOh_Z)

NLOh_pho = NLOfile.Get("photon_0")
NLOh_Z   = NLOfile.Get("zjets_0")
#NLOh_Z.Scale(3.0)
NLOh_pho.SetLineColor(ROOT.kBlack);NLOh_pho.SetMarkerColor(ROOT.kBlack); NLOh_pho.SetMarkerStyle(21); NLOh_pho.SetMarkerSize(0.8); NLOh_pho.SetLineWidth(2) 
NLOh_Z.SetLineColor(ROOT.kBlack);NLOh_Z.SetMarkerColor(ROOT.kBlack); NLOh_Z.SetMarkerStyle(21); NLOh_Z.SetMarkerSize(0.8); NLOh_Z.SetLineWidth(2) 

NLOh_pho_mr_u = NLOfile.Get("photon_0_w00");NLOh_pho_mr_u.SetLineColor(ROOT.kRed);NLOh_pho_mr_u.SetLineWidth(2);NLOh_pho_mr_u.SetLineStyle(1)
NLOh_pho_mr_d = NLOfile.Get("photon_0_w02");NLOh_pho_mr_d.SetLineColor(ROOT.kRed);NLOh_pho_mr_d.SetLineWidth(2);NLOh_pho_mr_d.SetLineStyle(2)
NLOh_pho_mf_u = NLOfile.Get("photon_0_w10");NLOh_pho_mf_u.SetLineColor(ROOT.kGreen);NLOh_pho_mf_u.SetLineWidth(2);NLOh_pho_mf_u.SetLineStyle(1)
NLOh_pho_mf_d = NLOfile.Get("photon_0_w12");NLOh_pho_mf_d.SetLineColor(ROOT.kGreen);NLOh_pho_mf_d.SetLineWidth(2);NLOh_pho_mf_d.SetLineStyle(2)

NLOh_Z_mr_u   = NLOfile.Get("zjets_0_w00");NLOh_Z_mr_u.SetLineColor(ROOT.kRed);NLOh_Z_mr_u.SetLineWidth(2);NLOh_Z_mr_u.SetLineStyle(1)
NLOh_Z_mr_d   = NLOfile.Get("zjets_0_w02");NLOh_Z_mr_d.SetLineColor(ROOT.kRed);NLOh_Z_mr_d.SetLineWidth(2);NLOh_Z_mr_d.SetLineStyle(2)
NLOh_Z_mf_u   = NLOfile.Get("zjets_0_w10");NLOh_Z_mf_u.SetLineColor(ROOT.kGreen);NLOh_Z_mf_u.SetLineWidth(2);NLOh_Z_mf_u.SetLineStyle(1)
NLOh_Z_mf_d   = NLOfile.Get("zjets_0_w12");NLOh_Z_mf_d.SetLineColor(ROOT.kGreen);NLOh_Z_mf_d.SetLineWidth(2);NLOh_Z_mf_d.SetLineStyle(2)

NLOh_pho        = getNormalizedHist(NLOh_pho,NLOh_pho); 
#NLOh_pho.Draw(); raw_input()
NLOh_Z          = getNormalizedHist(NLOh_Z,NLOh_Z) ;    
NLOh_pho_mr_u = getNormalizedHist(NLOh_pho_mr_u,NLOh_pho_mr_u)
NLOh_pho_mr_d = getNormalizedHist(NLOh_pho_mr_d,NLOh_pho_mr_u)
NLOh_pho_mf_u = getNormalizedHist(NLOh_pho_mf_u,NLOh_pho_mf_u)
NLOh_pho_mf_d = getNormalizedHist(NLOh_pho_mf_d,NLOh_pho_mf_u)
NLOh_Z_mr_u   = getNormalizedHist(NLOh_Z_mr_u,NLOh_Z_mr_u)
NLOh_Z_mr_d   = getNormalizedHist(NLOh_Z_mr_d,NLOh_Z_mr_u)
NLOh_Z_mf_u   = getNormalizedHist(NLOh_Z_mf_u,NLOh_Z_mf_u)
NLOh_Z_mf_d   = getNormalizedHist(NLOh_Z_mf_d,NLOh_Z_mf_u)


output = ROOT.TFile("Photon_Z_NLO_kfactors.root","RECREATE")
output.cd()
# Now we want to make Ratio of Z/Photon NLO, Z/Photon LO and Z NLO/LO, Photon NLO/LO
# NLO/LO
NLOh_pho_r_lo 	  = NLOh_pho.Clone()	 ;NLOh_pho_r_lo.SetName("pho_NLO_LO") 
NLOh_pho_mr_ur_lo = NLOh_pho_mr_u.Clone();NLOh_pho_mr_ur_lo.SetName("pho_NLO_LO_mrUp")
NLOh_pho_mr_dr_lo = NLOh_pho_mr_d.Clone();NLOh_pho_mr_dr_lo.SetName("pho_NLO_LO_mrDown")
NLOh_pho_mf_ur_lo = NLOh_pho_mf_u.Clone();NLOh_pho_mf_ur_lo.SetName("pho_NLO_LO_mfUp")
NLOh_pho_mf_dr_lo = NLOh_pho_mf_d.Clone();NLOh_pho_mf_dr_lo.SetName("pho_NLO_LO_mfDown")

NLOh_pho_r_lo.Divide(LOh_pho); NLOh_pho_r_lo.SetLineColor(ROOT.kBlack); NLOh_pho_r_lo.SetLineWidth(2)
NLOh_pho_mr_ur_lo.Divide(LOh_pho)
NLOh_pho_mr_dr_lo.Divide(LOh_pho)

NLOh_pho_mf_ur_lo.Divide(LOh_pho)
NLOh_pho_mf_dr_lo.Divide(LOh_pho)

cv_pho = ROOT.TCanvas("c_pho_nlo_lo","Photon NLO/LO",800,600)
NLOh_pho_r_lo.Draw("PEL")
NLOh_pho_mr_ur_lo.Draw("histsame")
NLOh_pho_mr_dr_lo.Draw("histsame")
NLOh_pho_mf_ur_lo.Draw("histsame")
NLOh_pho_mf_dr_lo.Draw("histsame")
cv_pho.Write()

NLOh_Z_r_lo 	  = NLOh_Z.Clone()	 ;NLOh_Z_r_lo.SetName("Z_NLO_LO") 
NLOh_Z_mr_ur_lo = NLOh_Z_mr_u.Clone();NLOh_Z_mr_ur_lo.SetName("Z_NLO_LO_mrUp")
NLOh_Z_mr_dr_lo = NLOh_Z_mr_d.Clone();NLOh_Z_mr_dr_lo.SetName("Z_NLO_LO_mrDown")
NLOh_Z_mf_ur_lo = NLOh_Z_mf_u.Clone();NLOh_Z_mf_ur_lo.SetName("Z_NLO_LO_mfUp")
NLOh_Z_mf_dr_lo = NLOh_Z_mf_d.Clone();NLOh_Z_mf_dr_lo.SetName("Z_NLO_LO_mfDown")

NLOh_Z_r_lo.Divide(LOh_Z); NLOh_Z_r_lo.SetLineColor(ROOT.kBlack)
NLOh_Z_mr_ur_lo.Divide(LOh_Z)
NLOh_Z_mr_dr_lo.Divide(LOh_Z)
NLOh_Z_mf_ur_lo.Divide(LOh_Z)
NLOh_Z_mf_dr_lo.Divide(LOh_Z)

cv_Z = ROOT.TCanvas("c_Z_nlo_lo","Photon NLO/LO",800,600)
NLOh_Z_r_lo.Draw("PEL")
NLOh_Z_mr_ur_lo.Draw("histsame")
NLOh_Z_mr_dr_lo.Draw("histsame")
NLOh_Z_mf_ur_lo.Draw("histsame")
NLOh_Z_mf_dr_lo.Draw("histsame")
cv_Z.Write()

# Ratios of photon/Z and to nominal!!!
LOh_Z_to_pho 	    = LOh_Z.Clone(); LOh_Z_to_pho.SetName("Z_pho_LO") ; LOh_Z_to_pho.SetLineColor(ROOT.kOrange); LOh_Z_to_pho.SetLineWidth(2)
NLOh_Z_to_pho 	    = NLOh_Z.Clone(); NLOh_Z_to_pho.SetName("Z_pho_NLO") 
NLOh_Z_mr_ur_to_pho = NLOh_Z_mr_u.Clone();NLOh_Z_mr_ur_to_pho.SetName("Z_pho_NLO_mrUp")
NLOh_Z_mr_dr_to_pho = NLOh_Z_mr_d.Clone();NLOh_Z_mr_dr_to_pho.SetName("Z_pho_NLO_mrDown")
NLOh_Z_mf_ur_to_pho = NLOh_Z_mf_u.Clone();NLOh_Z_mf_ur_to_pho.SetName("Z_pho_NLO_mfUp")
NLOh_Z_mf_dr_to_pho = NLOh_Z_mf_d.Clone();NLOh_Z_mf_dr_to_pho.SetName("Z_pho_NLO_mfDown")

LOh_Z_to_pho.Divide(LOh_pho) 
NLOh_Z_to_pho.Divide(NLOh_pho)	  ; NLOh_Z_to_pho.Draw(); raw_input() 
NLOh_Z_mr_ur_to_pho.Divide(NLOh_pho_mr_u)
NLOh_Z_mr_dr_to_pho.Divide(NLOh_pho_mr_d)
NLOh_Z_mf_ur_to_pho.Divide(NLOh_pho_mf_u)
NLOh_Z_mf_dr_to_pho.Divide(NLOh_pho_mf_d)

# We now make another set of up/down templates ONLY for the Z which will represent the uncertainty on the 
# Ratio Z/y from the pdfs. Note! ideally we would make one for the photon and one for the Z but we only 
# have (properly) the envelope on the ratio. 
# First make the RMS band histograms !
RMShist = NLOh_pho.Clone()
for b in range(RMShist.GetNbinsX()):
  RMShist.SetBinContent(b+1,NLOh_Z_to_pho.GetBinContent(b+1))
  # run through pdf hists and get RMS of toys 
  tys = []
  cnv = NLOh_Z_to_pho.GetBinContent(b+1)
  hG = ROOT.TH1F("h_rms_bin%d"%(b+1),"NNPDF ratio samples in bin %d"%(b+1),25,cnv*0.95,cnv*1.105)
  
  for i in range(100):
    hpdf = NLOfile.Get("ratio_pdf_%d"%i)
    tt = hpdf.GetBinContent(b+1)
    tys.append(tt)
    hG.Fill(tt)
  meanx = numpy.mean(tys)
  rms = (numpy.sum([((ty-meanx)**2)/100 for ty in tys]))**0.5
  RMShist.SetBinError(b+1,rms)
  hG.Fit("gaus")
  print rms, hG.GetRMS()
  savehists.append(hG)
  rms = []

RMShist.SetFillColor(ROOT.kMagenta)
RMShist.SetName("RMS_NNPDF_Z_Pho_NLO")

cv_NLO_LO = ROOT.TCanvas("c_R","Z/Photon",800,600)
NLOh_Z_to_pho.SetTitle("R Z(vv)/Photon")
NLOh_Z_to_pho.Draw("PEL")
RMShist.Draw("E2same")
LOh_Z_to_pho.Draw("histsame")
NLOh_Z_mr_ur_to_pho.Draw("histsame")
NLOh_Z_mr_dr_to_pho.Draw("histsame")
NLOh_Z_mf_ur_to_pho.Draw("histsame")
NLOh_Z_mf_dr_to_pho.Draw("histsame")
NLOh_Z_to_pho.Draw("PELsame")
cv_NLO_LO.Write()
# Write the histograms too 
savehists.append(LOh_pho )
savehists.append(LOh_Z   )
savehists.append(NLOh_pho)
savehists.append(NLOh_Z  )
savehists.append(NLOh_pho_mr_u)
savehists.append(NLOh_pho_mr_d)
savehists.append(NLOh_pho_mf_u)
savehists.append(NLOh_pho_mf_d)
savehists.append(NLOh_Z_mr_u  )
savehists.append(NLOh_Z_mr_d  )
savehists.append(NLOh_Z_mf_u  )
savehists.append(NLOh_Z_mf_d  )
savehists.append(NLOh_pho_r_lo 	 )
savehists.append(NLOh_pho_mr_ur_lo)
savehists.append(NLOh_pho_mr_dr_lo)
savehists.append(NLOh_pho_mf_ur_lo)
savehists.append(NLOh_pho_mf_dr_lo)
savehists.append(NLOh_Z_r_lo    )
savehists.append(NLOh_Z_mr_ur_lo)
savehists.append(NLOh_Z_mr_dr_lo)
savehists.append(NLOh_Z_mf_ur_lo)
savehists.append(NLOh_Z_mf_dr_lo)
savehists.append(LOh_Z_to_pho 	   )
savehists.append(NLOh_Z_to_pho 	   )
savehists.append(NLOh_Z_mr_ur_to_pho)
savehists.append(NLOh_Z_mr_dr_to_pho)
savehists.append(NLOh_Z_mf_ur_to_pho)
savehists.append(NLOh_Z_mf_dr_to_pho)


NLOh_Z_pdf_u = makeHist(RMShist,1,NLOh_Z); NLOh_Z_pdf_u.SetName("Z_NLO_LO_pdfUp")
NLOh_Z_pdf_d = makeHist(RMShist,-1,NLOh_Z); NLOh_Z_pdf_d.SetName("Z_NLO_LO_pdfDown")
NLOh_Z_pdf_u.Multiply(NLOh_pho)  # now this is NLOh_Z again but with up/dn error
NLOh_Z_pdf_d.Multiply(NLOh_pho)
# scale to make /LO
NLOh_Z_pdf_u.Divide(LOh_Z)
NLOh_Z_pdf_d.Divide(LOh_Z)
for b in range(NLOh_Z_pdf_u.GetNbinsX()):
 NLOh_Z_pdf_u.SetBinError(b+1,0)
 NLOh_Z_pdf_d.SetBinError(b+1,0)
savehists.append(NLOh_Z_pdf_u)
savehists.append(NLOh_Z_pdf_d)
savehists.append(RMShist)

for s in savehists: s.Write()
print "Output in ", output.GetName()
output.Close()

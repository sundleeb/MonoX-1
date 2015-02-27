# Makes a plot of the variations of the Z(vv) template combined in quadrature

import ROOT as r
import sys, numpy
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)
di0 = r.TFile.Open(sys.argv[1])


def makeFullHist(hn,sysu,sysd,n):
 sf = hn.Integral()/n
 en = 0#((n**0.5)*sf)/hn.Integral()

 h1su = hn.Clone()
 h1sd = hn.Clone()

 for i in range(hn.GetNbinsX()): 
   nb     = hn.GetBinContent(i+1)
   norm_e = 0#nb*en
   toterr_u = toterr_d = 0#norm_e*norm_e
   for j,syu in enumerate(sysu):
   	#print sysu[j].GetName(), "Up ", i,sysu[j].GetBinContent(i+1),nb
        if syu.GetBinContent(i+1) >= nb:
   	 toterr_u += (syu.GetBinContent(i+1)-nb)**2
	else:
   	 toterr_d += (nb - syu.GetBinContent(i+1))**2
   for j,syu in enumerate(sysd): 
   	#print sysd[j].GetName(), "Down", i,sysd[j].GetBinContent(i+1),nb
        if syu.GetBinContent(i+1) >= nb:
   	 toterr_u += (syu.GetBinContent(i+1)-nb)**2
	else:
   	 toterr_d += (nb - syu.GetBinContent(i+1))**2
   #print hn.GetName(), nb, toterr_u, toterr_d
   h1su.SetBinContent(i+1,(toterr_u)**0.5)
   h1sd.SetBinContent(i+1,(toterr_d)**0.5)
 #make a TGraphErrors
 return h1su,h1sd

def makeGrErrors(hn,hu,hd):
 gr = r.TGraphAsymmErrors()
 for i in range(hn.GetNbinsX()):
   gr.SetPoint(i,hn.GetBinCenter(i+1),hn.GetBinContent(i+1))
   gr.SetPointError(i,hn.GetBinWidth(i+1)/2,hn.GetBinWidth(i+1)/2,hd.GetBinContent(i+1),hu.GetBinContent(i+1))
 return gr

def makeDiffGrErrors(hn,hu,hd,hden):
 gr = r.TGraphAsymmErrors()
 for i in range(hn.GetNbinsX()):
   gr.SetPoint(i,hn.GetBinCenter(i+1),hn.GetBinContent(i+1)/hden.GetBinContent(i+1))
   gr.SetPointError(i,hn.GetBinWidth(i+1)/2,hn.GetBinWidth(i+1)/2,hd.GetBinContent(i+1)/hn.GetBinContent(i+1),hu.GetBinContent(i+1)/hn.GetBinContent(i+1))
   print "Bin ",i+1 ,hd.GetBinContent(i+1)/hn.GetBinContent(i+1),hu.GetBinContent(i+1)/hn.GetBinContent(i+1)
 return gr

def getNormalizedHist(hist, templatehist):
  thret = templatehist.Clone()
  nb = hist.GetNbinsX()
  for b in range(1,nb+1): 
    sfactor = 1./templatehist.GetBinWidth(b)
    thret.SetBinContent(b,hist.GetBinContent(b)*sfactor)
    thret.SetBinError(b,hist.GetBinError(b)*sfactor)
    thret.GetYaxis().SetTitle("Events/GeV")
  return thret


#paramsP = []
#params = [0,1,2,3,4,5,6,7,8,9]
# Photon = Combined model combined_model_par_0_Up
di0.cd()
photon_nom = 	  di0.Get("category_%s/ZJets_combined_model"%sys.argv[2]).Clone()
photon_sys_up = []#(di1.Get("category_%s/ZJets_combined_model_par_%d_Up"%(sys.argv[3],i))).Clone()   for i in paramsP]
photon_sys_dn = []#(di1.Get("category_%s/ZJets_combined_model_par_%d_Down"%(sys.argv[3],i))).Clone()   for i in paramsP]
norm_pho      = 1
i = 0
while i>=0:
 try:
  (di0.Get("category_%s/ZJets_combined_model_par_%d_Up"%(sys.argv[2],i)).Clone()).GetName() 
  photon_sys_up.append((di0.Get("category_%s/ZJets_combined_model_par_%d_Up"%(sys.argv[2],i))).Clone()) 
  photon_sys_dn.append((di0.Get("category_%s/ZJets_combined_model_par_%d_Down"%(sys.argv[2],i))).Clone())
  i+=1
 except : 
  i=-1 

pho_u, pho_d = makeFullHist(photon_nom,photon_sys_up,photon_sys_dn,norm_pho)
pho_u = getNormalizedHist(pho_u,pho_u)
pho_d = getNormalizedHist(pho_d,pho_d)
pho_n = getNormalizedHist(photon_nom,photon_nom)
grpho = makeGrErrors(pho_n,pho_u,pho_d)
grphod = makeDiffGrErrors(pho_n,pho_u,pho_d,pho_n) # ratio TO Zmm model!
grpho.SetFillColor(r.kGreen)
grphod.SetFillColor(r.kGreen)
pho_n.SetLineColor(r.kGreen)

zero = photon_nom.Clone()
zero.GetYaxis().SetNdivisions(5)
zero.GetYaxis().SetLabelSize(0.1)
zero.GetYaxis().SetTitleSize(0.12)
zero.GetXaxis().SetTitleSize(0.085)
zero.GetXaxis().SetLabelSize(0.1)
zero.Divide(photon_nom)
line = r.TLine(photon_nom.GetXaxis().GetXmin(),1,photon_nom.GetXaxis().GetXmax(),1)
line.SetLineColor(1)
line.SetLineStyle(2)
line.SetLineWidth(3)

canvrat = r.TCanvas("cr","cr",800,360)
canvrat.SetBottomMargin(0.16)
zero.SetTitle("")
zero.GetYaxis().SetTitle("variation/nominal")
zero.GetYaxis().SetTitleSize(0.06)
zero.GetXaxis().SetTitleSize(0.055)
zero.GetYaxis().SetTitleOffset(0.6)
zero.GetYaxis().SetLabelSize(0.07)
zero.GetXaxis().SetLabelSize(0.07)
zero.GetXaxis().SetTitle("E_{T}^{miss}")
zero.GetXaxis().SetTitleOffset(1.2)
#grzvvd.Draw("AL")
grphod.Draw("AL")
#zero.SetMaximum(3)
#zero.SetMinimum(0.5)
zero.SetMaximum(grphod.GetYaxis().GetXmax())
zero.SetMinimum(grphod.GetYaxis().GetXmin())
zero.Draw("hist")
grphod.Draw("E2same")
#zero.Draw("histLsame")
#zero.SetLineStyle(2);zero.SetLineColor(1)
line.Draw()
leg = r.TLegend(0.6,0.65,0.89,0.89)
leg.SetFillColor(0)
leg.SetTextFont(42)
leg.AddEntry(grphod,"Z(vv) from dimuon + #gamma+Jets","F")
leg.Draw()
canvrat.SetGridy()
canvrat.RedrawAxis()
r.gStyle.SetOptStat(0)
canvrat.SaveAs("errors_combined_or_zmm_%s.root"%sys.argv[2])
canvrat.SaveAs("errors_combined_or_zmm_%s.pdf"%sys.argv[2])
canvrat.SaveAs("errors_combined_or_zmm_%s.png"%sys.argv[2])

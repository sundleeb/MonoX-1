# simple SMP-14-005 study Z/Photon measurement

import ROOT as r 
r.gStyle.SetOptStat(0)
import array
#infile = r.TFile.Open("mono-x.root") 
infile = r.TFile.Open("../mono-x-vtagged.root") 
fkFactor = r.TFile.Open("../Photon_Z_NLO_kfactors.root")
nlo_pho = fkFactor.Get("pho_NLO_LO")
nlo_zjt = fkFactor.Get("Z_NLO_LO")
nlo_ewkUp    = fkFactor.Get("EWK_Up")
nlo_ewkDn    = fkFactor.Get("EWK_Dwon")
# Make it a correction on the Z by inverting !
#for b in range(nlo_ewkUp.GetNbinsX()): nlo_ewkUp.SetBinContent(b+1,1./nlo_ewkUp.GetBinContent(b+1))

#nlo_ewkDn    = nlo_ewkUp.Clone(); nlo_ewkDn.SetName("double_corr");# nlo_ewkDn.Multiply(nlo_ewkUp,0.5)
#for b in range(nlo_ewkDn.GetNbinsX()): nlo_ewkDn.SetBinContent(b+1,nlo_ewkDn.GetBinContent(b+1)**1.6)

nlo_pho_mrUp = fkFactor.Get("pho_NLO_LO_mrUp")
nlo_zjt_mrUp = fkFactor.Get("Z_NLO_LO_mrUp")
nlo_pho_mrDown = fkFactor.Get("pho_NLO_LO_mrDown")
nlo_zjt_mrDown = fkFactor.Get("Z_NLO_LO_mrDown")
nlo_pho_mfUp = fkFactor.Get("pho_NLO_LO_mfUp")
nlo_zjt_mfUp = fkFactor.Get("Z_NLO_LO_mfUp")
nlo_pho_mfDown = fkFactor.Get("pho_NLO_LO_mfDown")
nlo_zjt_mfDown = fkFactor.Get("Z_NLO_LO_mfDown")



r.gROOT.ProcessLine(".L diagonalizer.cc+")
from ROOT import diagonalizer

bins = array.array('d',[225,250,275,300,350,400,450,500,1000])
#bins = array.array('d',[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000])

phoX = "ptpho"
ZX   = "ptll"
#phoX = "jet1pt"
#ZX   = "jet1pt"

#phoX = "mvamet"
#ZX   = "mvamet"

base = r.TH1F("base",";p_{T}^{#mu#mu} or p_{T}^{#gamma}; R Z(#rightarrow#mu#mu)/#gamma",len(bins)-1,bins)
one  = r.TH1F("ONE",";p_{T}^{#mu#mu} or p_{T}^{#gamma};  R Z(#rightarrow#mu#mu)/#gamma",1,0,10000)
for b in range(one.GetNbinsX()): one.SetBinContent(b+1,1)

Workspace = infile.Get("category_inclusive/wspace_inclusive")
#Workspace = infile.Get("category_monojet/wspace_monojet")
diag = diagonalizer(Workspace)

photon_d = base.Clone(); photon_d.SetName("photon_data")
photon_d.Sumw2()
diag.generateWeightedTemplate(photon_d,one,"mvamet",phoX,Workspace.data("photon_data"))
photon_b =  photon_d.Clone(); photon_b.SetName("photon_bkg")
photon_b.Scale(0.03)

zmm_d = base.Clone(); zmm_d.SetName("zmm_data")
zmm_d.Sumw2()
diag.generateWeightedTemplate(zmm_d,one,"mvamet",ZX,Workspace.data("dimuon_data"))
zmm_b = base.Clone(); zmm_b.SetName("zmm_bkg")
diag.generateWeightedTemplate(zmm_b,one,"mvamet",ZX,Workspace.data("dimuon_all_background"))

# Add 1% muoneff/pho eff uncerts to datapoints
for b in range(photon_d.GetNbinsX()):
  pi = photon_d.GetBinContent(b+1);
  zi = zmm_d.GetBinContent(b+1);
  photon_d.SetBinError(b+1, ( (photon_d.GetBinError(b+1))**2 + (pi*0.01)**2 )**0.5)
  zmm_d.SetBinError(b+1, ( (zmm_d.GetBinError(b+1))**2 + (zi*0.01)**2 )**0.5)

#photon_d.Add(photon_b,-1)
#zmm_d.Add(zmm_b,-1)

# Photon to Z ratio in data -> Easy !
zmm_d.Divide(photon_d)
zmm_d.SetLineColor(1)
zmm_d.SetLineWidth(3)

# Now we do the same in MC BUT we have to correct the photon peice
diag.generateWeightedDataset("photon_gjet_nlo"		,nlo_pho,"weight","genVpt",Workspace,"photon_gjet")
diag.generateWeightedDataset("dimuon_zll_nlo"           ,nlo_zjt,"weight","genVpt",Workspace,"dimuon_zll")
diag.generateWeightedDataset("dimuon_zll_nlo_ewk"     	,nlo_ewkUp,"weight","genVpt",Workspace,"dimuon_zll_nlo")
diag.generateWeightedDataset("dimuon_zll_nlo_ewk_dn"    ,nlo_ewkDn,"weight","genVpt",Workspace,"dimuon_zll_nlo")  # this says, apply twice!!
#diag.generateWeightedDataset("photon_gjet_nlo"		,one,"weight","genVpt",Workspace,"photon_gjet")
#diag.generateWeightedDataset("dimuon_zll_nlo"           ,one,"weight","genVpt",Workspace,"dimuon_zll")
#diag.generateWeightedDataset("dimuon_zll_nlo_ewk"     	,nlo_ewkUp,"weight","genVpt",Workspace,"dimuon_zll_nlo")
#diag.generateWeightedDataset("dimuon_zll_nlo_ewk_dn"    ,nlo_ewkDn,"weight","genVpt",Workspace,"dimuon_zll_nlo")

# Correction QCD 
photon_mc = base.Clone(); photon_mc.SetName("photon_mc")
diag.generateWeightedTemplate(photon_mc,one,"genVpt",phoX,Workspace.data("photon_gjet_nlo"))

photon_mc_lo = base.Clone(); photon_mc_lo.SetName("photon_mc_RAW")
diag.generateWeightedTemplate(photon_mc_lo,one,"genVpt",phoX,Workspace.data("photon_gjet"))

zmm_mc_lo = base.Clone(); zmm_mc_lo.SetName("zmm_mc_RAW")
diag.generateWeightedTemplate(zmm_mc_lo,one,"genVpt",ZX,Workspace.data("dimuon_zll"))

zmm_mc = base.Clone(); zmm_mc.SetName("zmm_mc")
diag.generateWeightedTemplate(zmm_mc,one,"genVpt",ZX,Workspace.data("dimuon_zll_nlo")) # 0  ewk

zmm_mc_e_u = base.Clone(); zmm_mc_e_u.SetName("zmm_mc_e_u")
diag.generateWeightedTemplate(zmm_mc_e_u,one,"genVpt",ZX,Workspace.data("dimuon_zll_nlo_ewk"))	  # EWK U 
zmm_mc_e_d = base.Clone(); zmm_mc_e_d.SetName("zmm_mc_e_d")
diag.generateWeightedTemplate(zmm_mc_e_d,one,"genVpt",ZX,Workspace.data("dimuon_zll_nlo_ewk_dn")) # EWK D


# we also make QCD mr, mf scale uncertainties 
diag.generateWeightedDataset("dimuon_zll_EWK_only"     	,nlo_ewkUp,"weight","genVpt",Workspace,"dimuon_zll")

photon_mc_mrup = base.Clone(); photon_mc_mrup.SetName("photon_mc_mrup")
photon_mc_mrdn = base.Clone(); photon_mc_mrdn.SetName("photon_mc_mrdn")
photon_mc_mfup = base.Clone(); photon_mc_mfup.SetName("photon_mc_mfup")
photon_mc_mfdn = base.Clone(); photon_mc_mfdn.SetName("photon_mc_mfdn")
diag.generateWeightedTemplate(photon_mc_mrup,nlo_pho_mrUp,"genVpt",phoX,Workspace.data("photon_gjet"))  
diag.generateWeightedTemplate(photon_mc_mrdn,nlo_pho_mrDown,"genVpt",phoX,Workspace.data("photon_gjet")) 
diag.generateWeightedTemplate(photon_mc_mfup,nlo_pho_mfUp,"genVpt",phoX,Workspace.data("photon_gjet")) 
diag.generateWeightedTemplate(photon_mc_mfdn,nlo_pho_mfDown,"genVpt",phoX,Workspace.data("photon_gjet")) 

zmm_mc_mrup = base.Clone(); zmm_mc_mrup.SetName("zmm_mc_mrup")
zmm_mc_mrdn = base.Clone(); zmm_mc_mrdn.SetName("zmm_mc_mrdn")
zmm_mc_mfup = base.Clone(); zmm_mc_mfup.SetName("zmm_mc_mfup")
zmm_mc_mfdn = base.Clone(); zmm_mc_mfdn.SetName("zmm_mc_mfdn")

diag.generateWeightedTemplate(zmm_mc_mrup,nlo_zjt_mrUp,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mrdn,nlo_zjt_mrDown,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mfup,nlo_zjt_mfUp,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 
diag.generateWeightedTemplate(zmm_mc_mfdn,nlo_zjt_mfDown,"genVpt",ZX,Workspace.data("dimuon_zll_EWK_only")) 

zmm_mc_mrup.Divide(photon_mc_mrup)
zmm_mc_mrdn.Divide(photon_mc_mrdn)
zmm_mc_mfup.Divide(photon_mc_mfup)
zmm_mc_mfdn.Divide(photon_mc_mfdn)


#########################################################################################################

zmm_mc_lo.Divide(photon_mc_lo)
zmm_mc.Divide(photon_mc)

zmm_mc_e_u.Divide(photon_mc)
zmm_mc_e_d.Divide(photon_mc)

zmm_mc.SetLineWidth(3)
zmm_mc_lo.SetLineWidth(3)
zmm_mc_e_u.SetLineWidth(3)
zmm_mc_e_d.SetLineWidth(3)

errs = zmm_mc.Clone()
for b in range(zmm_mc.GetNbinsX()): 
	cv = zmm_mc.GetBinContent(b+1)
        diffu = abs(zmm_mc_e_u.GetBinContent(b+1)- cv )
        diffd = abs(zmm_mc_e_d.GetBinContent(b+1)- cv)

	errT = (max(diffu,diffd))**2

	# add in quad from the others 
	diffmc_mr_u = zmm_mc_mrup.GetBinContent(b+1) - cv
	diffmc_mr_d = zmm_mc_mrdn.GetBinContent(b+1) - cv
	diffmc_mf_u = zmm_mc_mfup.GetBinContent(b+1) - cv
	diffmc_mf_d = zmm_mc_mfdn.GetBinContent(b+1) - cv

	derr_mr = 0.5*(abs(diffmc_mr_u)+abs(diffmc_mr_d))
	derr_mf = 0.5*(abs(diffmc_mf_u)+abs(diffmc_mf_d))

	errT+=derr_mr**2
	errT+=derr_mf**2

	errs.SetBinError(b+1,errT**0.5)




zmm_mc_lo.SetLineColor(r.kOrange)
zmm_mc.SetLineColor(4)
errs.SetFillColor(r.kGray)

zmm_d.SetMarkerSize(1.2)
zmm_d.SetMarkerStyle(20)
zmm_d.GetXaxis().SetName("fake E_{T}^{miss}")
zmm_d.Draw("pel")
errs.Draw("sameE2")
zmm_mc.Draw("samehist")
zmm_mc_lo.Draw("same")
zmm_d.Draw("pelsame")

leg = r.TLegend(0.6,0.6,0.89,0.89)
leg.SetFillColor(0)
leg.SetTextFont(42)
leg.AddEntry(zmm_d,"Data #pm (stat + exp syst)","pel")
leg.AddEntry(zmm_mc_lo,"Madgraph Raw","L")
leg.AddEntry(zmm_mc,"NLO corrected, Theory #pm 1#sigma","LF")
leg.Draw()
raw_input()


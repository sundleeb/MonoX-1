void drawSfactors(std::string file, std::string category){
   TFile *fi = TFile::Open(file.c_str());
   
TH1F mc("mc","mc",1,0,1);
mc.SetMarkerSize(1.2);
mc.SetMarkerStyle(20);
mc.SetMarkerColor(1);
mc.SetLineColor(1);
mc.SetLineStyle(1);
mc.SetLineWidth(2);

TH1F dat("dat","dat",1,0,1);
dat.SetMarkerSize(1.2);
dat.SetMarkerStyle(20);
dat.SetMarkerColor(1);
dat.SetLineColor(1);
dat.SetLineWidth(2);

TH1F datafit("datafit","datafit",1,0,1);
datafit.SetMarkerSize(1.2);
datafit.SetMarkerStyle(24);
datafit.SetMarkerColor(1);
datafit.SetLineColor(4);
datafit.SetLineStyle(1);
datafit.SetLineWidth(2);


TH1F mcfit("mcfit","mcfit",1,0,1);
mcfit.SetMarkerSize(1.2);
mcfit.SetMarkerStyle(24);
mcfit.SetMarkerColor(2);
mcfit.SetLineColor(2);
mcfit.SetLineStyle(1);
mcfit.SetLineWidth(2);


std::string cats[1] = {category};

gROOT->SetBatch(1);
int c = 0;
gStyle->SetOptStat(0);
//for (int c=0;c<3;c++){
TLatex *lat = new TLatex();
lat->SetNDC();
lat->SetTextSize(0.04);
lat->SetTextFont(42);
  
  fi->cd(Form("category_%s",cats[c].c_str()));
  TLegend *ld = new TLegend(0.5,0.65,0.89,0.89);ld->SetFillColor(0);
  ld->AddEntry(&mcfit,"Z(#rightarrow#nu#nu) MC","L");
  ld->AddEntry(&datafit,"Corrected Z(#rightarrow#nu#nu) MC","L");
  signal_zjetsregion_mc_fit_before_after->SetLogy(); 
  signal_zjetsregion_mc_fit_before_after->Draw();
  ld->Draw();
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
  lat->DrawLatex(0.7,0.92,Form("%s category",cats[c].c_str()));
  signal_zjetsregion_mc_fit_before_after->SaveAs(Form("combined_post_fit_%s.pdf",cats[c].c_str()));
  signal_zjetsregion_mc_fit_before_after->SaveAs(Form("combined_post_fit_%s.png",cats[c].c_str()));
  
  TCanvas *c_pho = new TCanvas("cpho","cpho",800,550);
  TH1F *hpho = (TH1F*)fi->Get(Form("category_%s/photon_weights_%s",cats[c].c_str(),cats[c].c_str()));
  hpho->SetMarkerSize(1.0);
  hpho->SetMarkerStyle(20);
  hpho->GetXaxis()->SetTitle("MET (GeV)");
  hpho->GetYaxis()->SetTitle("R^{#gamma}");
  hpho->GetYaxis()->SetTitleSize(0.07);
  hpho->GetYaxis()->SetTitleOffset(0.6);
  hpho->GetXaxis()->SetTitleSize(0.04);
  hpho->SetTitle("");
  hpho->SetMarkerColor(kBlue+1);
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Simulation}");
  lat->DrawLatex(0.7,0.92,Form("%s category",cats[c].c_str()));
  hpho->GetYaxis()->SetRangeUser(0.,1.);
  hpho->Draw();
  c_pho->SaveAs(Form("photon_weights_%s.pdf",cats[c].c_str()));
  c_pho->SaveAs(Form("photon_weights_%s.png",cats[c].c_str()));
  
  TCanvas *c_Z = new TCanvas("cZ","cZ",800,550);
  TH1F *hZ = (TH1F*)fi->Get(Form("category_%s/zmm_weights_%s",cats[c].c_str(),cats[c].c_str()));
  hZ->SetMarkerSize(1.0);
  hZ->SetMarkerStyle(20);
  hZ->GetXaxis()->SetTitle("MET (GeV)");
  hZ->GetYaxis()->SetTitle("R^{Z}");
  hZ->GetYaxis()->SetTitleOffset(0.6);
  hZ->GetYaxis()->SetTitleSize(0.07);
  hZ->GetXaxis()->SetTitleSize(0.04);
  hZ->SetTitle("");
  hZ->SetMarkerColor(kBlue+1);
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Simulation}");
  lat->DrawLatex(0.7,0.92,Form("%s category",cats[c].c_str()));
  hZ->GetYaxis()->SetRangeUser(2,15);
  hZ->Draw();
  c_Z->SaveAs(Form("zmm_weights_%s.pdf",cats[c].c_str()));
  c_Z->SaveAs(Form("zmm_weights_%s.png",cats[c].c_str()));

  fi->cd(Form("category_%s",cats[c].c_str()));
  lat->SetTextSize(0.03);
  // Finally plot the Control Region
  //c_ControlRegion_0->SetLogy();
  c_ControlRegion_0->Draw();
  lat->DrawLatex(0.7,0.94,Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.7,0.03,"fake MET (GeV)");
  c_ControlRegion_0->SaveAs(Form("post_fit_photon_%s.pdf",cats[c].c_str()));
  c_ControlRegion_0->SaveAs(Form("post_fit_photon_%s.png",cats[c].c_str()));

  //c_ControlRegion_1->SetLogy();
  c_ControlRegion_1->Draw();
  lat->DrawLatex(0.7,0.94,Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.7,0.03,"fake MET (GeV)");
  c_ControlRegion_1->SaveAs(Form("post_fit_zmm_%s.pdf",cats[c].c_str()));
  c_ControlRegion_1->SaveAs(Form("post_fit_zmm_%s.png",cats[c].c_str()));

  // Canvas for the variations of the systematics 
  canv_variations->Draw();
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
  lat->DrawLatex(0.7,0.94,Form("%s category",cats[c].c_str()));
  canv_variations->SaveAs(Form("systematic_variations_%s.pdf",cats[c].c_str()));
  canv_variations->SaveAs(Form("systematic_variations_%s.png",cats[c].c_str()));

  canv_variations_ratio->Draw();
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
  lat->DrawLatex(0.7,0.94,Form("%s category",cats[c].c_str()));
  canv_variations_ratio->SaveAs(Form("systematic_variations_ratio_%s.pdf",cats[c].c_str()));
  canv_variations_ratio->SaveAs(Form("systematic_variations_ratio_%s.png",cats[c].c_str()));


  // Finally make a ratio of the pre->post fit expectation of the Z(vv) template!, bit of a pain but can do it!
  TCanvas *canCorr  = new TCanvas();
  /*
  double xmin = hpho->GetBinLowEdge(1);
  double xmax = hpho->GetBinLowEdge(hpho->GetNbinsX()+1);
  RooCurve *crv_mc = (RooCurve*) (zjets_signalregion_mc_fit_before_after->GetListOfPrimitives()->FindObject(Form("doubleExponential_dimuon_mc%s_Norm[mvamet]",cats[c].c_str())));
  RooCurve *crv_da = (RooCurve*) (zjets_signalregion_mc_fit_before_after->GetListOfPrimitives()->FindObject(Form("doubleExponential_dimuon_data%s_Norm[mvamet]",cats[c].c_str())));
  TGraph *gr = new TGraph();
  int pt=0;
  for (double x=xmin;x<=xmax;x+=1){
	double num = crv_da->Eval(x);
	double denum = crv_mc->Eval(x);
	gr->SetPoint(pt,x,num/denum);
	pt++;
  }
  gr->SetLineColor(4); gr->SetLineWidth(2);
  gr->Draw("AL");
  gr->GetXaxis()->SetTitle("E_{T}^{miss}");
  gr->GetYaxis()->SetTitle("r(E_{T}^{miss}) - Z#nu#nu Correction function");
  */
  TH1F *hc = (TH1F*)fi->Get(Form("category_%s/correction_weights_%s",cats[c].c_str(),cats[c].c_str()));
  hc->SetTitle("");
  hc->GetXaxis()->SetTitle("E_{T}^{miss}");
  hc->GetYaxis()->SetTitle("r(E_{T}^{miss}) - Z#nu#nu Correction function");
  hc->Draw("hist");
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
  lat->DrawLatex(0.7,0.94,Form("%s category",cats[c].c_str()));
  canCorr->SaveAs(Form("correction_zvv_ratio_%s.pdf",cats[c].c_str()));
  canCorr->SaveAs(Form("correction_zvv_ratio_%s.png",cats[c].c_str()));

}

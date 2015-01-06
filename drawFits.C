// Data 
void drawFits(std::string file, std::string category){
TFile *fi = TFile::Open(file.c_str());

TH1F dat("dat","dat",1,0,1);
dat.SetMarkerSize(1.2);
dat.SetMarkerStyle(20);
dat.SetMarkerColor(1);
dat.SetLineColor(1);
dat.SetLineWidth(2);

TH1F bkg("bkg","bkg",1,0,1);
bkg.SetMarkerSize(1.2);
bkg.SetMarkerStyle(kCircle);
bkg.SetMarkerColor(1);
bkg.SetLineColor(1);
bkg.SetLineWidth(2);

TH1F bkgfit("bkgfit","bkgfit",1,0,1);
bkgfit.SetMarkerSize(1.2);
bkgfit.SetMarkerStyle(24);
bkgfit.SetMarkerColor(1);
bkgfit.SetLineColor(1);
bkgfit.SetLineStyle(2);
bkgfit.SetLineWidth(2);

TH1F datafit("datafit","datafit",1,0,1);
datafit.SetMarkerSize(1.2);
datafit.SetMarkerStyle(24);
datafit.SetMarkerColor(1);
datafit.SetLineColor(4);
datafit.SetLineStyle(1);
datafit.SetLineWidth(2);

// MC
TH1F mc("mc","mc",1,0,1);
mc.SetMarkerSize(1.2);
mc.SetMarkerStyle(20);
mc.SetMarkerColor(1);
mc.SetLineColor(1);
mc.SetLineStyle(1);
mc.SetLineWidth(2);

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
//for (int c=0;c<3;c++){
TLatex *lat = new TLatex();
lat->SetNDC();
lat->SetTextSize(0.04);
lat->SetTextFont(42);
  fi->cd(Form("category_%s",cats[c].c_str()));
  TLegend *ld = new TLegend(0.5,0.65,0.89,0.89);ld->SetFillColor(0);
  ld->AddEntry(&dat,"Data","PE1");
  ld->AddEntry(&bkg,"Backgrounds","PE1");
  ld->AddEntry(&datafit,"Data Fit","L");
  ld->AddEntry(&bkgfit,"Backgrounds Fit","L");

  singlemuon_datafit->Draw();
  singlemuon_datafit->SetTitle(Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.7,0.92,Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
  ld->Draw(); 
  singlemuon_datafit->SaveAs(Form("data_singlemuon_%s.pdf",cats[c].c_str()));
  singlemuon_datafit->SaveAs(Form("data_singlemuon_%s.png",cats[c].c_str()));
  dimuon_datafit->Draw();
  dimuon_datafit->SetTitle(Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.7,0.92,Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
  ld->Draw(); 
  dimuon_datafit->SaveAs(Form("data_dimuon_%s.pdf",cats[c].c_str()));
  dimuon_datafit->SaveAs(Form("data_dimuon_%s.png",cats[c].c_str()));
   
  TLegend *lmw = new TLegend(0.5,0.75,0.89,0.89);lmw->SetFillColor(0);
  lmw->AddEntry(&mc,"W(#mu#nu) + jets MC ","PE1");
  lmw->AddEntry(&mcfit,"MC Fit","L");
  singlemuon_mcfit->Draw();
  singlemuon_mcfit->SetTitle(Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.7,0.92,Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
  lmw->Draw();
  singlemuon_mcfit->SaveAs(Form("mc_singlemuon_%s.pdf",cats[c].c_str()));
  singlemuon_mcfit->SaveAs(Form("mc_singlemuon_%s.png",cats[c].c_str()));

  TLegend *lmz = new TLegend(0.5,0.75,0.89,0.89); lmz->SetFillColor(0);
  lmz->AddEntry(&mc,"Z(#mu#mu) + jets MC","PE");
  lmz->AddEntry(&mcfit,"MC Fit","L");
  dimuon_mcfit->Draw();
  dimuon_mcfit->SetTitle(Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.7,0.92,Form("%s category",cats[c].c_str()));
  lat->DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}");
  //lat->DrawLatex(0.1,0.92,Form("%s category",cats[c].c_str()));
  lmz->Draw();
  dimuon_mcfit->SaveAs(Form("mc_dimuon_%s.pdf",cats[c].c_str()));
  dimuon_mcfit->SaveAs(Form("mc_dimuon_%s.png",cats[c].c_str()));

  singlemuon_ratio->SetTitle(Form("%s category",cats[c].c_str())); 
  singlemuon_ratio->SaveAs(Form("ratio_singlemuon_%s.pdf",cats[c].c_str())); 
  singlemuon_ratio->SaveAs(Form("ratio_singlemuon_%s.png",cats[c].c_str())); 
  dimuon_ratio->SetTitle(Form("%s category",cats[c].c_str())); 
  dimuon_ratio->SaveAs(Form("ratio_dimuon_%s.pdf",cats[c].c_str()));
  dimuon_ratio->SaveAs(Form("ratio_dimuon_%s.png",cats[c].c_str()));
//  dimuon_mcfit->Clear();
//  dimuon_datafit->Clear();
//  singlemuon_mcfit->Clear();
//  singlemuon_datafit->Clear();
  
//}

}

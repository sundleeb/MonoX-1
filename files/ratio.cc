#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include <string>
#include <sstream>

double* fAxis = new double[50];

void setupAxis() {
  fAxis[0] = 150.;
  for(int i0 = 1;  i0 < 25; i0++) fAxis[i0] = fAxis[i0-1]+6.;
  for(int i0 = 25; i0 < 35; i0++) fAxis[i0] = fAxis[i0-1]+10;
  for(int i0 = 35; i0 < 45; i0++) fAxis[i0] = fAxis[i0-1]+25;
  for(int i0 = 45; i0 < 49; i0++) fAxis[i0] = fAxis[i0-1]+50;
  fAxis[49] = 1500.;
}
TH1F* drawNew(std::string iLabel,TTree *iTree,std::string iWeight,std::string iCut,bool iNormalize=true) {
  std::string lName = iLabel;
  TH1F *lW0 = new TH1F("W0","W0",1,-1000000,10000000000);
  TH1F *lH0 = new TH1F(lName.c_str(),lName.c_str(),49,fAxis);
  if(iNormalize)  iTree->Draw("v_pt>>W0","evtweight");
  if(iNormalize)  iTree->Draw(("v_pt>>"+lName).c_str(),(iWeight+"evtweight"+iCut).c_str());
  if(iNormalize)  lH0->Scale(1./lW0->Integral());
  if(!iNormalize) iTree->Draw(("v_pt>>"+lName).c_str(),(iWeight+"mcweight"+iCut).c_str());
  delete lW0;
  return lH0;
}
TH1F* drawOld(std::string iLabel,TTree *iTree,std::string iWeight,std::string iCut) {
  std::string lName = iLabel;
  TH1F *lW0 = new TH1F("W0","W0",1,-1000000,10000000000);
  TH1F *lH0 = new TH1F(lName.c_str(),lName.c_str(),49,fAxis);
  iTree->Draw("dm_pt>>W0","effweight");
  iTree->Draw(("dm_pt>>"+lName).c_str(),(iWeight+"effweight"+iCut).c_str());
  lH0->Scale(1./lW0->Integral());
  delete lW0;
  return lH0;
}
TH1F** drawPdf(std::string iLabel0,TTree *iTree0,std::string iWeight0,std::string iCut0,int iId0) {
  TH1F **lH = new TH1F*[100];
  for(int i0 = 0; i0 < 100; i0++) {
    std::stringstream pWeight; pWeight << "*(pdf[" << i0 << "])*";
    std::stringstream pLabel0; pLabel0 << iLabel0 << "pdf" << i0;
    if(fabs(iId0) == 1) lH[i0]     = drawNew(pLabel0.str(),iTree0,iWeight0+pWeight.str(),iCut0,iId0 < 0);
    if(fabs(iId0) == 0) lH[i0]     = drawOld(pLabel0.str(),iTree0,iWeight0+pWeight.str(),iCut0);
  }
  return lH;
}
TH1F** drawScale(std::string iLabel0,TTree *iTree0,std::string iWeight0,std::string iCut0,int iId0) {
  TH1F**lH = new TH1F*[2];
  for(int i0 = 0; i0 < 2; i0++) {
    std::stringstream pWeight;
    if(i0 == 0) pWeight << "*scale00*";
    if(i0 == 1) pWeight << "*scale22*";
    std::stringstream pLabel0; pLabel0 << iLabel0 << "scale" << i0;
    if(fabs(iId0) == 1) lH[i0]     = drawNew(pLabel0.str(),iTree0,iWeight0+pWeight.str(),iCut0,iId0 < 0);
    if(fabs(iId0) == 0) lH[i0]     = drawOld(pLabel0.str(),iTree0,iWeight0+pWeight.str(),iCut0);
  }
  return lH;
}
TH1F* makeRatio(TH1F *iBH0,TH1F *iBH1) {
  std::string lNRatio = std::string(iBH0->GetName()) +"_"+ std::string(iBH1->GetName());
  TH1F *lRatio = (TH1F*) iBH0->Clone(lNRatio.c_str());
  lRatio->Divide(iBH1);
  return lRatio;
}
TH1F** pdfUnc(TH1F *iBH0,TH1F *iBH1,TH1F **iH0,TH1F** iH1) {
  std::string lNRatio = std::string(iBH0->GetName()) +"_"+ std::string(iBH1->GetName());
  TH1F *lRatio = (TH1F*) iBH0->Clone(lNRatio.c_str());
  lRatio->Divide(iBH1);
  int    *lNU = new int   [iBH0->GetNbinsX()];
  int    *lND = new int   [iBH0->GetNbinsX()];
  double *lXU = new double[iBH0->GetNbinsX()];
  double *lXD = new double[iBH0->GetNbinsX()];
  for(int i0 = 0; i0 < 100; i0++) {
    std::stringstream pTmp; pTmp << "tmp" << i0;
    TH1F* pRatio = (TH1F*) iH0[i0]->Clone(pTmp.str().c_str());
    pRatio->Divide(iH1[i0]);
    for(int i1 = 1; i1 < iBH0->GetNbinsX()+1; i1++) {
      double pCVal = lRatio->GetBinContent(i1);
      double pTVal = pRatio->GetBinContent(i1);
      if(pTVal > pCVal) lNU[i1-1]++;
      if(pTVal < pCVal) lND[i1-1]++;
      if(pTVal > pCVal) lXU[i1-1]+= (pTVal-pCVal)*(pTVal-pCVal);
      if(pTVal > pCVal) lXD[i1-1]+= (pTVal-pCVal)*(pTVal-pCVal);
    }
  }
  TH1F **lRatios = new TH1F*[2];
  lRatios[0] = (TH1F*) lRatio->Clone((lNRatio+"_pdfUp").c_str());
  lRatios[1] = (TH1F*) lRatio->Clone((lNRatio+"_pdfDown").c_str());
  for(int i0 = 1; i0 < iBH0->GetNbinsX()+1; i0++) lRatios[0]->SetBinContent(i0,lRatio->GetBinContent(i0)+sqrt(lXU[i0-1])/lNU[i0-1]);
  for(int i0 = 1; i0 < iBH0->GetNbinsX()+1; i0++) lRatios[1]->SetBinContent(i0,lRatio->GetBinContent(i0)+sqrt(lXD[i0-1])/lND[i0-1]);
  return lRatios;
}
TH1F** scaleUnc(TH1F *iBH0,TH1F *iBH1,TH1F **iH0,TH1F** iH1) {
  std::string lNRatio = std::string(iBH0->GetName()) +"_"+ std::string(iBH1->GetName());
  TH1F **lRatios = new TH1F*[2];
  lRatios[0] = (TH1F*) iH0[0]->Clone((lNRatio+"_scaleUp").c_str());
  lRatios[1] = (TH1F*) iH0[1]->Clone((lNRatio+"_scaleDown").c_str());
  lRatios[0]->Divide(iH1[0]);
  lRatios[1]->Divide(iH1[1]);
  return lRatios;
}
void write(std::string iName,int iN,TH1F** iH0) {
  TFile *lFile = new TFile(iName.c_str(),"UPDATE");
  for(int i0 = 0; i0 < iN; i0++) {
    iH0[i0]->Write();
  }
  lFile->Close();
}
TTree* load(std::string iFileName) {
  TFile* lFile; lFile = TFile::Open(iFileName.c_str());
  TTree* lTree = (TTree*) lFile->FindObjectAny("Events");
  return lTree;
}
void ratio() {
  setupAxis();
  std::string lGJetsLO  = "/tmp/pharris/Spring15_a25ns_GJets_HT_LO.root";
  std::string lGJetsNLO = "/tmp/pharris/A_13TeV_v2.root";
  TTree *lTGJetsLO  = load(lGJetsLO);
  TTree *lTGJetsNLO = load(lGJetsNLO);
  TH1F** lHGJets = new TH1F*[3];
  lHGJets[0] = drawNew("gjetsLO" ,lTGJetsLO ,""         ,"*(v_y    < 1.5)",false);
  lHGJets[1] = drawOld("gjetsNLO",lTGJetsNLO,"mcweight*","*(dm_eta < 1.5)");
  lHGJets[2] = makeRatio(lHGJets[1],lHGJets[0]);
  write("Ratio.root",3.,lHGJets);
  //W+jets NLO Merged/LO
  std::string lWJetsLO  = "/tmp/pharris/Spring15_a25ns_WJetsToLNu_HTLO.root";
  std::string lWJetsNLO = "/tmp/pharris/Spring15_a25ns_WJetsToLNu_amcatnlo_MINIAOD.root";
  TTree *lTWJetsLO  = load(lWJetsLO);
  TTree *lTWJetsNLO = load(lWJetsNLO);
  TH1F** lHWJets = new TH1F*[3];
  lHWJets[0] = drawNew("wjetsLO" ,lTWJetsLO ,""         ,"",false);
  lHWJets[1] = drawNew("wjetsNLO",lTWJetsNLO,"xs*"      ,"");
  lHWJets[2] = makeRatio(lHWJets[1],lHWJets[0]);
  write("Ratio.root",3.,lHWJets);
  //Ratio of Merged to 1jet  DY
  std::string lDYJetsNLO   = "/tmp/pharris/Spring15_a25ns_DYJetsToNuNu_TuneCUETP8M1_MINIAOD.root";
  std::string lDYJetsNLO1J = "/tmp/pharris/Z1j_13TeV_v3.root";
  TTree *lTDYJetsNLO   = load(lDYJetsNLO);
  TTree *lTDYJetsNLO1J = load(lDYJetsNLO1J);
  TH1F** lHDYJets = new TH1F*[3];
  lHDYJets[0] = drawNew("dyjetsNLO"  ,lTDYJetsNLO  ,"3855.*"    ,"");
  lHDYJets[1] = drawOld("dyjetsNLO1J",lTDYJetsNLO1J,"mcweight*" ,"");
  lHDYJets[2] = makeRatio(lHDYJets[1],lHDYJets[0]);
  write("Ratio.root",2.,lHDYJets);
  //Ratio of Merged to 1jet  W
  std::string lWJetsNLO1J = "/tmp/pharris/W1j_13TeV_v3.root";
  TTree *lTWJetsNLO1J = load( lWJetsNLO1J);
  TH1F** lHWJets1J = new TH1F*[2];
  lHWJets1J[0] = drawOld("wjetsNLO1J",lTWJetsNLO1J,"3.*mcweight*" ,"");
  lHWJets1J[1] = makeRatio(lHWJets1J[0],lHWJets[1]);
  write("Ratio.root",2.,lHWJets1J);  
  //PDF Z/W  && Z/G ratio
  /*
  TH1F** lDYPDF = drawPdf("dyjetsNLO1J",lTDYJetsNLO1J,"mcweight*"  ,"",0);    
  TH1F** lWPDF  = drawPdf("wjetsNLO1J" ,lTWJetsNLO1J ,"3.*mcweight*","",0);    
  TH1F** lGPDF  = drawPdf("gjetsNLO"   ,lTGJetsNLO   ,"mcweight*"  ,"*(dm_eta < 1.5)",0);    
  write("Ratio",100,lDYPDF);
  write("Ratio",100,lWPDF);
  write("Ratio",100,lGPDF);
  TH1F** lGDYPDF = pdfUnc(lHDYJets[1],lHGJets[1]  ,lDYPDF,lGPDF);
  TH1F** lWDYPDF = pdfUnc(lHDYJets[1],lHWJets1J[0],lDYPDF,lWPDF);
  write("Ratio",2,lGDYPDF);
  write("Ratio",2,lWDYPDF);
  */
  //Scale Z/G ratio
  TH1F** lDYScale = drawScale("dyjetsNLO1J",lTDYJetsNLO1J,"mcweight*","",0);    
  TH1F** lWScale  = drawScale("wjetsNLO1J" ,lTWJetsNLO1J ,"mcweight*","",0);    
  TH1F** lGScale  = drawScale("gjetsNLO"   ,lTGJetsNLO   ,"mcweight*","*(dm_eta < 1.5)",0);    
  write("Ratio.root",2,lDYScale);
  write("Ratio.root",2,lWScale);
  write("Ratio.root",2,lGScale);
  TH1F** lGDYScale = scaleUnc(lHDYJets[1],lHGJets[1]  ,lDYScale,lGScale);
  TH1F** lWDYScale = scaleUnc(lHDYJets[1],lHWJets1J[0],lDYScale,lWScale);
  write("Ratio.root",2,lGDYScale);
  write("Ratio.root",2,lWDYScale);
}

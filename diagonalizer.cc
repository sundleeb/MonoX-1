#ifndef DIAGONALIZER
#define DIAGONALIZER

// ROOT includes
#include "TROOT.h"
#include "TString.h"
#include "TMath.h"
#include "TMatrixDSym.h"
#include "TMatrixD.h"
#include "TVectorD.h"
#include "TIterator.h"
#include "TH2F.h"

// RooFit includes
#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooConstVar.h"
#include "RooFormulaVar.h"
#include "RooAddPdf.h"
#include "RooFitResult.h"
#include "RooArgSet.h"
#include "RooArgList.h"
#include "RooCmdArg.h"

// RooStats includes
#include "RooWorkspace.h"

#include <string>
#include <vector>
#include <map>
#include <iostream>

using namespace std;

class diagonalizer {
  
  public:
    diagonalizer(RooWorkspace *wspace);// RooAbsPdf *pdf);

    int generateVariations(RooFitResult *res_ptr);
    void resetPars();  // Reset back to best fit values
    void setEigenset(int,int /*>0 = +1, <0=-1*/);
    TH2F *retCovariance();
    
  private:
    RooDataSet *_data_;
    //RooAbsPdf  *_pdf_;
    RooWorkspace *_wspace;

    std::vector<double> original_values;
    RooArgList rooParameters;

    TMatrixD _evec;
    TVectorD _eval;
    TH2F *_h2covar;
    int _n_par;

    void getArgSetParameters(RooArgList & params,std::vector<double> &val);
    void setArgSetParameters(RooArgList & params,std::vector<double> &val);
};

diagonalizer::diagonalizer(RooWorkspace *wspace){//, RooAbsPdf *pdf){
    //_data = data;
    //_pdf = pdf;
    _wspace = wspace;
}


TH2F* diagonalizer::retCovariance(){
  
   if (_h2covar) return _h2covar;
   else { 
	std::cout << "NO COVARIANCE MATRIX, DID YOU DIAGONALIZE YET?" << std::endl;
	return 0;
   }
}
int diagonalizer::generateVariations(RooFitResult *res_ptr){// std::string dataSetName){
  //RooDataSet *data = (RooDataSet*)_wspace->data(dataSetName.c_str());  // weird but sure
  //assert(data);
  //
  RooArgList rooFloatParameters = res_ptr->floatParsFinal();  // Why not return a set ????!!!
 
  TMatrixD cov  = res_ptr->covarianceMatrix();
  cov.Print();
  //TVectorD eval;
  TMatrixD evec = cov.EigenVectors(_eval);
  _n_par = _eval.GetNoElements();
  evec.Print();
  _evec.ResizeTo(_n_par,_n_par);
  _h2covar = new TH2F(Form("covariance_fit_%s",res_ptr->GetName()),"Covariance",_n_par,0,_n_par,_n_par,0,_n_par);
  for (int l=0;l<_n_par;l++){
    for (int m=0;m<_n_par;m++){
      _h2covar->SetBinContent(l+1,m+1,cov(l,m));
      _evec(l,m) = evec(l,m); 
    }
  }

  _evec.Print();
  std::cout << "Eigenvalues (squares of errors)"<< std::endl;
  _eval.Print();
  // ---------------------------------------------------------------------------------------------------------------------
  //_evec = evec.Clone();
  //_eval = eval.Clone();

  std::cout << "Number of Parameters from the Fit -- " << _n_par  << std::endl;
  int pcount=1;
  TIterator *parsit = rooFloatParameters.createIterator();
  while (RooAbsArg *arg = (RooAbsArg*)parsit->Next()) {
     RooRealVar *vit = _wspace->var(arg->GetName());
     rooParameters.add(*vit);
     _h2covar->GetXaxis()->SetBinLabel(pcount,vit->GetName());
     _h2covar->GetYaxis()->SetBinLabel(pcount,vit->GetName());
     pcount++;
  }
  getArgSetParameters(rooParameters,original_values);

  return _n_par;
}
void diagonalizer::resetPars(){
  setArgSetParameters(rooParameters,original_values);
}
void diagonalizer::setEigenset(int par,int direction /*>0 = +1, <0=-1*/){
  //RooArgSet rooParameters;
  //_pdf->getParameters(*x)->Print();

  // fill vector with original parameters
  //std::vector <double> original_values;
  // first set to original parameters
  //setArgSetParameters(rooParameters,original_values);

  std::vector<double> new_values;
  
  int dir = direction>=0 ? 1 : -1;
    
  // this row in evec is the scales for the parameters
  double err = TMath::Sqrt(_eval[par]);
  std::cout << "Setting value of parameters from par " << par << " " << dir << " sigma" << std::endl; 
  new_values.clear(); // make sure its empty before we fill it
  for (int i=0;i<_n_par;i++){
    new_values.push_back(original_values[i] + dir*(_evec[i][par]*err));	
  }

  setArgSetParameters(rooParameters,new_values);

}
void diagonalizer::getArgSetParameters(RooArgList & params,std::vector<double> &val){

  val.clear();
  TIterator* iter(params.createIterator());
  for (TObject *a = iter->Next(); a != 0; a = iter->Next()) {
      RooRealVar *rrv = dynamic_cast<RooRealVar *>(a);
      //std::cout << "RooContainer:: -- Getting values from parameter -- " << std::endl;
      //rrv->Print();
      val.push_back(rrv->getVal());
  }
}

void diagonalizer::setArgSetParameters(RooArgList & params,std::vector<double> &val){

  int i = 0;
  TIterator* iter(params.createIterator());
  for (TObject *a = iter->Next(); a != 0; a = iter->Next()) {
      // each var must be shifted
      RooRealVar *rrv = dynamic_cast<RooRealVar *>(a);
      //std::cout << "RooContainer:: -- Setting values from parameter -- " << std::endl;
      //rrv->Print();
      std::cout << " Set parameter " << rrv->GetName() << " to " << val[i] << std::endl;
      rrv->setVal(val[i]);
      _wspace->var(rrv->GetName())->setVal(val[i]);
      i++;
  }
}

#endif

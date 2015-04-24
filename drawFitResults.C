void drawFitResults(std::string file){

   gStyle->SetOptStat(0);
   gStyle->SetPaintTextFormat(".2f");

   TFile *fi = TFile::Open(file.c_str());
   fi->cd();

   TCanvas *canv_cova = new TCanvas("covariance_matrix","",1600,1600);
   covariance_fit_fitresult_combined_pdf_combinedData->Draw("colZ");
   covariance_fit_fitresult_combined_pdf_combinedData->SetMarkerColor(kWhite);
   //covariance_fit_fitresult_combined_pdf_combinedData->Draw("textsame");
   //canv_cova->SetLogz();
   canv_cova->SaveAs("correlation_matrix.pdf");
   canv_cova->SaveAs("correlation_matrix.png");

   TCanvas *canv_corr = new TCanvas("correlation_matrix","",1600,1600);
   correlation_fit_fitresult_combined_pdf_combinedData->Draw("colZ");
   correlation_fit_fitresult_combined_pdf_combinedData->SetMarkerColor(kWhite);
   //correlation_fit_fitresult_combined_pdf_combinedData->Draw("textsame");
   //canv_corr->SetLogz();
   canv_corr->SaveAs("correlation_matrix.pdf");
   canv_corr->SaveAs("correlation_matrix.png");

   canv_hist_post_fit_nuisances->SetBottomMargin(0.5);
   canv_hist_post_fit_nuisances->SetRightMargin(0.02);
   canv_hist_post_fit_nuisances->SetLeftMargin(0.1);
   canv_hist_post_fit_nuisances->SaveAs("post_fit_nuisances.pdf");
   canv_hist_post_fit_nuisances->SaveAs("post_fit_nuisances.png");
}

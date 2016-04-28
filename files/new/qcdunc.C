TH1* getewkunc() {

    TFile* file = new TFile("uncertainties_EWK_24bins.root");
    TFile* fil2 = new TFile("scalefactors.root");

    TH1* gnom = (TH1*)file->Get("WJets_012j_NLO/nominal");
    TH1* gewu = (TH1*)file->Get("EWKcorr/W");

    //TH1* gnom = (TH1*)file->Get("GJets_1j_NLO/nominal_G");
    //TH1* gewu = (TH1*)file->Get("EWKcorr/photon");
    //TH1* gewu = (TH1*)fil2->Get("a_ewkcorr/a_ewkcorr");

    TH1* znom = (TH1*)file->Get("ZJets_012j_NLO/nominal");
    TH1* zewu = (TH1*)file->Get("EWKcorr/Z");
    //TH1* zewu = (TH1*)fil2->Get("z_ewkcorr/z_ewkcorr");

    //zewu->Multiply(znom);
    //gewu->Multiply(gnom);

    zewu->Divide(gewu);
    znom->Divide(gnom);

    for (int i = 1; i <= znom->GetNbinsX(); i++) {
        zewu->SetBinContent(i, 1.0 + fabs(zewu->GetBinContent(i) - znom->GetBinContent(i)) / znom->GetBinContent(i));
    }

    zewu->SetName("a_ewkcorr_overz_Upcommon");

    return zewu;
}


TH1* getpdfunc() {

    TFile* file = new TFile("uncertainties_EWK_24bins.root");

    TH1* gnom = (TH1*)file->Get("WJets_012j_NLO/nominal");
    TH1* gpdu = (TH1*)file->Get("WJets_012j_NLO/PDF");

    //TH1* gnom = (TH1*)file->Get("GJets_1j_NLO/nominal_G");
    //TH1* gpdu = (TH1*)file->Get("GJets_1j_NLO/PDF");

    TH1* znom = (TH1*)file->Get("ZJets_012j_NLO/nominal");
    TH1* zpdu = (TH1*)file->Get("ZJets_012j_NLO/PDF");

    for (int i = 1; i <= znom->GetNbinsX(); i++) {
        zpdu->SetBinContent(i, znom->GetBinContent(i)*(1.0 + zpdu->GetBinContent(i)));
        gpdu->SetBinContent(i, gnom->GetBinContent(i)*(1.0 + gpdu->GetBinContent(i)));
    }

    zpdu->Divide(gpdu);
    znom->Divide(gnom);

    for (int i = 1; i <= znom->GetNbinsX(); i++) {
        zpdu->SetBinContent(i, 1.0 + fabs(zpdu->GetBinContent(i) - znom->GetBinContent(i)) / znom->GetBinContent(i));
    }    

    zpdu->SetName("znlo1_over_anlo1_pdfUp");
    
    return zpdu;
}

TH1* getqcdunc(bool ren) {

    TFile* file = new TFile("uncertainties_EWK_24bins.root");

    TH1* gnom = (TH1*)file->Get("WJets_012j_NLO/nominal");
    TH1* greu = (TH1*)file->Get("WJets_012j_NLO/ren_up");
    TH1* gred = (TH1*)file->Get("WJets_012j_NLO/ren_down");
    TH1* gfau = (TH1*)file->Get("WJets_012j_NLO/fact_up");
    TH1* gfad = (TH1*)file->Get("WJets_012j_NLO/fact_down");

    /*
    TH1* gnom = (TH1*)file->Get("GJets_1j_NLO/nominal_G");
    TH1* greu = (TH1*)file->Get("GJets_1j_NLO/ren_up_G");
    TH1* gred = (TH1*)file->Get("GJets_1j_NLO/ren_down_G");
    TH1* gfau = (TH1*)file->Get("GJets_1j_NLO/fact_up_G");
    TH1* gfad = (TH1*)file->Get("GJets_1j_NLO/fact_down_G");
    */

    TH1* znom = (TH1*)file->Get("ZJets_012j_NLO/nominal");
    TH1* zreu = (TH1*)file->Get("ZJets_012j_NLO/ren_up");
    TH1* zred = (TH1*)file->Get("ZJets_012j_NLO/ren_down");
    TH1* zfau = (TH1*)file->Get("ZJets_012j_NLO/fact_up");
    TH1* zfad = (TH1*)file->Get("ZJets_012j_NLO/fact_down");

    TH1* zgn  = (TH1*)znom->Clone("zgn");
    TH1* zgau = (TH1*)znom->Clone("zgau");
    TH1* zgad = (TH1*)znom->Clone("zgad");
    TH1* zgas = (TH1*)znom->Clone("ZG_Acorr_unc");
    TH1* zgcu = (TH1*)znom->Clone("zgcu");
    TH1* zgcd = (TH1*)znom->Clone("zgcd");
    TH1* zgcs = (TH1*)znom->Clone("ZG_Corr_unc");
    TH1* zgts  = (TH1*)znom->Clone("znlo1_over_anlo1_renScaleUp");

    for (int i = 1; i <= znom->GetNbinsX(); i++) {
        float dz = fabs(zfad->GetBinContent(i) - znom->GetBinContent(i));
        float dg = fabs(gfad->GetBinContent(i) - gnom->GetBinContent(i));

        if (ren) {
            dz = fabs(zred->GetBinContent(i) - znom->GetBinContent(i));
            dg = fabs(gred->GetBinContent(i) - gnom->GetBinContent(i));
        }

        zgn->SetBinContent(i, znom->GetBinContent(i) / gnom->GetBinContent(i));
        zgau->SetBinContent(i, ( ((znom->GetBinContent(i)+dz) / (gnom->GetBinContent(i)-dg)) - (znom->GetBinContent(i) / gnom->GetBinContent(i)) ) );
        zgad->SetBinContent(i, (-((znom->GetBinContent(i)-dz) / (gnom->GetBinContent(i)+dg)) + (znom->GetBinContent(i) / gnom->GetBinContent(i)) ) );
        zgcu->SetBinContent(i, fabs( ((znom->GetBinContent(i)+dz) / (gnom->GetBinContent(i)+dg)) - (znom->GetBinContent(i) / gnom->GetBinContent(i)) ) );
        zgcd->SetBinContent(i, fabs( ((znom->GetBinContent(i)-dz) / (gnom->GetBinContent(i)-dg)) - (znom->GetBinContent(i) / gnom->GetBinContent(i)) ) );
    }   
    zgau->Scale(sqrt(0.5));
    zgad->Scale(sqrt(0.5));
    zgcu->Scale(sqrt(0.5));
    zgcd->Scale(sqrt(0.5));

    zgau->Divide(zgn);
    zgad->Divide(zgn);
    zgcu->Divide(zgn);
    zgcd->Divide(zgn);

    for (int i = 1; i <= znom->GetNbinsX(); i++) {
        float amax = zgau->GetBinContent(i);
        if (zgad->GetBinContent(i) > amax) amax = zgad->GetBinContent(i);
        zgas->SetBinContent(i, 1.+amax);
        float cmax = zgcu->GetBinContent(i);
        if (zgcd->GetBinContent(i) > cmax) cmax = zgcd->GetBinContent(i);
        zgcs->SetBinContent(i, 1.+cmax);
    }


    for (int i = 1; i <= znom->GetNbinsX(); i++) {
        zgts->SetBinContent(i, 1.0+sqrt((1.-zgas->GetBinContent(i))*(1.-zgas->GetBinContent(i)) + (1.-zgcs->GetBinContent(i))*(1.-zgcs->GetBinContent(i))) ); 
    }

    /*
    zgas->Draw("HIST");
    zgcs->Draw("HIST SAME");
    zgts->Draw("HIST SAME");

    TFile* outfile = new TFile("kfactors_24bins.root", "UPDATE");
    zgas->Write();
    zgcs->Write();
    outfile->Close();
    */

    return zgts;
}

void qcdunc() {

    TH1* hrenu = getqcdunc(true);
    TH1* hfacu = getqcdunc(false);
    TH1* hpdfu = getpdfunc();
    TH1* hewku = getewkunc();
    
    TH1* hnomi = (TH1*)hrenu->Clone("hnomi");
    //TH1* hrend = (TH1*)hrenu->Clone("hrend");
    //TH1* hfacd = (TH1*)hfacu->Clone("hfacd");
    //TH1* hpdfd = (TH1*)hpdfu->Clone("hpdfd");
    //TH1* hewkd = (TH1*)hewku->Clone("hewkd");

    TH1* hrend = (TH1*)hrenu->Clone("znlo1_over_anlo1_renScaleDown");
    TH1* hfacd = (TH1*)hfacu->Clone("znlo1_over_anlo1_facScaleDown");
    TH1* hpdfd = (TH1*)hpdfu->Clone("znlo1_over_anlo1_pdfDown");
    TH1* hewkd = (TH1*)hewku->Clone("a_ewkcorr_overz_Downcommon");

    for (int i = 1; i <= hrend->GetNbinsX(); i++) {
        hnomi->SetBinContent(i, 1.0);
        hrend->SetBinContent(i, 2.0 - hrend->GetBinContent(i));
        hfacd->SetBinContent(i, 2.0 - hfacd->GetBinContent(i));
        hpdfd->SetBinContent(i, 2.0 - hpdfd->GetBinContent(i));
        hewkd->SetBinContent(i, 2.0 - hewkd->GetBinContent(i));
    }

    hrenu->SetLineWidth(2);
    hfacu->SetLineWidth(2);
    hpdfu->SetLineWidth(2);
    hewku->SetLineWidth(2);

    hnomi->SetLineWidth(2);
    hrend->SetLineWidth(2);
    hfacd->SetLineWidth(2);
    hpdfd->SetLineWidth(2);
    hewkd->SetLineWidth(2);

    hrenu->SetLineColor(kRed);
    hfacu->SetLineColor(kMagenta);
    hpdfu->SetLineColor(kBlue);
    hewku->SetLineColor(kGray+1);

    hrend->SetLineColor(kRed);
    hfacd->SetLineColor(kMagenta);
    hpdfd->SetLineColor(kBlue);
    hewkd->SetLineColor(kGray+1);

    TCanvas* canvas = new TCanvas("canvas", "canvas", 600, 600);
    //TH1* frame = canvas->DrawFrame(200., 0.6, 1250., 1.6, "");
    //TH1* frame = canvas->DrawFrame(200., 0.6, 1000., 1.6, "");
    TH1* frame = canvas->DrawFrame(200., 0.6, 1250., 1.6, "");

    frame->GetXaxis()->SetTitle("Boson p_{T} [GeV]");
    frame->GetYaxis()->SetTitle("(d#sigma^{Z}/dp_{T})/(d#sigma^{#gamma}/dp_{T})  variation/nominal");

    /*
    hrenu->SetName("znlo1_over_anlo1_renScaleUp");
    hfacu->SetName("znlo1_over_anlo1_facScaleUp");
    hpdfu->SetName("znlo1_over_anlo1_pdfUp");
    hewku->SetName("a_ewkcorr_overz_Upcommon");
    hrend->SetName("znlo1_over_anlo1_renScaleDown");
    hfacd->SetName("znlo1_over_anlo1_facScaleDown");
    hpdfd->SetName("znlo1_over_anlo1_pdfDown");
    hewkd->SetName("a_ewkcorr_overz_Downcommon");
    */
    
    hrenu->SetName("znlo1_over_wnlo1_renScaleUp");
    hfacu->SetName("znlo1_over_wnlo1_facScaleUp");
    hpdfu->SetName("znlo1_over_wnlo1_pdfUp");
    hewku->SetName("w_ewkcorr_overz_Upcommon");
    hrend->SetName("znlo1_over_wnlo1_renScaleDown");
    hfacd->SetName("znlo1_over_wnlo1_facScaleDown");
    hpdfd->SetName("znlo1_over_wnlo1_pdfDown");
    hewkd->SetName("w_ewkcorr_overz_Downcommon");

    frame->Draw();
    hnomi->Draw("HIST SAME");
    hrenu->Draw("HIST SAME");
    hfacu->Draw("HIST SAME");
    hpdfu->Draw("HIST SAME");
    hewku->Draw("HIST SAME");
    hrend->Draw("HIST SAME");
    hfacd->Draw("HIST SAME");
    hpdfd->Draw("HIST SAME");
    hewkd->Draw("HIST SAME");

    TFile* f_out = new TFile("wtoz_unc.root","recreate");
    f_out->cd();
    hnomi->Write();
    hrenu->Write();
    hfacu->Write();
    hpdfu->Write();
    hewku->Write();
    hrend->Write();
    hfacd->Write();
    hpdfd->Write();
    hewkd->Write();
    f_out->Close();

    TLegend* leg = new TLegend(0.55, 0.65, 0.95, 0.9);
    leg->SetFillColor(0);
    leg->AddEntry(hnomi, "Central Value");
    leg->AddEntry(hrenu, "Ren. Scale Up/Down");
    leg->AddEntry(hfacu, "Fac. Scale Up/Down");
    leg->AddEntry(hpdfu, "PDF Up/Down");
    leg->AddEntry(hewku, "EWK Up/Down");
    leg->Draw("SAME");
}

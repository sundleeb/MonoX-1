# Configuration for the Mono-X categories
out_file_name = 'mono-x.root'
bins = range(200,1050,50)
categories = [
	{
	    'name':"monojet"
	   ,'in_file_name':"monojet.root"
	   #,'in_file_name':"inclusive-combo.root"
	   ,"cutstring":"mvamet>200 && mvamet<1000 &&weight<500"
	   ,"varstring":["mvamet",200,1000]
	   ,"weightname":"weight"
	   ,"bins":bins[:]
  	   ,"additionalvars":[['jet1pt',25,150,1000]]
	   ,"pdfmodel":0
           ,"recoilMC"  :"recoilfits/recoilfit_Zgj_pfmetraw_2012_mc.root"
           ,"recoilData":"recoilfits/recoilfit_Zgj_pfmetraw_2012_data.root"
           ,"muonSF"  : 0.985
           ,"photonSF": 0.97
	   ,"samples":
	   	{  # Format is TreeName : ['region','process',isMC,isSignal]  !! Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!
		  # Signal Region
		   "Znunu_signalMet"  	           :['signal','zjets',1,0]
                   ,"Zll_signalMet"	           :['signal','zll',1,0]
 		  ,"Wjets_signalMet"  	           :['signal','wjets',1,0]
		  ,"WW_signalMet"  	           :['signal','dibosons',1,0]
		  ,"WZ_signalMet"  	           :['signal','dibosons',1,0]
		  ,"ZZ_signalMet"  	           :['signal','dibosons',1,0]
		  ,"ttbar_signalMet"   	           :['signal','top',1,0]
		  ,"SingleTop_signalMet"           :['signal','top',1,0]
		  ,"QCD_signal"		           :['signal','qcd',1,0]
		  ,"ggH125_signalMet"             :['signal','Higgs125',1,1]
		  ,"VBFH125_signalMet"            :['signal','Higgs125',1,1]
		  ,"WH125_signalMet"   	   	  :['signal','Higgs125',1,1]
		  ,"ZH125_signalMet"   	   	  :['signal','Higgs125',1,1]
		  #,"GV_signal"   	:['signal','gv',1,0]
		  ,"data_signal"	           :['signal','data',0,0]

		  # Di muon-Control
		  ,"Zll_di_muon_controlMet"	   :['dimuon','zll',1,1]
		  ,"Znunu_di_muon_controlMet"  	   :['dimuon','zjets',1,0]
		  ,"Wjets_di_muon_controlMet"  	   :['dimuon','wjets',1,0]
		  ,"WW_di_muon_controlMet"  	   :['dimuon','dibosons',1,0]
		  ,"WZ_di_muon_controlMet"  	   :['dimuon','dibosons',1,0]
		  ,"ZZ_di_muon_controlMet"  	   :['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_controlMet"      :['dimuon','top',1,0]
		  ,"SingleTop_di_muon_controlMet"  :['dimuon','top',1,0]
		  #,"QCD_di_muon_controlMet"	:['dimuon','qcd',1,0]
		  #,"GV_di_muon_controlMet"   	:['dimuon','gv',1,0]
		  ,"data_di_muon_control"	   :['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_controlMet"	   :['singlemuon','zll',1,0]
		  #,"Znunu_single_muon_controlMet"     :['singlemuon','zjets',1,0]
		  ,"Wjets_single_muon_controlMet"  :['singlemuon','wjets',1,1]
		  ,"ZZ_single_muon_controlMet"     :['singlemuon','dibosons',1,0]
		  ,"WW_single_muon_controlMet"     :['singlemuon','dibosons',1,0]
		  ,"WZ_single_muon_controlMet"     :['singlemuon','dibosons',1,0]
		  ,"SingleTop_single_muon_controlMet" :['singlemuon','top',1,0]
		  ,"ttbar_single_muon_controlMet"  :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  #,"GV_single_muon_controlMet"   	   :['singlemuon','gv',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_controlMet"	   :['photon','gjet',1,1]
		  ,"Zll_photon_controlMet"	   :['photon','zll',1,0]
		  ,"Wjets_photon_controlMet"  	   :['photon','wjets',1,0]
		  ,"WW_photon_controlMet"  	   :['photon','dibosons',1,0]
		  ,"ZZ_photon_controlMet"  	   :['photon','dibosons',1,0]
		  ,"ttbar_photon_controlMet"   	   :['photon','top',1,0]
		  ,"SingleTop_photon_controlMet"   :['photon','top',1,0]
                  ,"QCD_photon_control"	           :['photon','qcd',1,0]
	   	},
                "metsamples":
	   	{
                    #Di Muon Control Region
                    "Zll_di_muon_control","Znunu_di_muon_control","Wjets_di_muon_control","WW_di_muon_control","WZ_di_muon_control","ZZ_di_muon_control",
                    "ttbar_di_muon_control","SingleTop_di_muon_control",
                    #Single Muon Control Region
                    "Wjets_single_muon_control","Zll_single_muon_control","WW_single_muon_control","WZ_single_muon_control","ZZ_single_muon_control","ttbar_single_muon_control",
                    "SingleTop_single_muon_control",
                    #Photon Control Region
                    "Photon_photon_control","Wjets_photon_control","Zll_photon_control","WW_photon_control","ZZ_photon_control","ttbar_photon_control","SingleTop_photon_control",
                    "QCD_photon_control",
                    #Signal Region
                    "Wjets_signal","Zll_signal","WW_signal","WZ_signal","ZZ_signal","ttbar_signal","SingleTop_signal","QCD_signal",
                    "ggH125_signal"    	,"VBFH125_signal"   	,"WH125_signal"   	,"ZH125_signal","Znunu_signal"
                },
	}

]

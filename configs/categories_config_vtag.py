# Configuration for the Mono-X categories
out_file_name = 'mono-x-vtagged.root'
BINS = [250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]
BINS = range(250,550,50)
BINS.append(1000)
categories = [
	{
	    'name':"resolved"
	   ,'in_file_name':"resolved-combo.root"
	   ,"cutstring":"mvamet>250 && mvamet<1000"
	   ,"varstring":["mvamet",250,1000]
	   ,"weightname":"weight"
	   ,"bins":BINS[:]
	   ,"samples":
	   	{  # Format is TreeName : ['region','process',isMC,isSignal]  !! Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!
		  # Signal Region
		   "Znunu_signal"  	:['signal','zjets',1,0]
		  ,"Zll_signal"	   	:['signal','zll',1,0]
		  ,"Wjets_signal"  	:['signal','wjets',1,0]
		  ,"WW_signal"  	:['signal','dibosons',1,0]
		  ,"WZ_signal"  	:['signal','dibosons',1,0]
		  ,"ZZ_signal"  	:['signal','dibosons',1,0]
		  ,"ttbar_signal"   	:['signal','top',1,0]
		  ,"SingleTop_signal"   :['signal','top',1,0]
		  ,"QCD_signal"		:['signal','qcd',1,0]
		  ,"ggH_signal"    	:['signal','ggH',1,1]
		  ,"VBFH_signal"   	:['signal','vbf',1,1]
		  ,"WH_signal"   	:['signal','wh',1,1]
		  ,"ZH_signal"   	:['signal','zh',1,1]
		  ,"data_signal"	:['signal','data',0,0]

		  # Di muon-Control
		  ,"Zll_di_muon_control"	:['dimuon','zll',1,1]
		  ,"Znunu_di_muon_control"  	:['dimuon','zjets',1,0]
		  ,"Wjets_di_muon_control"  	:['dimuon','wjets',1,0]
		  ,"WW_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"WZ_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"ZZ_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_control"   	:['dimuon','top',1,0]
		  ,"SingleTop_di_muon_control"  :['dimuon','top',1,0]
		  #,"QCD_di_muon_control"	:['dimuon','qcd',1,0]
		  ,"data_di_muon_control"	:['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_control"	   :['singlemuon','zll',1,0]
		  ,"Znunu_single_muon_control"     :['singlemuon','zjets',1,0]
		  ,"Wjets_single_muon_control"     :['singlemuon','wjets',1,1]
		  ,"WW_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"WZ_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"ZZ_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"ttbar_single_muon_control"     :['singlemuon','top',1,0]
		  ,"SingleTop_single_muon_control" :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  # Single muon control
		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_control"	   :['photon','gjet',1,1]
		  ,"Zll_photon_control"	   	:['photon','zll',1,0]
		  ,"Wjets_photon_control"  	:['photon','wjets',1,0]
		  ,"WW_photon_control"  	:['photon','dibosons',1,0]
		  ,"ZZ_photon_control"  	:['photon','dibosons',1,0]
		  ,"ttbar_photon_control"   	:['photon','top',1,0]
		  ,"SingleTop_photon_control"   :['photon','top',1,0]
		  ,"QCD_photon_control"		:['photon','qcd',1,0]

	   	}
	}, 
	{
	    'name':"boosted"
	   ,'in_file_name':"boosted.root"
	   ,"cutstring":"mvamet_>250 && mvamet_<1000"
	   ,"varstring":["mvamet_",250,1000]
	   ,"weightname":"weight_"
	   ,"bins":BINS[:]
	   ,"samples":
	   	{  # Format is TreeName : ['region','process',isMC,isSignal]  !! Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!
		  # Signal Region
		   "Znunu_signal"  	:['signal','zjets',1,0]
		  ,"Zll_signal"	   	:['signal','zll',1,0]
		  ,"Wjets_signal"  	:['signal','wjets',1,0]
		  ,"WW_signal"  	:['signal','dibosons',1,0]
		  ,"WZ_signal"  	:['signal','dibosons',1,0]
		  ,"ZZ_signal"  	:['signal','dibosons',1,0]
		  ,"ttbar_signal"   	:['signal','top',1,0]
		  ,"SingleTop_signal"   :['signal','top',1,0]
		  ,"QCD_signal"		:['signal','qcd',1,0]
		  ,"ggH_signal"    	:['signal','ggH',1,1]
		  ,"VBFH_signal"   	:['signal','vbf',1,1]
		  ,"WH_signal"   	:['signal','wh',1,1]
		  ,"ZH_signal"   	:['signal','zh',1,1]
		  ,"GV_signal"   	:['signal','gv',1,0]
		  ,"data_signal"	:['signal','data',0,0]

		  # Di muon-Control
		  ,"Zll_di_muon_control"	:['dimuon','zll',1,1]
		  ,"Znunu_di_muon_control"  	:['dimuon','zjets',1,0]
		  ,"Wjets_di_muon_control"  	:['dimuon','wjets',1,0]
		  ,"WW_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"WZ_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"ZZ_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_control"   	:['dimuon','top',1,0]
		  ,"SingleTop_di_muon_control"  :['dimuon','top',1,0]
		  #,"QCD_di_muon_control"	:['dimuon','qcd',1,0]
		  ,"GV_di_muon_control"   	:['dimuon','gv',1,0]
		  ,"data_di_muon_control"	:['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_control"	   :['singlemuon','zll',1,0]
		  #,"Znunu_single_muon_control"     :['singlemuon','zjets',1,0]
		  ,"Wjets_single_muon_control"     :['singlemuon','wjets',1,1]
		  ,"ZZ_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"WW_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"WZ_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"SingleTop_single_muon_control" :['singlemuon','top',1,0]
		  ,"ttbar_single_muon_control"     :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  #,"GV_single_muon_control"   	   :['singlemuon','gv',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_control"	   :['photon','gjet',1,1]
		  ,"Zll_photon_control"	   	:['photon','zll',1,0]
		  ,"Wjets_photon_control"  	:['photon','wjets',1,0]
		  ,"WW_photon_control"  	:['photon','dibosons',1,0]
		  ,"ZZ_photon_control"  	:['photon','dibosons',1,0]
		  ,"ttbar_photon_control"   	:['photon','top',1,0]
		  ,"SingleTop_photon_control"   :['photon','top',1,0]
		  ,"QCD_photon_control"		:['photon','qcd',1,0]
	   	}
	},
	{
	    'name':"inclusive"
	   ,'in_file_name':"monojet-combo.root"
	   ,"cutstring":"mvamet>200 && mvamet<1000"
	   ,"varstring":["mvamet",200,1000]
	   ,"weightname":"weight"
	   ,"bins":[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]
	   ,"samples":
	   	{  # Format is TreeName : ['region','process',isMC,isSignal]  !! Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!
		  # Signal Region
		   "Znunu_signal"  	:['signal','zjets',1,0]
		  ,"Zll_signal"	   	:['signal','zll',1,0]
		  ,"Wjets_signal"  	:['signal','wjets',1,0]
		  ,"WW_signal"  	:['signal','dibosons',1,0]
		  ,"WZ_signal"  	:['signal','dibosons',1,0]
		  ,"ZZ_signal"  	:['signal','dibosons',1,0]
		  ,"ttbar_signal"   	:['signal','top',1,0]
		  ,"SingleTop_signal"   :['signal','top',1,0]
		  ,"QCD_signal"		:['signal','qcd',1,0]
		  ,"ggH_signal"    	:['signal','ggH',1,1]
		  ,"VBFH_signal"   	:['signal','vbf',1,1]
		  ,"WH_signal"   	:['signal','wh',1,1]
		  ,"ZH_signal"   	:['signal','zh',1,1]
		  #,"GV_signal"   	:['signal','gv',1,0]
		  ,"data_signal"	:['signal','data',0,0]

		  # Di muon-Control
		  ,"Zll_di_muon_control"	:['dimuon','zll',1,1]
		  ,"Znunu_di_muon_control"  	:['dimuon','zjets',1,0]
		  ,"Wjets_di_muon_control"  	:['dimuon','wjets',1,0]
		  ,"WW_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"WZ_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"ZZ_di_muon_control"  	:['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_control"   	:['dimuon','top',1,0]
		  ,"SingleTop_di_muon_control"  :['dimuon','top',1,0]
		  #,"QCD_di_muon_control"	:['dimuon','qcd',1,0]
		  #,"GV_di_muon_control"   	:['dimuon','gv',1,0]
		  ,"data_di_muon_control"	:['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_control"	   :['singlemuon','zll',1,0]
		  #,"Znunu_single_muon_control"     :['singlemuon','zjets',1,0]
		  ,"Wjets_single_muon_control"     :['singlemuon','wjets',1,1]
		  ,"ZZ_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"WW_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"WZ_single_muon_control"  	   :['singlemuon','dibosons',1,0]
		  ,"SingleTop_single_muon_control" :['singlemuon','top',1,0]
		  ,"ttbar_single_muon_control"     :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  #,"GV_single_muon_control"   	   :['singlemuon','gv',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_control"	   :['photon','gjet',1,1]
		  ,"Zll_photon_control"	   	:['photon','zll',1,0]
		  ,"Wjets_photon_control"  	:['photon','wjets',1,0]
		  ,"WW_photon_control"  	:['photon','dibosons',1,0]
		  ,"ZZ_photon_control"  	:['photon','dibosons',1,0]
		  ,"ttbar_photon_control"   	:['photon','top',1,0]
		  ,"SingleTop_photon_control"   :['photon','top',1,0]
		  ,"QCD_photon_control"		:['photon','qcd',1,0]
	   	}
	}

]

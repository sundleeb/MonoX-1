# Configuration for the Mono-X categories
out_file_name = 'mono-x-vtagged.root'
BINS = [250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,650,800,1000,1500,2000]
BINS = range(250,750,50)
BINS.append(1000)
BINS.append(2000)

ALLVARS = [
  ['jet1pt',25,150,1000]
  ,["mll",25,75,125]
  ,["mt",30,50,200]
  ,["njets",10,0,10]
  ,["lep1pt",25,0,500]
  ,["ptll",40,100,1000]
  ,["ptpho",40,100,1000]
 ]

EXTRACUTSVT = [
#		["gjet","mvamet > 250      "]
#		,["zjets","mvamet > 250    "]
#		,["zll","mvamet > 250      "]
#		,["wjets","mvamet > 250    "]
#		,["dibosons","mvamet > 250 "]
#		,["top","mvamet > 250  "]
#		,["qcd","mvamet > 250  "]
#		,["data","mvamet > 250 "]
		["photon","ptpho > 170     "]
	      ]
EXTRACUTS = [
	#	["gjet","mvamet > 200      "]
#		,["zjets","mvamet > 200    "]
#		,["zll","mvamet > 200      "]
#		,["wjets","mvamet > 200    "]
#		,["dibosons","mvamet > 200 "]
#		,["top","mvamet > 200      "]
#		,["qcd","mvamet > 200      "]
#		,["data","mvamet > 200     "]
		["photon","ptpho > 170     "]
	      ]

categories = [
	{
	    'name':"boosted"
	   ,'in_file_name':"Phys14/boosted-combo-pfmetraw-fj200_v2.root"
	   ,"cutstring":"mvamet>250 && mvamet<2000"
	   #,"cutstring":"1>0"
	   ,"extra_cuts": EXTRACUTSVT[:]
	   ,"varstring":["mvamet",250,2000]
	   ,"weightname":"weight"
	   ,"bins":BINS[:]
	   ,"additionalvars":ALLVARS[:]
	   ,"pdfmodel":1
           ,"recoilMC"  :"recoilfits/recoilfit_Zgj_pfmetraw_2012_mc.root"
           ,"recoilData":"recoilfits/recoilfit_Zgj_pfmetraw_2012_data.root"
           ,"muonSF"  : 0.985
           ,"photonSF": 0.97
	   ,"samples":
	   	{  # Format is TreeName : ['region','process',isMC,isSignal]  !! Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!
		  # Signal Region
		   "Znunu_signal"  	        :['signal','zjets',1,0]
		  ,"Zll_signal"	                :['signal','zll',1,0]
		  ,"Wjets_signal"  	        :['signal','wjets',1,0]
		  #,"WW_signal"  	        :['signal','dibosons',1,0]
		  #,"WZ_signal"  	        :['signal','dibosons',1,0]
                  #,"ZZ_signal"  	        :['signal','dibosons',1,0]
		  ,"ttbar_signal"   	        :['signal','top',1,0]
		  ,"SingleTop_signal"           :['signal','top',1,0]
		  ,"QCD_signal"	                :['signal','qcd',1,0]
                  ,"MJDM100_V_signal"           :['signal','ggH',1,1]
                  ,"data_signal"    	        :['signal','data',0,0]

		  # Di muon-Control
		  ,"Zll_di_muon_control"	  :['dimuon','zll',1,1]
		  ,"Znunu_di_muon_control"  	  :['dimuon','zjets',1,0]
		  ,"Wjets_di_muon_control"  	  :['dimuon','wjets',1,0]
		  #,"WW_di_muon_control"  	  :['dimuon','dibosons',1,0]
		  #,"WZ_di_muon_control"  	  :['dimuon','dibosons',1,0]
		  #,"ZZ_di_muon_control"  	  :['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_control"        :['dimuon','top',1,0]
		  ,"SingleTop_di_muon_control"    :['dimuon','top',1,0]
		  ,"data_di_muon_control"	  :['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_control"	   :['singlemuon','zll',1,0]
		  ,"Wjets_single_muon_control"     :['singlemuon','wjets',1,1]
		  #,"ZZ_single_muon_control"        :['singlemuon','dibosons',1,0]
		  #,"WW_single_muon_control"        :['singlemuon','dibosons',1,0]
		  #,"WZ_single_muon_control"        :['singlemuon','dibosons',1,0]
		  ,"SingleTop_single_muon_control" :['singlemuon','top',1,0]
		  ,"ttbar_single_muon_control"     :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_control"	   :['photon','gjet',1,1]
		  ,"Zll_photon_control"            :['photon','zll',1,0]
		  ,"Wjets_photon_control"  	   :['photon','wjets',1,0]
		  #,"WW_photon_control"  	   :['photon','dibosons',1,0]
		  #,"ZZ_photon_control"  	   :['photon','dibosons',1,0]
		  ,"ttbar_photon_control"   	   :['photon','top',1,0]
		  ,"SingleTop_photon_control"      :['photon','top',1,0]
                   ,"QCD_photon_control"	   :['photon','qcd',1,0]
	   	},
        },                     
    	{
	    'name':"monojet"
           ,'in_file_name':"Phys14/monojet-combo-pfmetraw-fj200_v2.root"
	   ,"cutstring":"mvamet>200 && mvamet<2000"
	   #,"cutstring":"1>0"
	   ,"extra_cuts": EXTRACUTS[:]
	   ,"varstring":["mvamet",200,2000]
	   ,"weightname":"weight"
	   ,"bins":[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,500,600,700,800,900,1000,1200,1500,2000]
	   ,"additionalvars":ALLVARS[:]
	   ,"pdfmodel":0
           ,"recoilMC"  :"recoilfits/recoilfit_Zgj_pfmetraw_2012_mc.root"
           ,"recoilData":"recoilfits/recoilfit_Zgj_pfmetraw_2012_data.root"
           ,"muonSF"  : 0.985
           ,"photonSF": 0.97
	   ,"samples":
	   	{  # Format is TreeName : ['region','process',isMC,isSignal]  !! Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!
		  # Signal Region
		  "Znunu_signal"  	           :['signal','zjets',1,0]
                  ,"Zll_signal"	                   :['signal','zll',1,0]
 		  ,"Wjets_signal"  	           :['signal','wjets',1,0]
		  #,"WW_signal"  	           :['signal','dibosons',1,0]
		  #,"WZ_signal"  	           :['signal','dibosons',1,0]
		  #,"ZZ_signal"  	           :['signal','dibosons',1,0]
		  ,"ttbar_signal"   	           :['signal','top',1,0]
		  ,"SingleTop_signal"              :['signal','top',1,0]
		  ,"QCD_signal"		           :['signal','qcd',1,0]
		  ,"MJDM100_V_signal"              :['signal','ggH',1,1]
                  ,"data_signal"	           :['signal','data',0,0]

		  # Di muon-Control
		  ,"Zll_di_muon_control"	   :['dimuon','zll',1,1]
		  ,"Znunu_di_muon_control"  	   :['dimuon','zjets',1,0]
		  ,"Wjets_di_muon_control"  	   :['dimuon','wjets',1,0]
		  #,"WW_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  #,"WZ_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  #,"ZZ_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_control"         :['dimuon','top',1,0]
		  ,"SingleTop_di_muon_control"     :['dimuon','top',1,0]
		  ,"data_di_muon_control"	   :['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_control"	   :['singlemuon','zll',1,0]
		  ,"Wjets_single_muon_control"     :['singlemuon','wjets',1,1]
		  #,"ZZ_single_muon_control"        :['singlemuon','dibosons',1,0]
		  #,"WW_single_muon_control"        :['singlemuon','dibosons',1,0]
		  #,"WZ_single_muon_control"        :['singlemuon','dibosons',1,0]
		  ,"SingleTop_single_muon_control" :['singlemuon','top',1,0]
		  ,"ttbar_single_muon_control"     :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_control"	   :['photon','gjet',1,1]
		  ,"Zll_photon_control"	           :['photon','zll',1,0]
		  ,"Wjets_photon_control"  	   :['photon','wjets',1,0]
		  #,"WW_photon_control"  	   :['photon','dibosons',1,0]
		  #,"ZZ_photon_control"  	   :['photon','dibosons',1,0]
		  ,"ttbar_photon_control"   	   :['photon','top',1,0]
		  ,"SingleTop_photon_control"      :['photon','top',1,0]
                  ,"QCD_photon_control"	           :['photon','qcd',1,0]
                  },
	}
]

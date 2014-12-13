# Configuration for the Mono-X categories
out_file_name = 'mono-x.root'
bins = range(200,1050,50)
categories = [
	{
	    'name':"monojet"
	   ,'in_file_name':"Output_Marco.root"
	   ,"cutstring":"mvamet>200 && mvamet<1000 && jet1pt>160"
	   ,"varstring":["mvamet",200,1000]
	   ,"weightname":"weight"
	   #,"bins":[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]
	   ,"bins":bins[:]
	   ,"samples":
	   	{  # Format is TreeName : ['region','process',isMC,isSignal]  !! Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!
		   "DY"  :['signal','zjets',1,0]
		  ,"DYLL":['signal','zll',1,0]
		  ,"W"   :['signal','wjets',1,0]
		  ,"WHT" :['signal','wjets',1,0]
		  ,"WW"  :['signal','dibosons',1,0]
		  ,"WZ"  :['signal','dibosons',1,0]
		  ,"ZZ"  :['signal','dibosons',1,0]
		  ,"T"   :['signal','top',1,0]
		  ,"TT"  :['signal','top',1,0]
		  ,"GGH0"    :['signal','ggH',1,1]
		  ,"VBFH0"   :['signal','vbf',1,1]
		  ,"data_obs":['signal','data',0,0]
		  ,"Zvv_control"	:['dimuon','data',0,0]
		  ,"Zvv_control_mc"	:['dimuon','zll',1,1]
		  ,"TT_control_bkg_mc"	:['dimuon','backgrounds',1,0]
		  ,"T_control_bkg_mc"	:['dimuon','backgrounds',1,0]
		  ,"WW_control_bkg_mc"	:['dimuon','backgrounds',1,0]
		  ,"WZ_control_bkg_mc"	:['dimuon','backgrounds',1,0]
		  ,"ZZ_control_bkg_mc"	:['dimuon','backgrounds',1,0]
		  ,"DY_sl_control_bkg_mc" :['singlemuon','zll',1,0]
 		  ,"TT_sl_control_bkg_mc" :['singlemuon','backgrounds',1,0]
 		  ,"T_sl_control_bkg_mc"  :['singlemuon','backgrounds',1,0]
 		  ,"WW_sl_control_bkg_mc" :['singlemuon','backgrounds',1,0]
 		  ,"WZ_sl_control_bkg_mc" :['singlemuon','backgrounds',1,0]
 		  ,"Wlv_control"	  :['singlemuon','data',0,0]
 		  ,"Wlv_control_mc_1"     :['singlemuon','wjets',1,1]
 		  ,"Wlv_control_mc_2"     :['singlemuon','wjets',1,1]
 		  ,"ZZ_sl_control_bkg_mc" :['singlemuon','backgrounds',1,0] 
 		  ,"PhoData" :['photon','data',0,0] 
 		  ,"GJet"    :['photon','gjet',1,1] 
	   	}
	}

]

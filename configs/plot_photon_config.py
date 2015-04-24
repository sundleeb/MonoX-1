import ROOT as r
directory = "category_resolved"
signals = {	 
           # "signal_ggH": ["ggH",r.kAzure+10	,0] 
           #,"signal_vbf": ["VBF",r.kRed	,0] 
	   }

#key_order = ["Z#rightarrow ll","QCD","Dibosons","top","W#rightarrow #mu#nu","#gamma + jet"]
key_order = ["QCD","#gamma + jet"]

backgrounds = { 
		"#gamma + jet":		[["photon_dimuon_combined_model.root:$DIRECTORY/ZJets_photon_gjet_nlo_combined_model$VAR"],		r.kGreen+1,   0]
		#,"QCD":	  	[["Purity=0.97"],		r.kRed+2,   0]
		,"QCD":	  		[["photon_dimuon_combined_model.root:$DIRECTORY/ZJets_photon_gjet_backgrounds_combined_model$VAR"],		r.kRed+2,   0,0.7]
		#,"QCD":	  	[["Purity=0.97"],		r.kRed+2,   0]
	      }

dataname  = "photon_data$VAR"

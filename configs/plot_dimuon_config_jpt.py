import ROOT as r
directory = "category_resolved"
signals = {	 
           # "signal_ggH": ["ggH",r.kAzure+10	,0] 
           #,"signal_vbf": ["VBF",r.kRed	,0] 
	   }

key_order = ["Dibosons","Top","Z#rightarrow #mu#mu"]

backgrounds = { 
		"Top":			  [["dimuon_top$VAR"],		r.kRed+1,   0]
		,"Dibosons":		  [["dimuon_dibosons$VAR"],		r.kGray,   0]
		,"Z#rightarrow #mu#mu":	  [["photon_dimuon_combined_model.root:$DIRECTORY/ZJets_dimuon_zll_combined_model$VAR"],		r.kGreen+3,   0]

	      }

dataname  = "dimuon_data$VAR"

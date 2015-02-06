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
		,"Z#rightarrow #mu#mu":	  [["dimuon_zll$VAR"],		r.kGreen+3,   0]
		#,"Z#rightarrow #mu#mu":	  [["dimuon_zll"],	r.kGreen+3,   0]
		#,"QCD":	  		  [["dimuon_qcd"],		r.kRed+2,   0]

	      }

dataname  = "dimuon_data$VAR"

import ROOT as r
directory = "category_resolved"
signals = {	 
           # "signal_ggH": ["ggH",r.kAzure+10	,0] 
           #,"signal_vbf": ["VBF",r.kRed	,0] 
	   }

key_order = ["QCD","Z#rightarrow ll","Dibosons","Top","W#rightarrow#mu#nu"]

backgrounds = { 
		"Top":			  [["singlemuon_top$VAR"],		r.kRed+1,   0]
		,"Dibosons":		  [["singlemuon_dibosons$VAR"],	r.kGray,   0]
		,"W#rightarrow#mu#nu":	  [["singlemuon_wjets$VAR"],		r.kAzure-3,  0]
		,"QCD":	  		  [["singlemuon_qcd$VAR"],		r.kRed+2,   0]
		,"Z#rightarrow ll":	  [["singlemuon_zll$VAR"],		r.kGreen+3,  0]

	      }

dataname  = "singlemuon_data$VAR"

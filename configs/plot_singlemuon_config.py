import ROOT as r
directory = "category_resolved"
signals = {	 
           # "signal_ggH": ["ggH",r.kAzure+10	,0] 
           #,"signal_vbf": ["VBF",r.kRed	,0] 
	   }

key_order = ["QCD","Z#rightarrow ll","Dibosons","Top","W#rightarrow#mu#nu"]

backgrounds = { 
		"Top":			  [["singlemuon_top"],		r.kRed+1,   0]
		,"Dibosons":		  [["singlemuon_dibosons"],		r.kGray,   0]
		,"W#rightarrow#mu#nu":	  [["corrected_singlemuon_wjets"],				r.kAzure-3,  0]
		,"QCD":	  		  [["singlemuon_qcd"],		r.kRed+2,   0]
		,"Z#rightarrow ll":	  [["corrected_singlemuon_zll"],		r.kGreen+3,  0]

	      }

dataname  = "singlemuon_data"

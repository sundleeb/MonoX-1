import ROOT as r
directory = "category_resolved"
signals = {	 
           # "signal_ggH": ["ggH",r.kAzure+10	,0] 
           #,"signal_vbf": ["VBF",r.kRed	,0] 
	   }

#key_order = ["Z#rightarrow ll","QCD","Dibosons","top","W#rightarrow #mu#nu","#gamma + jet"]
key_order = ["QCD","#gamma + jet"]

backgrounds = { 
		"#gamma + jet":	[["photon_gjet$VAR"],		r.kGreen+1,   0]
		,"QCD":	  	[["photon_qcd$VAR"],		r.kRed+2,   0]
	      }

dataname  = "photon_data$VAR"

import ROOT as r
directory = "category_resolved"
signals = {	 
           # "signal_ggH": ["ggH",r.kAzure+10	,0] 
           #,"signal_vbf": ["VBF",r.kRed	,0] 
	   }

key_order = ["Z#rightarrow ll","QCD","Dibosons","top","W#rightarrow #mu#nu","#gamma + jet"]

backgrounds = { 
		"#gamma + jet":			  [["photon_gjet"],		r.kGreen+1,   0]
		,"top":			  [["photon_top"],		r.kBlue-2,   0]
		,"Dibosons":		  [["photon_dibosons"],		r.kPink-4,   0]
		,"Z#rightarrow ll":	  [["photon_zll"],		r.kGreen+1,  0]
		,"W#rightarrow #mu#nu":	  [["photon_wjets"], 		r.kOrange-2, 0]
		,"Z#rightarrow #nu#nu":	  [["photon_zjets"],	r.kBlue-9,   0]
		,"QCD":	  		  [["photon_qcd"],		r.kRed+2,   0]
	      }

dataname  = "photon_data"

import ROOT as r
directory = "category_inclusive"
signals = {	 
            "signal_ggH": ["ggH",r.kAzure+10	,0] 
           ,"signal_vbf": ["VBF",r.kRed		,0] 
           ,"signal_wh":  ["WH",r.kMagenta+1	,0] 
           ,"signal_zh":  ["ZH",r.kOrange	,0] 
	   }

key_order = ["Z#rightarrow ll","QCD","Dibosons","top","W#rightarrow #mu#nu","Z#rightarrow #nu#nu"]

backgrounds = { 
		"top":			  [["signal_top"],		r.kRed+1,   0]
		,"Dibosons":		  [["signal_dibosons"],		r.kGray,    0]
		,"Z#rightarrow ll":	  [["signal_zll"],		r.kGreen+3, 0]
		#,"W#rightarrow #mu#nu":   [["signal_wjets"], 		r.kAzure-3, 0]
		,"W#rightarrow #mu#nu":  [["corrected_signal_wjets"], 	r.kAzure-3, 0]
		#,"Z#rightarrow #nu#nu":   [["signal_zjets"],		r.kBlue-9,  0]
		#,"Z#rightarrow #nu#nu":  [["corrected_signal_zjets"],	r.kBlue-9,  0]
		,"Z#rightarrow #nu#nu":  [["photon_dimuon_combined_model.root:$DIRECTORY/$CAT_combined_model"],	r.kBlue-9,   0]
		,"QCD":	  		  [["signal_qcd"],		r.kRed+2,   0]

	      }

dataname  = "signal_data"

import ROOT as r
directory = "category_inclusive"
signals = {	 
            "signal_ggHjet1pt": ["ggH",r.kAzure+10	,0] 
           ,"signal_vbfjet1pt": ["VBF",r.kRed		,0] 
           ,"signal_whjet1pt":  ["WH",r.kMagenta+1	,0] 
           ,"signal_zhjet1pt":  ["ZH",r.kOrange	,0] 
	   }

key_order = ["Z#rightarrow ll","QCD","Dibosons","top","W#rightarrow #mu#nu","Z#rightarrow #nu#nu"]

backgrounds = { 
		"top":			  [["signal_topjet1pt"],		r.kRed+1,   0]
		,"Dibosons":		  [["signal_dibosonsjet1pt"],		r.kGray,    0]
		,"Z#rightarrow ll":	  [["signal_zlljet1pt"],		r.kGreen+3, 0]
		#,"W#rightarrow #mu#nu":   [["signal_wjets"], 		r.kAzure-3, 0]
		,"W#rightarrow #mu#nu":  [["corrected_signal_wjetsjet1pt"], 	r.kAzure-3, 0]
		#,"Z#rightarrow #nu#nu":   [["signal_zjets"],		r.kBlue-9,  0]
		,"Z#rightarrow #nu#nu":  [["corrected_signal_zjetsjet1pt"],	r.kBlue-9,  0]
		#,"Z#rightarrow #nu#nu":  [["photon_dimuon_combined_model.root:$DIRECTORY/$CAT_combined_model"],	r.kBlue-9,   0]
		,"QCD":	  		  [["signal_qcdjet1pt"],		r.kRed+2,   0]

	      }

dataname  = "signal_datajet1pt"

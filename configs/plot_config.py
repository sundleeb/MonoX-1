import ROOT as r
directory = "category_inclusive"
signals = {	 
            "signal_wh": ["wH",r.kAzure+10	,0] 
           ,"signal_zh": ["zh",r.kRed		,0] 
	   }

key_order = ["Z#rightarrow ll","Dibosons","top","W#rightarrow #mu#nu","Z#rightarrow #nu#nu"]

backgrounds = { 
		"top":			  [["signal_top"],		r.kBlue-2,   0]
		,"Dibosons":		  [["signal_dibosons"],		r.kPink-4,   0]
		,"Z#rightarrow ll":	  [["signal_zll"],		r.kGreen+1,  0]
		,"W#rightarrow #mu#nu":	  [["corrected_signal_wjets"], 		r.kOrange-2, 0]
		,"Z#rightarrow #nu#nu":	  [["photon_dimuon_combined_model.root:category_inclusive/inclusive_combined_model"],	r.kBlue-9,   0]
		#,"Z#rightarrow #nu#nu":	  [["corrected_signal_zjets"],	r.kBlue-9,   0]
		#,"QCD":	  		  [["signal_qcd"],		r.kRed+2,   0]

	      }

dataname  = "signal_data"

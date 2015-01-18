import ROOT as r
directory = "category_monojet"
signals = {	 
           # "signal_ggHjet1pt": ["ggH",r.kAzure+10	,0] 
           #,"signal_vbfjet1pt": ["VBF",r.kRed		,0] 
           #,"signal_whjet1pt":  ["WH",r.kMagenta+1	,0] 
           #,"signal_zhjet1pt":  ["ZH",r.kOrange	,0] 
           "signal_Higgs125jet1pt":  ["Higgs m_{H}=125 GeV",r.kOrange	,0] 
	   }

key_order = ["Z(#rightarrow ll)+jets","QCD","Dibosons","top","W(#rightarrow l#nu)+jets","Z(#rightarrow #nu#nu)+jets"]

backgrounds = { 
		"top":			  [["signal_topjet1pt"],		r.kRed+1,   0]
		,"Dibosons":		  [["signal_dibosonsjet1pt"],		r.kGray,    0]
		,"Z(#rightarrow ll)+jets":     [["signal_zlljet1pt"],		r.kGreen+3, 0]
		,"W(#rightarrow l#nu)+jets":   [["signal_wjetsjet1pt"], 	r.kAzure-3, 0]
		,"Z(#rightarrow #nu#nu)+jets": [["signal_zjetsjet1pt"],		r.kBlue-9,  0]
		,"QCD":	  		  [["signal_qcdjet1pt"],		r.kRed+2,   0]

	      }

dataname  = "signal_datajet1pt"

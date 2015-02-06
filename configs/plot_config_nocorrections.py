import ROOT as r
directory = "category_inclusive"
signals = {	 
            "signal_ggH": ["ggH",r.kAzure+10	,0] 
           ,"signal_vbf": ["VBF",r.kRed		,0] 
           ,"signal_wh":  ["WH",r.kMagenta+1	,0] 
           ,"signal_zh":  ["ZH",r.kOrange	,0] 
	   }

key_order = ["Z(#rightarrow ll)+jets","QCD","Dibosons","top","W(#rightarrow l#nu)+jets","Z(#rightarrow #nu#nu)+jets"]

backgrounds = { 
		"top":			  [["signal_top"],		r.kRed+1,   0]
		,"Dibosons":		  [["signal_dibosons"],		r.kGray,    0]
		,"Z(#rightarrow ll)+jets":[["signal_zll"],		r.kGreen+3, 0]
		,"W(#rightarrow l#nu)+jets":    [["signal_wjets"], 	r.kAzure-3, 0]
		,"Z(#rightarrow #nu#nu)+jets":  [["signal_zjets"],	r.kBlue-9,   0]
		,"QCD":	  		        [["signal_qcd"],		r.kRed+2,   0]

	      }

dataname  = "signal_data"

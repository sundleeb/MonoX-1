import ROOT as r
directory = "shapes_fit_s"


signals = {
 	   #"Higgs #rightarrow inv, m_{H}=125 GeV":[
	   #	["mono-x-vtagged.root:category_$CAT/signal_ggH"
#		,"mono-x-vtagged.root:category_$CAT/signal_vbf"
#                ,"mono-x-vtagged.root:category_$CAT/signal_wh"
#                ,"mono-x-vtagged.root:category_$CAT/signal_zh"
#		] ,r.kOrange	,0],
# 	  "#splitline{Scalar Mediator}{m_{MED}=925 GeV, m_{DM}=10 GeV}":[
#	  	["card_$CAT.root:signal_ggH"
 	  "Contrived Signal":[
	  	["card_$CAT.root:crazy"
	  
	  ] ,r.kAzure+10	,0,1000]
	   }

key_order = ["Z(#rightarrow ll)+jets","QCD","Dibosons","top","W(#rightarrow l#nu)+jets","Z(#rightarrow #nu#nu)+jets"]

backgrounds = { 
		"top":			  	[["$CAT/top"],		r.kRed+1,   0]
		,"Dibosons":		  	[["$CAT/dibosons"],		r.kGray,    0]
		,"Z(#rightarrow ll)+jets":	[["$CAT/zll"],		r.kGreen+3, 0]
		,"W(#rightarrow l#nu)+jets":    [["$CAT/wjets"], 	r.kAzure-3, 0]
		,"Z(#rightarrow #nu#nu)+jets":  [["$CAT/zjets"],	r.kBlue-9,   0]
		,"QCD":	  		        [["$CAT/qcd"],		r.kRed+2,   0]

	      }

dataname  = "mono-x.root:category_$CAT/signal_data"

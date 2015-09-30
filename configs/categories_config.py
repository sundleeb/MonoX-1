# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'mono-x.root'

# can define any thing useful here which may be common to several categories, eg binning in MET 
bins = range(200,1100,100)

# Define each of the categories in a dictionary of the following form .. 
#	'name' : the category name 
#	'in_file_name' : input ntuple file for this category 
#	'cutstring': add simple cutrstring, applicable to ALL regions in this category (eg mvamet > 200)
#	'varstring': the main variable to be fit in this category (eg mvamet), must be named as the branch in the ntuples
#	'weightname': name of the weight variable 
#	'bins': binning given as a python list
#	'additionalvars': list additional variables to be histogrammed by the first stage, give as a list of lists, each list element 
#			  as ['variablename',nbins,min,max]
#	'pdfmodel': integer --> N/A  redudant for now unless we move back to parameteric fitting estimates
# 	'samples' : define tree->region/process map given as a dictionary with each entry as follows 
#		TreeName : ['region','process',isMC,isSignal] --> Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!!

#  OPTIONAL --> 'extra_cuts': additional cuts maybe specific to this control region (eg ptphoton cuts) if this key is missing, the code will not complain   
 
monojet_category = {
	    'name':"monojet"
	   ,'in_file_name':"monojet.root"
	   ,"cutstring":"mvamet>200 && mvamet<1000 && weight<500"
	   ,"varstring":["mvamet",200,1000]
	   ,"weightname":"weight"
	   ,"bins":bins[:]
  	   ,"additionalvars":[['jet1pt',25,150,1000]]
	   ,"pdfmodel":0
	   ,"samples":
	   	{  
		  # Signal Region
		   "Znunu_signal"  	           :['signal','zjets',1,0]
                   ,"Zll_signal"	           :['signal','zll',1,0]
 		  ,"Wjets_signal"  	           :['signal','wjets',1,0]
		  ,"WW_signal"  	           :['signal','dibosons',1,0]
		  ,"WZ_signal"  	           :['signal','dibosons',1,0]
		  ,"ZZ_signal"  	           :['signal','dibosons',1,0]
		  ,"ttbar_signal"   	           :['signal','top',1,0]
		  ,"SingleTop_signal"              :['signal','top',1,0]
		  ,"QCD_signal"		           :['signal','qcd',1,0]
		  ,"ggH125_signal"                 :['signal','ggH',1,1]
		  ,"VBFH125_signal"                :['signal','vbf',1,1]
		  ,"WH125_signal"   	   	   :['signal','wh',1,1]
		  ,"ZH125_signal"   	   	   :['signal','zh',1,1]
		  ,"data_signal"	           :['signal','data',0,0]

		  # Di muon-Control
		  ,"Zll_di_muon_control"	   :['dimuon','zll',1,1]
		  ,"Znunu_di_muon_control"  	   :['dimuon','zjets',1,0]
		  ,"Wjets_di_muon_control"  	   :['dimuon','wjets',1,0]
		  ,"WW_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  ,"WZ_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  ,"ZZ_di_muon_control"  	   :['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_control"         :['dimuon','top',1,0]
		  ,"SingleTop_di_muon_control"     :['dimuon','top',1,0]
		  ,"data_di_muon_control"	   :['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_control"	   :['singlemuon','zll',1,0]
		  ,"Wjets_single_muon_control"     :['singlemuon','wjets',1,1]
		  ,"ZZ_single_muon_control"        :['singlemuon','dibosons',1,0]
		  ,"WW_single_muon_control"        :['singlemuon','dibosons',1,0]
		  ,"WZ_single_muon_control"        :['singlemuon','dibosons',1,0]
		  ,"SingleTop_single_muon_control" :['singlemuon','top',1,0]
		  ,"ttbar_single_muon_control"     :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  # Photon control region
		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_control"	   :['photon','gjet',1,1]
		  ,"Zll_photon_control"	           :['photon','zll',1,0]
		  ,"Wjets_photon_control"  	   :['photon','wjets',1,0]
		  ,"WW_photon_control"  	   :['photon','dibosons',1,0]
		  ,"ZZ_photon_control"  	   :['photon','dibosons',1,0]
		  ,"ttbar_photon_control"   	   :['photon','top',1,0]
		  ,"SingleTop_photon_control"      :['photon','top',1,0]
                  ,"QCD_photon_control"	           :['photon','qcd',1,0]
	   	},
}
categories = [monojet_category]

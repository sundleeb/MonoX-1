# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'mono-x.root'

# can define any thing useful here which may be common to several categories, eg binning in MET 
#bins = range(200,1200,200)
bins = [200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]

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
 
ALLMETSAMPLES = [ 
                    #Di Electron Control Region
                    "Zll_di_electron_control","Wjets_di_electron_control","WW_di_electron_control","WZ_di_electron_control","ZZ_di_electron_control",
                    "ttbar_di_electron_control","SingleTop_di_electron_control",
                    #Single Electron Control Region
                    "Wjets_single_electron_control","Zll_single_electron_control","WW_single_electron_control","WZ_single_electron_control","ZZ_single_electron_control","ttbar_single_electron_control",
                    "SingleTop_single_electron_control",
                    #Di Muon Control Region
                    "Zll_di_muon_control","Wjets_di_muon_control","WW_di_muon_control","WZ_di_muon_control","ZZ_di_muon_control",
                    "ttbar_di_muon_control","SingleTop_di_muon_control",
                    #Single Muon Control Region
                    "Wjets_single_muon_control","Zll_single_muon_control","WW_single_muon_control","WZ_single_muon_control","ZZ_single_muon_control","ttbar_single_muon_control",
                    "SingleTop_single_muon_control","QCD_single_muon_control",
                    #Photon Control Region
                    "Photon_photon_control","ttbar_photon_control",#"Wjets_photon_control","Zll_photon_control","WW_photon_control","ZZ_photon_control","ttbar_photon_control","SingleTop_photon_control",
                    "QCD_photon_control",
                    #Signal Region
                    "Wjets_signal","Zll_signal","WW_signal","WZ_signal","ZZ_signal","ttbar_signal","SingleTop_signal","QCD_signal","Znunu_signal"
                    #"ggH125_signal"    	,"VBFH125_signal"   	,"WH125_signal"   	,"ZH125_signal",
		]
monojet_category = {
	    'name':"monojet"
	   ,'in_file_name':"monojet-combo-electron.root"
	   ,"cutstring":"mvamet>200 && mvamet<1000 && weight<500"
            ,"varstring":["mvamet",200,1000]
	   ,"weightname":"weight"
	   ,"bins":bins[:]
	   #,"bins":[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]
           ,"recoilMC":"recoilfits/recoilfit_gjetsMC_Zu1_pf_v1.root"
           ,"recoilData":"recoilfits/recoilfit_gjetsData_Zu1_pf_v1.root"
  	   ,"additionalvars":[['jet1pt',25,150,1000]]
	   ,"pdfmodel":0
	   ,"samples":
	   	{  
		  # Signal Region
		   "Znunu_signalMet"  	           :['signal','zjets',1,0]
                   ,"Zll_signalMet"	           :['signal','zll',1,0]
 		  ,"Wjets_signalMet"  	           :['signal','wjets',1,0]
		  ,"WW_signalMet"  	           :['signal','dibosons',1,0]
		  ,"WZ_signalMet"  	           :['signal','dibosons',1,0]
		  ,"ZZ_signalMet"  	           :['signal','dibosons',1,0]
		  ,"ttbar_signalMet"   	           :['signal','top',1,0]
		  ,"SingleTop_signalMet"           :['signal','top',1,0]
		  ,"QCD_signalMet"		   :['signal','qcd',1,0]
		  ,"ggH125_signalMet"              :['signal','ggH',1,1]
		  ,"VBFH125_signalMet"             :['signal','vbf',1,1]
		  ,"WH125_signalMet"   	   	   :['signal','wh',1,1]
		  ,"ZH125_signalMet"   	   	   :['signal','zh',1,1]
		  ,"data_signal"	           :['signal','data',0,0]

		  # Di muon-Control
		  ,"Zll_di_muon_controlMet"	   :['dimuon','zll',1,1]
		  ,"Znunu_di_muon_controlMet"  	   :['dimuon','zjets',1,0]
		  ,"Wjets_di_muon_controlMet"  	   :['dimuon','wjets',1,0]
		  ,"WW_di_muon_controlMet"  	   :['dimuon','dibosons',1,0]
		  ,"WZ_di_muon_controlMet"  	   :['dimuon','dibosons',1,0]
		  ,"ZZ_di_muon_controlMet"  	   :['dimuon','dibosons',1,0]
		  ,"ttbar_di_muon_controlMet"      :['dimuon','top',1,0]
		  ,"SingleTop_di_muon_controlMet"  :['dimuon','top',1,0]
		  ,"data_di_muon_control"	   :['dimuon','data',0,0]

		  # Single muon control
		  ,"Zll_single_muon_controlMet"	   :['singlemuon','zll',1,0]
		  ,"Wjets_single_muon_controlMet"     :['singlemuon','wjets',1,1]
		  ,"ZZ_single_muon_controlMet"        :['singlemuon','dibosons',1,0]
		  ,"WW_single_muon_controlMet"        :['singlemuon','dibosons',1,0]
		  ,"WZ_single_muon_controlMet"        :['singlemuon','dibosons',1,0]
		  ,"SingleTop_single_muon_controlMet" :['singlemuon','top',1,0]
		  ,"ttbar_single_muon_controlMet"     :['singlemuon','top',1,0]
		  ,"QCD_single_muon_control"	   :['singlemuon','qcd',1,0]
		  ,"data_single_muon_control"	   :['singlemuon','data',0,0]

		  # Photon control region
		  ,"data_photon_control"	   :['photon','data',0,0]
		  ,"Photon_photon_controlMet"	   :['photon','gjet',1,1]
		  ,"Zll_photon_controlMet"	   :['photon','zll',1,0]
		  ,"Wjets_photon_controlMet"  	   :['photon','wjets',1,0]
		  ,"WW_photon_controlMet"  	   :['photon','dibosons',1,0]
		  ,"ZZ_photon_controlMet"  	   :['photon','dibosons',1,0]
		  ,"ttbar_photon_controlMet"   	   :['photon','top',1,0]
		  ,"SingleTop_photon_controlMet"   :['photon','top',1,0]
                  ,"QCD_photon_controlMet"	   :['photon','qcd',1,0]
	   	},
                "metsamples":ALLMETSAMPLES[:] # For Recoil Corrections
}
categories = [monojet_category]

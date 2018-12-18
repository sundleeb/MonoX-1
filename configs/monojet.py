# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis

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
#  OPTIONAL --> 'extra_cuts': additional cuts maybe specific to this control region (eg ptpho cuts) if this key is missing, the code will not complain   

# Can define anything useful here outside the catefory dictionary which may be common to several categories, eg binning in MET, systematics ecc
# systematics will expect samples with sample_sys_Up/Down but will skip if not found 

signals = {}
with open('../../../../Panda_Analysis/CMSSW_8_0_29/src/PandaAnalysis/LPC_T3/merging/signals.txt', 'r') as signal_file:
                for line in signal_file:
                    name = line.rstrip()
                    signals[name+'_signal'] = ['signal',name+'_signal',1,1]

samples = {  
    # Signal Region
#   "VH_signal"    	       :['signal','vh',1,0]
    "Zvv_signal"    	       :['signal','zjets',1,0]
    ,"Zll_signal"	       :['signal','zll',1,0]
    ,"Wlv_signal"  	       :['signal','wjets',1,0]
    ,"Diboson_signal"         :['signal','dibosons',1,0]
    ,"ttbar_signal"   	       :['signal','ttbar',1,0]
    ,"ST_signal"              :['signal','stop',1,0]
    ,"QCD_signal"             :['signal','qcd',1,0]
    ,"Data_signal"	       :['signal','data',0,0]

    # Di muon-Control
#   ,"VH_zmm"                    :['dimuon','vh',1,0] 
    ,"Zll_zmm"	               :['dimuon','zll',1,1]
    ,"Diboson_zmm"    	       :['dimuon','dibosons',1,0]
    ,"ttbar_zmm"    	       :['dimuon','ttbar',1,0]
    ,"Data_zmm"    	       :['dimuon','data',0,0]

    # Di electron-Control
#   ,"VH_zee"                    :['dielectron','vh',1,0] 
    ,"Zll_zee"                   :['dielectron','zll',1,1]
    ,"Diboson_zee"               :['dielectron','dibosons',1,0]
    ,"ttbar_zee"                 :['dielectron','ttbar',1,0]
    ,"Data_zee"                  :['dielectron','data',0,0]

    # Single muon (w) control
#   ,"VH_mn"                    :['singlemuon','vh',1,0] 
    ,"Zll_mn"                   :['singlemuon','zll',1,0]
    ,"Wlv_mn"                   :['singlemuon','wjets',1,1]
    ,"Diboson_mn"               :['singlemuon','dibosons',1,0]
    ,"ttbar_mn"                 :['singlemuon','ttbar',1,0]
    ,"QCD_mn"                   :['singlemuon','qcd',1,0]
    ,"Data_mn"                  :['singlemuon','data',0,0]

    # Single electron (w) control
#   ,"VH_en"                    :['singleelectron','vh',1,0] 
    ,"Zll_en"                   :['singleelectron','zll',1,0]
    ,"Wlv_en"                   :['singleelectron','wjets',1,1]
    ,"Diboson_en"               :['singleelectron','dibosons',1,0]
    ,"ttbar_en"                 :['singleelectron','ttbar',1,1]
    ,"ST_en"                    :['singleelectron','stop',1,0]
    ,"QCD_en"                   :['singleelectron','qcd',1,0]
    ,"Data_en"                  :['singleelectron','data',0,0]

    # Single photon control
    ,"Pho_pho"                   :['singlephoton','gjets',1,1]
    ,"QCD_pho"                   :['singlephoton','qcd',1,0]
    ,"Data_pho"                  :['singlephoton','data',0,0]
    }

samples.update(signals)
samples_0tag = {}
for sample in samples: 
        samples_0tag[sample+'_0tag'] = samples[sample]
samples_dict = {'0tag':samples_0tag}

bins = [250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0]
systematics=["btag","mistag"]
monojet_category = {}
out_file_name = 'monojet.root'
categories = []
for s in ['0tag']:
     monojet_category[s] = {
        'name':"monojet_"+s
        ,'in_file_name':"/uscms_data/d3/naina25/panda/limits/fittingForest_"+s+".root"
        ,"cutstring":"1"
        ,"varstring":["min(999.9999,met)",250,1250]
        ,"weightname":"weight"
        ,"bins":bins[:]
        ,"additionalvars":[]
        ,"pdfmodel":0
        ,"samples":samples_dict[s]
        }

     categories.append(monojet_category[s])

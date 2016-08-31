# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 

out_file_name = 'mono-x.root'

bins = [175.0,190.0,250.0,400.0,700.0]

monophoton_category = {
	    'name':"monophoton"
            ,'in_file_name':"/afs/cern.ch/user/b/ballen/public/monophTrees.root"
            ,"cutstring":"phoPtHighMet>175"
            ,"varstring":["phoPtHighMet",175,1000]
            ,"weightname":"weight"
            ,"bins":bins[:]
            ,"additionalvars":[['phoPtHighMet',100,200,1250]]
            ,"pdfmodel":0
            ,"samples":
	   	{          
		  # Signal Region
                   "monoph-phoPtHighMet-minor"    :['signal','minor',1,0]
                  ,"monoph-phoPtHighMet-gjets"    :['signal','gjets',1,0]
                  ,"monoph-phoPtHighMet-vvg"      :['signal','vvg',1,0]
                  ,"monoph-phoPtHighMet-halo"     :['signal','halo',1,0]
                  ,"monoph-phoPtHighMet-hfake"    :['signal','hfake',1,0]
                  ,"monoph-phoPtHighMet-efake"    :['signal','efake',1,0]
                  ,"monoph-phoPtHighMet-wg"       :['signal','wg',1,0]
                  ,"monoph-phoPtHighMet-zg"       :['signal','zg',1,0]
                  ,"monoph-phoPtHighMet-data_obs" :['signal','data',0,0]
                  ,"monoph-phoPtHighMet-dmv-500-1":['signal','dm_v500_1',1,1]

                  # Dimuon Control Region
                  ,"dimu-phoPtHighMet-vvg"        :['dimu','vvg',1,0]
                  ,"dimu-phoPtHighMet-zjets"      :['dimu','zjets',1,0]
                  ,"dimu-phoPtHighMet-tt"         :['dimu','tt',1,0]
                  ,"dimu-phoPtHighMet-zgam"       :['dimu','zg',1,0]
                  ,"dimu-phoPtHighMet-data_obs"   :['dimu','data',0,0]
                   
                  # Dielectron Control Region
                  ,"diel-phoPtHighMet-vvg"        :['diel','vvg',1,0]
                  ,"diel-phoPtHighMet-tt"         :['diel','tt',1,0]
                  ,"diel-phoPtHighMet-zjets"      :['diel','zjets',1,0]
                  ,"diel-phoPtHighMet-zgam"       :['diel','zg',1,0]
                  ,"diel-phoPtHighMet-data_obs"   :['diel','data',0,0]

                  # Single muon Control Region
                  ,"monomu-phoPtHighMet-vvg"      :['singlemu','vvg',1,0]
                  ,"monomu-phoPtHighMet-zgamm"    :['singlemu','zgamm',1,0]
                  ,"monomu-phoPtHighMet-top"      :['singlemu','top',1,0]
                  ,"monomu-phoPtHighMet-wg"       :['singlemu','wg',1,0]
                  ,"monomu-phoPtHighMet-data_obs" :['singlemu','data',0,0]

                   # Single Electron Control Region
                  ,"monoel-phoPtHighMet-vvg"       :['singleel','vvg',1,0]
                  ,"monoel-phoPtHighMet-zgamm"     :['singleel','zgamm',1,0]
                  ,"monoel-phoPtHighMet-top"       :['singleel','top',1,0]
                  ,"monoel-phoPtHighMet-wg"        :['singleel','wg',1,0]
                  ,"monoel-phoPtHighMet-data_obs"  :['singleel','data',0,0]

	   	},
}

categories = [monophoton_category]

#! /bin/bash
# Make some pretty plots from canvases inside the root files produced from the fitting 
# of the dimuon and single muon control regions
#root -l -q -b 'drawFits.C("mono-x-vtagged.root","inclusive")'
#root -l -b -q 'drawFits.C("mono-x-vtagged.root","boosted")'
#root -l -b -q 'drawFits.C("mono-x-vtagged.root","resolved")'

# Some more plots for the photon+Zmm control regions combined fit.
root -l -q -b 'drawSfactors.C("photon_dimuon_combined_model.root","inclusive")'
root -l -b -q 'drawSfactors.C("photon_dimuon_combined_model.root","boosted")'
root -l -b -q 'drawSfactors.C("photon_dimuon_combined_model.root","resolved")'

root -l -q -b 'drawSfactorsW.C("photon_dimuon_combined_model.root","inclusive")'
root -l -b -q 'drawSfactorsW.C("photon_dimuon_combined_model.root","boosted")'
root -l -b -q 'drawSfactorsW.C("photon_dimuon_combined_model.root","resolved")'

# Make dimuon/single muon CR plots (note for dimuon, the fake MET is obsolete) before and after corrections
python makePlot.py mono-x-vtagged.root plot_dimuon_config plot_singlemuon_config plot_dimuon_config_nocorrections plot_singlemuon_config_nocorrections -d category_boosted  -x "fake E_{T}^{miss} (GeV)" -b  -c boosted  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_dimuon_config plot_singlemuon_config plot_dimuon_config_nocorrections plot_singlemuon_config_nocorrections -d category_resolved -x "fake E_{T}^{miss} (GeV)" -b  -c resolved  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_dimuon_config plot_singlemuon_config plot_dimuon_config_nocorrections plot_singlemuon_config_nocorrections -d category_inclusive -x "fake E_{T}^{miss} (GeV)" -b  -c inclusive # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  

# Do the same but for additional variables 
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_singlemuon_config_jpt plot_dimuon_config_nocorrections_jpt plot_singlemuon_config_nocorrections_jpt -v jet1pt -d category_boosted  -x "ca08 Jet p_{T} (GeV)" -b  -c boosted  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_singlemuon_config_jpt plot_dimuon_config_nocorrections_jpt plot_singlemuon_config_nocorrections_jpt -v jet1pt -d category_resolved -x "Dijet p_{T} (GeV)" -b  -c resolved  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_singlemuon_config_jpt plot_dimuon_config_nocorrections_jpt plot_singlemuon_config_nocorrections_jpt -v jet1pt -d category_inclusive -x "Lead Jet p_{T} (GeV)" -b  -c inclusive # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  

# Dimuon additionals 
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v njets -o NJETS -d category_boosted  -x "N Jets" -b  -c boosted  --nospec 
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v njets -o NJETS -d category_inclusive  -x "N Jets" -b  -c inclusive   --nospec 
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v njets -o NJETS -d category_resolved  -x "N Jets" -b  -c resolved   --nospec 
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v mll -o MLL -d category_boosted  -x "m_{#mu#mu} (GeV)" -b  -c boosted  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v mll -o MLL -d category_inclusive  -x "m_{#mu#mu} (GeV0" -b  -c inclusive  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v mll -o MLL -d category_resolved  -x "m_{#mu#mu} (GeV)" -b  -c resolved  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v lep1pt -o L1PT -d category_boosted    -x "Lead Muon p_{T} (GeV)" -b  -c boosted  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v lep1pt -o L1PT -d category_inclusive  -x "Lead Muon p_{T} (GeV)" -b  -c inclusive  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v lep1pt -o L1PT -d category_resolved   -x "Lead Muon p_{T} (GeV)" -b  -c resolved  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v ptll  -o PTLL -d category_boosted    -x "p_{T}^{#mu#mu} (GeV)" -b  -c boosted  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v ptll  -o PTLL -d category_inclusive  -x "p_{T}^{#mu#mu} (GeV)" -b  -c inclusive  
python makePlot.py mono-x-vtagged.root plot_dimuon_config_jpt plot_dimuon_config_nocorrections_jpt -v ptll  -o PTLL -d category_resolved   -x "p_{T}^{#mu#mu} (GeV)" -b  -c resolved  

#Single muon additionals
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v njets -o NJETS -d category_boosted  -x "N Jets" -b  -c boosted   --nospec 
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v njets -o NJETS -d category_inclusive  -x "N Jets" -b  -c inclusive   --nospec 
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v njets -o NJETS -d category_resolved  -x "N Jets" -b  -c resolved   --nospec 
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v mt -o MT -d category_boosted  -x "m_{T} (GeV)" -b  -c boosted  
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v mt -o MT -d category_inclusive  -x "m_{T} (GeV0" -b  -c inclusive  
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v mt -o MT -d category_resolved  -x "m_{T} (GeV)" -b  -c resolved  
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v lep1pt -o L1PT -d category_boosted    -x "Lead Muon p_{T} (GeV)" -b  -c boosted  
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v lep1pt -o L1PT -d category_inclusive  -x "Lead Muon p_{T} (GeV)" -b  -c inclusive  
python makePlot.py mono-x-vtagged.root plot_singlemuon_config_jpt plot_singlemuon_config_nocorrections_jpt -v lep1pt -o L1PT -d category_resolved   -x "Lead Muon p_{T} (GeV)" -b  -c resolved  

# Make a plot of the signal region (Uses the g+jet+Zmm combined model for the Zvv template)
python makePlot.py mono-x-vtagged.root plot_config plot_config_nocorrections -d category_boosted   -x "E_{T}^{miss} (GeV)" -b -g -c boosted  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config plot_config_nocorrections -d category_resolved  -x "E_{T}^{miss} (GeV)" -b -g -c resolved  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config plot_config_nocorrections -d category_inclusive -x "E_{T}^{miss} (GeV)" -b -g -c inclusive # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  

# Make a plot of the signal region (Uses the g+jet+Zmm combined model for the Zvv template)
python makePlot.py mono-x-vtagged.root plot_config_jpt plot_config_nocorrections_jpt -v jet1pt  -d category_boosted   -x "ca08 Jet p_{T} (GeV)" -b -g -c boosted  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config_jpt plot_config_nocorrections_jpt -v jet1pt  -d category_resolved  -x "Dijet p_{T} (GeV)" -b -g -c resolved  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config_jpt plot_config_nocorrections_jpt -v jet1pt  -d category_inclusive -x "Lead Jet p_{T} (GeV)" -b -g -c inclusive # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config_jpt plot_config_nocorrections_jpt -v njets -o NJETS  -d category_inclusive -x "N Jets" -b -g -c inclusive  --nospec # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config_jpt plot_config_nocorrections_jpt -v njets -o NJETS  -d category_resolved -x "N Jets" -b -g -c resolved  --nospec # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config_jpt plot_config_nocorrections_jpt -v njets -o NJETS  -d category_boosted -x "N Jets" -b -g -c boosted  --nospec # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  

# Now if its there make inclusive versions 
python makePlot.py mono-x.root plot_config_combsignal     -d category_monojet  		  -x "E_{T}^{miss} (GeV)"   -b  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x.root plot_config_combsignal_jpt -d category_monojet  -v jet1pt  -x "Lead Jet p_{T} (GeV)" -b  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind 
python makePlot.py mono-x.root plot_config_combsignal_jpt -d category_monojet  -v njets  -o NJETS -x "N Jets" -b  --nospec  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  

# Finally the photons !
python makePlot.py mono-x-vtagged.root  plot_photon_config plot_photon_config_nocorrection -d category_inclusive -x "photon p_{T} (GeV)" -v "ptpho" -c inclusive 
python makePlot.py mono-x-vtagged.root  plot_photon_config plot_photon_config_nocorrection -d category_boosted -x "photon p_{T} (GeV)" -v "ptpho" -c boosted 
python makePlot.py mono-x-vtagged.root  plot_photon_config plot_photon_config_nocorrection -d category_resolved -x "photon p_{T} (GeV)" -v "ptpho" -c resolved 

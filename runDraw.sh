#! /bin/bash
# Make some pretty plots from canvases inside the root files produced from the fitting 
# of the dimuon and single muon control regions
root -l -q -b 'drawFits.C("mono-x-vtagged.root","inclusive")'
root -l -b -q 'drawFits.C("mono-x-vtagged.root","boosted")'
root -l -b -q 'drawFits.C("mono-x-vtagged.root","resolved")'

# Some more plots for the photon+Zmm control regions combined fit.
root -l -q -b 'drawSfactors.C("photon_dimuon_combined_model.root","inclusive")'
root -l -b -q 'drawSfactors.C("photon_dimuon_combined_model.root","boosted")'
root -l -b -q 'drawSfactors.C("photon_dimuon_combined_model.root","resolved")'

python makePlot.py mono-x-vtagged.root plot_dimuon_config plot_singlemuon_config -d category_boosted   -x "fake E_{T}^{miss} (GeV)" -b  -c boosted  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_dimuon_config plot_singlemuon_config -d category_resolved  -x "fake E_{T}^{miss} (GeV)" -b  -c resolved  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_dimuon_config plot_singlemuon_config -d category_inclusive -x "fake E_{T}^{miss} (GeV)" -b  -c inclusive # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  

# Make a plot of the signal region (Uses the g+jet+Zmm combined model for the Zvv template)
python makePlot.py mono-x-vtagged.root plot_config -d category_boosted   -x "E_{T}^{miss} (GeV)" -b -g -c boosted  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config -d category_resolved  -x "E_{T}^{miss} (GeV)" -b -g -c resolved  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x-vtagged.root plot_config -d category_inclusive -x "E_{T}^{miss} (GeV)" -b -g -c inclusive # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  


python makePlot.py mono-x.root plot_config_nocorrections -d category_monojet   -x "E_{T}^{miss} (GeV)" -b  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  
python makePlot.py mono-x.root plot_config_jpt -d category_monojet   -x "Lead Jet p_{T} (GeV)" -b  # -o label -> Will use the Zmumu+gjet CR result for Zvv template, -g == blind  

# also make the uncorrected for the 3 categories
python makePlot.py mono-x-vtagged.root plot_config_nocorrections -d category_inclusive -x "E_{T}^{miss} (GeV)"   -g -b -c inclusive 
python makePlot.py mono-x-vtagged.root plot_config_jpt 		 -d category_inclusive -x "Lead Jet p_{T} (GeV)" -g -b -c inclusive
python makePlot.py mono-x-vtagged.root plot_config_nocorrections -d category_resolved  -x "E_{T}^{miss} (GeV)"   -g -b -c resolved
python makePlot.py mono-x-vtagged.root plot_config_jpt 		 -d category_resolved  -x "Dijet p_{T} (GeV)" -g -b -c resolved
python makePlot.py mono-x-vtagged.root plot_config_nocorrections -d category_boosted   -x "E_{T}^{miss} (GeV)"   -g -b -c boosted 
python makePlot.py mono-x-vtagged.root plot_config_jpt 		 -d category_boosted   -x "ca08 Jet p_{T} (GeV)" -g -b -c boosted

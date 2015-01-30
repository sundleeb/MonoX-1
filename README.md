MonoX
=====
(Note, steps 1,2 and 3 are configured with the config categories_config_vtag_Bacon, 
change to others as you see fit)

Prepare the trees ...

  1) python addMet.py categories_config_vtag_Bacon

  2) python addEff.py categories_config_vtag_Bacon

MonoX fitting etc

Produce templates from flat trees and additionally fit 
(di)muon control regions to correct V+Jet templates. Modify the config to suit your ntuples

  3) python buildModel.py config/categories_config_vtag_Bacon

Run photon+Jet + dimuon combined control samples, calculates scale-factors on the fly
(Takes output from prefvious step as input)

  4) python runCombinedModel.py 

Make a bunch of plots from the output files to put into documentation, for CR and SR
  
  5) ./runDraw.sh

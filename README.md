MonoX
=====
(Note, steps 1,2 and 3 are configured with the config categories_config_vtag_Bacon, 
change to others as you see fit)

Prepare the trees ...

  1) python addMet.py categories_config_vtag_Bacon

  2) python addEff.py categories_config_vtag_Bacon

  3) python shiftMet.py --file resolved-combo.root
  4) python shiftMet.py --file boosted-combo.root
  5) python shiftMet.py --file monojet-combo.root

MonoX fitting etc

Produce templates from flat trees and additionally fit 
(di)muon control regions to correct V+Jet templates. Modify the config to suit your ntuples

  6) python buildModel.py categories_config_vtag_Bacon

Run photon+Jet + dimuon combined control samples, calculates scale-factors on the fly
(Takes output from prefvious step as input)
  7) python runCombinedModel.py 

Make a bunch of plots from the output files to put into documentation, for CR and SR
  
  8) ./runDraw.sh
